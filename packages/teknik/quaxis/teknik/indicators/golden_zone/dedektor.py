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

# Bağlam göstergeleri ORTAK modüle taşındı: harmonik dedektörler de aynı
# değerleri yazıyor ve ikinci bir kopyanın sessizce ayrışması ölçümü bozar.
from quaxis.teknik.indicators.ortak.gostergeler import (
    adx,
    atr,
    bollinger_genislik,
    ema,
    macd_histogram,
    obv_egim,
    rsi,
    stokastik,
)
from quaxis.teknik.indicators.ortak.gostergeler import guvenli as _guvenli

META = IndicatorMeta(
    name="golden_zone",
    version="0.1.0",
    category="yapi",
    description="Yapı kırılımı sonrası 0.62-0.79 düzeltme bölgesine dönüş (ICT OTE)",
    # W1 eklendi (Faz 7.1): kuralın kendisi zaman diliminden bağımsız ve
    # bar-cinsi parametreler `for_timeframe` ile ölçekleniyor. Eklenmeden
    # önce haftalık taramada motor HİÇ iş açmıyordu — doğru davranış, ama
    # "haftalıkta kaç sinyal" sorusu da cevapsız kalıyordu.
    supported_timeframes=(Timeframe.H4, Timeframe.D1, Timeframe.W1),
)


