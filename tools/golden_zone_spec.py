"""Gerçek veriden Golden Zone ChartSpec üretir — K5'in girdisi.

    python tools/golden_zone_spec.py --sembol THYAO
    python tools/golden_zone_spec.py --sembol THYAO --sinyal -2   # sondan ikinci

Çıktı: `apps/web/ornek/<sembol>-golden-zone.chartspec.json`

**Neden ayrı bir araç.** `packages/chart` göstergeleri tanımaz,
`packages/teknik` çizim bilmez — katman ayrımı (README madde 2). İkisini
birbirine bağlamak bir ARACIN işidir, kütüphanenin değil. Burada olan tek
şey `IndicatorResult` → `OTESonucu` çevirisi.

**Fikstür değil, gerçek veri.** K5 "gerçek veriyle ekran görüntüsü alınır"
der. Elle uydurulmuş bir fikstür, dedektörün gerçekte ne ürettiğini
gizleyebilir — ki Faz 4'te tam olarak bu oldu: komposer güzel bir formasyon
çiziyordu ama adı yanlıştı ve kimse gerçek çıktıya bakmamıştı.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))
sys.path.insert(0, str(KOK / "packages" / "chart"))

import pandas as pd  # noqa: E402
from quaxis.chart.komposer.golden_zone import bestele  # noqa: E402
from quaxis.chart.roller import Yon  # noqa: E402
from quaxis.chart.tipler import Bar, Capa, FibSeviyesi, OTESonucu  # noqa: E402
from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.data.providers.yfinance_provider import YFinanceProvider  # noqa: E402
from quaxis.teknik.data.store import Store  # noqa: E402
from quaxis.teknik.indicators.golden_zone import GoldenZone, GoldenZoneParams  # noqa: E402
from quaxis.teknik.olcum.bariyer import barrier_outcome  # noqa: E402

#: K4'ün çıktısı. Grafiğin künyesine AYNEN geçer — "kurulum oluştu" ile
#: "kenar kanıtlandı" birbirine karışmasın.
VERDIKT = "kanıtlanmadı"


def _epoch(t: pd.Timestamp) -> int:
    return int(t.timestamp())


def _capa(df: pd.DataFrame, fiyat: float, t: pd.Timestamp, onay_t: pd.Timestamp, ad: str) -> Capa:
    return Capa(t=_epoch(t), fiyat=float(fiyat), onay_t=_epoch(onay_t), etiket=ad)


def sonuca_cevir(
    df: pd.DataFrame, sembol: str, ad: str, tf: str, sinyal, p: GoldenZoneParams, pencere: int
) -> OTESonucu:
    """`Signal` + OHLCV → `OTESonucu`. Komposer bunu bekler."""
    yuk = sinyal.payload
    capa100, capa0 = float(yuk["capa100"]), float(yuk["capa0"])
    bos_t = pd.Timestamp(yuk["bos_bar"])

    # Çıpaların KENDİ barları: bacak içinde uç değerin görüldüğü barlar.
    bacak = df.loc[:sinyal.detected_at]
    ekstrem = bacak[bacak["low"] == capa100] if yuk["capa0"] > yuk["capa100"] else bacak[
        bacak["high"] == capa100
    ]
    t100 = ekstrem.index[-1] if len(ekstrem) else bos_t
    zirve = bacak[bacak["high"] == capa0] if yuk["capa0"] > yuk["capa100"] else bacak[
        bacak["low"] == capa0
    ]
    t0 = zirve.index[-1] if len(zirve) else sinyal.bar_time

    boy = abs(capa0 - capa100)
    isaret = 1.0 if str(sinyal.direction) in ("long", "al") else -1.0
    seviyeler = [
        FibSeviyesi(oran=0.0, fiyat=capa0, ad="hedef"),
        FibSeviyesi(oran=p.bolge_sig, fiyat=capa0 - boy * p.bolge_sig * isaret, ad="giriş"),
        FibSeviyesi(
            oran=p.tatli_nokta, fiyat=capa0 - boy * p.tatli_nokta * isaret, ad="tatlı nokta"
        ),
        FibSeviyesi(oran=p.bolge_derin, fiyat=capa0 - boy * p.bolge_derin * isaret, ad=""),
        FibSeviyesi(oran=1.0, fiyat=float(yuk["stop"]), ad="stop"),
    ]

    # Kurulum ne oldu? K4'ün kullandığı AYNI bariyer mantığı — grafik ile
    # ölçüm farklı şeyler söylerse ikisi de güvenilmez olur.
    cikis = barrier_outcome(
        df, sinyal.detected_at, stop=float(yuk["stop"]), target=float(yuk["hedef"]),
        direction=sinyal.direction, max_bars=int(yuk["zaman_bariyeri"]),
        entry=float(yuk["giris"]),
    )

    # Levha: sinyalin etrafında `pencere` bar. Tüm seriyi çizmek kurulumu
    # görünmez bir noktaya indirirdi.
    i = df.index.get_loc(sinyal.detected_at)
    bas = max(0, min(i, df.index.get_loc(t100)) - 12)
    # Çıkış barından sonra biraz nefes payı: kurulumun sonucu kenara
    # yapışmasın.
    cikis_i = df.index.get_loc(cikis.exit_t) if cikis is not None else i
    son = min(len(df), max(i + pencere, cikis_i + 8))
    kesit = df.iloc[bas:son]

    barlar = [
        Bar(
            t=_epoch(t), acilis=float(r.open), yuksek=float(r.high),
            dusuk=float(r.low), kapanis=float(r.close), hacim=float(r.volume),
        )
        for t, r in kesit.iterrows()
    ]

    supurme = None
    if yuk.get("supurme") and yuk.get("supurme_bar"):
        st = pd.Timestamp(yuk["supurme_bar"])
        supurme = _capa(df, float(yuk["supurme_fiyat"]), st, st, "süpürme")

    return OTESonucu(
        sembol=sembol,
        ad=ad,
        zaman_dilimi=tf,
        barlar=barlar,
        capa100=_capa(df, capa100, t100, t100, "%100"),
        capa0=_capa(df, capa0, t0, t0, "%0"),
        bos_t=_epoch(bos_t),
        kirilan_seviye=float(yuk["kirilan_seviye"]),
        seviyeler=seviyeler,
        bolge=(p.bolge_sig, p.bolge_derin),
        giris_t=_epoch(sinyal.detected_at),
        giris_fiyat=float(yuk["giris"]),
        yon=Yon.AL if isaret > 0 else Yon.SAT,
        durum="bolgede",
        verdikt=VERDIKT,
        teyitler={
            "fvg": bool(yuk.get("fvg")),
            "order_block": yuk.get("order_block") is not None,
            "supurme": bool(yuk.get("supurme")),
        },
        supurme=supurme,
        cikis_t=_epoch(cikis.exit_t) if cikis is not None else None,
        cikis_fiyat=(
            float(yuk["hedef"]) if cikis is not None and cikis.outcome == "hedef"
            else float(yuk["stop"]) if cikis is not None and cikis.outcome == "stop"
            else float(df["close"].loc[cikis.exit_t]) if cikis is not None
            else None
        ),
        cikis_turu=cikis.outcome if cikis is not None else "",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Gerçek veriden Golden Zone ChartSpec")
    ap.add_argument("--sembol", default="THYAO")
    ap.add_argument("--ad", default=None, help="tam ad; verilmezse sembolün kendisi")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--sinyal", type=int, default=-1, help="kaçıncı sinyal (-1 = sonuncu)")
    ap.add_argument("--pencere", type=int, default=45, help="sinyalden sonra kaç bar")
    a = ap.parse_args()

    market, tf = Market(a.market), Timeframe(a.zaman_dilimi)
    df = Store(YFinanceProvider()).get(a.sembol, tf, market)
    df.attrs["symbol"], df.attrs["timeframe"] = a.sembol, tf

    p = GoldenZoneParams()
    sonuc = GoldenZone(p)(df)
    if not sonuc.signals:
        print(f"{a.sembol}: hiç sinyal yok. Başka sembol dene.")
        return 1

    sinyal = sonuc.signals[a.sinyal]
    spec = bestele(
        sonuca_cevir(df, a.sembol, a.ad or a.sembol, tf.value, sinyal, p, a.pencere),
        ornek_mi=False,
    )

    hedef = KOK / "apps" / "web" / "ornek" / f"{a.sembol.lower()}-golden-zone.chartspec.json"
    hedef.write_text(spec.json(), encoding="utf-8")
    print(
        f"{a.sembol} · {sinyal.detected_at.date()} · {sinyal.direction} · "
        f"giriş {sinyal.payload['giris']:.2f} stop {sinyal.payload['stop']:.2f} "
        f"hedef {sinyal.payload['hedef']:.2f}"
    )
    print(f"teyitler: fvg={sinyal.payload['fvg']} ob={sinyal.payload['order_block']} "
          f"süpürme={sinyal.payload['supurme']}")
    if spec.katmanlar:
        bant = next((k for k in spec.katmanlar if k.tur == "bant"), None)
        if bant is not None and bant.bitis:
            print(f"çıkış: {pd.Timestamp(bant.bitis, unit='s').date()}")
    print(f"{hedef.relative_to(KOK)} yazıldı ({hedef.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
