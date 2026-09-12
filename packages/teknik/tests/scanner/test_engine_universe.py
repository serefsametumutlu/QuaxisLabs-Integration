"""Motorun "universe" iş yolu: tüm evren + endeks TEK işte, sonuç sembol
sembol açılır.

Ağ ve parquet önbelleği GEREKTİRMEZ — `_fetch_and_prepare` sentetik veriyle
değiştirilir, gösterge test kataloğundan gelir. Eski depoda bu test gerçek
`momentum.alpha_rank` göstergesine ve onun fikstürlerine bağlıydı; gösterge
katmanı sıfırdan yazılacağı için (ADR-002) bağ koparıldı — test edilen şey
zaten MOTOR, gösterge değil.
"""

from __future__ import annotations

import pytest
from _ornek_katalog import KATALOG_ADRESI, sentetik_ohlcv
from quaxis.teknik.core.types import Market
from quaxis.teknik.data.universe import BENCHMARK_SYMBOL
from quaxis.teknik.scanner import engine

_EVREN = ["AAAA", "BBBB", "CCCC", "DDDD", "EEEE"]


@pytest.fixture
def _sentetik(monkeypatch: pytest.MonkeyPatch) -> dict:
    kiyas = BENCHMARK_SYMBOL[Market.BIST]
    seriler = {s: sentetik_ohlcv(tohum=sum(map(ord, s)), bar=300) for s in _EVREN}
    endeks = sentetik_ohlcv(tohum=99, bar=300)

    def sahte_fetch(symbol, market, timeframe, lookback_bars, drop_open_bar):
        if symbol == kiyas:
            return endeks
        if symbol in seriler:
            return seriler[symbol]
        raise FileNotFoundError(symbol)

    monkeypatch.setattr(engine, "_fetch_and_prepare", sahte_fetch)
    return seriler


def test_universe_isi_sembol_bazli_hatalari_bildirir(_sentetik: dict) -> None:
    semboller = list(_sentetik) + ["YOKSEMBOL"]
    ham = engine._run_universe_worker(
        KATALOG_ADRESI, "test.rank", "bist", "1D", semboller, 600, True
    )
    assert ham["error"] is None
    assert ham["symbol_errors"] == {"YOKSEMBOL": "FileNotFoundError: YOKSEMBOL"}
    assert set(ham["symbol_results"]) <= set(_sentetik)
    assert len(ham["symbol_results"]) > 0


def test_universe_sonucu_duz_listeye_acilir(_sentetik: dict) -> None:
    semboller = list(_sentetik) + ["YOKSEMBOL"]
    ham = engine._run_universe_worker(
        KATALOG_ADRESI, "test.rank", "bist", "1D", semboller, 600, True
    )
    kosular = engine._universe_result_to_runs(ham)
    basarili = [r for r in kosular if r.error is None]
    hatali = [r for r in kosular if r.error is not None]

    assert len(basarili) == len(ham["symbol_results"])
    assert len(hatali) == 1
    assert hatali[0].symbol == "YOKSEMBOL"
    assert all(r.result is not None and r.params_hash for r in basarili)


def test_ust_seviye_hata_tek_kosuya_donusur(monkeypatch: pytest.MonkeyPatch) -> None:
    """Endeks verisi hiç çekilemezse iş tamamen düşer ve BU durum tek bir
    hatalı koşu olarak raporlanır — sessizce boş sonuç dönmez."""

    def bozuk_fetch(*args, **kwargs):
        raise ValueError("endeks verisi yok")

    monkeypatch.setattr(engine, "_fetch_and_prepare", bozuk_fetch)
    ham = engine._run_universe_worker(KATALOG_ADRESI, "test.rank", "bist", "1D", ["AAAA"], 600, True)
    kosular = engine._universe_result_to_runs(ham)
    assert len(kosular) == 1
    assert kosular[0].error is not None
    assert kosular[0].symbol.startswith("__universe__:")
