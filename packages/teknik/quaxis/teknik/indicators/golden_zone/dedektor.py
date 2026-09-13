"""Golden Zone (ICT OTE) dedektörü — K2.

Kural `docs/strateji/kaynak/golden-zone-K0.md`'de, sayfa/bağlantı
numaralarıyla. Buradaki kod o kuralın birebir karşılığıdır.

    1. yapı kırılımı (BOS)   — kapanış, onaylı bir salınım tepesini aşar
    2. yer değiştirme bacağı — çıpalar: %100 = bacağın dibi, %0 = zirvesi
    3. bölgeye dönüş         — 0.62–0.79 → SİNYAL

**Süpürme, FVG ve Order Block sinyali FİLTRELEMEZ; payload'a bayrak olarak
yazılır.** Sebebi tasarımsal: kullanıcı kararı "katmanlı ölçüm". Katmanlar
dedektörün içinde sabitlenirse hangi katmanın kenar *eklediği* ölçülemez —
sadece hepsi birlikte ölçülebilir. López de Prado'nun meta-etiketleme
reçetesi (s.51-53) tam tersini söyler: önce yüksek recall'lı birincil model,
sonra precision'ı düzelten ikincil katman. Filtre K4'te, veride uygulanır.

## Non-repaint gerekçesi

Üç çıpanın üçü de sinyal barından önce kesinleşir:

* Salınım pivotları `pivot_sag` bar sonra ONAYLANIR; onaylanmadan kullanılmaz.
* %100 çıpası = kırılıma kadar olan bacağın en düşük dibi — geçmiş, kapanmış.
* %0 çıpası = kırılımdan sinyale kadarki en yüksek tepe. Yalnızca BÜYÜR ve
  yalnızca `[bos, t]` barlarından hesaplanır; bar t'de yeniden hesaplandığında
  aynı değeri verir.

Bu yüzden `bar_time` (bacağın zirvesinin barı) ile `detected_at` (bölgeye
girilen bar) FARKLIDIR ve fark kaydedilir. Bacağın "en iyi" ucunu sonradan
seçmek — ileriye bakıp daha yüksek bir tepe bulunca çıpayı kaydırmak —
repaint'in ta kendisidir.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

import numpy as np
import pandas as pd
from quaxis.teknik.core.indicator import BaseIndicator
from quaxis.teknik.core.params import params_hash
from quaxis.teknik.core.types import (
    Box,
    IndicatorMeta,
    IndicatorResult,
    Level,
    Marker,
    Signal,
    Timeframe,
)
from quaxis.teknik.indicators.golden_zone.parametreler import GoldenZoneParams

META = IndicatorMeta(
    name="golden_zone",
    version="0.1.0",
    category="yapi",
    description="Yapı kırılımı sonrası 0.62-0.79 düzeltme bölgesine dönüş (ICT OTE)",
    supported_timeframes=(Timeframe.H4, Timeframe.D1),
)


def atr(df: pd.DataFrame, periyot: int) -> np.ndarray:
    """Wilder ATR. İlk `periyot` bar NaN kalır — ısınma dolmadan eşik
    uygulanmaz; ısınmayı sıfır saymak stratejiyi kayırır."""
    y, d, k = (df["high"].to_numpy(float), df["low"].to_numpy(float),
               df["close"].to_numpy(float))
    onceki = np.concatenate(([np.nan], k[:-1]))
    tr = np.maximum(y - d, np.maximum(np.abs(y - onceki), np.abs(d - onceki)))
    wilder = pd.Series(tr).ewm(alpha=1.0 / periyot, adjust=False, min_periods=periyot)
    return wilder.mean().to_numpy()


@dataclass(frozen=True)
class _Pivot:
    i: int
    fiyat: float
    onay_i: int
    """Pivotun BİLİNEBİLİR olduğu bar. Bundan önce kullanmak repaint'tir."""


def _pivotlar(seri: np.ndarray, sol: int, sag: int, *, tepe: bool) -> list[_Pivot]:
    """Onaylı salınım uçları. Bir uç, sağındaki `sag` bar kapanmadan bilinemez."""
    out: list[_Pivot] = []
    n = len(seri)
    for i in range(sol, n - sag):
        pencere = seri[i - sol : i + sag + 1]
        uc = seri[i]
        if (tepe and uc == pencere.max()) or (not tepe and uc == pencere.min()):
            out.append(_Pivot(i, float(uc), i + sag))
    return out


def _son_onayli(pivotlar: list[_Pivot], t: int, once: int | None = None) -> _Pivot | None:
    """`t` barında bilinen, (verilirse) `once` barından önceki son pivot."""
    for p in reversed(pivotlar):
        if p.onay_i <= t and (once is None or p.i < once):
            return p
    return None


