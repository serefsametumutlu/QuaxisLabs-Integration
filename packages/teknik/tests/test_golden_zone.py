"""Golden Zone (ICT OTE) — K1/K2 testleri.

En önemlisi `test_repaint_yok`: dedektör geçmişi yeniden yazıyorsa
ürettiği her sayı süstür. Diğerleri kuralın kendisini sabitler — bir gün
biri "wick de geçersiz kılsın" derse hangi testin kırılacağı belli olsun.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quaxis.teknik.core.types import Timeframe
from quaxis.teknik.indicators.golden_zone import GoldenZone, GoldenZoneParams
from quaxis.teknik.testing.repaint import repaint_test


def _df(o, y, d, k, *, bas="2024-01-01") -> pd.DataFrame:
    """OHLCV şemasını zorlar: high >= max(o,c), low <= min(o,c)."""
    idx = pd.date_range(bas, periods=len(k), freq="1D", tz="UTC")
    o, y, d, k = (np.asarray(x, dtype=float) for x in (o, y, d, k))
    y = np.maximum(y, np.maximum(o, k))
    d = np.minimum(d, np.minimum(o, k))
    df = pd.DataFrame(
        {"open": o, "high": y, "low": d, "close": k, "volume": np.ones(len(k))},
        index=idx, dtype=float,
    )
    df.attrs["symbol"] = "TEST"
    df.attrs["timeframe"] = Timeframe.D1
    return df


def _kurulum_serisi() -> pd.DataFrame:
    """Elle kurulmuş bir boğa OTE senaryosu.

        · 0-29    ısınma (ATR dolsun)
        · 30-36   salınım dibi (köken)
        · 37-46   yer değiştirme: güçlü yükseliş, salınım tepesi aşılır
        · 47-58   0.62'den 0.79'a kadar düzeltme
    """
    k = [100.0] * 30
    k += [100, 99, 98, 97, 96, 95, 94]          # dip: 94
    k += [96, 99, 103, 108, 112, 117, 121, 126, 130, 134]  # yükseliş: 134
    k += [131, 128, 124, 120, 116, 112, 109, 106, 104, 103]  # 0.62 bölgesine düzeltme
    k += [101, 100]                                          # 0.79'a kadar derinleşir
    k = [float(x) for x in k]
    y = [x + 1.0 for x in k]
    d = [x - 1.0 for x in k]
    o = [k[0]] + k[:-1]
    return _df(o, y, d, k)


@pytest.fixture
def dedektor() -> GoldenZone:
    return GoldenZone(GoldenZoneParams(yer_degistirme_atr=1.0))


def _uzun(sonuc) -> object:
    """Senaryodaki boğa sinyali. Seri düşüşle başladığı için önce bir ayı
    kurulumu da doğar — dedektörün iki yönlü çalıştığının kanıtı."""
    uzunlar = [s for s in sonuc.signals if s.direction == "long"]
    assert uzunlar, "boğa sinyali bekleniyordu"
    return uzunlar[0]


# ----------------------------------------------------------- K2: repaint


def test_repaint_yok(dedektor: GoldenZone) -> None:
    """Walk-forward eşitlik. Geçmişe bir şey yazan dedektör hiçbir şey
    kanıtlayamaz — bu test kırılırsa strateji K2'yi geçemez."""
    r = np.random.default_rng(11)
    n = 260
    adim = r.normal(0, 1.2, n)
    kapanis = 100 + np.cumsum(adim)
    gurultu = np.abs(r.normal(0, 0.6, n))
    df = _df(
        list(np.concatenate(([kapanis[0]], kapanis[:-1]))),
        list(kapanis + gurultu), list(kapanis - gurultu), list(kapanis),
    )
    rapor = repaint_test(dedektor, df, tail=70, stride=2)
    assert rapor.passed, "\n".join(rapor.mismatches[:10])


