"""Üç bariyerli R ölçümünün testleri.

Kritik olanlar: **aynı barda iki bariyer de vurulduğunda stop kazanıyor mu**
(iyimserlik testi) ve **gerçek bir asimetrik kenarı bulup olmayanı
uydurmuyor mu**.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quaxis.teknik.core.types import Signal
from quaxis.teknik.olcum.bariyer import _toplu_r, barrier_outcome, measure_r

TUR = 200  # testte hız için düşük; üretimde 2000

#: Mekanik testleri maliyetSİZ koşar: "hangi bariyer vuruldu" sorusunun
#: cevabı komisyona bağlı değildir. Maliyetin kendisi ayrı testlerde ölçülür.
BEDAVA = {"komisyon": 0.0, "kayma": 0.0}


def _ohlc(kapanis: list[float], *, yuksek=None, dusuk=None) -> pd.DataFrame:
    idx = pd.date_range("2024-01-01", periods=len(kapanis), freq="1D", tz="UTC")
    k = np.asarray(kapanis, dtype=float)
    return pd.DataFrame(
        {
            "open": k,
            "high": k if yuksek is None else np.asarray(yuksek, dtype=float),
            "low": k if dusuk is None else np.asarray(dusuk, dtype=float),
            "close": k,
            "volume": np.ones(len(k)),
        },
        index=idx,
    )


def _sinyal(t, yon="long") -> Signal:
    return Signal(t, t, yon, "confirmed", 1.0, {})


# ------------------------------------------------------------ tek işlem


def test_hedefe_ulasan_islem_pozitif_r() -> None:
    df = _ohlc([100, 101, 102, 103, 104, 105])
    s = barrier_outcome(df, df.index[0], stop=98.0, target=104.0, **BEDAVA)
    assert s is not None
    assert s.outcome == "hedef"
    assert s.r_multiple == 2.0  # (104-100)/(100-98)
    assert s.bars_held == 4


def test_stopa_carpan_islem_eksi_bir_r() -> None:
    df = _ohlc([100, 99, 98, 97])
    s = barrier_outcome(df, df.index[0], stop=98.0, target=110.0, **BEDAVA)
    assert s is not None
    assert s.outcome == "stop"
    assert s.r_multiple == -1.0


def test_ayni_barda_iki_bariyer_de_vurulursa_stop_kazanir() -> None:
    """Bar içi sıralamayı bilmiyoruz; emin olmadığımız yerde stratejinin
    LEHİNE varsaymak backtest'i yalancı yapar."""
    df = _ohlc([100, 100], yuksek=[100, 120], dusuk=[100, 90])
    s = barrier_outcome(df, df.index[0], stop=95.0, target=110.0, **BEDAVA)
    assert s is not None
    assert s.outcome == "stop"
    assert s.r_multiple == -1.0


def test_hicbir_bariyer_vurulmazsa_zaman_cikisi() -> None:
    df = _ohlc([100, 100.5, 101, 100.2, 100.8])
    s = barrier_outcome(df, df.index[0], stop=90.0, target=120.0, max_bars=3, **BEDAVA)
    assert s is not None
    assert s.outcome == "zaman"
    assert s.bars_held == 3
    assert s.r_multiple == (100.2 - 100) / 10


def test_short_yonu_dogru_isaretlenir() -> None:
    """Düşüşte açılan short hedefe ulaşır; R pozitif olmalı."""
    df = _ohlc([100, 98, 96, 94])
    s = barrier_outcome(df, df.index[0], stop=102.0, target=96.0, direction="short", **BEDAVA)
    assert s is not None
    assert s.outcome == "hedef"
    assert s.r_multiple == 2.0  # (100-96)/(102-100)


def test_stop_yanlis_tarafta_ise_olculmez() -> None:
    """Long'ta stop girişin üstündeyse sinyal geçersizdir; sıfır risk
    sonsuz R üretir — ölçüme sokulmaz."""
    df = _ohlc([100, 101, 102])
    assert barrier_outcome(df, df.index[0], stop=105.0, target=110.0, **BEDAVA) is None


