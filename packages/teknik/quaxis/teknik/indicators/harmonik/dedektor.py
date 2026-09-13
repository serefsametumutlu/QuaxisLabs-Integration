"""Harmonik formasyon dedektörleri — K2.

Kural `docs/strateji/kaynak/harmonik-pesavento-K0.md`'de, kitabın bölüm
numaralarıyla. Buradaki kod o kuralın birebir karşılığıdır.

    almaşık pivot zinciri  →  oranlar tutuyor mu  →  D bir FİYAT SEVİYESİ
    olarak hesaplanır  →  fiyat D'ye dokunur  →  SİNYAL

## D bir pivot DEĞİLDİR

Harmonik dedektörlerin klasik repaint kaynağı budur: D'yi "sonradan oluşmuş
bir dip" olarak aramak. Öyle arandığında D ancak `pivot_sag` bar sonra
bilinir ve grafiğe geriye dönük çizilir — gerçek zamanda alınamayacak bir
fiyattan alım varsayılır.

Burada D **hesaplanır**: son pivot (C) onaylandığı anda D'nin fiyatı
deterministiktir. Sonrası beklemektir. Fiyat o seviyeye dokunduğu barın
İÇİNDE sinyal doğar; hiçbir şey geriye kaydırılmaz.

## C onaylanana kadar geçen barlar

C, kendi barından `pivot_sag` bar SONRA onaylanır. O aralıkta fiyat D'ye
çoktan dokunmuş olabilir. Bu durumda kurulum **açılmaz**: bilemediğimiz bir
anda gerçekleşen bir dokunuşu sinyal saymak, ölçüme var olmayan bir işlem
eklemektir. `_D_onceden_vuruldu` tam bunu engeller ve kaçırılan kurulumlar
kaçırılmış olarak kalır.

## Yön

Dedektör hem boğa hem ayı kurulumu üretir. Ayı tarafı BIST'te doğrudan
işleme çevrilemez (açığa satış kısıtlı) ama ölçüm nesnesi olarak değerlidir:
formasyonun öngörü taşıyıp taşımadığı yönden bağımsız bir sorudur. Hangi
yönün raporlanacağına K4 karar verir.

Hesap **x-uzayında** yapılır: ayı kurulumunda fiyatlar `-1` ile çarpılır ve
boğa formülleri aynen uygulanır. İki ayrı formül kümesi yazmak, birinde
yapılan düzeltmenin diğerine geçmemesi demekti.

## Bağlam alanları FİLTRE DEĞİLDİR

KURAL-28 (uyarı işaretleri) ve KURAL-29 (teyit işaretleri) payload'a **sayı**
olarak yazılır, sinyali filtrelemez. Kitap "uyarı işareti varsa 1 bar bekle"
diyor (KURAL-30) ama "büyük gap", "geniş bar" için eşik VERMİYOR. Eşiği
dedektöre gömmek, o eşiği sonradan sonuca göre seçme kapısını açardı.
Bekleme tekniği K4'te veri üstünde, ön kayıtlı olarak sınanacak.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

import numpy as np
import pandas as pd
from quaxis.teknik.core.indicator import BaseIndicator
from quaxis.teknik.core.params import params_hash
from quaxis.teknik.core.types import (
    IndicatorMeta,
    IndicatorResult,
    Level,
    Line,
    Marker,
    Signal,
    Timeframe,
)
from quaxis.teknik.indicators.harmonik.parametreler import (
    AbcdParams,
    GartleyParams,
    HarmonikParams,
    KelebekParams,
    UcSurusParams,
)
from quaxis.teknik.indicators.harmonik.pivotlar import Pivot, pivotlar, zincire_ekle
from quaxis.teknik.indicators.ortak.gostergeler import (
    adx,
    atr,
    bollinger_genislik,
    ema,
    guvenli,
    macd_histogram,
    obv_egim,
    rsi,
    stokastik,
)

ZAMAN_DILIMLERI = (Timeframe.H4, Timeframe.D1, Timeframe.W1)


def oran_uyar(oran: float, kume: tuple[float, ...], tolerans: float) -> float | None:
    """Oran kümedeki bir hedefe tolerans içinde uyuyorsa O HEDEFİ döner.

    En yakın hedef seçilir. Hangi orana uyduğunu döndürmek şart: payload'a
    yazılıp "hangi Fibonacci oranı daha iyi çalışıyor" sorusu K4'te
    ölçülebilsin diye. `oran` NaN ise (sıfır uzunlukta bacak) None.
    """
    if not np.isfinite(oran):
        return None
    en_iyi: float | None = None
    en_kucuk = tolerans
    for hedef in kume:
        fark = abs(oran - hedef)
        if fark <= en_kucuk:
            en_iyi, en_kucuk = hedef, fark
    return en_iyi


@dataclass(frozen=True)
class _Baglam:
    """Sinyal barında ölçülen bağlam. Hiçbiri sinyali FİLTRELEMEZ."""

    ema20: np.ndarray
    ema50: np.ndarray
    ema200: np.ndarray
    rsi14: np.ndarray
    atr50: np.ndarray
    hacim_ort: np.ndarray
    adx14: np.ndarray
    macd_hist: np.ndarray
    bb_yuzdelik: np.ndarray
    stok14: np.ndarray
    obv_egim20: np.ndarray
    ciro_ort: np.ndarray


@dataclass
class _Kurulum:
    """Oranları tutmuş, fiyatın D'ye dokunmasını bekleyen formasyon."""

    boga: bool
    dogdu_i: int
    """Formasyonun BİLİNEBİLİR olduğu bar (C'nin onay barı)."""
    noktalar: list[tuple[str, int, float]]
    """(ad, bar indeksi, fiyat) — X/A/B/C ya da O/S1/A/S2/C."""
    giris: float
    stop: float
    hedef: float
    gecersiz: float
    """Bu seviyenin ötesinde GÖVDE kapanışı formasyonu bozar (C'nin ötesi)."""
    oranlar: dict[str, float] = field(default_factory=dict)

    @property
    def anahtar(self) -> tuple[int, ...]:
        """Aynı pivot dizisinden ikinci bir kurulum doğmasın diye kimlik."""
        return tuple(i for _, i, _ in self.noktalar)


