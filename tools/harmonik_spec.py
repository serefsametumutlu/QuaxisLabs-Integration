"""Gerçek veriden harmonik ChartSpec üretir — K5'in girdisi.

    python tools/harmonik_spec.py --formasyon gartley --sembol THYAO
    python tools/harmonik_spec.py --formasyon abcd --en-iyi   # evrende ara

Çıktı: `apps/web/ornek/<sembol>-<formasyon>.chartspec.json`

**Neden ayrı bir araç.** `packages/chart` göstergeleri tanımaz,
`packages/teknik` çizim bilmez — katman ayrımı (README madde 2). İkisini
birbirine bağlamak bir ARACIN işidir. Burada olan tek şey
`IndicatorResult` → `HarmonikSonucu` çevirisi.

**Fikstür değil, gerçek veri.** K5 "gerçek veriyle ekran görüntüsü alınır"
der. Elle uydurulmuş bir fikstür dedektörün gerçekte ne ürettiğini
gizleyebilir — Faz 4'te tam olarak bu oldu.

**`--en-iyi` neyi seçer.** En kârlı sinyali DEĞİL: en okunaklı olanı
(bacakları dengeli, formasyonu levhaya sığan). Grafik bir reklam değil,
kuralın görünür hâli; hedefe ulaşmış örnek seçmek verdikti gizlemenin
görsel hâli olurdu. Seçim ölçütü açıkça `_okunakliluk` fonksiyonunda.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))
sys.path.insert(0, str(KOK / "packages" / "chart"))
sys.stdout.reconfigure(encoding="utf-8")

import pandas as pd  # noqa: E402
from quaxis.chart.komposer.harmonik import bestele  # noqa: E402
from quaxis.chart.roller import Yon  # noqa: E402
from quaxis.chart.tipler import Bar, Capa, FibSeviyesi, HarmonikSonucu  # noqa: E402
from quaxis.teknik.core.types import Timeframe  # noqa: E402
from quaxis.teknik.indicators.harmonik import (  # noqa: E402
    Abcd,
    Gartley,
    Kelebek,
    UcSurus,
)
from quaxis.teknik.olcum.bariyer import barrier_outcome  # noqa: E402

#: K4'ün çıktısı. Grafiğin künyesine AYNEN geçer.
VERDIKT = "kanıtlanmadı"

#: Vitrin örnekleri bu tarihten SONRA başlamalı.
#:
#: **Ölçülmüş veri kusuru.** Kaynak (yfinance) BIST için 2014 öncesinde
#: gerçek açılış fiyatı vermiyor; `open` alanını `close` ile dolduruyor.
#: THYAO'da `açılış == kapanış` oranı 2011'de %99, 2012'de %99, 2013'te
#: %66 — 2015 sonrasında %2-5. Gövdesi olmayan mum çizgi gibi görünür:
#: Three Drives örneği (BURVA 2011) seçilince levhada 106 barın 106'sı
#: doji çıkıyor ve grafik mum grafiği gibi durmuyordu.
#:
#: Vitrin örneğinin bu dönemden seçilmesi yalnız çirkin değil YANILTICI:
#: kullanıcı "bizim çizicimiz bozuk" sanır. Sınır burada, çünkü
#: düzeltilecek yer VERİ KAYNAĞI, çizici değil.
EN_ERKEN = "2014-01-01"

DEDEKTOR = {
    "abcd": Abcd,
    "gartley": Gartley,
    "kelebek": Kelebek,
    "uc_surus": UcSurus,
}

#: D seviyesinin hangi fibo oranı olduğu — formasyona göre değişir.
D_ORANI = {
    "harmonik_abcd": "cd",
    "harmonik_gartley": "d",
    "harmonik_kelebek": "d",
    "harmonik_uc_surus": "s3_uzanti",
}

#: Stop seviyesinin fibo oranı. AB=CD'de bir sonraki uzantı, Gartley'de
#: X'in kendisi (%100), diğerlerinde 1.618.
STOP_ORANI = {
    "harmonik_abcd": 1.272,
    "harmonik_gartley": 1.0,
    "harmonik_kelebek": 1.618,
    "harmonik_uc_surus": 1.618,
}


def _epoch(t: pd.Timestamp) -> int:
    return int(t.timestamp())


def _okunaklilik(df: pd.DataFrame, s) -> float:  # noqa: ANN001
    """Küçük daha iyi. Ölçüt: formasyonun bar genişliği ile fiyat
    genişliğinin dengesi.

    Çok uzun bir formasyon levhada yassılaşır, çok kısa olan mumların
    arasında kaybolur. **Getiriye bakılmıyor** — bakılsaydı seçilen örnek
    verdikti yalanlardı.
    """
    noktalar = s.payload["noktalar"]
    barlar = [df.index.get_loc(pd.Timestamp(n["bar"])) for n in noktalar.values()]
    genislik = max(barlar) - min(barlar)
    fiyatlar = [n["fiyat"] for n in noktalar.values()]
    yukseklik = (max(fiyatlar) - min(fiyatlar)) / max(fiyatlar)
    # 40-90 bar arası ve %20-60 fiyat aralığı "okunaklı" sayılır.
    return abs(genislik - 65) / 65 + abs(yukseklik - 0.40) / 0.40


def sonuca_cevir(
    df: pd.DataFrame, sembol: str, ad: str, tf: str, s, pencere: int
) -> HarmonikSonucu:
    """`Signal` + OHLCV → `HarmonikSonucu`."""
    yuk = s.payload
    formasyon = yuk["formasyon"]
    giris, stop, hedef = yuk["giris"], yuk["stop"], yuk["hedef"]

    noktalar = [
        Capa(
            t=_epoch(pd.Timestamp(n["bar"])),
            fiyat=float(n["fiyat"]),
            # Pivot ONAY barında çizilir. Dedektör onay barını ayrıca
            # taşımadığı için sinyalin `onay_bar`ı değil, pivotun kendi
            # barı kullanılıyor: formasyonun geometrisi mumlara OTURMAK
            # zorunda, yoksa çizilen şey fiyatın gerçekte gittiği yer
            # olmaz. (K5 i1 bulgusu — gerekçe aşağıda.)
            onay_t=_epoch(pd.Timestamp(n["bar"])),
            etiket=etiket,
        )
        for etiket, n in yuk["noktalar"].items()
    ]
    d = Capa(
        t=_epoch(s.detected_at),
        fiyat=float(giris),
        onay_t=_epoch(s.detected_at),
        etiket="D",
    )

    oranlar = yuk["oranlar"]
    d_orani = float(oranlar.get(D_ORANI[formasyon], 1.0))
    seviyeler = [
        FibSeviyesi(oran=d_orani, fiyat=float(giris), ad="giriş"),
        FibSeviyesi(oran=STOP_ORANI[formasyon], fiyat=float(stop), ad="stop"),
        FibSeviyesi(oran=0.618, fiyat=float(hedef), ad="hedef"),
    ]

    # Kurulum ne oldu? K4'ün kullandığı AYNI bariyer mantığı — grafik ile
    # ölçüm farklı şeyler söylerse ikisi de güvenilmez olur.
    cikis = barrier_outcome(
        df, s.detected_at, stop=float(stop), target=float(hedef),
        direction=s.direction, max_bars=int(yuk["zaman_bariyeri"]),
        entry=float(giris), giris_bari_riskli=True,
    )

    # Levha KURULUMUN etrafına odaklanır. **K5 i1 bulgusu:** pencere
    # `i + pencere` ile de büyütülüyordu ve DOGUB örneğinde çıkıştan sonraki
    # ralli levhanın %45'ini yiyor, formasyon sol tarafa sıkışıyordu.
    # Kurulum sonuçlandıysa ölçü çıkıştır; birkaç bar nefes payı yeter.
    i = df.index.get_loc(s.detected_at)
    ilk_nokta = min(df.index.get_loc(pd.Timestamp(n["bar"])) for n in yuk["noktalar"].values())
    # Sol pay 8 bar değil 22: levhanın sol ÜST köşesinde HUD bloğu
    # (sembol · strateji · ödül/risk) duruyor ve o bir HTML katmanı —
    # SVG onu göremez. AB=CD örneğinde ilk köşe (A) tam HUD'ın altına
    # düşüyor ve rozeti görünmüyordu (K5 i12). 22 bar, HUD'ın genişliğini
    # tipik bar aralığında geçiyor.
    bas = max(0, ilk_nokta - 22)
    cikis_i = df.index.get_loc(cikis.exit_t) if cikis is not None else i
    son = min(len(df), (cikis_i + 10) if cikis is not None else i + pencere)
    kesit = df.iloc[bas:son]

    barlar = [
        Bar(
            t=_epoch(t), acilis=float(r.open), yuksek=float(r.high),
            dusuk=float(r.low), kapanis=float(r.close), hacim=float(r.volume),
        )
        for t, r in kesit.iterrows()
    ]

    durum = {"hedef": "tamamlandi", "stop": "gecersiz", "zaman": "izleniyor"}
    return HarmonikSonucu(
        sembol=sembol,
        ad=ad,
        zaman_dilimi=tf,
        barlar=barlar,
        formasyon=formasyon,
        noktalar=noktalar,
        d=d,
        seviyeler=seviyeler,
        yon=Yon.AL if s.direction == "long" else Yon.SAT,
        durum=durum.get(cikis.outcome, "izleniyor") if cikis else "izleniyor",
        verdikt=VERDIKT,
        oranlar={k: float(v) for k, v in oranlar.items()},
        cikis_t=_epoch(cikis.exit_t) if cikis else None,
        cikis_fiyat=float(
            stop if cikis and cikis.outcome == "stop"
            else hedef if cikis and cikis.outcome == "hedef"
            else df["close"].loc[cikis.exit_t] if cikis else 0.0
        ) if cikis else None,
        cikis_turu=cikis.outcome if cikis else "",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--formasyon", default="gartley", choices=sorted(DEDEKTOR))
    ap.add_argument("--sembol", default="")
    ap.add_argument("--en-iyi", action="store_true")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--pencere", type=int, default=30)
    ap.add_argument("--sinyal", type=int, default=-1)
    a = ap.parse_args()

    kok = KOK / "data" / "ohlcv" / "bist"
    ded = DEDEKTOR[a.formasyon]()
    semboller = (
        [a.sembol] if a.sembol
        else sorted(p.name for p in kok.iterdir() if (p / f"{a.zaman_dilimi}.parquet").exists())
    )

    en_iyi = None
    for sembol in semboller:
        yol = kok / sembol / f"{a.zaman_dilimi}.parquet"
        if not yol.exists():
            continue
        df = pd.read_parquet(yol)
        df.attrs["timeframe"] = Timeframe(a.zaman_dilimi)
        df.attrs["symbol"] = sembol
        sinyaller = [
            s
            for s in ded(df).signals
            if s.direction == "long" and s.detected_at >= pd.Timestamp(EN_ERKEN, tz="UTC")
        ]
        if not sinyaller:
            continue
        if not a.en_iyi:
            s = sinyaller[a.sinyal]
            en_iyi = (0.0, sembol, df, s)
            break
        for s in sinyaller:
            puan = _okunaklilik(df, s)
            if en_iyi is None or puan < en_iyi[0]:
                en_iyi = (puan, sembol, df, s)

    if en_iyi is None:
        print("sinyal bulunamadı", file=sys.stderr)
        return 1

    puan, sembol, df, s = en_iyi
    sonuc = sonuca_cevir(df, sembol, sembol, a.zaman_dilimi, s, a.pencere)
    spec = bestele(sonuc)

    hedef = KOK / "apps" / "web" / "ornek" / f"{sembol.lower()}-{a.formasyon}.chartspec.json"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(
        spec.json(), encoding="utf-8"
    )
    print(f"{sembol} · {s.detected_at.date()} · okunaklılık={puan:.3f}")
    print(f"  yön={s.direction} durum={sonuc.durum} çıkış={sonuc.cikis_turu}")
    print(f"  oranlar={ {k: round(v, 3) for k, v in sonuc.oranlar.items()} }")
    print(f"yazıldı: {hedef.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
