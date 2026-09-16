"""Tarama → web köprüsünün testleri.

Bu testler "JSON üretiliyor mu" diye sormaz. Köprünün **yalan söyleyemediğini**
kanıtlar: rozetin pasaporttan geldiğini, sahipsiz bir göstergenin sessizce
geçemediğini, tanınmayan bir sinyal durumunun griye düşmediğini ve kırpılan
satırın sayısının künyeye yazıldığını.

Arayüzdeki tarama tablosu aylarca maket veriyle çalıştı ve bunun tek sebebi
motorun eksikliği değildi — gerçek veriyi maket veriden ayırt eden bir kural
da yoktu. Aşağıdaki her test o kurallardan birini tutar.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sqlite3
import sys

KOK = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "packages" / "teknik"))
sys.path.insert(0, str(KOK / "tools"))


def _yukle(ad: str):
    spec = importlib.util.spec_from_file_location(ad, KOK / "tools" / f"{ad}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[ad] = mod
    spec.loader.exec_module(mod)
    return mod


disaktar = _yukle("tarama_disaktar")
pasaport = _yukle("pasaport")


def test_her_katalog_gostergesi_bir_pasaporta_bagli() -> None:
    """Rozet uydurulamaz: haritada olmayan gösterge = rozetsiz satır."""
    from quaxis.teknik.indicators.katalog import KATALOG

    harita = disaktar.gosterge_haritasi()
    eksik = sorted(set(KATALOG.names()) - set(harita))
    assert not eksik, f"şu göstergeler hiçbir pasaportta sahiplenilmemiş: {eksik}"


def test_rozet_pasaportun_verdiktidir() -> None:
    """Haritadaki verdikt, göstergeyi sahiplenen pasaportun künyesinden gelir."""
    harita = disaktar.gosterge_haritasi()
    kunyeler = {p.slug: p.kunye for p in pasaport.pasaportlar()}

    for gosterge, kayit in harita.items():
        kunye = kunyeler[kayit["pasaport"]]
        beklenen = disaktar.VERDIKT_ADI[str(kunye["verdikt"]).strip()]
        assert kayit["verdikt"] == beklenen, (
            f"{gosterge}: rozet '{kayit['verdikt']}', pasaport '{beklenen}'"
        )


def test_dogrulayici_sahipsiz_gostergeyi_yakalar() -> None:
    """`pasaport.py dogrula` sahipsiz göstergeyi bulgu olarak yazar."""
    hepsi = pasaport.pasaportlar()
    assert not pasaport.gosterge_sahipligi(hepsi), "şu an tutarlı olmalı"

    # Bir pasaportun bildirimini boşaltınca kural ötmeli.
    kirik = [p for p in hepsi if p.kunye.get("gostergeler")]
    assert kirik, "en az bir pasaport gösterge bildiriyor olmalı"
    yedek = dict(kirik[0].kunye)
    kirik[0].kunye = {**yedek, "gostergeler": {}}
    try:
        bulgular = pasaport.gosterge_sahipligi(hepsi)
        assert bulgular, "sahipsiz kalan göstergeler bulgu üretmeliydi"
        assert any("gostergeler" in b.mesaj for b in bulgular)
    finally:
        kirik[0].kunye = yedek


def test_verdikt_adlari_pasaportun_kapali_kumesini_karsilar() -> None:
    """Künyede geçerli olan her verdiktin bir arayüz karşılığı var."""
    assert set(disaktar.VERDIKT_ADI) == set(pasaport.VERDIKTLER)


def test_paket_adlari_pasaportun_kapali_kumesini_karsilar() -> None:
    assert set(disaktar.PAKET_ADI) == set(pasaport.PAKETLER)


def test_durum_adi_tum_sinyal_durumlarini_kapsar() -> None:
    """`SignalState`'e yeni bir durum eklenirse bu test düşer — arayüzde
    etiketsiz hücre çıkmadan önce."""
    import typing

    from quaxis.teknik.core import types

    durumlar = set(typing.get_args(types.SignalState))
    assert durumlar == set(disaktar.DURUM_ADI), (
        f"eşleşmeyen: {durumlar ^ set(disaktar.DURUM_ADI)}"
    )


def test_kesilen_satir_kunyeye_yazilir(tmp_path, monkeypatch) -> None:
    """Sessiz kırpma yasak: sınır yüzünden düşen satır sayısı raporlanır."""
    db = tmp_path / "results.db"
    _sahte_db(db)
    cikti = tmp_path / "tarama-verisi.json"
    monkeypatch.setattr(disaktar, "DEFAULT_DB_PATH", db)
    monkeypatch.setattr(disaktar, "CIKTI", cikti)
    monkeypatch.setattr(disaktar, "_seri_ve_fiyat", lambda *a: ([1.0, 2.0], 2.0))

    kod = disaktar.main(["--run-id", "bist_2026-01-02", "--azami-satir", "1"])
    assert kod == 0
    veri = json.loads(cikti.read_text(encoding="utf-8"))
    assert veri["kunye"]["eslesen"] == 2
    assert veri["kunye"]["yazilan"] == 1
    assert veri["kunye"]["kesilen"] == 1


def _sahte_db(yol: pathlib.Path) -> None:
    """İki sinyallik en küçük veritabanı — gerçek şemayla."""
    from quaxis.teknik.scanner.results import ResultsStore, RunRecord

    with ResultsStore(db_path=yol) as depo:
        depo.start_run(
            RunRecord(
                run_id="bist_2026-01-02", started_at="2026-01-02T00:00:00+00:00",
                finished_at=None, market="bist", timeframes=["1d"], universe_size=2,
                indicator_names=["golden_zone"], git_sha=None, status="running",
            )
        )
        depo.finish_run("bist_2026-01-02", "2026-01-02T00:05:00+00:00", "completed")

    yuk = json.dumps({"giris": 10.0, "stop": 9.0, "hedef": 12.0})
    with sqlite3.connect(yol) as conn:
        for i, sembol in enumerate(("AAAA", "BBBB")):
            conn.execute(
                "INSERT INTO signals VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                ("bist_2026-01-02", sembol, "bist", "1D", "golden_zone", "h",
                 "2026-01-02T00:00:00+00:00", f"2026-01-0{2 + i}T00:00:00+00:00",
                 "long", "confirmed", 1.0, "p", yuk, i),
            )