class HarmonikTemel(BaseIndicator):
    """Dört formasyonun ortak motoru.

    Alt sınıflar yalnız `_aday`'ı yazar: zincirin son halkalarından bir
    kurulum çıkarır ya da çıkaramaz. Zincir kurma, dokunma takibi,
    geçersizlik, bağlam ve kayıt burada — tek yerde.
    """

    meta: ClassVar[IndicatorMeta]
    #: Alt sınıflar bunu KENDİ parametre tipiyle daraltır; `_aday` içinde
    #: `self.params` doğru tiple okunabilsin diye.
    params: HarmonikParams
    #: Formasyonun kaç ONAYLI pivota ihtiyacı var (D hariç — o hesaplanır).
    NOKTA_SAYISI: ClassVar[int]
    #: Payload'daki `event` alanı.
    OLAY: ClassVar[str]

    def __init__(self, params: HarmonikParams | None = None) -> None:
        self.params = params or HarmonikParams()

    # ----------------------------------------------------------- ana döngü

    def compute(
        self, df: pd.DataFrame, context: dict[str, Any] | None = None
    ) -> IndicatorResult:
        p = self.params
        sonuc = IndicatorResult(
            indicator=self.meta.name,
            version=self.meta.version,
            params_hash=params_hash(p),
            symbol=str(df.attrs.get("symbol", "")),
            timeframe=Timeframe(df.attrs.get("timeframe", Timeframe.D1)),
        )
        n = len(df)
        if n < p.atr_periyot + (p.pivot_sol + p.pivot_sag) * self.NOKTA_SAYISI + 5:
            return sonuc

        yuksek = df["high"].to_numpy(float)
        dusuk = df["low"].to_numpy(float)
        kapanis = df["close"].to_numpy(float)
        hacim = df["volume"].to_numpy(float)
        a = atr(df, p.atr_periyot)
        bag = self._baglam_serileri(df, kapanis, a)

        tum_pivotlar = pivotlar(yuksek, dusuk, p.pivot_sol, p.pivot_sag)
        sirada = 0
        zincir: list[Pivot] = []
        canli: list[_Kurulum] = []
        gorulen: set[tuple[int, ...]] = set()

        for t in range(n):
            # ATR ısınması burada barı ATLAMAZ: atlamak pivot zincirinin o
            # bardaki halkasını da düşürür ve zincir sessizce ayrışırdı.
            # Isınmamış bağlam değerleri `None` olarak yazılır.
            canli = [k for k in canli if self._yasiyor(k, t, kapanis)]

            # 1) Bekleyen kurulumlarda D'ye dokunuldu mu. Kurulumun DOĞDUĞU
            #    barda dokunma sayılmaz: formasyon o barın KAPANIŞINDA
            #    bilinir hâle geldi, bar içinde değil.
            for kur in list(canli):
                if t <= kur.dogdu_i:
                    continue
                # **D2 — hacimsiz barda sinyal DOĞMAZ** (ön kayıt:
                # `docs/olcum/onkayit-veri-duzeltme.md`).
                #
                # Hacimsiz barda açılış = yüksek = düşük = kapanış olur,
                # yani bar tek bir sayıdır ve bir seviyeye "dokunmuş"
                # sayılabilir. Ama o fiyattan kimse işlem yapmadı;
                # sağlayıcı son fiyatı tekrar ediyor. Böyle bir dokunuş
                # gerçekte verilemeyecek bir emirdir.
                #
                # Kurulum ÖLMEZ, yalnız o bar atlanır: fiyat ertesi gün
                # gerçekten seviyeye gelirse sinyal doğar.
                if hacim[t] <= 0:
                    continue
                if self._dokundu(kur, t, yuksek, dusuk):
                    self._kaydet(sonuc, kur, t, df, a, bag)
                    canli.remove(kur)

            # 2) Bu barda onaylanan pivotları zincire ekle.
            degisti = False
            while sirada < len(tum_pivotlar) and tum_pivotlar[sirada].onay_i <= t:
                degisti |= zincire_ekle(zincir, tum_pivotlar[sirada])
                sirada += 1

            # 3) Zincir değiştiyse yeni bir formasyon doğmuş olabilir.
            if degisti and len(zincir) >= self.NOKTA_SAYISI:
                kuyruk = zincir[-self.NOKTA_SAYISI :]
                kur = self._aday_kur(kuyruk, t)
                if (
                    kur is not None
                    and kur.anahtar not in gorulen
                    and not any(k.boga == kur.boga for k in canli)
                    and not self._onceden_vuruldu(kur, t, yuksek, dusuk)
                ):
                    canli.append(kur)
                    gorulen.add(kur.anahtar)

        return sonuc

    # -------------------------------------------------------- x-uzayı

    @staticmethod
    def _isaret(boga: bool) -> float:
        """Ayı kurulumunda fiyatlar `-1` ile çarpılır; boğa formülleri aynen
        geçerli olur. Bkz. modül docstring'i."""
        return 1.0 if boga else -1.0

    def _aday_kur(self, kuyruk: list[Pivot], t: int) -> _Kurulum | None:
        """Zincir kuyruğunu x-uzayına çevirip alt sınıfa verir.

        Yön, kuyruğun SON halkasının türünden çıkar: son halka bir tepeyse
        D onun altına düşer (boğa kurulumu), dipse üstüne çıkar (ayı).
        """
        boga = kuyruk[-1].tepe
        s = self._isaret(boga)
        # Almaşıklık zincirin kendi sözleşmesi; yine de burada kilitlenir —
        # bozulursa oranlar sessizce anlamsızlaşırdı.
        for onceki, sonraki in zip(kuyruk, kuyruk[1:], strict=False):
            if onceki.tepe == sonraki.tepe:
                return None
        return self._aday(kuyruk, [s * q.fiyat for q in kuyruk], t)

    def _aday(self, kuyruk: list[Pivot], x: list[float], t: int) -> _Kurulum | None:
        raise NotImplementedError

    def _kurulum(
        self,
        kuyruk: list[Pivot],
        adlar: tuple[str, ...],
        t: int,
        *,
        boga: bool,
        x_giris: float,
        x_stop: float,
        x_hedef: float,
        x_gecersiz: float,
        oranlar: dict[str, float],
    ) -> _Kurulum:
        s = self._isaret(boga)
        return _Kurulum(
            boga=boga,
            dogdu_i=t,
            noktalar=[(ad, q.i, q.fiyat) for ad, q in zip(adlar, kuyruk, strict=True)],
            giris=s * x_giris,
            stop=s * x_stop,
            hedef=s * x_hedef,
            gecersiz=s * x_gecersiz,
            oranlar=oranlar,
        )

    # ------------------------------------------------------- yaşam döngüsü

    def _yasiyor(self, k: _Kurulum, t: int, kapanis: np.ndarray) -> bool:
        """İki geçersizlik: süre dolması ve C'nin ötesinde GÖVDE kapanışı.

        C'nin aşılması formasyonu bozar çünkü C'nin formasyonun son salınım
        ucu olduğu varsayımı çöker — zincir de zaten o pivotu değiştirir.
        Fitil geçebilir, gövde geçemez (Golden Zone'daki kuralın aynısı:
        gevşetilmesi sinyal sayısını sessizce yarıya indiriyordu).
        """
        if t - k.dogdu_i > self.params.donus_max_bar:
            return False
        asti = kapanis[t] > k.gecersiz if k.boga else kapanis[t] < k.gecersiz
        return not asti

    def _dokundu(self, k: _Kurulum, t: int, y: np.ndarray, d: np.ndarray) -> bool:
        """Boğa kurulumunda barın DİBİ D'ye inerse dokunuldu sayılır."""
        return bool(d[t] <= k.giris) if k.boga else bool(y[t] >= k.giris)

    def _onceden_vuruldu(
        self, k: _Kurulum, t: int, y: np.ndarray, d: np.ndarray
    ) -> bool:
        """C'nin kendi barı ile onay barı arasında D zaten vuruldu mu.

        Vurulduysa kurulum AÇILMAZ. O aralıkta formasyonun varlığını
        bilmiyorduk; dokunuşu sinyal saymak, gerçekte verilemeyecek bir emri
        ölçüme eklemek olurdu. Kaçan kaçmıştır.
        """
        c_i = k.noktalar[-1][1]
        if t <= c_i:
            return False
        dilim = slice(c_i + 1, t + 1)
        if k.boga:
            return bool(d[dilim].min() <= k.giris)
        return bool(y[dilim].max() >= k.giris)

    # ------------------------------------------------------------- bağlam

    def _baglam_serileri(
        self, df: pd.DataFrame, kapanis: np.ndarray, a: np.ndarray
    ) -> _Baglam:
        bb = bollinger_genislik(kapanis, 20)
        hacim = df["volume"].to_numpy(float)
        return _Baglam(
            ema20=ema(kapanis, 20),
            ema50=ema(kapanis, 50),
            ema200=ema(kapanis, 200),
            rsi14=rsi(kapanis, 14),
            atr50=atr(df, 50),
            hacim_ort=pd.Series(hacim).rolling(20, min_periods=20).mean().to_numpy(),
            adx14=adx(df, 14),
            macd_hist=macd_histogram(kapanis),
            bb_yuzdelik=pd.Series(bb).rolling(120, min_periods=120)
            .rank(pct=True)
            .to_numpy(),
            stok14=stokastik(df, 14),
            obv_egim20=obv_egim(df, 20),
            ciro_ort=pd.Series(kapanis * hacim).rolling(20, min_periods=20)
            .mean()
            .to_numpy(),
        )

    def _baglam(
        self, kur: _Kurulum, t: int, df: pd.DataFrame, a: np.ndarray, bag: _Baglam
    ) -> dict[str, Any]:
        """Sinyal barında ölçülen bağlam. FİLTRE DEĞİL — ölçüm girdisi.

        Alan adları Golden Zone ile KASITLI olarak aynı: `tools/
        kosul_taramasi.py` iki stratejiyi aynı koşul kümesiyle tarayabilsin
        ve sonuçlar yan yana konabilsin diye.

        Harmoniğe özgü olanlar KURAL-28/29'dan gelir ve hepsi SAYIDIR:

        * `gap_atr` — C'den girişe kadarki en büyük boşluk (uyarı işareti).
        * `aralik_atr` — sinyal barının genişliği (geniş bar = uyarı).
        * `kuyruk_kapanis` — kapanışın barın neresinde olduğu (kuyruklu
          kapanış = teyit). Boğada 1'e yakın olması iyi sayılır.
        * `cimbiz` — önceki barla aynı seviyeden dönüş (teyit).
        """
        yon = 1.0 if kur.boga else -1.0
        k = float(df["close"].iloc[t])
        atr_t = float(a[t]) if not np.isnan(a[t]) else 0.0
        e50, e200 = bag.ema50[t], bag.ema200[t]
        e50_onceki = bag.ema50[t - 5] if t >= 5 else np.nan

        c_i = kur.noktalar[-1][1]
        acilis = df["open"].to_numpy(float)
        kapanis = df["close"].to_numpy(float)
        y = df["high"].to_numpy(float)
        d = df["low"].to_numpy(float)

        # KURAL-28: CD bacağındaki en büyük boşluk.
        if t > c_i + 1:
            bosluk = np.abs(acilis[c_i + 1 : t + 1] - kapanis[c_i : t])
            gap = float(bosluk.max())
        else:
            gap = 0.0

        aralik = y[t] - d[t]
        # Boğada kapanış barın ÜST ucuna yakınsa alt fitil uzun demektir.
        kuyruk = (k - d[t]) / aralik if aralik > 0 else None
        if kuyruk is not None and not kur.boga:
            kuyruk = 1.0 - kuyruk

        # KURAL-29 cımbız: iki barın ucu ATR'nin %10'u içinde buluşuyorsa.
        cimbiz = None
        if t > 0 and atr_t > 0:
            uc, onceki_uc = (d[t], d[t - 1]) if kur.boga else (y[t], y[t - 1])
            cimbiz = bool(abs(uc - onceki_uc) <= 0.1 * atr_t)

        hacim_ort = bag.hacim_ort[c_i]
        hacim = float(df["volume"].iloc[c_i])

        def uyum(deger: float) -> bool | None:
            return None if np.isnan(deger) else bool((k - deger) * yon > 0)

        return {
            "ema50_uyum": uyum(e50),
            "ema200_uyum": uyum(e200),
            "ema_egim_uyum": (
                None
                if np.isnan(e50) or np.isnan(e50_onceki)
                else bool((e50 - e50_onceki) * yon > 0)
            ),
            "ema20_50_uyum": (
                None
                if np.isnan(bag.ema20[t]) or np.isnan(bag.ema50[t])
                else bool((bag.ema20[t] - bag.ema50[t]) * yon > 0)
            ),
            "ema50_uzaklik_atr": (
                None if np.isnan(e50) or atr_t <= 0 else float((k - e50) * yon / atr_t)
            ),
            "rsi14": guvenli(bag.rsi14[t]),
            "adx14": guvenli(bag.adx14[t]),
            "macd_uyum": (
                None
                if np.isnan(bag.macd_hist[t])
                else bool(bag.macd_hist[t] * yon > 0)
            ),
            "bb_yuzdelik": guvenli(bag.bb_yuzdelik[t]),
            "stok14": guvenli(bag.stok14[t]),
            "obv_uyum": (
                None
                if np.isnan(bag.obv_egim20[t])
                else bool(bag.obv_egim20[t] * yon > 0)
            ),
            "atr_rejim": (
                None
                if np.isnan(bag.atr50[t]) or bag.atr50[t] <= 0 or atr_t <= 0
                else float(atr_t / bag.atr50[t])
            ),
            "hacim_orani": (
                None
                if np.isnan(hacim_ort) or hacim_ort <= 0
                else float(hacim / hacim_ort)
            ),
            "ciro": guvenli(bag.ciro_ort[t]),
            "govde_orani": (
                None if aralik <= 0 else float(abs(k - float(acilis[t])) / aralik)
            ),
            "aralik_atr": None if atr_t <= 0 else float(aralik / atr_t),
            # --- KURAL-28 / KURAL-29: uyarı ve teyit işaretleri ---
            "gap_atr": None if atr_t <= 0 else float(gap / atr_t),
            "kuyruk_kapanis": None if kuyruk is None else float(kuyruk),
            "cimbiz": cimbiz,
            # --- formasyonun kendi ölçüleri ---
            "olusum_bar": int(t - c_i),
            "formasyon_bar": int(c_i - kur.noktalar[0][1]),
            "bacak_atr": (
                None
                if atr_t <= 0
                else float(abs(kur.noktalar[0][2] - kur.giris) / atr_t)
            ),
        }

    # -------------------------------------------------------------- kayıt

    def _kaydet(
        self,
        sonuc: IndicatorResult,
        kur: _Kurulum,
        t: int,
        df: pd.DataFrame,
        a: np.ndarray,
        bag: _Baglam,
    ) -> None:
        p = self.params
        c_ad, c_i, c_fiyat = kur.noktalar[-1]
        bar_t = df.index[c_i]
        tespit_t = df.index[t]
        risk = abs(kur.giris - kur.stop)
        odul = abs(kur.hedef - kur.giris)

        sonuc.signals.append(
            Signal(
                bar_time=bar_t,
                detected_at=tespit_t,
                direction="long" if kur.boga else "short",
                state="confirmed",
                score=1.0,
                payload={
                    "event": self.OLAY,
                    "formasyon": self.meta.name,
                    # K4'ün üç bariyerli R ölçümü bu üçünü okur.
                    "giris": float(kur.giris),
                    "stop": float(kur.stop),
                    "hedef": float(kur.hedef),
                    "zaman_bariyeri": int(p.zaman_bariyeri),
                    # Ödül/risk bir SONUÇ değil, geometrinin ta kendisi:
                    # formasyon daha oluşurken bellidir. Payload'a yazılması
                    # "hangi R:R aralığı işe yarıyor" sorusunu ölçülebilir
                    # kılar.
                    "odul_risk": None if risk <= 0 else float(odul / risk),
                    "noktalar": {
                        ad: {"bar": df.index[i].isoformat(), "fiyat": float(f)}
                        for ad, i, f in kur.noktalar
                    },
                    "oranlar": dict(kur.oranlar),
                    "onay_bar": df.index[kur.dogdu_i].isoformat(),
                    **self._baglam(kur, t, df, a, bag),
                },
            )
        )

        # Formasyonun bacakları: X→A→B→C→D. Sinyal barında doğar; hiçbir
        # nokta sonradan kaydırılmaz.
        noktalar = [(df.index[i], float(f)) for _, i, f in kur.noktalar]
        noktalar.append((tespit_t, float(kur.giris)))
        sonuc.lines.append(
            Line(
                points=tuple(noktalar),
                label=self.meta.name,
                style="harmonik_bacak",
            )
        )
        for ad, i, f in kur.noktalar:
            sonuc.markers.append(
                Marker(t=df.index[i], price=float(f), text=ad, kind="pivot")
            )
        sonuc.markers.append(
            Marker(t=tespit_t, price=float(kur.giris), text="D", kind="signal")
        )
        # `start` boş bırakılırsa walk-forward karşılaştırması seviyeleri
        # "hep vardı" sayar ve sonradan doğan her seviye repaint görünür.
        sonuc.levels += [
            Level(price=float(kur.giris), label="giriş", style="entry", start=tespit_t),
            Level(price=float(kur.stop), label="stop", style="stop", start=tespit_t),
            Level(price=float(kur.hedef), label="hedef", style="target", start=tespit_t),
        ]


