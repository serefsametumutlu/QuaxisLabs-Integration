"""K4 — sembol-kümelenmiş ileri getiri ölçümü.

Bir stratejinin **işe yarayıp yaramadığını** ölçen çekirdek. Eleme değil
**etiketleme** yapar: sonuç ne çıkarsa pasaporta ve siteye o yazılır.

Dört tasarım kararı ve gerekçeleri:

1. **Bağımsız gözlem birimi SEMBOL'dür, bar değil.** Aynı sembolün ardışık
   barları bağımsız değildir; bar sayarsan örneklem sahte büyür ve p değeri
   sahte küçülür. Her sembol TEK bir gözlem üretir: o sembolün sinyallerinin
   ortalama ileri getirisi.

2. **Adil baz permütasyonla kurulur.** "Sinyal +%1.18 getirdi" tek başına
   hiçbir şey söylemez — piyasa zaten yükseliyorsa rastgele bir bar da
   getirir. Baz, AYNI sembolde, AYNI sayıda, AYNI yön karışımıyla seçilmiş
   rastgele barların getirisidir. Böylece düz "piyasa yükseldi" etkisi
   ayıklanır.

3. **Parametrik varsayım yok.** Getiri dağılımları normal değil; p değeri
   permütasyonla hesaplanır.

4. **IS/OOS ayrımı.** Eşikler geçmişte oturur, iddia GÖRÜLMEMİŞ dönemde
   ölçülür. Yalnız OOS penceresindeki sinyaller sayılır.

Çoklu test düzeltmesi (`bh_fdr`) ayrı bir adımdır: birçok strateji test
edilecek, düzeltme olmadan biri tesadüfen "çalışıyor" görünür.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd
from quaxis.teknik.core.types import Direction, Signal

#: Varsayılan permütasyon turu. Az tur = kaba p değeri; p ancak 1/(B+1)
#: çözünürlüğünde okunabilir.
VARSAYILAN_TUR = 2000

#: IS/OOS bölme noktası — serinin ilk %70'i içeride, son %30'u dışarıda.
VARSAYILAN_OOS_ORANI = 0.30

#: Taraf başına komisyon ve kayma (fiyatın oranı) — `bariyer.py` ile AYNI
#: varsayım. İki ölçüm farklı maliyet kullanırsa sonuçları kıyaslanamaz.
#:
#: Bu alanın eklenmesinin sebebi ölçülmüş bir hata: maliyetsiz ölçüm
#: Golden Zone'da bulunan kenarın TAMAMI kadar bir fark yaratıyordu.
VARSAYILAN_KOMISYON = 0.0005
VARSAYILAN_KAYMA = 0.0005


def maliyet_dus(getiri: np.ndarray | float, komisyon: float, kayma: float):
    """Brüt getiriden gidiş-dönüş maliyeti düşer.

    Giriş de çıkış da piyasa emri sayılır (momentum kurulumunda giriş,
    sıralama barının KAPANIŞINDADIR — limit emir değil), dolayısıyla iki
    tarafta da komisyon + kayma vardır:

        net = (1 + brüt) × (1 − c) / (1 + c) − 1
    """
    c = komisyon + kayma
    return (1.0 + getiri) * (1.0 - c) / (1.0 + c) - 1.0


@dataclass(frozen=True)
class SymbolMeasurement:
    """Tek bir sembolün katkısı — analizin bağımsız gözlem birimi."""

    symbol: str
    n_signals: int
    signal_return: float
    """Sinyal barlarının yön-düzeltilmiş ortalama ileri getirisi."""
    baseline_return: float
    """Aynı sembolde rastgele barların ortalama getirisi (adil baz)."""

    @property
    def difference(self) -> float:
        return self.signal_return - self.baseline_return


@dataclass(frozen=True)
class ForwardReturnResult:
    """K4 çıktısı. `verdict` alanı pasaporta olduğu gibi geçer."""

    universe: int
    """Ölçüme giren sembol sayısı."""
    independent_observations: int
    """Sinyal ÜRETEN sembol sayısı — istatistiğin gerçek n'i."""
    total_signals: int
    horizon: int
    oos_ratio: float
    mean_difference: float
    p_value: float
    permutations: int
    measurements: tuple[SymbolMeasurement, ...]

    @property
    def verdict(self) -> str:
        """FDR'den ÖNCEKİ ham etiket. Aile düzeltmesi `bh_fdr` ile yapılır ve
        nihai verdikt orada belirlenir."""
        if self.independent_observations == 0:
            return "olculmedi"
        return "kenar-var" if self.p_value <= 0.05 else "kanitlanmadi"