def test_ileri_bar_yoksa_none() -> None:
    df = _ohlc([100, 101])
    assert barrier_outcome(df, df.index[1], stop=98.0, target=110.0, **BEDAVA) is None


def test_max_bars_seri_sonunu_asamaz() -> None:
    df = _ohlc([100, 101, 102])
    s = barrier_outcome(df, df.index[0], stop=90.0, target=120.0, max_bars=999, **BEDAVA)
    assert s is not None
    assert s.exit_t == df.index[-1]


# --------------------------------------------------- evren geneli ölçüm


def _rastgele_ohlc(n=400, tohum=1, egim=0.0) -> pd.DataFrame:
    r = np.random.default_rng(tohum)
    k = 100 + np.cumsum(r.normal(egim, 1.0, n))
    gurultu = np.abs(r.normal(0, 0.4, n))
    return _ohlc(list(k), yuksek=list(k + gurultu), dusuk=list(k - gurultu))


def test_gercek_asimetrik_kenari_bulur() -> None:
    """Sinyaller bilerek yükselişin hemen öncesine konursa hedef oranı
    yükselir ve ölçüm bunu adil baza karşı görmeli."""
    ohlc, islemler = {}, {}
    for i in range(20):
        df = _rastgele_ohlc(tohum=i)
        ohlc[f"S{i}"] = df
        k = df["close"].to_numpy()
        # Sinyaller OOS penceresine konur; measure_r yalnız orayı sayar.
        oos = int(len(df) * 0.7)
        ileri = k[oos + 30 :] / k[oos:-30] - 1.0
        en_iyi = np.argsort(ileri)[-5:] + oos
        kayit = []
        for b in en_iyi:
            t = df.index[int(b)]
            giris = float(k[int(b)])
            kayit.append((_sinyal(t), giris * 0.98, giris * 1.04))
        islemler[f"S{i}"] = kayit

    s = measure_r(ohlc, islemler, max_bars=30, permutations=TUR, seed=7, **BEDAVA)
    assert s.n_symbols == 20
    assert s.mean_r > s.baseline_mean_r
    assert s.p_value < 0.05, s
    assert s.verdict == "kenar-var"


def test_kenar_yokken_kenar_uydurmaz() -> None:
    r = np.random.default_rng(42)
    ohlc, islemler = {}, {}
    for i in range(20):
        df = _rastgele_ohlc(tohum=100 + i)
        ohlc[f"S{i}"] = df
        kayit = []
        for b in r.integers(285, 360, size=5):
            t = df.index[int(b)]
            giris = float(df["close"].iloc[int(b)])
            kayit.append((_sinyal(t), giris * 0.98, giris * 1.04))
        islemler[f"S{i}"] = kayit

    s = measure_r(ohlc, islemler, max_bars=30, permutations=TUR, seed=7, **BEDAVA)
    assert s.p_value > 0.05, s
    assert s.verdict == "kanitlanmadi"


def test_cikis_oranlari_toplami_bire_esittir() -> None:
    """Her işlem üç bariyerden BİRİNDEN çıkar; kaçak işlem olmamalı."""
    df = _rastgele_ohlc(tohum=3)
    kayit = []
    for b in (300, 320, 340):
        giris = float(df["close"].iloc[b])
        kayit.append((_sinyal(df.index[b]), giris * 0.98, giris * 1.04))
    s = measure_r({"S": df}, {"S": kayit}, max_bars=20, permutations=20, seed=1, **BEDAVA)
    assert s.target_rate + s.stop_rate + s.time_rate == 1.0
    assert s.n_trades == 3