@dataclass(frozen=True)
class _Baglam:
    """Sinyal barında ölçülen bağlam değerleri.

    **Hiçbiri sinyali FİLTRELEMEZ.** Hepsi payload'a yazılır ve hangi
    koşulun kenar EKLEDİĞİ `tools/kosul_taramasi.py` ile ölçülür. Koşulu
    dedektöre gömmek, "hangi gösterge işe yarıyor" sorusunu ölçülemez hâle
    getirirdi — bu stratejinin bütün mesele'si o soru.

    Hepsi t barına kadarki veriden hesaplanır; ileriye bakış yok.
    """

    ema20: np.ndarray
    ema50: np.ndarray
    ema200: np.ndarray
    rsi14: np.ndarray
    atr50: np.ndarray
    hacim_ort: np.ndarray
    adx14: np.ndarray
    macd_hist: np.ndarray
    bb_genislik: np.ndarray
    bb_yuzdelik: np.ndarray
    stok14: np.ndarray
    obv_egim20: np.ndarray
    ciro_ort: np.ndarray


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
        bb = bollinger_genislik(kapanis, 20)
        bag = _Baglam(
            ema20=ema(kapanis, 20),
            ema50=ema(kapanis, 50),
            ema200=ema(kapanis, 200),
            rsi14=rsi(kapanis, 14),
            atr50=atr(df, 50),
            hacim_ort=pd.Series(df["volume"].to_numpy(float))
            .rolling(20, min_periods=20).mean().to_numpy(),
            adx14=adx(df, 14),
            macd_hist=macd_histogram(kapanis),
            bb_genislik=bb,
            # Bugünkü sıkışma son 120 bara göre nerede? Mutlak genişlik
            # semboller arasında kıyaslanamaz, yüzdelik kıyaslanabilir.
            bb_yuzdelik=pd.Series(bb).rolling(120, min_periods=120)
            .rank(pct=True).to_numpy(),
            stok14=stokastik(df, 14),
            obv_egim20=obv_egim(df, 20),
            ciro_ort=pd.Series(kapanis * df["volume"].to_numpy(float))
            .rolling(20, min_periods=20).mean().to_numpy(),
        )
        tepeler = _pivotlar(yuksek, p.pivot_sol, p.pivot_sag, tepe=True)
        dipler = _pivotlar(dusuk, p.pivot_sol, p.pivot_sag, tepe=False)

        canli: list[_Kurulum] = []
        for t in range(n):
            if np.isnan(a[t]):
                continue
            canli = [k for k in canli if self._yasiyor(k, t, kapanis)]
            self._capa0_guncelle(canli, t, yuksek, dusuk)

            for kur in list(canli):
                # **D2 — hacimsiz barda sinyal DOĞMAZ** (ön kayıt:
                # `docs/olcum/onkayit-veri-duzeltme.md`). Hacimsiz barda
                # dört fiyat da aynı sayıdır ve bölgeye "girmiş"
                # sayılabilir; ama o fiyattan kimse işlem yapmadı.
                if float(df["volume"].iloc[t]) <= 0:
                    continue
                sinyal = self._bolgeye_girdi_mi(kur, t, df, a)
                if sinyal is not None:
                    self._kaydet(sonuc, kur, sinyal, t, df, a, bag)
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

    def _baglam(
        self, kur: _Kurulum, t: int, df: pd.DataFrame, a: np.ndarray, bag: _Baglam
    ) -> dict[str, Any]:
        """Sinyal barında ölçülen bağlam. FİLTRE DEĞİL — ölçüm girdisi.

        Her biri bir hipotez taşır ve hipotez adıyla birlikte yazılıdır:

        * `ema50_uyum` / `ema200_uyum` — "trendle işlem yap". ICT'nin öznel
          "daily bias"ının ölçülebilir karşılığı.
        * `ema_egim_uyum` — seviye değil EĞİM: fiyat ortalamanın üstünde
          olabilir ama ortalama düşüyor olabilir.
        * `rsi14` — düzeltmenin tükenip tükenmediği.
        * `hacim_orani` — yer değiştirme hacimle mi geldi? SMC'nin iddiası bu.
        * `atr_rejim` — kısa vadeli oynaklık uzun vadeliye göre nerede.
        * `bacak_atr` — bacağın ATR cinsinden boyu (eşik değil, DEĞER).
        * `donus_bar` — kırılımdan bölgeye kaç barda dönüldü. Hızlı dönüş
          güçlü sayılır; ölçelim.
        * `derinlik` — bölgeye ne kadar derin girildi (0.62…1.0).
        """
        yon = 1.0 if kur.boga else -1.0
        k = float(df["close"].iloc[t])
        boy = abs(kur.capa0 - kur.capa100)
        atr_t = float(a[t])

        e50, e200 = bag.ema50[t], bag.ema200[t]
        e50_onceki = bag.ema50[t - 5] if t >= 5 else np.nan
        hacim = float(df["volume"].iloc[kur.bos_i])
        hacim_ort = bag.hacim_ort[kur.bos_i]

        # Fiyatın bölgeye ne kadar derin girdiği: barın uç noktası esas.
        uc = float(df["low"].iloc[t]) if kur.boga else float(df["high"].iloc[t])
        derinlik = abs(kur.capa0 - uc) / boy if boy > 0 else None

        def uyum(deger: float) -> bool | None:
            if np.isnan(deger):
                return None
            return bool((k - deger) * yon > 0)

        return {
            "ema50_uyum": uyum(e50),
            "ema200_uyum": uyum(e200),
            "ema_egim_uyum": (
                None if np.isnan(e50) or np.isnan(e50_onceki)
                else bool((e50 - e50_onceki) * yon > 0)
            ),
            "rsi14": _guvenli(bag.rsi14[t]),
            "hacim_orani": (
                None if hacim_ort is None or np.isnan(hacim_ort) or hacim_ort <= 0
                else float(hacim / hacim_ort)
            ),
            "atr_rejim": (
                None if np.isnan(bag.atr50[t]) or bag.atr50[t] <= 0
                else float(atr_t / bag.atr50[t])
            ),
            "bacak_atr": None if atr_t <= 0 else float(boy / atr_t),
            "donus_bar": int(t - kur.bos_i),
            "derinlik": None if derinlik is None else float(derinlik),
            # --- ikinci tur: trend gücü, momentum, sıkışma, hacim teyidi ---
            "adx14": _guvenli(bag.adx14[t]),
            "macd_uyum": (
                None if np.isnan(bag.macd_hist[t])
                else bool(bag.macd_hist[t] * yon > 0)
            ),
            "bb_yuzdelik": _guvenli(bag.bb_yuzdelik[t]),
            "stok14": _guvenli(bag.stok14[t]),
            "obv_uyum": (
                None if np.isnan(bag.obv_egim20[t])
                else bool(bag.obv_egim20[t] * yon > 0)
            ),
            "ema20_50_uyum": (
                None if np.isnan(bag.ema20[t]) or np.isnan(bag.ema50[t])
                else bool((bag.ema20[t] - bag.ema50[t]) * yon > 0)
            ),
            # Fiyat ortalamadan ne kadar uzakta — aşırı uzaklaşmış mı?
            "ema50_uzaklik_atr": (
                None if np.isnan(e50) or atr_t <= 0 else float((k - e50) * yon / atr_t)
            ),
            # Sinyal barının karakteri: gövde/aralık oranı ve aralık/ATR.
            "govde_orani": (
                None if (float(df["high"].iloc[t]) - float(df["low"].iloc[t])) <= 0
                else float(
                    abs(k - float(df["open"].iloc[t]))
                    / (float(df["high"].iloc[t]) - float(df["low"].iloc[t]))
                )
            ),
            "aralik_atr": (
                None if atr_t <= 0
                else float((float(df["high"].iloc[t]) - float(df["low"].iloc[t])) / atr_t)
            ),
            # Likidite: ortalama ciro. Gösterge değil ama gerçek bir filtre —
            # ince sembolde ölçülen kenar uygulanamaz.
            "ciro": _guvenli(bag.ciro_ort[t]),
        }

    def _kaydet(
        self, sonuc: IndicatorResult, kur: _Kurulum, giris: float,
        t: int, df: pd.DataFrame, a: np.ndarray, bag: _Baglam,
    ) -> None:
        p = self.params
        boy = abs(kur.capa0 - kur.capa100)
        isaret = 1.0 if kur.boga else -1.0
        derin = kur.capa0 - boy * p.bolge_derin * isaret
        orta = kur.capa0 - boy * p.orta_esik * isaret
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
                    "orta_esik": float(orta),
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
                    **self._baglam(kur, t, df, a, bag),
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
            Level(price=float(orta), label=f"{p.orta_esik:.3f}", style="fib_orta",
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
