"""K4 — üç bariyerli R-katsayısı ölçümü.

`ileri_getiri.py` bir sinyalin N bar sonraki getirisini ölçer. Bu yeterli
DEĞİL ve nedeni somut: ICT/SMC ailesinin bütün iddiası **asimetrik R**'dir —
0.705'ten derin girersen stop küçük (dip altı), hedef uzak (önceki tepe).
%35 isabetle 3R kazandıran bir sistem kârlıdır ama **10 barlık ileri
getiride hiç görünmez**.

Nitekim ICT kavramlarını "hiçbir anlamlı kenar yok" diye bulan en titiz
çalışma (648 backtest, SPY/QQQ/DIA/IWM) **zaman bazlı çıkış** kullanmıştı:
5/10/20 bar, stop yok hedef yok. O kurulum, ölçtüğü şeyin iddiasını görmeye
yapısal olarak kapalıydı. Bu modül o kör noktayı kapatır.

Üç bariyer (López de Prado'nun triple barrier yöntemi):

    ┌─ hedef  → +R
    │
  giriş ─────────────── zaman ─→ kalan R
    │
    └─ stop   → −1R

**Aynı barda iki bariyer de vurulursa STOP kazanır.** Bu iyimserliğe karşı
alınmış bilinçli bir karardır: bar içi sıralamayı bilmiyoruz ve emin
olmadığımız yerde stratejinin lehine varsaymak, backtest'i yalancı yapmanın
en sessiz yoludur. (Önceki projenin motorunda düzeltilen on kusurdan biri
tam olarak "bar içi SL/TP önceliği" idi.)
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd
from quaxis.teknik.core.types import Direction, Signal

VARSAYILAN_TUR = 2000

#: IS/OOS bölme noktası — `ileri_getiri.VARSAYILAN_OOS_ORANI` ile AYNI olmalı.
#: İki ölçüm farklı pencerelerden sayı üretirse aynı tabloda yan yana duran
#: iki sütun farklı şeyleri anlatır ve rapor sessizce yanıltır.
VARSAYILAN_OOS_ORANI = 0.30


@dataclass(frozen=True)
class BarrierOutcome:
    """Tek bir işlemin sonucu."""

    symbol: str
    entry_t: pd.Timestamp
    exit_t: pd.Timestamp
    r_multiple: float
    outcome: str
    """`"hedef"` · `"stop"` · `"zaman"` — hangi bariyer vuruldu."""
    bars_held: int


@dataclass(frozen=True)
class RResult:
    """Evren geneli R dağılımı ve adil baza karşı p değeri."""

    n_trades: int
    n_symbols: int
    win_rate: float
    mean_r: float
    median_r: float
    target_rate: float
    stop_rate: float
    time_rate: float
    baseline_mean_r: float
    p_value: float
    permutations: int
    outcomes: tuple[BarrierOutcome, ...]
    oos_ratio: float = VARSAYILAN_OOS_ORANI

    @property
    def expectancy(self) -> float:
        """İşlem başına beklenen R. Kârlılığın tek sayılık özeti."""
        return self.mean_r

    @property
    def verdict(self) -> str:
        if self.n_symbols == 0:
            return "olculmedi"
        return "kenar-var" if self.p_value <= 0.05 else "kanitlanmadi"


def _sign(direction: Direction) -> float:
    return 1.0 if str(direction) in ("long", "al") else -1.0


def barrier_outcome(
    ohlc: pd.DataFrame,
    entry_t: pd.Timestamp,
    *,
    stop: float,
    target: float,
    direction: Direction = "long",
    max_bars: int = 60,
    symbol: str = "",
) -> BarrierOutcome | None:
    """Girişten sonraki barları tek tek yürüyüp hangi bariyerin vurulduğunu bulur.

    `stop` ve `target` FİYAT seviyeleridir, mesafe değil. Giriş, sinyal barının
    KAPANIŞIDIR — bar içinden giriş varsaymak geçmişi yeniden yazmaktır.

    Yeterli ileri bar yoksa ya da risk sıfırsa `None` döner; eksik veriyi
    "başabaş" saymak stratejiyi kayırır.
    """
    try:
        i = ohlc.index.get_loc(entry_t)
    except KeyError:
        return None
    if not isinstance(i, int) or i + 1 >= len(ohlc):
        return None

    yon = _sign(direction)
    giris = float(ohlc["close"].iloc[i])
    risk = (giris - stop) * yon
    if risk <= 0:
        return None  # stop yanlış tarafta: sinyal geçersiz, ölçüme girmez

    son = min(i + max_bars, len(ohlc) - 1)
    yuksek = ohlc["high"].to_numpy(dtype=float)
    dusuk = ohlc["low"].to_numpy(dtype=float)

    for j in range(i + 1, son + 1):
        if yon > 0:
            stop_vuruldu = dusuk[j] <= stop
            hedef_vuruldu = yuksek[j] >= target
        else:
            stop_vuruldu = yuksek[j] >= stop
            hedef_vuruldu = dusuk[j] <= target

        # İKİSİ DE aynı barda vurulduysa STOP kazanır — bar içi sıralamayı
        # bilmiyoruz, emin olmadığımız yerde stratejinin lehine varsaymayız.
        if stop_vuruldu:
            return BarrierOutcome(symbol, entry_t, ohlc.index[j], -1.0, "stop", j - i)
        if hedef_vuruldu:
            r = (target - giris) * yon / risk
            return BarrierOutcome(symbol, entry_t, ohlc.index[j], r, "hedef", j - i)

    kapanis = float(ohlc["close"].iloc[son])
    r = (kapanis - giris) * yon / risk
    return BarrierOutcome(symbol, entry_t, ohlc.index[son], r, "zaman", son - i)


def _rastgele_baz(
    ohlc: pd.DataFrame,
    sonuclar: Sequence[BarrierOutcome],
    risk_orani: Sequence[float],
    hedef_orani: Sequence[float],
    yon: Sequence[float],
    max_bars: int,
    r: np.random.Generator,
    oos_i: int = 0,
) -> float:
    """Aynı sembolde, AYNI risk/hedef mesafeleriyle rastgele barlardan giriş.

    Adil baz budur: "bu sinyalde girmek, aynı risk yapısıyla rastgele bir
    barda girmekten daha iyi mi?" Piyasanın genel yönü böylece ayıklanır.

    Rastgele barlar da sinyallerle AYNI pencereden seçilir (`oos_i`); farklı
    pencereden seçilirse baz, ölçtüğü şeyden başka bir dönemi anlatır.
    """
    n = len(ohlc)
    secilebilir = np.arange(oos_i, n - max_bars - 1)
    if len(secilebilir) == 0 or not sonuclar:
        return 0.0
    toplam = []
    for k in range(len(sonuclar)):
        i = int(r.choice(secilebilir))
        giris = float(ohlc["close"].iloc[i])
        y = yon[k]
        stop = giris - risk_orani[k] * giris * y
        hedef = giris + hedef_orani[k] * giris * y
        s = barrier_outcome(
            ohlc, ohlc.index[i], stop=stop, target=hedef,
            direction="long" if y > 0 else "short", max_bars=max_bars,
        )
        if s is not None:
            toplam.append(s.r_multiple)
    return float(np.mean(toplam)) if toplam else 0.0


def measure_r(
    ohlc: dict[str, pd.DataFrame],
    islemler: dict[str, Sequence[tuple[Signal, float, float]]],
    *,
    max_bars: int = 60,
    oos_ratio: float = VARSAYILAN_OOS_ORANI,
    permutations: int = VARSAYILAN_TUR,
    seed: int = 20260913,
) -> RResult:
    """Evren geneli R ölçümü.

    `islemler`: {sembol: [(sinyal, stop_fiyati, hedef_fiyati), …]}. Stop ve
    hedef STRATEJİNİN kendi kuralından gelir — ölçüm onları uydurmaz.

    **Yalnız OOS penceresindeki sinyaller sayılır** — `ileri_getiri.measure`
    ile aynı kesim. İddia görülmemiş dönemde ölçülür; iki ölçüm farklı
    pencere kullanırsa katman tablosundaki iki sütun farklı şeyleri anlatır.

    p değeri, `ileri_getiri.measure` ile aynı mantıkta: sembol düzeyinde,
    aynı risk yapısıyla rastgele girişlere karşı permütasyon.
    """
    r = np.random.default_rng(seed)
    sonuclar: list[BarrierOutcome] = []
    sembol_farklari: list[float] = []
    sembol_bos: list[np.ndarray] = []

    for sembol, kayitlar in islemler.items():
        df = ohlc.get(sembol)
        if df is None or not kayitlar:
            continue
        oos_i = int(len(df) * (1.0 - oos_ratio))
        oos_bas = df.index[min(oos_i, len(df) - 1)]
        kendi: list[BarrierOutcome] = []
        risk_o, hedef_o, yonler = [], [], []
        for sinyal, stop, hedef in kayitlar:
            if sinyal.detected_at < oos_bas:
                continue  # IS penceresi: iddia burada ölçülmez
            s = barrier_outcome(
                df, sinyal.detected_at, stop=stop, target=hedef,
                direction=sinyal.direction, max_bars=max_bars, symbol=sembol,
            )
            if s is None:
                continue
            kendi.append(s)
            giris = float(df["close"].loc[sinyal.detected_at])
            y = _sign(sinyal.direction)
            risk_o.append(abs(giris - stop) / giris)
            hedef_o.append(abs(hedef - giris) / giris)
            yonler.append(y)

        if not kendi:
            continue
        sonuclar += kendi
        gercek = float(np.mean([s.r_multiple for s in kendi]))

        bos = np.array(
            [
                _rastgele_baz(df, kendi, risk_o, hedef_o, yonler, max_bars, r, oos_i)
                for _ in range(permutations)
            ]
        )
        sembol_farklari.append(gercek - float(bos.mean()))
        sembol_bos.append(bos)

    if not sonuclar:
        return RResult(
            0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, permutations, (), oos_ratio
        )

    rler = np.array([s.r_multiple for s in sonuclar])
    gozlenen = float(np.mean(sembol_farklari))
    bos_matris = np.vstack(sembol_bos)
    bos_ortalama = bos_matris.mean(axis=0)
    merkezli = bos_ortalama - bos_ortalama.mean()
    p = float((1 + int(np.sum(merkezli >= gozlenen))) / (permutations + 1))

    return RResult(
        n_trades=len(sonuclar),
        n_symbols=len(sembol_farklari),
        win_rate=float(np.mean(rler > 0)),
        mean_r=float(rler.mean()),
        median_r=float(np.median(rler)),
        target_rate=float(np.mean([s.outcome == "hedef" for s in sonuclar])),
        stop_rate=float(np.mean([s.outcome == "stop" for s in sonuclar])),
        time_rate=float(np.mean([s.outcome == "zaman" for s in sonuclar])),
        baseline_mean_r=float(bos_matris.mean()),
        p_value=p,
        permutations=permutations,
        outcomes=tuple(sonuclar),
        oos_ratio=oos_ratio,
    )
