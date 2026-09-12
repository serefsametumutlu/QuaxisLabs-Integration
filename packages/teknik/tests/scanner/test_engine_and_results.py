"""Tarama motoru + sonuç deposu: uçtan uca, idempotentlik, diff ve
kaybolan-sinyal (repaint) alarmı.

**Ağ yok, önbellek yok, atlama yok.** Eski depoda bu testler gerçek
göstergelere ve `data/ohlcv/` altındaki gerçek parquet önbelleğine bağlıydı;
önbellek yoksa ATLANIYORLARDI — yani temiz bir klonda hiçbir şey
kanıtlamıyorlardı. Burada veri `SentetikSaglayici`'dan, göstergeler test
kataloğundan gelir; test her makinede koşar.

Test edilen şey ZATEN motordur, gösterge değil (göstergeler ADR-002 gereği
Bölüm C'de sıfırdan yazılacak).
"""

from __future__ import annotations

import os
import warnings
from collections.abc import Iterator
from pathlib import Path

import pytest
from _ornek_katalog import KATALOG_ADRESI, SentetikSaglayici
from quaxis.teknik.core.types import Market, Timeframe
from quaxis.teknik.data.store import Store
from quaxis.teknik.scanner import engine
from quaxis.teknik.scanner.results import ResultsStore, RunRecord

_EVREN = ["AAAA", "BBBB", "CCCC", "DDDD"]
_GOSTERGELER = ["test.honest_sma_cross", "test.centered_pivot"]


@pytest.fixture(scope="module", autouse=True)
def veri_koku(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Path]:
    """Sentetik sağlayıcıdan parquet önbelleği kurar.

    Motorun işçileri AYRI SÜREÇLERDE koşar ve `Store`'u kendileri kurar; bu
    yüzden veri gerçekten diske yazılmalı — monkeypatch süreç sınırını geçmez.
    """
    kok = tmp_path_factory.mktemp("ohlcv")
    # ORTAM DEĞİŞKENİ: işçi süreçler veri kökünü buradan okur; monkeypatch
    # süreç sınırını geçmez (bkz. quaxis/teknik/yollar.py::VERI_KOK).
    os.environ["QUAXIS_TEKNIK_DATA"] = str(kok)
    store = Store(SentetikSaglayici(), root=kok)
    from datetime import UTC, datetime

    for sembol in _EVREN:
        store.update(
            sembol, Market.BIST,
            start=datetime(2024, 1, 1, tzinfo=UTC),
            end=datetime(2024, 12, 31, tzinfo=UTC),
            timeframes=(Timeframe.D1,),
        )
    try:
        yield kok
    finally:
        os.environ.pop("QUAXIS_TEKNIK_DATA", None)


def _kucuk_tarama(run_id: str) -> engine.ScanRun:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return engine.run(
            run_id=run_id, universe=_EVREN, timeframes=[Timeframe.D1],
            indicator_names=_GOSTERGELER, market=Market.BIST,
            catalog=KATALOG_ADRESI, lookback_bars=300, workers=1,
        )


def _kaydet(store: ResultsStore, run_id: str, scan: engine.ScanRun) -> None:
    store.start_run(
        RunRecord(
            run_id=run_id, started_at="2026-01-01T00:00:00", finished_at=None,
            market="bist", timeframes=["1d"], universe_size=len(_EVREN),
            indicator_names=_GOSTERGELER, git_sha=None, status="running",
        )
    )
    store.persist(run_id, [r.to_symbol_indicator_run() for r in scan.results])
    store.finish_run(run_id, "2026-01-01T00:05:00", "completed")


