"""Harmonik formasyonlar — K1/K2 testleri.

Bu dosyanın iki işi var:

1. **Kuralı kilitlemek.** Her formasyon için kitabın oranlarıyla kurulmuş
   sentetik bir "ders kitabı" örneği var. Oranlar kaydığında bu testler
   düşer — dedektörün kuralı sessizce değişemez.
2. **Non-repaint sözleşmesini kanıtlamak.** Harmonik dedektörlerin klasik
   hatası D'yi sonradan oluşmuş bir dip olarak aramaktır. Buradaki testler
   D'nin BİR HEDEF olduğunu ve geçmişe hiçbir şeyin kaydırılmadığını
   doğrular.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quaxis.teknik.core.types import Timeframe
from quaxis.teknik.indicators.harmonik import (
    Abcd,
    AbcdParams,
    Gartley,
    GartleyParams,
    HarmonikParams,
    Kelebek,
    KelebekParams,
    UcSurus,
    UcSurusParams,
)
from quaxis.teknik.indicators.harmonik.dedektor import HarmonikTemel, oran_uyar
from quaxis.teknik.indicators.harmonik.pivotlar import Pivot, pivotlar, zincire_ekle

ONEK = [130.0, 118.0, 132.0, 115.0]
"""Formasyondan ÖNCE gelen gürültü: ısınmayı doldurur ve zincirin
formasyonu boşlukta değil, gerçek bir salınım dizisinin içinde bulmasını
sağlar."""


def yol(noktalar: list[float], adim: int = 12) -> np.ndarray:
    """Verilen köşelerden geçen parçalı doğrusal fiyat yolu."""
    out = [noktalar[0]]
    for a, b in zip(noktalar, noktalar[1:], strict=False):
        out += list(np.linspace(a, b, adim + 1))[1:]
    return np.array(out)


def cerceve(k: np.ndarray) -> pd.DataFrame:
    idx = pd.date_range("2020-01-01", periods=len(k), freq="1D", tz="UTC")
    df = pd.DataFrame(
        {
            "open": k,
            "high": k * 1.0005,
            "low": k * 0.9995,
            "close": k,
            "volume": np.full(len(k), 1e6),
        },
        index=idx,
    )
    df.attrs["timeframe"] = Timeframe.D1
    df.attrs["symbol"] = "TEST"
    return df


def aynala(df: pd.DataFrame, eksen: float) -> pd.DataFrame:
    """Çerçeveyi fiyat ekseninde yansıtır: tepeler dip, dipler tepe olur.

    Yalnız kapanışı yansıtıp fitilleri yeniden türetmek YETMEZ — bu
    çerçevede fitiller çarpımsal (`close * 1.0005`), dolayısıyla yansıtılmış
    seride aynı fitiller oluşmaz ve pivot FİYATLARI birebir aynalanmaz.
    Testin ölçmek istediği şey dedektörün x-uzayı dönüşümü; girdideki
    asimetri o ölçümü bulandırırdı.
    """
    ters = df.copy()
    ters["open"] = eksen - df["open"]
    ters["close"] = eksen - df["close"]
    ters["high"] = eksen - df["low"]
    ters["low"] = eksen - df["high"]
    ters.attrs.update(df.attrs)
    return ters


# ------------------------------------------------- ders kitabı formasyonları
#
# Oranlar kitaptan. Gartley ve Kelebek'te AB bacağı SERBEST seçilmedi:
# "içinde AB=CD olmalı" kuralı, D'nin XA'ya sabitlenmesiyle birleşince AB'yi
# belirli bir bantla sınırlar. Aşağıdaki değerler o bandın içinden.

X, A = 100.0, 200.0
XA = A - X


def gartley_yolu() -> np.ndarray:
    ab, bc = 0.647, 0.786  # ab = .786 / (2 - bc)
    b = A - ab * XA
    c = b + bc * (A - b)
    d = A - 0.786 * XA
    return yol([*ONEK, X, A, b, c, d - 3.0])


def kelebek_yolu() -> np.ndarray:
    ab, bc = 0.618, 0.618
    b = A - ab * XA
    c = b + bc * (A - b)
    d = A - 1.272 * XA
    return yol([*ONEK, X, A, b, c, d - 3.0])


def abcd_yolu() -> np.ndarray:
    a, b = 200.0, 120.0
    c = b + 0.618 * (a - b)
    d = c - (a - b)
    return yol([150.0, 160.0, 145.0, a, b, c, d - 3.0])


def uc_surus_yolu() -> np.ndarray:
    o, s1 = 215.0, 140.0
    a = s1 + 0.618 * (o - s1)
    s2 = a - 1.272 * (a - s1)
    c = s2 + 0.618 * (a - s2)
    d3 = c - 1.272 * (c - s2)
    return yol([210.0, 218.0, 205.0, o, s1, a, s2, c, d3 - 3.0])


ORNEKLER: list[tuple[str, type[HarmonikTemel], np.ndarray]] = [
    ("abcd", Abcd, abcd_yolu()),
    ("gartley", Gartley, gartley_yolu()),
    ("kelebek", Kelebek, kelebek_yolu()),
    ("uc_surus", UcSurus, uc_surus_yolu()),
]


@pytest.mark.parametrize(("ad", "sinif", "fiyat"), ORNEKLER)
def test_ders_kitabi_formasyonu_bulunur(
    ad: str, sinif: type[HarmonikTemel], fiyat: np.ndarray
) -> None:
    """Kitabın oranlarıyla kurulmuş formasyon TAM OLARAK bir kez bulunmalı."""
    sonuc = sinif()(cerceve(fiyat))
    assert len(sonuc.signals) == 1, f"{ad}: {len(sonuc.signals)} sinyal"
    assert sonuc.signals[0].direction == "long"


@pytest.mark.parametrize(("ad", "sinif", "fiyat"), ORNEKLER)
def test_ayi_tarafi_aynadir(
    ad: str, sinif: type[HarmonikTemel], fiyat: np.ndarray
) -> None:
    """Fiyat serisi aynalanınca AYNI formasyon ters yönde bulunmalı.

    Hesap x-uzayında yapılıyor (ayıda fiyatlar -1 ile çarpılır). Bu test o
    dönüşümün doğru olduğunu kilitler: ayı tarafı ayrı bir formül kümesi
    olsaydı, birinde yapılan düzeltme diğerine geçmeyebilirdi.
    """
    eksen = 400.0
    boga = sinif()(cerceve(fiyat))
    ayi = sinif()(aynala(cerceve(fiyat), eksen))
    assert len(ayi.signals) == len(boga.signals) == 1
    assert ayi.signals[0].direction == "short"
    for alan in ("giris", "stop", "hedef"):
        assert ayi.signals[0].payload[alan] == pytest.approx(
            eksen - boga.signals[0].payload[alan], rel=1e-9
        )


@pytest.mark.parametrize(("ad", "sinif", "fiyat"), ORNEKLER)
def test_stop_ve_hedef_girisin_dogru_taraflarinda(
    ad: str, sinif: type[HarmonikTemel], fiyat: np.ndarray
) -> None:
    """Boğada stop girişin ALTINDA, hedef ÜSTÜNDE olmalı.

    Ölçülmüş bir hatanın kilidi: Golden Zone'da stop bölgeye göre, giriş bar
    kapanışına göre hesaplanıyordu ve ikisi çakıştığında risk SIFIR oluyordu
    — +48R gibi saçma bazlar doğurmuştu.
    """
    s = sinif()(cerceve(fiyat)).signals[0].payload
    assert s["stop"] < s["giris"] < s["hedef"]
    assert s["odul_risk"] > 0


# --------------------------------------------------------- K2: non-repaint


@pytest.mark.parametrize(("ad", "sinif", "fiyat"), ORNEKLER)
def test_repaint_yok(ad: str, sinif: type[HarmonikTemel], fiyat: np.ndarray) -> None:
    """Seri farklı yerlerden kesilince, kesime kadarki sinyaller BİREBİR
    aynı kalmalı. Kalmıyorsa dedektör geleceği görüyor demektir."""
    df = cerceve(fiyat)
    dedektor = sinif()
    tam = dedektor(df)

    def ozet(sonuc: object) -> list[tuple]:
        return [
            (s.bar_time, s.detected_at, s.direction, round(s.payload["giris"], 9))
            for s in sonuc.signals  # type: ignore[attr-defined]
        ]

    for kesim in range(40, len(df) + 1, 7):
        kesik = dedektor(cerceve(fiyat[:kesim]))
        kesim_t = df.index[kesim - 1]
        beklenen = [x for x in ozet(tam) if x[1] <= kesim_t]
        assert ozet(kesik) == beklenen, f"{ad}: kesim={kesim} ayrışıyor"


@pytest.mark.parametrize(("ad", "sinif", "fiyat"), ORNEKLER)
def test_sinyal_pivot_barinda_degil_dokunma_barinda_dogar(
    ad: str, sinif: type[HarmonikTemel], fiyat: np.ndarray
) -> None:
    """`bar_time` formasyonun son pivotu, `detected_at` D'ye dokunulan bar.

    İkisi eşit çıkarsa dedektör D'yi bir pivot sanıyor demektir — harmonik
    repaint'in tam kaynağı budur.
    """
    s = sinif()(cerceve(fiyat)).signals[0]
    assert s.detected_at > s.bar_time
    onay = pd.Timestamp(s.payload["onay_bar"])
    assert s.bar_time < onay <= s.detected_at


def test_d_onceden_vurulmussa_kurulum_acilmaz() -> None:
    """C onaylanana kadar geçen barlarda D zaten vurulduysa sinyal YOKTUR.

    O aralıkta formasyonun varlığını bilmiyorduk; dokunuşu sinyal saymak
    gerçekte verilemeyecek bir emri ölçüme eklemek olurdu.
    """
    ab, bc = 0.647, 0.786
    b = A - ab * XA
    c = b + bc * (A - b)
    d = A - 0.786 * XA
    # C'den sonra tek bir barda D'nin ALTINA çakılan seri: C'nin onayı
    # (pivot_sag = 3 bar) gelmeden dokunuş olup biter.
    fiyat = np.concatenate([yol([*ONEK, X, A, b, c]), np.array([d - 20.0] * 10)])
    assert Gartley()(cerceve(fiyat)).signals == []


def test_sure_dolunca_kurulum_olur() -> None:
    """D'ye uzun süre dokunulmazsa kurulum ölür; aylar sonraki tesadüfi bir
    dokunuş formasyonun sonucu sayılamaz."""
    ab, bc = 0.647, 0.786
    b = A - ab * XA
    c = b + bc * (A - b)
    d = A - 0.786 * XA
    yatay = np.full(60, c - 1.0)
    fiyat = np.concatenate([yol([*ONEK, X, A, b, c]), yatay, yol([c - 1.0, d - 3.0])])
    kisa = Gartley(GartleyParams(donus_max_bar=10))(cerceve(fiyat))
    uzun = Gartley(GartleyParams(donus_max_bar=200))(cerceve(fiyat))
    assert kisa.signals == []
    assert len(uzun.signals) == 1


def test_c_asilirsa_kurulum_gecersizdir() -> None:
    """C'nin ötesinde GÖVDE kapanışı formasyonu bozar: C'nin son salınım ucu
    olduğu varsayımı çöker."""
    ab, bc = 0.647, 0.786
    b = A - ab * XA
    c = b + bc * (A - b)
    d = A - 0.786 * XA
    fiyat = yol([*ONEK, X, A, b, c, c + 30.0, d - 3.0])
    assert Gartley()(cerceve(fiyat)).signals == []


# ------------------------------------------------------ K1: kural kilitleri


def test_bc_ab_yi_asarsa_abcd_gecersiz() -> None:
    """Kitabın açık kuralı: BC, AB'yi aşarsa formasyon yoktur."""
    a, b = 200.0, 120.0
    c = b + 1.10 * (a - b)  # BC > AB
    d = c - (a - b)
    assert Abcd()(cerceve(yol([150.0, 160.0, 145.0, a, b, c, d - 3.0]))).signals == []