def _fvg_var(df: pd.DataFrame, bas: int, son: int, esik: float, *, boga: bool) -> bool:
    """Üç mumluk adil değer boşluğu: ortadaki mum, iki komşusunun arasında
    dokunulmamış bir aralık bırakır."""
    y, d = df["high"].to_numpy(float), df["low"].to_numpy(float)
    for i in range(bas + 2, son + 1):
        bosluk = d[i] - y[i - 2] if boga else d[i - 2] - y[i]
        if bosluk > esik:
            return True
    return False


def _order_block(df: pd.DataFrame, bos_i: int, bacak_bas: int, *, boga: bool) -> float | None:
    """Yer değiştirmeden ÖNCEKİ son ters yönlü mumun gövdesi.

    Boğa kurulumunda: yükselişi başlatan son düşüş mumu. Fiyat oraya dönerse
    "kurumsal emir bloğuna dönüş" denir. Burada yalnızca seviyesi döner;
    teyit sayılıp sayılmayacağına K4 karar verecek.
    """
    a, k = df["open"].to_numpy(float), df["close"].to_numpy(float)
    d, y = df["low"].to_numpy(float), df["high"].to_numpy(float)
    for i in range(bos_i, max(bacak_bas - 1, 0), -1):
        if boga and k[i] < a[i]:
            return float(d[i])
        if not boga and k[i] > a[i]:
            return float(y[i])
    return None


@dataclass
class _Kurulum:
    """Kırılım olmuş, bölgeye dönüş bekleyen canlı kurulum."""

    boga: bool
    bos_i: int
    bacak_bas_i: int
    capa100: float
    capa0: float
    capa0_i: int
    supurme: bool
    #: Kırılan salınım seviyesi. Grafikte "BOS" çizgisi BUNU gösterir;
    #: kırılım barının kapanışını göstermek yanlış sayı yazmak olurdu.
    kirilan: float
    #: Süpürmenin gerçekleştiği bar ve wick ucu. Süpürme yoksa None —
    #: %100 çıpasıyla aynı noktaya ikinci bir işaret koymak, grafikte
    #: okunmaz bir yığın üretiyordu.
    supurme_i: int | None
    supurme_fiyat: float | None