def test_kucuk_evren_uctan_uca(tmp_path: Path) -> None:
    scan = _kucuk_tarama("test_e2e")
    assert len(scan.results) == len(_EVREN) * len(_GOSTERGELER)
    assert scan.error_count == 0, [r.error for r in scan.results if r.error]
    assert len(scan.data_quality) == len(_EVREN)

    store = ResultsStore(db_path=tmp_path / "r.db", json_root=tmp_path / "json")
    _kaydet(store, "test_e2e", scan)

    assert len(store.query(run_id="test_e2e")) > 0
    assert store.latest_run("bist") == "test_e2e"

    # results.db'den TAM IndicatorResult geri okuma yolu.
    ucluler = store.list_symbol_indicators("test_e2e", timeframe="1D")
    assert ("AAAA", "1D", "test.honest_sma_cross") in ucluler
    sonuc = store.read_result("test_e2e", "AAAA", "1D", "test.honest_sma_cross")
    assert sonuc is not None
    assert sonuc.indicator == "test.honest_sma_cross"
    assert store.read_result("test_e2e", "AAAA", "1D", "yok.boyle") is None
    store.close()


def test_ayni_veriyle_iki_kosu_bit_bit_ayni(tmp_path: Path) -> None:
    """Deterministiklik kuralının tarama tarafındaki karşılığı: aynı veri +
    aynı parametre = aynı satırlar (yalnız run_id farklı)."""
    scan1 = _kucuk_tarama("run_a")
    scan2 = _kucuk_tarama("run_b")

    store = ResultsStore(db_path=tmp_path / "r.db", json_root=tmp_path / "json")
    _kaydet(store, "run_a", scan1)
    _kaydet(store, "run_b", scan2)

    def _run_id_siz(rows: list[dict]) -> list[tuple]:
        return sorted(
            (r["symbol"], r["timeframe"], r["indicator"], r["pattern_id"], r["state"], r["bar_time"])
            for r in rows
        )

    assert _run_id_siz(store.query(run_id="run_a")) == _run_id_siz(store.query(run_id="run_b"))
    store.close()


def test_ayni_tarama_iki_kez_kaydedilince_diff_bos(tmp_path: Path) -> None:
    """Aynı veri iki kez kaydedilirse yeni sinyal de kaybolan sinyal de
    OLMAMALI — repaint alarmı yanlış yere çalmamalı."""
    scan = _kucuk_tarama("ayni_tarama")
    store = ResultsStore(db_path=tmp_path / "r.db", json_root=tmp_path / "json")
    for run_id in ("run_a", "run_b"):
        _kaydet(store, run_id, scan)

    diff = store.diff("run_a", "run_b")
    assert diff.new_signals == []
    assert diff.missing_signals == []
    assert not diff.has_repaint_alarm
    store.close()


def test_kaybolan_sinyal_repaint_alarmi_kaldirir(tmp_path: Path) -> None:
    """Bir sinyal önceki koşuda varken sonrakinde yoksa bu bir REPAINT
    şüphesidir ve sessiz kalmaz."""
    store = ResultsStore(db_path=tmp_path / "r.db", json_root=tmp_path / "json")
    for run_id in ("run_a", "run_b"):
        store.start_run(
            RunRecord(
                run_id=run_id, started_at="2026-01-01T00:00:00", finished_at=None,
                market="bist", timeframes=["1d"], universe_size=1,
                indicator_names=["test.honest_sma_cross"], git_sha=None, status="running",
            )
        )
    store._conn.execute(  # noqa: SLF001 — test için doğrudan satır enjeksiyonu
        "INSERT INTO signals (run_id, symbol, market, timeframe, indicator, params_hash, "
        "bar_time, detected_at, direction, state, score, pattern_id, payload_json) "
        "VALUES ('run_a','HAYALET','bist','1d','test.honest_sma_cross','h1',"
        "'2026-01-01T00:00:00','2026-01-01T00:00:00','long','confirmed',0.9,'ghost','{}')"
    )
    store._conn.commit()
    store.finish_run("run_a", "2026-01-01T00:05:00", "completed")
    store.finish_run("run_b", "2026-01-01T00:05:00", "completed")

    diff = store.diff("run_a", "run_b")
    assert diff.has_repaint_alarm
    assert len(diff.missing_signals) == 1
    assert diff.missing_signals[0]["pattern_id"] == "ghost"
    store.close()