def test_is_penceresindeki_islemler_sayilmaz() -> None:
    """İddia GÖRÜLMEMİŞ dönemde ölçülür. İleri getiri ölçümü zaten böyle
    çalışıyordu; R'nin tüm seriyi sayması, katman tablosunda iki sütunun
    farklı pencerelerden konuşması demekti."""
    df = _rastgele_ohlc(tohum=9)
    giris = float(df["close"].iloc[50])  # IS penceresi
    kayit = [(_sinyal(df.index[50]), giris * 0.98, giris * 1.04)]
    s = measure_r({"S": df}, {"S": kayit}, max_bars=20, permutations=20, seed=1, **BEDAVA)
    assert s.n_trades == 0
    assert s.verdict == "olculmedi"


def test_toplu_r_tek_tek_hesapla_ayni_sonucu_verir() -> None:
    """Hız için yazılan vektörel yol ile referans yol AYNI sayıyı vermeli.

    Boş dağılım vektörel yoldan, gerçek sinyaller referans yoldan geçiyor.
    İkisi sessizce ayrışırsa sinyal ile bazı FARKLI kurallarla ölçmüş
    oluruz ve p değeri anlamını kaybeder — hem de hiçbir test kırılmadan.
    """
    df = _rastgele_ohlc(n=600, tohum=17)
    yuksek = df["high"].to_numpy(float)
    dusuk = df["low"].to_numpy(float)
    kapanis = df["close"].to_numpy(float)
    girisler = np.arange(100, 400, 7)

    for risk_o, hedef_o, yon in ((0.02, 0.04, 1.0), (0.03, 0.09, 1.0), (0.02, 0.05, -1.0)):
        toplu = _toplu_r(yuksek, dusuk, kapanis, girisler, risk_o, hedef_o, yon, 30, 0.0, 0.0)
        tek_tek = []
        for i in girisler:
            giris = float(kapanis[i])
            s = barrier_outcome(
                df, df.index[int(i)],
                stop=giris - risk_o * giris * yon,
                target=giris + hedef_o * giris * yon,
                direction="long" if yon > 0 else "short", max_bars=30, **BEDAVA,
            )
            if s is not None:
                tek_tek.append(s.r_multiple)
        assert toplu == pytest.approx(np.array(tek_tek))


def test_giris_seviyesi_kapanisin_yerine_gecer() -> None:
    """**Ölçülmüş hatanın regresyonu.**

    Golden Zone limit emirle çalışır: giriş 0.62 seviyesidir, sinyal zaten
    fiyat oraya DOKUNDUĞU için üretilir. Kapanışı giriş saymak riski
    (giriş − stop) barın nerede kapandığına bağlı kılıyordu; kapanış
    stop'un dibindeyse risk sıfıra iniyor ve R patlıyordu — rastgele baz
    +12R gibi imkânsız değerler veriyordu."""
    df = _ohlc([100, 96, 104, 110], yuksek=[100, 100, 105, 112], dusuk=[100, 95.5, 96, 103])
    # Kapanış 96, stop 95 → kapanıştan risk 1 birim; bölgeden (98) risk 3 birim.
    kapanistan = barrier_outcome(df, df.index[1], stop=95.0, target=104.0, **BEDAVA)
    bolgeden = barrier_outcome(df, df.index[1], stop=95.0, target=104.0, entry=98.0, **BEDAVA)
    assert kapanistan is not None and bolgeden is not None
    assert kapanistan.r_multiple == pytest.approx(8.0)   # (104-96)/1
    assert bolgeden.r_multiple == pytest.approx(2.0)     # (104-98)/3


def test_sifir_riskli_giris_olculmez() -> None:
    """Giriş stop'un üstündeyse risk sıfırdır; sonsuz R üretmek yerine
    işlem hiç sayılmaz."""
    df = _ohlc([100, 101, 102])
    assert barrier_outcome(df, df.index[0], stop=100.0, target=110.0, **BEDAVA) is None


