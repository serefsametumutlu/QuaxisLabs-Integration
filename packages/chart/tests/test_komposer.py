"""Salınım Fibo ABCD komposeri — referansın neyi göstermesi gerektiğini sabitler."""

from __future__ import annotations

import dataclasses

import pytest
from quaxis.chart.komposer.swing_fib_abcd import bestele
from quaxis.chart.ornek.thyao_swing_fib_abcd import fib, sonuc
from quaxis.chart.roller import AlanRol, RozetRol, SeviyeRol


@pytest.fixture(scope="module")
def spec():
    return bestele(sonuc(), ornek_mi=True)


def _rol(spec, tur):
    return [k for k in spec.katmanlar if k.tur == tur]


def test_fibo_merdiveni_tam_dokuz_seviye(spec):
    seviyeler = _rol(spec, "seviye")
    assert len(seviyeler) == 9
    assert {s.rol for s in seviyeler} == {
        SeviyeRol.FIB_0,
        SeviyeRol.FIB_236,
        SeviyeRol.FIB_382,
        SeviyeRol.FIB_500,
        SeviyeRol.FIB_618,
        SeviyeRol.FIB_786,
        SeviyeRol.FIB_1,
        SeviyeRol.FIB_1272,
        SeviyeRol.FIB_1618,
    }


def test_referanstaki_fiyatlar_birebir(spec):
    """Referans görselden okunan sayılar. Değişirse grafik referansı tutmaz."""
    beklenen = {
        SeviyeRol.FIB_0: 209.10,
        SeviyeRol.FIB_236: 199.90,
        SeviyeRol.FIB_382: 194.20,
        SeviyeRol.FIB_500: 189.60,
        SeviyeRol.FIB_618: 185.00,
        SeviyeRol.FIB_786: 178.45,
        SeviyeRol.FIB_1: 170.10,
        SeviyeRol.FIB_1272: 159.49,
        SeviyeRol.FIB_1618: 146.00,
    }
    bulunan = {s.rol: s.fiyat for s in _rol(spec, "seviye")}
    assert bulunan == pytest.approx(beklenen)


def test_fibo_bandi_0618_0786_arasi(spec):
    (bant,) = _rol(spec, "bant")
    assert bant.rol is AlanRol.BOLGE_ALTIN
    assert bant.alt == pytest.approx(fib(0.786))
    assert bant.ust == pytest.approx(fib(0.618))


def test_iki_formasyon_govdesi(spec):
    alanlar = _rol(spec, "alan")
    assert len(alanlar) == 2
    assert all(a.rol is AlanRol.FORMASYON for a in alanlar)
    assert all(len(a.noktalar) == 3 for a in alanlar)


def test_tamamlanma_rozeti_yon_tasir(spec):
    (rozet,) = _rol(spec, "rozet")
    assert rozet.rol is RozetRol.DURUM_TAMAMLANDI
    assert rozet.yon.value == "sat"
    assert "159.49" in rozet.metin


def test_kose_isaretleri_bes_pivot(spec):
    isaretler = _rol(spec, "isaret")
    assert {i.metin for i in isaretler} == {"X", "A", "B", "C", "D"}


def test_pivotlar_ONAY_barinda_cizilir():
    """Non-repaint sözleşmesinin çizim tarafı: işaret pivotun kendi barında
    değil, ONAYLANDIĞI barda durur. Yoksa grafik geçmişi yeniden yazar."""
    s = sonuc()
    spec = bestele(s, ornek_mi=True)
    a = s.pivot("A")
    assert a.onay_t > a.t
    kose_a = next(k for k in spec.katmanlar if k.tur == "isaret" and k.metin == "A")
    assert kose_a.nokta.t == a.onay_t


def test_bilinmeyen_durum_reddedilir():
    s = dataclasses.replace(sonuc(), durum="belirsiz")
    with pytest.raises(ValueError, match="Bilinmeyen formasyon durumu"):
        bestele(s)


def test_eksik_pivot_uydurulmaz():
    s = sonuc()
    eksik = dataclasses.replace(s, pivotlar=[p for p in s.pivotlar if p.etiket != "A"])
    with pytest.raises(ValueError, match="pivotu sonuçta yok"):
        bestele(eksik)


def test_y_araligi_merdiveni_kapsar(spec):
    """1.618 mumların çok altında; panel aralığı onu içermezse 'nereye kadar
    düşebilir' sorusu grafikte cevapsız kalır."""
    fiyat = next(p for p in spec.paneller if p.id == "fiyat")
    assert fiyat.y is not None
    assert fiyat.y.alt < 146.00
    assert fiyat.y.ust > 209.10
    assert fiyat.y.gerekce  # gerekçe yazılmadan aralık genişletilemez


def test_seriler_tam_dizi(spec):
    assert all(len(s.veri) == 140 for s in spec.seriler)


def test_uretim_deterministik():
    """Aynı fikstür = bit bit aynı ChartSpec. Deterministiklik kuralı."""
    assert bestele(sonuc(), ornek_mi=True).json() == bestele(sonuc(), ornek_mi=True).json()
