"""Pasaport doğrulayıcının testleri.

Bu testler "kod çalışıyor mu" diye sormaz; **kapıların gerçekten kapı olduğunu**
kanıtlar. Önceki projede süreç bir kontrol listesiydi ve listeye uyulmadı —
K5 hiç yapılmadı, K4 sona bırakıldı. Aşağıdaki her test, o hatalardan birinin
artık sessizce yapılamayacağını gösterir.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("pasaport", KOK / "tools" / "pasaport.py")
pasaport = importlib.util.module_from_spec(_spec)
sys.modules["pasaport"] = pasaport
assert _spec.loader is not None
_spec.loader.exec_module(pasaport)


KUNYE = """---
slug: {slug}
ad: Deneme
paket: yapi
referans: ""
verdikt: {verdikt}
kapilar:
{kapilar}
---
"""

GOVDE_ESIK = """
### Eşikler

| Eşik | Değer | Kaynak |
|---|---|---|
| {ad} | {deger} | {kaynak} |

## K1 · Sözleşme
"""


def _kapilar(gecilen: dict[str, dict]) -> str:
    satir = []
    for k in pasaport.KAPILAR:
        v = gecilen.get(k, {})
        gecildi = v.get("gecildi")
        kanit = v.get("kanit", [])
        ek = f", onay: {v['onay'] or 'null'}" if "onay" in v else ""
        satir.append(
            f"  {k}: {{ gecildi: {gecildi or 'null'}, kanit: {kanit}{ek} }}"
        )
    return "\n".join(satir)


def _yaz(tmp: pathlib.Path, slug: str, gecilen: dict, *, verdikt="olculmedi", govde="") -> pathlib.Path:
    p = tmp / f"{slug}.md"
    p.write_text(
        KUNYE.format(slug=slug, verdikt=verdikt, kapilar=_kapilar(gecilen)) + govde,
        encoding="utf-8",
    )
    return p


@pytest.fixture
def pasaport_koku(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    kok = tmp_path / "strateji"
    kok.mkdir()
    monkeypatch.setattr(pasaport, "PASAPORT_KOK", kok)
    monkeypatch.setattr(pasaport, "KOK", tmp_path)
    return kok


def _mesajlar(p) -> str:
    return " ".join(b.mesaj for b in pasaport.dogrula(p))


# ----------------------------------------------------------- 1. kapı sırası


def test_kapi_atlanamaz(pasaport_koku: pathlib.Path) -> None:
    """K2 geçilmiş ama K1 açık — eski süreçte tam olarak bu oluyordu."""
    yol = _yaz(
        pasaport_koku, "x",
        {"K0": {"gecildi": "2026-01-01", "kanit": []}, "K2": {"gecildi": "2026-01-02", "kanit": []}},
    )
    assert "kapı atlanamaz" in _mesajlar(pasaport.oku(yol))


def test_sirayla_gecilmis_kapilar_sikayet_uretmez(pasaport_koku: pathlib.Path) -> None:
    (pasaport_koku.parent / "k.md").write_text("x", encoding="utf-8")
    yol = _yaz(
        pasaport_koku, "x",
        {
            "K0": {"gecildi": "2026-01-01", "kanit": ["k.md"]},
            "K1": {"gecildi": "2026-01-02", "kanit": ["k.md"]},
        },
        govde=GOVDE_ESIK.format(ad="pivot_sag", deger="5", kaynak="Pesavento s.44"),
    )
    assert "kapı atlanamaz" not in _mesajlar(pasaport.oku(yol))


# --------------------------------------------------------------- 2. kanıt


def test_kanitsiz_kapi_gecilemez(pasaport_koku: pathlib.Path) -> None:
    yol = _yaz(pasaport_koku, "x", {"K0": {"gecildi": "2026-01-01", "kanit": []}})
    assert "hiç kanıt gösterilmemiş" in _mesajlar(pasaport.oku(yol))


def test_olmayan_kanit_dosyasi_yakalanir(pasaport_koku: pathlib.Path) -> None:
    yol = _yaz(
        pasaport_koku, "x",
        {"K0": {"gecildi": "2026-01-01", "kanit": ["docs/olcum/yok.md"]}},
        govde=GOVDE_ESIK.format(ad="a", deger="1", kaynak="Kitap s.10"),
    )
    assert "kanıt dosyası yok" in _mesajlar(pasaport.oku(yol))


# -------------------------------------------------- 3. ezberden sayı yasak


def test_kaynaksiz_esik_reddedilir(pasaport_koku: pathlib.Path) -> None:
    (pasaport_koku.parent / "k.md").write_text("x", encoding="utf-8")
    yol = _yaz(
        pasaport_koku, "x",
        {"K0": {"gecildi": "2026-01-01", "kanit": ["k.md"]}},
        govde=GOVDE_ESIK.format(ad="min_salinim_atr", deger="2.0", kaynak="*(…)*"),
    )
    assert "ezberden sayı yasak" in _mesajlar(pasaport.oku(yol))


def test_uydurma_kaynak_reddedilir(pasaport_koku: pathlib.Path) -> None:
    """"genel kabul" gibi bir kaynak geçerli değil: ya sayfa ya K3 ölçümü."""
    (pasaport_koku.parent / "k.md").write_text("x", encoding="utf-8")
    yol = _yaz(
        pasaport_koku, "x",
        {"K0": {"gecildi": "2026-01-01", "kanit": ["k.md"]}},
        govde=GOVDE_ESIK.format(ad="bolge_alt", deger="0.618", kaynak="genel kabul"),
    )
    assert "ne sayfa alıntısı ne K3 ölçümü" in _mesajlar(pasaport.oku(yol))


def test_k3_olcumu_gecerli_kaynaktir(pasaport_koku: pathlib.Path) -> None:
    (pasaport_koku.parent / "k.md").write_text("x", encoding="utf-8")
    yol = _yaz(
        pasaport_koku, "x",
        {"K0": {"gecildi": "2026-01-01", "kanit": ["k.md"]}},
        govde=GOVDE_ESIK.format(ad="min_salinim_atr", deger="2.0", kaynak="K3: docs/olcum/x.md"),
    )
    assert "ezberden" not in _mesajlar(pasaport.oku(yol))


def test_bos_esik_tablosu_yakalanir(pasaport_koku: pathlib.Path) -> None:
    (pasaport_koku.parent / "k.md").write_text("x", encoding="utf-8")
    yol = _yaz(pasaport_koku, "x", {"K0": {"gecildi": "2026-01-01", "kanit": ["k.md"]}})
    assert "Eşikler tablosu boş" in _mesajlar(pasaport.oku(yol))


# ------------------------------------------------------------- 4. verdikt


def test_olculmeden_etiket_konamaz(pasaport_koku: pathlib.Path) -> None:
    """Dürüstlük kuralının (README madde 6) makine karşılığı."""
    yol = _yaz(pasaport_koku, "x", {}, verdikt="kenar-var")
    assert "ölçülmeden etiket konmaz" in _mesajlar(pasaport.oku(yol))


def test_k4_gecilince_verdikt_guncellenmeli(pasaport_koku: pathlib.Path) -> None:
    gecilen = {k: {"gecildi": "2026-01-01", "kanit": ["k.md"]} for k in ("K0", "K1", "K2", "K3", "K4")}
    (pasaport_koku.parent / "k.md").write_text("x", encoding="utf-8")
    yol = _yaz(
        pasaport_koku, "x", gecilen, verdikt="olculmedi",
        govde=GOVDE_ESIK.format(ad="a", deger="1", kaynak="Kitap s.10"),
    )
    assert "verdikt hâlâ 'olculmedi'" in _mesajlar(pasaport.oku(yol))


def test_gecersiz_verdikt_reddedilir(pasaport_koku: pathlib.Path) -> None:
    yol = _yaz(pasaport_koku, "x", {}, verdikt="calisiyor")
    assert "verdikt geçersiz" in _mesajlar(pasaport.oku(yol))


# ------------------------------------------------------- 5. K5 görsel kapısı


def test_k5_kullanici_onayi_olmadan_kapanmaz(pasaport_koku: pathlib.Path, tmp_path) -> None:
    """Eski projede hiç yapılmayan kapı. Onaysız geçilemez."""
    (pasaport_koku.parent / "k.md").write_text("x", encoding="utf-8")
    gecilen = {k: {"gecildi": "2026-01-01", "kanit": ["k.md"]} for k in ("K0", "K1", "K2", "K3", "K4")}
    gecilen["K5"] = {"gecildi": "2026-01-02", "kanit": ["k.md"], "onay": None}
    yol = _yaz(
        pasaport_koku, "x", gecilen, verdikt="kanitlanmadi",
        govde=GOVDE_ESIK.format(ad="a", deger="1", kaynak="Kitap s.10"),
    )
    assert "kullanıcı onayı yok" in _mesajlar(pasaport.oku(yol))


def test_k5_uc_iterasyon_ister(pasaport_koku: pathlib.Path, tmp_path) -> None:
    (pasaport_koku.parent / "k.md").write_text("x", encoding="utf-8")
    ui = tmp_path / "docs" / "design" / "ui"
    ui.mkdir(parents=True)
    (ui / "x-i1.png").write_bytes(b"1")
    gecilen = {k: {"gecildi": "2026-01-01", "kanit": ["k.md"]} for k in ("K0", "K1", "K2", "K3", "K4")}
    gecilen["K5"] = {"gecildi": "2026-01-02", "kanit": ["k.md"], "onay": "2026-01-02"}
    yol = _yaz(
        pasaport_koku, "x", gecilen, verdikt="kanitlanmadi",
        govde=GOVDE_ESIK.format(ad="a", deger="1", kaynak="Kitap s.10"),
    )
    assert "en az 3 iterasyon karesi" in _mesajlar(pasaport.oku(yol))


# --------------------------------------------------- 6. tek strateji kuralı


def test_ayni_anda_iki_strateji_yolda_olamaz(pasaport_koku: pathlib.Path) -> None:
    _yaz(pasaport_koku, "bir", {"K0": {"gecildi": "2026-01-01", "kanit": ["k.md"]}})
    _yaz(pasaport_koku, "iki", {"K0": {"gecildi": "2026-01-02", "kanit": ["k.md"]}})
    bulgular = pasaport.tek_strateji_kurali(pasaport.pasaportlar())
    assert bulgular and "aynı anda 2 strateji yolda" in bulgular[0].mesaj


def test_biten_strateji_yolu_tikamaz(pasaport_koku: pathlib.Path) -> None:
    tam = {k: {"gecildi": "2026-01-01", "kanit": ["k.md"]} for k in pasaport.KAPILAR}
    _yaz(pasaport_koku, "bitti", tam, verdikt="kanitlanmadi")
    _yaz(pasaport_koku, "yeni", {"K0": {"gecildi": "2026-02-01", "kanit": ["k.md"]}})
    assert pasaport.tek_strateji_kurali(pasaport.pasaportlar()) == []


# ------------------------------------------------------------------ şablon


def test_depodaki_sablon_okunabilir_ve_bos_kapilarla_gelir() -> None:
    """Şablonun kendisi geçerli bir pasaport olmalı — yoksa `yeni` komutu
    bozuk dosya üretir."""
    p = pasaport.oku(pasaport.SABLON)
    assert p.gecilen == []
    assert p.kunye["verdikt"] == "olculmedi"
    assert set(p.kunye["kapilar"]) == set(pasaport.KAPILAR)
