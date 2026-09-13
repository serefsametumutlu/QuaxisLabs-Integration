"""Kesitsel Momentum — K1/K2 testleri.

`UniverseIndicator` jenerik `repaint_test`'e GİREMEZ: o test tek bir df
alır, bu indikatör evren sözlüğü ister. `catalog.populate_registry` bu
yüzden evren indikatörlerini `register_verified_elsewhere` ile kaydeder —
"başka yerde doğrulandı" demek, **burada** doğrulandı demektir.

`test_repaint_yok` o borcu ödüyor: evren farklı tarihlerden kesilir ve
kesim anına kadarki sinyallerin BİREBİR aynı kaldığı doğrulanır.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from quaxis.teknik.core.types import Timeframe
from quaxis.teknik.indicators.kesitsel_momentum import (
    KesitselMomentum,
    KesitselMomentumParams,
)

BAR = 400


def _seri(n: int, tohum: int, egim: float) -> pd.DataFrame:
    r = np.random.default_rng(tohum)
    k = 100 * np.exp(np.cumsum(r.normal(egim, 0.01, n)))
    idx = pd.date_range("2020-01-01", periods=n, freq="1D", tz="UTC")
    df = pd.DataFrame(
        {"open": k, "high": k * 1.01, "low": k * 0.99, "close": k, "volume": np.full(n, 1e6)},
        index=idx,
    )
    df.attrs["timeframe"] = Timeframe.D1
    return df


def _evren(n_sembol: int = 20, n_bar: int = BAR) -> dict[str, pd.DataFrame]:
    """Eğimleri KASITLI olarak farklı: sıralamanın ayıracağı bir şey olsun."""
    return {
        f"S{i:02d}": _seri(n_bar, tohum=i, egim=(i - n_sembol / 2) * 0.0004)
        for i in range(n_sembol)
    }


@pytest.fixture
def dedektor() -> KesitselMomentum:
    return KesitselMomentum(KesitselMomentumParams(geriye_bakis=60, tutus=10))


# ----------------------------------------------------------- K2: repaint


def test_repaint_yok(dedektor: KesitselMomentum) -> None:
    """Evren farklı tarihlerden kesilince, kesim anına kadarki sinyaller
    BİREBİR aynı kalmalı. Kalmıyorsa sıralama geleceği görüyor demektir."""
    evren = _evren()
    endeks = _seri(BAR, tohum=99, egim=0.0002)
    tam = dedektor(evren, endeks)

    for kesim in (250, 300, 350):
        kesik_evren = {s: df.iloc[:kesim] for s, df in evren.items()}
        kesik = dedektor(kesik_evren, endeks.iloc[:kesim])
        kesim_t = evren["S00"].index[kesim - 1]

        for sembol, r in kesik.items():
            tam_sinyal = [
                s for s in tam.get(sembol, r).signals if s.detected_at <= kesim_t
            ] if sembol in tam else []
            kesik_sinyal = [s.detected_at for s in r.signals]
            assert [s.detected_at for s in tam_sinyal] == kesik_sinyal, (
                f"{sembol}: kesim={kesim} sinyalleri ayrışıyor"
            )


def test_sinyal_kendi_barinda_dogar(dedektor: KesitselMomentum) -> None:
    """Bu kurulumda 'onaylanma' diye ayrı bir an yok: sıralama o barın
    kapanışında zaten kesin."""
    sonuc = dedektor(_evren(), _seri(BAR, 99, 0.0002))
    for r in sonuc.values():
        for s in r.signals:
            assert s.bar_time == s.detected_at


# ------------------------------------------------------- K1: kural kilidi


def test_sadece_ust_dilim_secilir() -> None:
    """En güçlü eğimli semboller seçilmeli, en zayıflar seçilmemeli."""
    d = KesitselMomentum(KesitselMomentumParams(geriye_bakis=60, tutus=10, ust_dilim=0.20))
    evren = _evren(20)
    sonuc = d(evren, _seri(BAR, 99, 0.0002))
    secilen = set(sonuc)
    # Eğim sembol indeksiyle artıyor: S19 en güçlü, S00 en zayıf.
    assert "S19" in secilen
    assert "S00" not in secilen


def test_ortusen_sinyal_uretilmez() -> None:
    """Chan s.151: her gün yeniden dengelemek sinyalleri bağımsız YAPMAZ.
    25 günlük tutuşta her bar sinyal üretmek aynı işlemi 25 kez saymaktır —
    örneklem sahte büyür, p değeri sahte küçülür."""
    tutus = 10
    d = KesitselMomentum(KesitselMomentumParams(geriye_bakis=60, tutus=tutus))
    sonuc = d(_evren(), _seri(BAR, 99, 0.0002))
    assert sonuc, "en az bir sembol sinyal vermeliydi"
    for sembol, r in sonuc.items():
        zamanlar = [s.detected_at for s in r.signals]
        araliklar = [
            (b - a).days for a, b in zip(zamanlar, zamanlar[1:], strict=False)
        ]
        assert all(x >= tutus for x in araliklar), f"{sembol}: örtüşen sinyal {araliklar}"


def test_atlama_sirlamayi_degistirir() -> None:
    """12-1 varyantı son ayı atlar; farklı bir sıralama üretmeli, yoksa
    iki künyeyi ayrı tutmanın anlamı kalmaz."""
    evren, endeks = _evren(), _seri(BAR, 99, 0.0002)
    temel = KesitselMomentum(KesitselMomentumParams(geriye_bakis=60, tutus=10))
    atlamali = KesitselMomentum(
        KesitselMomentumParams(geriye_bakis=60, tutus=10, atlama_gun=21)
    )
    a = {s: [x.detected_at for x in r.signals] for s, r in temel(evren, endeks).items()}
    b = {s: [x.detected_at for x in r.signals] for s, r in atlamali(evren, endeks).items()}
    assert a != b


def test_ciro_filtresi_eler() -> None:
    """İnce sembolde 12 aylık getiri sıralaması fiyat değil gürültü sıralar."""
    evren = _evren(20)
    evren["S19"]["volume"] = 1.0  # en güçlü sembol ama cirosu yok
    d = KesitselMomentum(
        KesitselMomentumParams(geriye_bakis=60, tutus=10, asgari_ciro=1e5)
    )
    assert "S19" not in d(evren, _seri(BAR, 99, 0.0002))


def test_payload_olcume_gereken_alanlari_tasir() -> None:
    """K4 `tutus`'u ufuk olarak okur; taşımazsa ölçüm kendi ufkunu uydurur."""
    sonuc = KesitselMomentum(KesitselMomentumParams(geriye_bakis=60, tutus=10))(
        _evren(), _seri(BAR, 99, 0.0002)
    )
    s = next(iter(sonuc.values())).signals[0]
    assert set(s.payload) >= {"tutus", "momentum_getiri", "yuzdelik", "evren", "giris"}
    assert s.payload["tutus"] == 10


# ----------------------------------------------------------- parametreler


def test_atlama_geriye_bakistan_kucuk_olmali() -> None:
    with pytest.raises(ValueError, match="ölçülecek pencere kalmaz"):
        KesitselMomentumParams(geriye_bakis=21, atlama_gun=21)


def test_ust_dilim_orandir() -> None:
    with pytest.raises(ValueError, match="üst dilim"):
        KesitselMomentumParams(ust_dilim=1.5)


def test_bos_evren_cokmez(dedektor: KesitselMomentum) -> None:
    assert dedektor.compute_universe({}, _seri(BAR, 1, 0.0)) == {}