def forward_return(close: pd.Series, t: pd.Timestamp, horizon: int) -> float | None:
    """`t` barından `horizon` bar sonrasına kadar getiri.

    Yeterli ileri bar yoksa `None` döner — eksik veriyi sıfır saymak,
    stratejiyi kayırmanın en sessiz yoludur.
    """
    try:
        i = close.index.get_loc(t)
    except KeyError:
        return None
    if not isinstance(i, int) or i + horizon >= len(close):
        return None
    bas = float(close.iloc[i])
    if bas == 0:
        return None
    return float(close.iloc[i + horizon]) / bas - 1.0


def _direction_sign(direction: Direction) -> float:
    """Short sinyalde düşüş KAZANÇtır; getiri işareti ona göre çevrilir."""
    return 1.0 if str(direction) in ("long", "al") else -1.0


def _oos_start(close: pd.Series, oos_ratio: float) -> pd.Timestamp:
    kesim = int(len(close) * (1.0 - oos_ratio))
    return close.index[min(kesim, len(close) - 1)]


def measure_symbol(
    symbol: str,
    close: pd.Series,
    signals: Sequence[Signal],
    *,
    horizon: int,
    oos_ratio: float = VARSAYILAN_OOS_ORANI,
    permutations: int = VARSAYILAN_TUR,
    rng: np.random.Generator | None = None,
    komisyon: float = VARSAYILAN_KOMISYON,
    kayma: float = VARSAYILAN_KAYMA,
) -> SymbolMeasurement | None:
    """Bir sembolün sinyal getirisini ve adil bazını ölçer.

    Sinyalin barı olarak **`detected_at`** kullanılır, `bar_time` değil:
    sinyal ancak onaylandığı barda bilinebilirdi; pivotun kendi barından
    işlem açmak geçmişi yeniden yazmak olur.

    Sinyal üretmeyen sembol `None` döner ve gözlem sayılmaz.
    """
    r = rng if rng is not None else np.random.default_rng(0)
    oos_bas = _oos_start(close, oos_ratio)

    getiriler: list[float] = []
    yonler: list[float] = []
    for s in signals:
        t = s.detected_at
        if t < oos_bas:
            continue  # IS penceresi: iddia burada ölçülmez
        g = forward_return(close, t, horizon)
        if g is None:
            continue
        yon = _direction_sign(s.direction)
        getiriler.append(maliyet_dus(g * yon, komisyon, kayma))
        yonler.append(yon)

    if not getiriler:
        return None

    # Adil baz: AYNI pencerede, AYNI sayıda, AYNI yön karışımıyla rastgele bar.
    oos_i = close.index.get_loc(oos_bas)
    if not isinstance(oos_i, int):
        oos_i = int(np.asarray(oos_i).min())
    secilebilir = np.arange(oos_i, len(close) - horizon)
    if len(secilebilir) == 0:
        return None

    kapanis = close.to_numpy(dtype=float)
    ileri = kapanis[secilebilir + horizon] / kapanis[secilebilir] - 1.0
    yon_dizi = np.asarray(yonler)
    # Maliyet BAZA DA uygulanır; yalnız sinyale uygulamak ölçümü
    # stratejinin aleyhine saptırırdı.
    ortalamalar = _permutasyon_ortalamalari(
        ileri, yon_dizi, permutations, r, komisyon, kayma
    )

    return SymbolMeasurement(
        symbol=symbol,
        n_signals=len(getiriler),
        signal_return=float(np.mean(getiriler)),
        baseline_return=float(np.mean(ortalamalar)),
    )


