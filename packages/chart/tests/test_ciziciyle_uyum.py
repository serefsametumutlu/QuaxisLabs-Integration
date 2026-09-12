"""Python sözleşmesi ile web çizicisi ayrı düşmemeli.

Gerçek risk şu: biri `roller.py`'ye yeni bir rol ekler, çiziciye eklemeyi
unutur. O rol ChartSpec'te geçerli olur ama ekranda `ChartSpecHatasi` atar —
ya da daha kötüsü, ileride biri "hata atmasın" diye varsayılana düşürür ve
ADR-001'in yasakladığı sessiz griye dönüş geri gelir.

Bu test iki tarafı metin düzeyinde karşılaştırır: TypeScript'i çalıştırmaya
gerek yok, rol adları iki dosyada da düz metin.
"""

from __future__ import annotations

import pathlib
import re

import pytest
from quaxis.chart.roller import AlanRol, CizgiRol, EtiketRol, IsaretRol, RozetRol, SeviyeRol, Yon

WEB = pathlib.Path(__file__).resolve().parents[3] / "apps" / "web"
TIPLER = WEB / "lib" / "chartspec.ts"
ROL_TABLOSU = WEB / "components" / "grafik" / "roller.ts"


def _ts_dizisi(kaynak: str, ad: str) -> set[str]:
    """`export const X_ROLLERI = ["a", "b"] as const;` içindeki adları çıkarır."""
    m = re.search(rf"{ad}\s*=\s*\[(.*?)\]\s*as const", kaynak, re.S)
    if not m:
        raise AssertionError(f"{ad} dizisi bulunamadı.")
    return set(re.findall(r'"([^"]+)"', m.group(1)))


@pytest.fixture(scope="module")
def tipler() -> str:
    return TIPLER.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def tablo() -> str:
    return ROL_TABLOSU.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("enum", "ts_adi"),
    [
        (SeviyeRol, "SEVIYE_ROLLERI"),
        (AlanRol, "ALAN_ROLLERI"),
        (CizgiRol, "CIZGI_ROLLERI"),
        (IsaretRol, "ISARET_ROLLERI"),
        (EtiketRol, "ETIKET_ROLLERI"),
        (RozetRol, "ROZET_ROLLERI"),
    ],
)
def test_rol_kumeleri_ayni(enum, ts_adi, tipler):
    py = {u.value for u in enum}
    ts = _ts_dizisi(tipler, ts_adi)
    assert py == ts, (
        f"{enum.__name__} ile {ts_adi} ayrı düşmüş.\n"
        f"  yalnız Python'da: {sorted(py - ts)}\n"
        f"  yalnız TypeScript'te: {sorted(ts - py)}"
    )


@pytest.mark.parametrize(
    "enum",
    [SeviyeRol, AlanRol, CizgiRol, IsaretRol, EtiketRol, RozetRol],
)
def test_her_rolun_cizim_stili_var(enum, tablo):
    """Rol tablosunda karşılığı olmayan rol, ekranda hataya düşer."""
    eksik = [u.value for u in enum if f"{u.value}:" not in tablo]
    assert not eksik, (
        f"{enum.__name__} rollerinin çizici tablosunda karşılığı yok: {eksik}. "
        f"components/grafik/roller.ts'e eklenmeli."
    )


def test_yon_degerleri_ayni(tipler):
    py = {u.value for u in Yon}
    ts = set(re.findall(r'export type Yon = "(\w+)" \| "(\w+)"', tipler)[0])
    assert py == ts


def test_surum_ayni(tipler):
    from quaxis.chart.spec import SURUM

    m = re.search(r'CHARTSPEC_SURUM = "([\d.]+)"', tipler)
    assert m and m.group(1) == SURUM