def test_toplu_r_ayni_barda_stopu_secer() -> None:
    """Vektörel yol da iyimserliğe karşı aynı kararı vermeli."""
    df = _ohlc([100, 100], yuksek=[100, 120], dusuk=[100, 90])
    r = _toplu_r(
        df["high"].to_numpy(float), df["low"].to_numpy(float), df["close"].to_numpy(float),
        np.array([0]), 0.05, 0.10, 1.0, 5, 0.0, 0.0,
    )
    assert r == pytest.approx(np.array([-1.0]))


def test_is_penceresi_aramak_icin_acilabilir() -> None:
    """Koşul taraması IS'te ARAR, OOS'ta doğrular. Arama penceresi açıkça
    istenmedikçe kapalıdır: varsayılan `oos`."""
    df = _rastgele_ohlc(tohum=9)
    giris = float(df["close"].iloc[50])
    kayit = [(_sinyal(df.index[50]), giris * 0.98, giris * 1.04)]
    varsayilan = measure_r({"S": df}, {"S": kayit}, max_bars=20, permutations=20, seed=1, **BEDAVA)
    arama = measure_r(
        {"S": df}, {"S": kayit}, max_bars=20, permutations=20, seed=1, pencere="is", **BEDAVA
    )
    assert varsayilan.n_trades == 0
    assert arama.n_trades == 1


def test_islemsiz_evren_olculmedi_doner() -> None:
    s = measure_r({}, {}, permutations=10)
    assert s.n_trades == 0
    assert s.verdict == "olculmedi"


# --------------------------------------------------------- işlem maliyeti


def test_maliyet_r_den_dusulur() -> None:
    """**Ölçümün ikinci kör noktası.** Maliyetsiz ölçüm her kenarı olduğundan
    büyük gösterir ve bu soyut değil: koşul taraması +0.069R'lik bir etki
    buldu, aynı dönemde %0.3 gidiş-dönüş maliyet 0.068R ediyordu — yani
    maliyet, bulunan kenarın TAMAMI kadardı."""
    df = _ohlc([100, 101, 102, 103, 104, 105])
    bedava = barrier_outcome(df, df.index[0], stop=98.0, target=104.0, **BEDAVA)
    maliyetli = barrier_outcome(
        df, df.index[0], stop=98.0, target=104.0, komisyon=0.001, kayma=0.001
    )
    assert bedava is not None and maliyetli is not None
    assert bedava.r_multiple == 2.0
    # giriş 100×0.001 + çıkış 104×0.002 = 0.308 fiyat birimi, risk 2 → 0.154R
    assert maliyetli.r_multiple == pytest.approx(2.0 - 0.154)


def test_stop_maliyetle_bir_R_den_kotudur() -> None:
    """Stop olan işlem tam −1R kaybetmez: komisyonu da öder."""
    df = _ohlc([100, 99, 98, 97])
    s = barrier_outcome(df, df.index[0], stop=98.0, target=110.0, komisyon=0.001, kayma=0.0)
    assert s is not None
    assert s.r_multiple < -1.0


def test_maliyet_baza_da_uygulanir() -> None:
    """Maliyeti yalnız gerçek işlemlere uygulayıp baz havuzuna uygulamamak,
    ölçümü stratejinin ALEYHİNE saptırırdı. Vektörel yol ile referans yol
    aynı maliyetle aynı sayıyı vermeli."""
    df = _rastgele_ohlc(n=600, tohum=17)
    yuksek = df["high"].to_numpy(float)
    dusuk = df["low"].to_numpy(float)
    kapanis = df["close"].to_numpy(float)
    girisler = np.arange(100, 400, 11)

    toplu = _toplu_r(yuksek, dusuk, kapanis, girisler, 0.03, 0.06, 1.0, 30, 0.001, 0.001)
    tek_tek = []
    for i in girisler:
        giris = float(kapanis[i])
        s = barrier_outcome(
            df, df.index[int(i)], stop=giris * 0.97, target=giris * 1.06,
            max_bars=30, komisyon=0.001, kayma=0.001,
        )
        if s is not None:
            tek_tek.append(s.r_multiple)
    assert toplu == pytest.approx(np.array(tek_tek))
