"""Kesitsel Momentum dedektörü — K2.

Kural `docs/strateji/kaynak/kesitsel-momentum-K0.md`'de, sayfa numarasıyla
(Chan 2013, s.145–146):

    her bar: evrendeki her sembolün son 252 günlük getirisini SIRALA
             üst %10'u AL, 25 gün TUT

Bu bir grafik kurulumu değil. Tek bir sembole bakarak "momentum var mı"
denemez; sıralama tanım gereği **evrenin tamamını aynı anda** görmeyi
gerektirir. O yüzden `BaseIndicator` değil `UniverseIndicator`.

## Yalnız alış

BIST'te açığa satış kısıtlı (kullanıcı kararı, 2026-09-13). Kaynak uzun/kısa
kuruyor; biz yalnız üst dilimi alıyoruz. Bu, kaynağın piyasa-nötr yapısını
bozar: kazancın ne kadarı momentumdan, ne kadarı BIST'in kendi
sürüklenmesinden belli olmaz. **Ayıklaması ölçümde**, adil bazda.

## Örtüşmeyen sinyal — Chan'ın uyarısından türetilmiştir

Chan (s.151): *"Momentum portföyünü her gün yeniden dengeleyebiliriz ama bu
ticaret sinyallerini daha bağımsız yapmaz."*

25 günlük tutuşta her bar sinyal üretirsek aynı işlemi 25 kez saymış
oluruz: örneklem sahte büyür, p değeri sahte küçülür. Bu yüzden bir sembol
için yeni sinyal, öncekinin tutuşu **bitmeden** üretilmez.

## Non-repaint gerekçesi

`t` barındaki sıralama yalnız `[t-252, t]` aralığındaki kapanışları kullanır;
`t`'den sonraki hiçbir bar görülmez. Sinyal `t`'nin kapanışında doğar ve
`bar_time == detected_at == t`'dir — bu kurulumda "onaylanma" diye ayrı bir
an yok, sıralama o barın kapanışında zaten kesindir.
"""

from __future__ import annotations

from typing import ClassVar

import numpy as np
import pandas as pd
from quaxis.teknik.core.indicator import UniverseIndicator
from quaxis.teknik.core.params import params_hash
from quaxis.teknik.core.types import IndicatorMeta, IndicatorResult, Marker, Signal, Timeframe
from quaxis.teknik.indicators.kesitsel_momentum.parametreler import KesitselMomentumParams

META = IndicatorMeta(
    name="kesitsel_momentum",
    version="0.1.0",
    category="universe",
    description="Evrenin üst %10'unu 252 günlük getiriye göre seçer, 25 gün tutar",
    supported_timeframes=(Timeframe.D1, Timeframe.W1),
)


def _kapanis_matrisi(universe: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """{sembol: df} → (tarih × sembol) kapanış matrisi.

    Semboller farklı tarihlerde işlem görmeye başlar; hizalama olmadan
    "aynı bardaki sıralama" diye bir şey tanımlanamaz.
    """
    return pd.DataFrame({s: df["close"] for s, df in universe.items()}).sort_index()


def _ciro_matrisi(universe: dict[str, pd.DataFrame], pencere: int) -> pd.DataFrame:
    ciro = pd.DataFrame(
        {s: df["close"] * df["volume"] for s, df in universe.items()}
    ).sort_index()
    return ciro.rolling(pencere, min_periods=pencere).mean()


class KesitselMomentum(UniverseIndicator):
    """Evren-geneli momentum sıralaması."""

    meta: ClassVar[IndicatorMeta] = META

    def __init__(self, params: KesitselMomentumParams | None = None) -> None:
        self.params = params or KesitselMomentumParams()

    def compute_universe(
        self, universe: dict[str, pd.DataFrame], index_df: pd.DataFrame
    ) -> dict[str, IndicatorResult]:
        p = self.params
        if not universe:
            return {}

        kapanis = _kapanis_matrisi(universe)
        ciro = _ciro_matrisi(universe, p.ciro_penceresi) if p.asgari_ciro > 0 else None

        # Momentum getirisi: [t-geriye_bakis, t-atlama_gun] aralığı.
        # `shift` ileri değil GERİ bakar; hiçbir satır t'den sonrasını görmez.
        son = kapanis.shift(p.atlama_gun)
        ilk = kapanis.shift(p.geriye_bakis)
        with np.errstate(divide="ignore", invalid="ignore"):
            getiri = son / ilk - 1.0

        # Her bar için kesitsel yüzdelik sıra (1.0 = en yüksek getirili).
        yuzdelik = getiri.rank(axis=1, pct=True, na_option="keep")
        if ciro is not None:
            yuzdelik = yuzdelik.where(ciro >= p.asgari_ciro)

        esik = 1.0 - p.ust_dilim
        sonuclar: dict[str, IndicatorResult] = {}
        tarihler = kapanis.index

        for sembol, df in universe.items():
            if sembol not in yuzdelik.columns:
                continue
            sonuc = IndicatorResult(
                indicator=META.name, version=META.version, params_hash=params_hash(p),
                symbol=sembol, timeframe=Timeframe(df.attrs.get("timeframe", Timeframe.D1)),
            )
            y = yuzdelik[sembol].to_numpy(dtype=float)
            g = getiri[sembol].to_numpy(dtype=float)
            k = kapanis[sembol].to_numpy(dtype=float)
            evren_n = yuzdelik.notna().sum(axis=1).to_numpy()

            sonraki_uygun = 0
            for i in range(len(tarihler)):
                if i < sonraki_uygun or np.isnan(y[i]) or y[i] < esik:
                    continue
                # Örtüşmeyen sinyal: bu sembol tutuş bitene kadar susar.
                sonraki_uygun = i + p.tutus
                t = tarihler[i]
                sonuc.signals.append(
                    Signal(
                        bar_time=t,
                        detected_at=t,
                        direction="long",
                        state="confirmed",
                        score=float(y[i]),
                        payload={
                            "event": "kesitsel_momentum_ust_dilim",
                            "momentum_getiri": float(g[i]),
                            "yuzdelik": float(y[i]),
                            "evren": int(evren_n[i]),
                            "tutus": int(p.tutus),
                            "geriye_bakis": int(p.geriye_bakis),
                            "atlama_gun": int(p.atlama_gun),
                            "giris": float(k[i]),
                        },
                    )
                )
                sonuc.markers.append(
                    Marker(t=t, price=float(k[i]), text=f"%{y[i] * 100:.0f}", kind="signal")
                )
            if sonuc.signals:
                sonuclar[sembol] = sonuc
        return sonuclar


def olustur(params: KesitselMomentumParams | None = None) -> KesitselMomentum:
    """Katalog adresi bu fabrikayı gösterir."""
    return KesitselMomentum(params)


#: "12-1" varyantı: son ay atlanır. Akademik literatürün standardı;
#: Chan'ın kodu atlamıyor. Hangisinin doğru olduğu K3'te ölçülecek,
#: o yüzden ikisi de katalogda AYRI künye olarak duruyor.
ATLAMALI_AD = "kesitsel_momentum_12_1"

META_ATLAMALI = IndicatorMeta(
    name=ATLAMALI_AD,
    version=META.version,
    category=META.category,
    description="Aynı sıralama, son ay atlanarak (12-1) — kısa vadeli dönüş etkisi dışlanır",
    supported_timeframes=META.supported_timeframes,
)


def olustur_atlamali() -> KesitselMomentum:
    d = KesitselMomentum(KesitselMomentumParams(atlama_gun=21))
    d.meta = META_ATLAMALI
    return d