def measure(
    seri: dict[str, pd.Series],
    sinyaller: dict[str, Sequence[Signal]],
    *,
    horizon: int = 20,
    oos_ratio: float = VARSAYILAN_OOS_ORANI,
    permutations: int = VARSAYILAN_TUR,
    seed: int = 20260913,
    komisyon: float = VARSAYILAN_KOMISYON,
    kayma: float = VARSAYILAN_KAYMA,
) -> ForwardReturnResult:
    """Evren geneli K4 ölçümü.

    p değeri **sembol düzeyinde** permütasyonla hesaplanır: her turda her
    sembol için rastgele barlar seçilir, sembol ortalamaları alınır, sonra
    semboller arası ortalama fark bulunur. Gözlemlenen fark bu boş dağılımın
    neresinde duruyor — p budur.
    """
    r = np.random.default_rng(seed)
    olcumler: list[SymbolMeasurement] = []
    bos_daginim: list[np.ndarray] = []

    for symbol, close in seri.items():
        sig = sinyaller.get(symbol, ())
        olcum = measure_symbol(
            symbol, close, sig,
            horizon=horizon, oos_ratio=oos_ratio, permutations=permutations, rng=r,
            komisyon=komisyon, kayma=kayma,
        )
        if olcum is None:
            continue
        olcumler.append(olcum)
        bos_daginim.append(
            _null_distribution(
                close, sig, horizon, oos_ratio, permutations, r, komisyon, kayma
            )
        )

    if not olcumler:
        return ForwardReturnResult(
            universe=len(seri), independent_observations=0, total_signals=0,
            horizon=horizon, oos_ratio=oos_ratio, mean_difference=0.0, p_value=1.0,
            permutations=permutations, measurements=(),
        )

    gozlenen = float(np.mean([o.difference for o in olcumler]))
    bos = np.vstack(bos_daginim)  # (sembol, tur)
    bos_ortalama = bos.mean(axis=0)
    merkezli = bos_ortalama - bos_ortalama.mean()
    # +1'ler: gözlemin kendisi de dağılımın bir üyesidir; p asla tam 0 olamaz.
    p = float((1 + int(np.sum(merkezli >= gozlenen))) / (permutations + 1))

    return ForwardReturnResult(
        universe=len(seri),
        independent_observations=len(olcumler),
        total_signals=sum(o.n_signals for o in olcumler),
        horizon=horizon,
        oos_ratio=oos_ratio,
        mean_difference=gozlenen,
        p_value=p,
        permutations=permutations,
        measurements=tuple(olcumler),
    )


def _null_distribution(
    close: pd.Series,
    signals: Sequence[Signal],
    horizon: int,
    oos_ratio: float,
    permutations: int,
    r: np.random.Generator,
    komisyon: float = VARSAYILAN_KOMISYON,
    kayma: float = VARSAYILAN_KAYMA,
) -> np.ndarray:
    """Bir sembolün boş dağılımı: rastgele barlardan sembol ortalamaları."""
    oos_bas = _oos_start(close, oos_ratio)
    yonler = [
        _direction_sign(s.direction)
        for s in signals
        if s.detected_at >= oos_bas and forward_return(close, s.detected_at, horizon) is not None
    ]
    oos_i = close.index.get_loc(oos_bas)
    if not isinstance(oos_i, int):
        oos_i = int(np.asarray(oos_i).min())
    secilebilir = np.arange(oos_i, len(close) - horizon)
    if not yonler or len(secilebilir) == 0:
        return np.zeros(permutations)

    kapanis = close.to_numpy(dtype=float)
    ileri = kapanis[secilebilir + horizon] / kapanis[secilebilir] - 1.0
    return _permutasyon_ortalamalari(
        ileri, np.asarray(yonler), permutations, r, komisyon, kayma
    )


def _permutasyon_ortalamalari(
    ileri: np.ndarray, yon: np.ndarray, permutations: int, r: np.random.Generator,
    komisyon: float = 0.0, kayma: float = 0.0,
) -> np.ndarray:
    """Tüm turları TEK seferde çeker: (tur, sinyal) matrisi → tur ortalamaları.

    Tur başına ayrı bir numpy çağrısı yapmak 543 sembol × 2000 tur = 1.1
    milyon küçük çağrı demekti; matris hâli aynı sayıyı dakikalar yerine
    saniyelerde üretiyor. Çekiliş ve sonuç AYNI — yalnızca aynı işlem
    toplu yapılıyor.
    """
    sec = r.integers(0, len(ileri), size=(permutations, len(yon)))
    return maliyet_dus(ileri[sec] * yon, komisyon, kayma).mean(axis=1)


def bh_fdr(p_values: dict[str, float], q: float = 0.05) -> dict[str, bool]:
    """Benjamini-Hochberg — hangi stratejiler q eşiğini GEÇER.

    Tek bir stratejiye bakıp "p<0.05, çalışıyor" demek, çok sayıda strateji
    test edildiğinde yanıltıcıdır: 20 stratejinin biri tesadüfen geçer. Aile
    burada tanımlanır ve düzeltme ailenin tamamına uygulanır.
    """
    if not p_values:
        return {}
    adlar = sorted(p_values, key=lambda k: p_values[k])
    m = len(adlar)
    esik_indeksi = 0
    for i, ad in enumerate(adlar, start=1):
        if p_values[ad] <= q * i / m:
            esik_indeksi = i
    gecenler = set(adlar[:esik_indeksi])
    return {ad: ad in gecenler for ad in p_values}