def test_gartley_d_x_i_asarsa_bulunmaz() -> None:
    """D, X'i aşarsa o artık Gartley değil Kelebek'tir."""
    ab, bc = 0.618, 0.618
    b = A - ab * XA
    c = b + bc * (A - b)
    d = A - 1.272 * XA  # X'in altında
    fiyat = yol([*ONEK, X, A, b, c, d - 3.0])
    assert Gartley()(cerceve(fiyat)).signals == []
    assert len(Kelebek()(cerceve(fiyat)).signals) == 1


def test_abcd_sarti_kapatilinca_daha_cok_formasyon_gecer() -> None:
    """Şart bir PARAMETRE: kenar ekleyip eklemediği K4'te ölçülebilsin diye.

    Kapatıldığında eleme gevşer, yani açıkken gerçekten eliyor demektir.
    """
    r = np.random.default_rng(11)
    fiyat = 100 * np.exp(np.cumsum(r.normal(0, 0.02, 3000)))
    df = cerceve(fiyat)
    sikı = len(Gartley()(df).signals)
    gevsek = len(Gartley(GartleyParams(abcd_sarti=False))(df).signals)
    assert gevsek > sikı


def test_tolerans_daraldikca_sinyal_azalir() -> None:
    """Tolerans kitapta YOK; K3'ten türetilecek. En azından monoton olmalı —
    olmasaydı 'toleransı ölçümle seçmek' anlamsız olurdu."""
    r = np.random.default_rng(3)
    df = cerceve(100 * np.exp(np.cumsum(r.normal(0, 0.02, 3000))))
    sayilar = [
        len(Abcd(AbcdParams(tolerans=t))(df).signals) for t in (0.02, 0.05, 0.10)
    ]
    assert sayilar == sorted(sayilar)