def test_detected_at_bar_time_ile_ayni_degil(dedektor: GoldenZone) -> None:
    """Çıpa bacağın zirvesinde, sinyal bölgeye dönüşte. İkisi aynı bar
    olsaydı, kurulumun tanımı gereği imkânsız bir şey iddia ederdik."""
    s = _uzun(dedektor(_kurulum_serisi()))
    assert s.detected_at > s.bar_time


# ------------------------------------------------------- K1: kural kilidi


def test_bolgede_sinyal_uretilir(dedektor: GoldenZone) -> None:
    s = _uzun(dedektor(_kurulum_serisi()))
    assert s.payload["event"] == "golden_zone_bolgede"


def test_stop_ve_hedef_payloadda(dedektor: GoldenZone) -> None:
    """K4'ün üç bariyerli R ölçümü bu iki anahtarı okur. Yoksa asimetri
    ölçülemez ve strateji, kendi iddiasını göremeyen bir ölçüme girer."""
    s = _uzun(dedektor(_kurulum_serisi()))
    assert s.payload["stop"] < s.payload["giris"] < s.payload["hedef"]
    assert s.payload["stop"] == pytest.approx(s.payload["capa100"])


def test_yapisal_hedef_bacagin_ucudur() -> None:
    """Kaynağa birebir sadık mod: hedef = %0 çıpası."""
    d = GoldenZone(GoldenZoneParams(yer_degistirme_atr=1.0, hedef_modu="yapisal"))
    s = _uzun(d(_kurulum_serisi()))
    assert s.payload["hedef"] == pytest.approx(s.payload["capa0"])


def test_yapisal_hedefin_asimetrisi_lehte() -> None:
    """Kurulumun kendi aritmetiği: düzeltme TEPEDEN ölçüldüğü için 0.62
    girişte risk 0.38 bacak, ödül 0.62 bacak — 1.63:1.

    ICT'nin 0.705'e "sweet spot" demesinin sebebi bu: derine girildikçe
    stop küçülür, hedef uzaklaşır. Bu test o ilişkiyi kilitler; biri
    çıpaları ters çevirirse (risk ile ödülü yer değiştirirse) burada
    yakalanır."""
    d = GoldenZone(GoldenZoneParams(yer_degistirme_atr=1.0, hedef_modu="yapisal"))
    s = _uzun(d(_kurulum_serisi()))
    risk = s.payload["giris"] - s.payload["stop"]
    odul = s.payload["hedef"] - s.payload["giris"]
    assert odul / risk == pytest.approx(0.62 / 0.38, rel=1e-6)


def test_derin_giris_asimetriyi_iyilestirir() -> None:
    """0.79'dan girmek 3.76:1, 0.62'den girmek 1.63:1 verir."""
    for sig, beklenen in ((0.62, 0.62 / 0.38), (0.79, 0.79 / 0.21)):
        d = GoldenZone(
            GoldenZoneParams(
                yer_degistirme_atr=1.0, hedef_modu="yapisal",
                bolge_sig=sig, bolge_derin=max(sig + 0.01, 0.79), orta_esik=sig,
            )
        )
        s = _uzun(d(_kurulum_serisi()))
        risk = s.payload["giris"] - s.payload["stop"]
        odul = s.payload["hedef"] - s.payload["giris"]
        assert odul / risk == pytest.approx(beklenen, rel=1e-6)


def test_r_kati_hedefi_risk_katidir() -> None:
    d = GoldenZone(
        GoldenZoneParams(yer_degistirme_atr=1.0, hedef_modu="r_kati", hedef_r_kati=3.0)
    )
    s = _uzun(d(_kurulum_serisi()))
    risk = s.payload["giris"] - s.payload["stop"]
    assert s.payload["hedef"] == pytest.approx(s.payload["giris"] + 3.0 * risk)


def test_gecersiz_hedef_modu_reddedilir() -> None:
    with pytest.raises(ValueError, match="hedef_modu"):
        GoldenZoneParams(hedef_modu="ne_olsa")


