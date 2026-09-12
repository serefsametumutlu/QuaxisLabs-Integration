"""K3/K4 ölçüm makinesinin testleri.

En önemli iki test şunlar: **gerçekten var olan bir kenarı buluyor mu** ve
**olmayan bir kenarı uyduruyor mu**. Bir ölçüm aracı bu ikisini geçmiyorsa,
verdiği her sayı süstür.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quaxis.teknik.core.types import Signal
from quaxis.teknik.olcum.ileri_getiri import (
    bh_fdr,
    forward_return,
    measure,
    measure_symbol,
)
from quaxis.teknik.olcum.kalibrasyon import calibrate

UFUK = 10
TUR = 400  # testte hız için düşük; üretimde 2000


def _seri(n: int = 400, tohum: int = 1, egim: float = 0.0) -> pd.Series:
    r = np.random.default_rng(tohum)
    adim = r.normal(egim, 1.0, n)
    kapanis = 100 + np.cumsum(adim)
    idx = pd.date_range("2024-01-01", periods=n, freq="1D", tz="UTC")
    return pd.Series(kapanis, index=idx, name="close")


def _sinyal(t, yon="long") -> Signal:
    return Signal(t, t, yon, "confirmed", 1.0, {})


# ------------------------------------------------------------ ileri getiri


def test_ileri_getiri_dogru_hesaplanir() -> None:
    idx = pd.date_range("2024-01-01", periods=5, freq="1D", tz="UTC")
    s = pd.Series([100.0, 101.0, 102.0, 103.0, 110.0], index=idx)
    assert forward_return(s, idx[0], 4) == pytest.approx(0.10)


def test_yeterli_ileri_bar_yoksa_none_doner() -> None:
    """Eksik veriyi sıfır saymak stratejiyi kayırmanın en sessiz yoludur."""
    idx = pd.date_range("2024-01-01", periods=5, freq="1D", tz="UTC")
    s = pd.Series([100.0, 101, 102, 103, 110], index=idx)
    assert forward_return(s, idx[3], 4) is None


# ------------------------------------------------- kenar var / kenar yok


def test_gercek_kenari_bulur() -> None:
    """Sinyaller BİLEREK yükselişin hemen öncesine konursa ölçüm bunu
    yakalamalı. Yakalayamayan bir araç hiçbir şey kanıtlamaz."""
    seri, sinyaller = {}, {}
    for i in range(25):
        s = _seri(tohum=i)
        seri[f"S{i}"] = s
        # OOS penceresinde, ileri getirisi en yüksek 6 bara sinyal koy.
        oos = int(len(s) * 0.7)
        ileri = s.to_numpy()[oos + UFUK :] / s.to_numpy()[oos:-UFUK] - 1.0
        en_iyi = np.argsort(ileri)[-6:]
        sinyaller[f"S{i}"] = [_sinyal(s.index[oos + int(k)]) for k in en_iyi]

    sonuc = measure(seri, sinyaller, horizon=UFUK, permutations=TUR, seed=7)
    assert sonuc.independent_observations == 25
    assert sonuc.mean_difference > 0
    assert sonuc.p_value < 0.05, sonuc
    assert sonuc.verdict == "kenar-var"


def test_kenar_yokken_kenar_uydurmaz() -> None:
    """Rastgele barlara konmuş sinyaller "çalışıyor" görünmemeli."""
    r = np.random.default_rng(42)
    seri, sinyaller = {}, {}
    for i in range(25):
        s = _seri(tohum=100 + i)
        seri[f"S{i}"] = s
        oos = int(len(s) * 0.7)
        barlar = r.integers(oos, len(s) - UFUK, size=6)
        sinyaller[f"S{i}"] = [_sinyal(s.index[int(b)]) for b in barlar]

    sonuc = measure(seri, sinyaller, horizon=UFUK, permutations=TUR, seed=7)
    assert sonuc.p_value > 0.05, sonuc
    assert sonuc.verdict == "kanitlanmadi"


def test_yukselen_piyasa_tek_basina_kenar_sayilmaz() -> None:
    """ADİL BAZ testi: piyasa güçlü yükselirken rastgele konmuş LONG
    sinyaller pozitif getirir — ama baz da aynı kadar getirir, fark kalmaz.
    Bu ayıklama olmasaydı her strateji boğa piyasasında "çalışıyor" görünürdü."""
    r = np.random.default_rng(3)
    seri, sinyaller = {}, {}
    for i in range(25):
        s = _seri(tohum=200 + i, egim=0.35)  # güçlü yükseliş
        seri[f"S{i}"] = s
        oos = int(len(s) * 0.7)
        barlar = r.integers(oos, len(s) - UFUK, size=6)
        sinyaller[f"S{i}"] = [_sinyal(s.index[int(b)]) for b in barlar]

    sonuc = measure(seri, sinyaller, horizon=UFUK, permutations=TUR, seed=7)
    ham = np.mean([o.signal_return for o in sonuc.measurements])
    assert ham > 0, "kurgu gereği ham getiri pozitif olmalı"
    assert sonuc.p_value > 0.05, sonuc
    assert sonuc.verdict == "kanitlanmadi"


# -------------------------------------------------------- sembol kümeleme


def test_sinyalsiz_sembol_gozlem_sayilmaz() -> None:
    """Bağımsız gözlem SEMBOL'dür; sinyal üretmeyen sembol n'i şişirmez."""
    seri = {f"S{i}": _seri(tohum=i) for i in range(10)}
    sinyaller = {"S0": [_sinyal(seri["S0"].index[350])]}
    sonuc = measure(seri, sinyaller, horizon=UFUK, permutations=50, seed=1)
    assert sonuc.universe == 10
    assert sonuc.independent_observations == 1


def test_is_penceresindeki_sinyaller_sayilmaz() -> None:
    """İddia GÖRÜLMEMİŞ dönemde ölçülür; IS'teki sinyal gözlem üretmez."""
    s = _seri()
    erken = [_sinyal(s.index[10])]
    assert measure_symbol("S", s, erken, horizon=UFUK, permutations=20) is None