class GoldenZone(BaseIndicator):
    """ICT OTE dedektörü."""

    meta: ClassVar[IndicatorMeta] = META

    def __init__(self, params: GoldenZoneParams | None = None) -> None:
        self.params = params or GoldenZoneParams()

    def compute(
        self, df: pd.DataFrame, context: dict[str, Any] | None = None
    ) -> IndicatorResult:
        p = self.params
        sonuc = IndicatorResult(
            indicator=META.name, version=META.version, params_hash=params_hash(p),
            symbol=str(df.attrs.get("symbol", "")),
            timeframe=Timeframe(df.attrs.get("timeframe", Timeframe.D1)),
        )
        n = len(df)
        if n < p.atr_periyot + p.pivot_sol + p.pivot_sag + 5:
            return sonuc

        yuksek, dusuk = df["high"].to_numpy(float), df["low"].to_numpy(float)
        kapanis = df["close"].to_numpy(float)
        a = atr(df, p.atr_periyot)
        tepeler = _pivotlar(yuksek, p.pivot_sol, p.pivot_sag, tepe=True)
        dipler = _pivotlar(dusuk, p.pivot_sol, p.pivot_sag, tepe=False)

        canli: list[_Kurulum] = []
        for t in range(n):
            if np.isnan(a[t]):
                continue
            canli = [k for k in canli if self._yasiyor(k, t, kapanis)]
            self._capa0_guncelle(canli, t, yuksek, dusuk)

            for kur in list(canli):
                sinyal = self._bolgeye_girdi_mi(kur, t, df, a)
                if sinyal is not None:
                    self._kaydet(sonuc, kur, sinyal, t, df, a)
                    canli.remove(kur)

            yeni = self._kirilim_var_mi(t, tepeler, dipler, yuksek, dusuk, kapanis, a)
            if yeni is not None and not any(k.boga == yeni.boga for k in canli):
                canli.append(yeni)

        return sonuc

    # ------------------------------------------------------------------

    def _yasiyor(self, k: _Kurulum, t: int, kapanis: np.ndarray) -> bool:
        """Geçersizlik: %100 çıpasının ötesinde GÖVDE kapanışı.

        Wick geçebilir, gövde geçemez — ICT'nin kuralı bu ve gevşetilmesi
        sinyal sayısını sessizce yarıya indirir. Ayrıca zaman aşımı.
        """
        if t - k.bos_i > self.params.donus_max_bar:
            return False
        gecti = kapanis[t] < k.capa100 if k.boga else kapanis[t] > k.capa100
        return not gecti

    def _capa0_guncelle(self, canli: list[_Kurulum], t: int, y: np.ndarray, d: np.ndarray) -> None:
        """%0 çıpası yalnızca BÜYÜR ve yalnızca geçmiş barlardan hesaplanır."""
        for k in canli:
            if k.boga and y[t] > k.capa0:
                k.capa0, k.capa0_i = float(y[t]), t
            elif not k.boga and d[t] < k.capa0:
                k.capa0, k.capa0_i = float(d[t]), t

    def _kirilim_var_mi(
        self, t: int, tepeler: list[_Pivot], dipler: list[_Pivot],
        y: np.ndarray, d: np.ndarray, k: np.ndarray, a: np.ndarray,
    ) -> _Kurulum | None:
        """Kapanış onaylı bir salınım ucunu aşarsa yapı kırıldı demektir."""
        p = self.params
        for boga in (True, False):
            uc = _son_onayli(tepeler if boga else dipler, t)
            if uc is None or uc.i >= t:
                continue
            kirildi = k[t] > uc.fiyat if boga else k[t] < uc.fiyat
            # Kırılım TAZE olmalı: önceki bar da aşmışsa bu aynı kırılımın
            # devamıdır, yeni bir kurulum değil. Bu kontrol olmadan yükselen
            # her bar ayrı bir kurulum doğurur ve sinyaller çoğalır.
            onceki_de = t > 0 and (k[t - 1] > uc.fiyat if boga else k[t - 1] < uc.fiyat)
            if not kirildi or onceki_de:
                continue

            koken = _son_onayli(dipler if boga else tepeler, t, once=t)
            if koken is None or koken.i >= t:
                continue
            bacak = slice(koken.i, t + 1)
            capa100 = float(d[bacak].min()) if boga else float(y[bacak].max())
            capa0 = float(y[bacak].max()) if boga else float(d[bacak].min())
            boy = abs(capa0 - capa100)
            if boy < p.yer_degistirme_atr * a[t]:
                continue  # gürültü; yapı kırılımı değil

            uc_i = int(np.argmax(y[bacak])) if boga else int(np.argmin(d[bacak]))
            capa0_i = uc_i + koken.i
            onceki_uc = _son_onayli(dipler if boga else tepeler, t, once=koken.i)
            supurme = bool(
                onceki_uc is not None
                and (
                    (boga and d[koken.i] < onceki_uc.fiyat and k[koken.i] > onceki_uc.fiyat)
                    or (not boga and y[koken.i] > onceki_uc.fiyat and k[koken.i] < onceki_uc.fiyat)
                )
            )
            return _Kurulum(
                boga, t, koken.i, capa100, capa0, capa0_i, supurme,
                kirilan=uc.fiyat,
                supurme_i=koken.i if supurme else None,
                supurme_fiyat=float(d[koken.i] if boga else y[koken.i]) if supurme else None,
            )
        return None

    def _bolgeye_girdi_mi(
        self, kur: _Kurulum, t: int, df: pd.DataFrame, a: np.ndarray
    ) -> float | None:
        """Fiyat bölgenin sığ ucuna DOKUNDUYSA giriş seviyesini döner."""
        if t <= kur.bos_i:
            return None
        p = self.params
        boy = kur.capa0 - kur.capa100 if kur.boga else kur.capa100 - kur.capa0
        if boy <= 0:
            return None
        sig = kur.capa0 - boy * p.bolge_sig if kur.boga else kur.capa0 + boy * p.bolge_sig
        d, y = float(df["low"].iloc[t]), float(df["high"].iloc[t])
        if kur.boga and d <= sig:
            return sig
        if not kur.boga and y >= sig:
            return sig
        return None

    def _kaydet(
        self, sonuc: IndicatorResult, kur: _Kurulum, giris: float,
        t: int, df: pd.DataFrame, a: np.ndarray,
    ) -> None:
        p = self.params
        boy = abs(kur.capa0 - kur.capa100)
        isaret = 1.0 if kur.boga else -1.0
        derin = kur.capa0 - boy * p.bolge_derin * isaret
        tatli = kur.capa0 - boy * p.tatli_nokta * isaret
        stop = kur.capa100 - boy * p.stop_tamponu * isaret
        if p.hedef_modu == "yapisal":
            hedef = kur.capa0
        else:
            # Hedef girişten `hedef_r_kati` × risk kadar ötede. Yapısal modda
            # hedef mesafesi giriş derinliğiyle değişir (0.62'de 1.63R,
            # 0.79'da 3.76R); bu mod hepsini aynı risk profiline sabitler.
            risk = abs(giris - stop)
            hedef = giris + risk * p.hedef_r_kati * isaret

        bar_t = df.index[kur.capa0_i]
        tespit_t = df.index[t]
        yon = "long" if kur.boga else "short"

        sonuc.signals.append(
            Signal(
                bar_time=bar_t,
                detected_at=tespit_t,
                direction=yon,
                state="confirmed",
                score=1.0,
                payload={
                    "event": "golden_zone_bolgede",
                    # K4'ün üç bariyerli R ölçümü bu ikisini okur.
                    "stop": float(stop),
                    "hedef": float(hedef),
                    "giris": float(giris),
                    "hedef_modu": p.hedef_modu,
                    "capa100": float(kur.capa100),
                    "capa0": float(kur.capa0),
                    "bolge_sig": float(giris),
                    "bolge_derin": float(derin),
                    "tatli_nokta": float(tatli),
                    "zaman_bariyeri": int(p.zaman_bariyeri),
                    "bos_bar": df.index[kur.bos_i].isoformat(),
                    "kirilan_seviye": float(kur.kirilan),
                    # --- katman bayrakları: FİLTRE DEĞİL, ÖLÇÜM GİRDİSİ ---
                    "supurme": kur.supurme,
                    "supurme_bar": (
                        df.index[kur.supurme_i].isoformat() if kur.supurme_i is not None else None
                    ),
                    "supurme_fiyat": kur.supurme_fiyat,
                    "fvg": _fvg_var(
                        df, kur.bacak_bas_i, kur.bos_i, p.fvg_min_atr * float(a[t]), boga=kur.boga
                    ),
                    "order_block": _order_block(df, kur.bos_i, kur.bacak_bas_i, boga=kur.boga),
                },
            )
        )
        # Kutu SİNYAL barında doğar, bacağın zirvesinde değil. t0'ı geriye
        # atmak görsel repaint'tir: geçmişi kaydıran biri, bölgeyi daha
        # bilinemezken çizilmiş görür. t1 ileri uzar (extend-only, serbest).
        sonuc.boxes.append(
            Box(
                t0=tespit_t, t1=df.index[min(t + p.zaman_bariyeri, len(df) - 1)],
                low=min(giris, derin), high=max(giris, derin),
                label=f"OTE {p.bolge_sig:.3f}-{p.bolge_derin:.3f}", style="zone",
            )
        )
        # Seviyeler kurulumun PENCERESİNE aittir, tüm geçmişe değil:
        # `start` boş bırakılırsa walk-forward karşılaştırması onları
        # "hep vardı" sayar ve sonradan doğan her seviye repaint görünür.
        sonuc.levels += [
            Level(price=float(tatli), label=f"{p.tatli_nokta:.3f}", style="fib_sweet",
                  start=tespit_t),
            Level(price=float(stop), label="stop", style="stop", start=tespit_t),
            Level(price=float(hedef), label="hedef", style="target", start=tespit_t),
        ]
        sonuc.markers.append(
            Marker(t=tespit_t, price=float(giris), text="OTE", kind="signal")
        )


#: `hedef_modu="r_kati"` varyantının katalog adı. Aynı dedektör, farklı
#: hedef — iki AYRI soru sorulduğu için iki ayrı künye.
R_KATI_AD = "golden_zone_r2"

META_R_KATI = IndicatorMeta(
    name=R_KATI_AD,
    version=META.version,
    category=META.category,
    description="OTE bölgesi, hedef sabit 2R (derinlikten arındırılmış ölçüm)",
    supported_timeframes=META.supported_timeframes,
)


def olustur(params: GoldenZoneParams | None = None) -> GoldenZone:
    """Katalog adresi bu fabrikayı gösterir (bkz. core/catalog.py)."""
    return GoldenZone(params)


def olustur_r_kati() -> GoldenZone:
    """Hedefi sabit R katına koyan varyant.

    Yapısal modda hedef mesafesi giriş derinliğiyle değişir (0.62'de 1.63R,
    0.79'da 3.76R). Bu varyant hepsini aynı risk profiline sabitler ve
    "bölgenin kendisi öngörü taşıyor mu" sorusunu derinlikten arındırır.
    """
    d = GoldenZone(GoldenZoneParams(hedef_modu="r_kati"))
    d.meta = META_R_KATI
    return d