def test_ayni_pivot_dizisinden_ikinci_kurulum_dogmaz() -> None:
    """Zincir her değiştiğinde aday aranır; aynı X/A/B/C dizisi iki kez
    kurulum üretirse sinyaller sahte biçimde çoğalır."""
    r = np.random.default_rng(5)
    df = cerceve(100 * np.exp(np.cumsum(r.normal(0, 0.02, 4000))))
    sonuc = Abcd()(df)
    anahtarlar = [
        tuple(n["bar"] for n in s.payload["noktalar"].values()) for s in sonuc.signals
    ]
    assert len(anahtarlar) == len(set(anahtarlar))


def test_payload_olcume_gereken_alanlari_tasir() -> None:
    """K4 üç bariyerli R'yi bu üç alandan okur; taşımazsa ölçüm kendi
    seviyelerini uydurur."""
    s = Gartley()(cerceve(gartley_yolu())).signals[0]
    assert set(s.payload) >= {
        "giris",
        "stop",
        "hedef",
        "zaman_bariyeri",
        "odul_risk",
        "oranlar",
        "noktalar",
    }
    # KURAL-28/29 işaretleri SAYIDIR, filtre değil.
    assert set(s.payload) >= {"gap_atr", "kuyruk_kapanis", "cimbiz", "aralik_atr"}