def test_short_sinyal_yonu_duzeltilir() -> None:
    """Düşüşte açılan short kazandırır; ölçüm bunu pozitif saymalı."""
    idx = pd.date_range("2024-01-01", periods=200, freq="1D", tz="UTC")
    dusen = pd.Series(np.linspace(200, 100, 200), index=idx)
    t = idx[150]
    olcum = measure_symbol("S", dusen, [_sinyal(t, "short")], horizon=UFUK, permutations=20)
    assert olcum is not None
    assert olcum.signal_return > 0


# --------------------------------------------------------------- BH-FDR


def test_fdr_tek_sansli_bulgu_elenir() -> None:
    """20 stratejinin biri tesadüfen p=0.04 verir; düzeltme onu geçirmemeli."""
    p = {f"s{i}": 0.9 for i in range(19)}
    p["sansli"] = 0.04
    assert bh_fdr(p, q=0.05)["sansli"] is False


def test_fdr_gercek_bulgulari_gecirir() -> None:
    p = {f"guclu{i}": 0.0001 for i in range(5)}
    p.update({f"zayif{i}": 0.8 for i in range(5)})
    sonuc = bh_fdr(p, q=0.05)
    assert all(sonuc[f"guclu{i}"] for i in range(5))
    assert not any(sonuc[f"zayif{i}"] for i in range(5))


def test_fdr_bos_aile() -> None:
    assert bh_fdr({}) == {}


# ---------------------------------------------------------- kalibrasyon


def test_sifir_aday_bozuk_teshisi() -> None:
    """648/648 sembolde sıfır aday — önceki projenin sessiz hatası."""
    sonuc = calibrate("x", "4H", {f"S{i}": 0 for i in range(648)})
    assert sonuc.zero_candidate_symbols == 648
    assert "BOZUK" in sonuc.diagnosis


def test_cok_gevsek_teshisi() -> None:
    sonuc = calibrate("x", "1D", {f"S{i}": 200 for i in range(100)})
    assert "ÇOK GEVŞEK" in sonuc.diagnosis


def test_makul_teshis() -> None:
    sonuc = calibrate("x", "1D", {f"S{i}": (i % 7) for i in range(100)})
    assert "MAKUL" in sonuc.diagnosis
    assert sonuc.per_symbol_max == 6


def test_hatali_sembol_sifir_adaydan_ayri_sayilir() -> None:
    """"Veri çekilemedi" ile "aday bulunamadı" aynı şey değildir."""
    sonuc = calibrate("x", "1D", {"A": 3, "B": 0}, error_symbols=5)
    assert sonuc.error_symbols == 5
    assert sonuc.zero_candidate_symbols == 1