def test_giris_bolgenin_sig_ucunda(dedektor: GoldenZone) -> None:
    """0.62 ilk temas seviyesidir; girişi 0.705'e kaydırmak sinyalin
    yarısını sessizce düşürür."""
    s = _uzun(dedektor(_kurulum_serisi()))
    boy = s.payload["capa0"] - s.payload["capa100"]
    beklenen = s.payload["capa0"] - boy * 0.62
    assert s.payload["giris"] == pytest.approx(beklenen)
    assert s.payload["bolge_derin"] < s.payload["orta_esik"] < s.payload["giris"]


def test_katman_bayraklari_filtre_degil(dedektor: GoldenZone) -> None:
    """Süpürme/FVG/OB sinyali ELEMEZ — payload'a yazılır.

    Katmanlar dedektörde sabitlenirse hangisinin kenar EKLEDİĞİ ölçülemez;
    kullanıcı kararı "katmanlı ölçüm" tam olarak bunu gerektiriyor."""
    s = _uzun(dedektor(_kurulum_serisi()))
    assert set(s.payload) >= {"supurme", "fvg", "order_block"}
    assert isinstance(s.payload["supurme"], bool)
    assert isinstance(s.payload["fvg"], bool)


def test_govde_kapanisi_gecersiz_kilar_wick_kilmaz() -> None:
    """ICT kuralı: %100 ötesinde GÖVDE kapanışı geçersizdir; wick geçebilir.

    Wick'i de geçersiz saymak sinyal sayısını sessizce yarıya indirir —
    bu yüzden ayrım kodda birebir duruyor ve testle kilitli."""
    d = GoldenZone(GoldenZoneParams(yer_degistirme_atr=1.0))
    temel = _kurulum_serisi()

    # Düzeltme sırasında bir bar çıpanın ALTINA sarkıyor ama üstünde kapanıyor.
    wick = temel.copy()
    wick.attrs = dict(temel.attrs)
    wick.iloc[50, wick.columns.get_loc("low")] = 90.0  # çıpa 93.0 civarı
    assert d(wick).signals, "sadece wick sarkması kurulumu öldürmemeli"

    # Aynı barda GÖVDE de altına kapanıyor: kurulum ölür.
    govde = temel.copy()
    govde.attrs = dict(temel.attrs)
    for kolon in ("low", "close", "open", "high"):
        govde.iloc[48, govde.columns.get_loc(kolon)] = 90.0
    govde.iloc[48, govde.columns.get_loc("high")] = 91.0
    assert not [s for s in d(govde).signals if s.direction == "long"]


def test_gurultu_yapi_kirilimi_sayilmaz() -> None:
    """Yer değiştirme eşiği yüksekse düz seride sinyal çıkmamalı."""
    r = np.random.default_rng(3)
    n = 200
    k = 100 + np.cumsum(r.normal(0, 0.2, n))
    df = _df(list(k), list(k + 0.1), list(k - 0.1), list(k))
    d = GoldenZone(GoldenZoneParams(yer_degistirme_atr=8.0))
    assert d(df).signals == []


def test_zaman_asimi_kurulumu_oldurur() -> None:
    """Kırılımdan sonra bölgeye dönüş gelmezse kurulum süresi dolar."""
    kisa = GoldenZone(GoldenZoneParams(yer_degistirme_atr=1.0, donus_max_bar=2))
    uzunlar = [s for s in kisa(_kurulum_serisi()).signals if s.direction == "long"]
    assert uzunlar == []


# ----------------------------------------------------------- parametreler


def test_bolge_sinirlari_dogrulanir() -> None:
    with pytest.raises(ValueError, match="sığ<derin"):
        GoldenZoneParams(bolge_sig=0.8, bolge_derin=0.6)


def test_orta_esik_bolgenin_disinda_olamaz() -> None:
    with pytest.raises(ValueError, match="ölçülemeyen bir sayı"):
        GoldenZoneParams(orta_esik=0.95)


def test_params_hash_deterministik() -> None:
    a = GoldenZone(GoldenZoneParams())
    b = GoldenZone(GoldenZoneParams())
    df = _kurulum_serisi()
    assert a(df).params_hash == b(df).params_hash