def test_baglam_alanlari_golden_zone_ile_ayni_adlari_kullanir() -> None:
    """`tools/kosul_taramasi.py` iki stratejiyi aynı koşul kümesiyle
    tarayabilsin ve sonuçlar yan yana konabilsin diye."""
    s = Gartley()(cerceve(gartley_yolu())).signals[0]
    assert set(s.payload) >= {
        "ema50_uyum",
        "ema200_uyum",
        "macd_uyum",
        "adx14",
        "rsi14",
        "bb_yuzdelik",
        "stok14",
        "obv_uyum",
        "ciro",
    }


def test_kisa_seride_cokmez() -> None:
    for sinif in (Abcd, Gartley, Kelebek, UcSurus):
        assert sinif()(cerceve(np.linspace(100, 110, 20))).signals == []


# ---------------------------------------------------------------- pivotlar


def test_zincir_almasiktir() -> None:
    """Art arda iki tepe zincire GİRMEZ; yalnız daha uç olan kalır."""
    zincir: list[Pivot] = []
    assert zincire_ekle(zincir, Pivot(0, 100.0, True, 3))
    assert not zincire_ekle(zincir, Pivot(5, 95.0, True, 8))  # daha alçak tepe
    assert zincir[-1].fiyat == 100.0
    assert zincire_ekle(zincir, Pivot(6, 110.0, True, 9))  # daha yüksek tepe
    assert zincir == [Pivot(6, 110.0, True, 9)]
    assert zincire_ekle(zincir, Pivot(9, 90.0, False, 12))
    assert [p.tepe for p in zincir] == [True, False]