# ------------------------------------------------------------ FORMASYON-01


class Abcd(HarmonikTemel):
    """AB=CD — A, B, C ve hesaplanan D. X yok."""

    params: AbcdParams
    params: GartleyParams
    params: KelebekParams
    params: UcSurusParams
    NOKTA_SAYISI: ClassVar[int] = 3
    OLAY: ClassVar[str] = "harmonik_abcd"
    meta: ClassVar[IndicatorMeta] = IndicatorMeta(
        name="harmonik_abcd",
        version="0.1.0",
        category="formasyon",
        description="AB=CD: BC, AB'yi geri çeker; CD bacağı D hedefini verir (Pesavento)",
        supported_timeframes=ZAMAN_DILIMLERI,
    )

    def __init__(self, params: AbcdParams | None = None) -> None:
        super().__init__(params or AbcdParams())

    def _aday(self, kuyruk: list[Pivot], x: list[float], t: int) -> _Kurulum | None:
        p = self.params
        xa, xb, xc = x
        ab = xa - xb
        if ab <= 0:
            return None

        # BC, AB'yi geri çeker. Oran 1'i aşarsa (BC > AB) formasyon
        # GEÇERSİZ — kitabın açık kuralı.
        bc_ham = (xc - xb) / ab
        bc = oran_uyar(bc_ham, p.geri_cekilme_oranlari, p.tolerans)
        if bc is None or bc_ham >= 1.0:
            return None

        x_d = xc - ab * p.cd_orani
        # D, B'yi AŞMALI — aşmıyorsa ortada yeni bir uç yok, formasyon yok.
        if x_d >= xb:
            return None

        x_stop = xc - ab * p.stop_orani
        x_stop -= ab * p.stop_tamponu
        x_hedef = x_d + (xa - x_d) * p.hedef_orani
        return self._kurulum(
            kuyruk,
            ("A", "B", "C"),
            t,
            boga=kuyruk[-1].tepe,
            x_giris=x_d,
            x_stop=x_stop,
            x_hedef=x_hedef,
            x_gecersiz=xc,
            oranlar={"bc": bc, "bc_ham": bc_ham, "cd": p.cd_orani},
        )


# ------------------------------------------------------------ FORMASYON-02


class Gartley(HarmonikTemel):
    """Gartley '222' — X, A, B, C ve XA'nın .786'sında hesaplanan D."""

    NOKTA_SAYISI: ClassVar[int] = 4
    OLAY: ClassVar[str] = "harmonik_gartley"
    meta: ClassVar[IndicatorMeta] = IndicatorMeta(
        name="harmonik_gartley",
        version="0.1.0",
        category="formasyon",
        description="Gartley 222: D, XA'nın .786 geri çekilmesi; içinde AB=CD (Pesavento)",
        supported_timeframes=ZAMAN_DILIMLERI,
    )

    def __init__(self, params: GartleyParams | None = None) -> None:
        super().__init__(params or GartleyParams())

    def _aday(self, kuyruk: list[Pivot], x: list[float], t: int) -> _Kurulum | None:
        p = self.params
        xx, xa, xb, xc = x
        xa_boy = xa - xx
        ab_boy = xa - xb
        if xa_boy <= 0 or ab_boy <= 0:
            return None

        # Geçersizlik (kitap): B, X'i aşarsa · C, A'yı aşarsa.
        if xb <= xx or xc >= xa:
            return None

        ab = oran_uyar(ab_boy / xa_boy, p.geri_cekilme_oranlari, p.tolerans)
        bc = oran_uyar((xc - xb) / ab_boy, p.geri_cekilme_oranlari, p.tolerans)
        if ab is None or bc is None:
            return None

        x_d = xa - xa_boy * p.d_geri_cekilme
        # D, X'i AŞMAMALI (kitap) ve B'nin ötesinde olmalı — aksi hâlde CD
        # bacağı ters yöne bakar, ki böyle bir formasyon geometrik olarak
        # kurulamaz.
        if x_d <= xx or x_d >= xb:
            return None

        # Kitap: Gartley'in İÇİNDE bir AB=CD bulunmak ZORUNDA. CD'nin AB'ye
        # EŞİT olması şart değil — kitabın AB=CD bölümü uzatılmış CD'yi de
        # (1.27–2.00) aynı formasyon sayıyor.
        abcd_ham = (xc - x_d) / ab_boy
        abcd = oran_uyar(abcd_ham, p.abcd_oranlari, p.abcd_tolerans)
        if p.abcd_sarti and abcd is None:
            return None

        x_stop = xx - xa_boy * p.stop_tamponu
        x_hedef = x_d + (xa - x_d) * p.hedef_orani
        return self._kurulum(
            kuyruk,
            ("X", "A", "B", "C"),
            t,
            boga=kuyruk[-1].tepe,
            x_giris=x_d,
            x_stop=x_stop,
            x_hedef=x_hedef,
            x_gecersiz=xc,
            oranlar={
                "ab": ab,
                "bc": bc,
                "d": p.d_geri_cekilme,
                "abcd": abcd if abcd is not None else float("nan"),
                "abcd_ham": abcd_ham,
            },
        )