def test_pivot_onay_bari_sag_kol_kadar_sonradir() -> None:
    """Bir uç, sağındaki `sag` bar kapanmadan BİLİNEMEZ."""
    k = np.array([1.0, 2, 3, 9, 3, 2, 1, 2, 3], dtype=float)
    (tepe,) = [p for p in pivotlar(k, k, 3, 3) if p.tepe]
    assert tepe.i == 3
    assert tepe.onay_i == 6


def test_oran_uyar_en_yakini_secer() -> None:
    assert oran_uyar(0.60, (0.5, 0.618, 0.786), 0.05) == 0.618
    assert oran_uyar(0.60, (0.5, 0.618, 0.786), 0.01) is None
    assert oran_uyar(float("nan"), (0.5,), 0.5) is None


# ------------------------------------------------------------ parametreler


def test_tolerans_sinirlari() -> None:
    with pytest.raises(ValueError, match="tolerans"):
        HarmonikParams(tolerans=0.6)
    with pytest.raises(ValueError, match="tolerans"):
        HarmonikParams(tolerans=0.0)


def test_kelebek_uzantisi_biri_asmali() -> None:
    with pytest.raises(ValueError, match="D, X'i AŞMALI"):
        KelebekParams(d_uzanti=0.786)


def test_kelebek_stop_girisin_disinda_olmali() -> None:
    with pytest.raises(ValueError, match="uzantı sırası bozuk"):
        KelebekParams(d_uzanti=1.618, stop_uzanti=1.272)


def test_abcd_stop_girisin_otesinde_olmali() -> None:
    with pytest.raises(ValueError, match="stop oranı"):
        AbcdParams(cd_orani=1.272, stop_orani=1.0)


def test_gartley_d_bir_i_asamaz() -> None:
    with pytest.raises(ValueError, match="Kelebek olur"):
        GartleyParams(d_geri_cekilme=1.272)


def test_surus_uzantisi_biri_asmali() -> None:
    with pytest.raises(ValueError, match="sürüş uzantısı"):
        UcSurusParams(surus_uzanti=0.786)


def test_bar_alanlari_zaman_dilimine_gore_olceklenir() -> None:
    """`donus_max_bar` TAKVİMSEL bir süre: 4H'te aynı takvim penceresi daha
    çok bar eder. Ölçeklenmezse haftalıkta kurulum hiç yaşamaz."""
    p = HarmonikParams(donus_max_bar=40)
    assert p.for_timeframe(Timeframe.H4).donus_max_bar == 120
    assert p.for_timeframe(Timeframe.W1).donus_max_bar == 8