# ------------------------------------------------------------ FORMASYON-03


class Kelebek(HarmonikTemel):
    """Butterfly — D, X'in ÖTESİNDE, XA'nın 1.272 uzantısında."""

    NOKTA_SAYISI: ClassVar[int] = 4
    OLAY: ClassVar[str] = "harmonik_kelebek"
    meta: ClassVar[IndicatorMeta] = IndicatorMeta(
        name="harmonik_kelebek",
        version="0.1.0",
        category="formasyon",
        description="Butterfly: D, XA'nın 1.272 uzantısı; stop 1.618'in dışı (Pesavento)",
        supported_timeframes=ZAMAN_DILIMLERI,
    )

    def __init__(self, params: KelebekParams | None = None) -> None:
        super().__init__(params or KelebekParams())

    def _aday(self, kuyruk: list[Pivot], x: list[float], t: int) -> _Kurulum | None:
        p = self.params
        xx, xa, xb, xc = x
        xa_boy = xa - xx
        ab_boy = xa - xb
        if xa_boy <= 0 or ab_boy <= 0:
            return None
        if xb <= xx or xc >= xa:
            return None

        ab = oran_uyar(ab_boy / xa_boy, p.geri_cekilme_oranlari, p.tolerans)
        bc = oran_uyar((xc - xb) / ab_boy, p.geri_cekilme_oranlari, p.tolerans)
        if ab is None or bc is None:
            return None

        x_d = xa - xa_boy * p.d_uzanti
        # Kelebek'in tanımı: D, X'i AŞAR. Uzantı 1'den büyük olduğu için
        # parametre doğrulaması bunu zaten garanti eder; burada kural
        # KODDA da görünsün diye kilitleniyor.
        if x_d >= xx:
            return None

        abcd_ham = (xc - x_d) / ab_boy
        abcd = oran_uyar(abcd_ham, p.abcd_oranlari, p.abcd_tolerans)
        if p.abcd_sarti and abcd is None:
            return None

        x_stop = xa - xa_boy * p.stop_uzanti - xa_boy * p.stop_tamponu
        x_hedef = x_d + (xa - x_d) * p.hedef_orani
        return self._kurulum(
            kuyruk,
            ("X", "A", "B", "C"),
            t,
            boga=kuyruk[-1].tepe,
            x_giris=x_d,
            x_stop=x_stop,
            x_hedef=x_hedef,
            x_gecersiz=xc,
            oranlar={
                "ab": ab,
                "bc": bc,
                "d": p.d_uzanti,
                "abcd": abcd if abcd is not None else float("nan"),
                "abcd_ham": abcd_ham,
            },
        )


# ------------------------------------------------------------ FORMASYON-04


class UcSurus(HarmonikTemel):
    """Three Drives — art arda üç uzantı sürüşü.

    Beş onaylı pivot gerekir: `O` (sürüşlere giren uç), `S1`, `A`, `S2`, `C`.
    `O` şart çünkü kitap "A geri çekilmesi" derken bir önceki BACAĞA göre
    ölçüyor; o bacağın başlangıcı `O`'dur. `O` olmadan A'nın oranı
    hesaplanamaz ve kuralın yarısı sessizce uygulanmamış olurdu.
    """

    NOKTA_SAYISI: ClassVar[int] = 5
    OLAY: ClassVar[str] = "harmonik_uc_surus"
    meta: ClassVar[IndicatorMeta] = IndicatorMeta(
        name="harmonik_uc_surus",
        version="0.1.0",
        category="formasyon",
        description="Three Drives: her sürüş bir öncekinin 1.272 uzantısı (Pesavento)",
        supported_timeframes=ZAMAN_DILIMLERI,
    )

    def __init__(self, params: UcSurusParams | None = None) -> None:
        super().__init__(params or UcSurusParams())

    def _aday(self, kuyruk: list[Pivot], x: list[float], t: int) -> _Kurulum | None:
        p = self.params
        xo, xs1, xa, xs2, xc = x
        giris_bacak = xo - xs1
        s2_bacak = xa - xs1
        if giris_bacak <= 0 or s2_bacak <= 0:
            return None

        # Geçersizlik (kitap): A, O'yu aşarsa · C, A'yı aşarsa.
        if xa >= xo or xc >= xa:
            return None
        # Her sürüş bir öncekinden İLERİ olmalı.
        if xs2 >= xs1:
            return None

        a_oran = oran_uyar(
            (xa - xs1) / giris_bacak, p.geri_cekilme_oranlari, p.tolerans
        )
        if a_oran is None:
            return None

        # Sürüş 2, S1→A geri çekilmesinin uzantısıdır. Kitap "genelde her iki
        # sürüşte AYNI oran" diyor; bu yüzden gözlenen uzantı, D3'ü
        # yansıtacağımız oranla AYNI olmak zorunda.
        s2_uzanti = (xa - xs2) / s2_bacak
        if abs(s2_uzanti - p.surus_uzanti) > p.tolerans:
            return None

        s3_bacak = xc - xs2
        if s3_bacak <= 0:
            return None
        c_oran = oran_uyar(s3_bacak / (xa - xs2), p.geri_cekilme_oranlari, p.tolerans)
        if c_oran is None:
            return None

        x_d = xc - s3_bacak * p.surus_uzanti
        if x_d >= xs2:  # üçüncü sürüş ikinciyi aşmalı
            return None

        x_stop = xc - s3_bacak * p.stop_uzanti - s3_bacak * p.stop_tamponu
        # K0: hedef, SÜRÜŞ 3 salınımının geri çekilmesi (C → D3).
        x_hedef = x_d + (xc - x_d) * p.hedef_orani
        return self._kurulum(
            kuyruk,
            ("O", "S1", "A", "S2", "C"),
            t,
            boga=kuyruk[-1].tepe,
            x_giris=x_d,
            x_stop=x_stop,
            x_hedef=x_hedef,
            x_gecersiz=xc,
            oranlar={
                "a": a_oran,
                "s2_uzanti": s2_uzanti,
                "c": c_oran,
                "s3_uzanti": p.surus_uzanti,
            },
        )


# ---------------------------------------------------------------- fabrika


def olustur_abcd(params: AbcdParams | None = None) -> Abcd:
    return Abcd(params)


def olustur_gartley(params: GartleyParams | None = None) -> Gartley:
    return Gartley(params)


def olustur_kelebek(params: KelebekParams | None = None) -> Kelebek:
    return Kelebek(params)


def olustur_uc_surus(params: UcSurusParams | None = None) -> UcSurus:
    return UcSurus(params)
