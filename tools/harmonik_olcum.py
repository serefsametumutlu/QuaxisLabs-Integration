"""Harmonik K4 — üç bariyerli R ölçümü, sembol-kümelenmiş, BH-FDR ile.

    python tools/harmonik_olcum.py --zaman-dilimi 1D

## Aile burada tanımlanır

**Sekiz test:** dört formasyon × iki giriş varyantı. Aile
`docs/olcum/onkayit-harmonik-teyit.md` §5'te **sonuç görülmeden**
sabitlendi ve genişletilmeyecek. BH-FDR sekizine birden uygulanır.

| varyant | giriş |
|---|---|
| `kor` | fiyat D'ye dokunduğu anda, limit dolum |
| `teyit` | KURAL-30: bir sonraki bar işlem yönünde kapanırsa o kapanışta |

`kor` varyantında `giris_bari_riskli=True`: limit dolum barın İÇİNDE
gerçekleşir ve barın kalanı canlıdır. Tanı koşusu sinyallerin %14–28'inin
giriş barında zaten stop olduğunu ve ölçümün bunu saymadığını buldu. Bu
hata harmonikleri KAYIRIYORDU; düzeltilmesi sonucu kötüleştirecek.

`teyit` varyantında giriş bar KAPANIŞIDIR, dolayısıyla bayrak gereksiz —
bar zaten bitmiştir.

## Pencere

Birincil pencere **tüm dönem**. Gerekçe ön kayıt §4: IS/OOS ayrımı
eşiklerin GETİRİYE bakarak seçilmesine karşı bir korumadır; bizim
eşiklerimiz K3'te yalnız aday sayısından türetildi ve o koşuda ölçüm
aracı hiç çağrılmadı. Ayırmanın koruduğu bir şey yok, tek etkisi
örneklemi %70 küçültmek — ve o küçülme Gartley'i 27 sembole düşürüp
verdikt yazılamaz hâle getirmişti.

IS ve OOS ayrıca raporlanır; tutarsızlık bir BULGUDUR, seçim hakkı değil.
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import datetime as dt
import pathlib
import sys

import pandas as pd

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "packages" / "teknik")]
sys.stdout.reconfigure(encoding="utf-8")

from quaxis.teknik.core.types import Signal, Timeframe  # noqa: E402
from quaxis.teknik.indicators.harmonik import (  # noqa: E402
    Abcd,
    AbcdParams,
    Gartley,
    GartleyParams,
    Kelebek,
    KelebekParams,
    UcSurus,
    UcSurusParams,
)
from quaxis.teknik.olcum.bariyer import (  # noqa: E402
    VARSAYILAN_KAYMA,
    VARSAYILAN_KOMISYON,
    RResult,
    measure_r,
)
from quaxis.teknik.olcum.ileri_getiri import bh_fdr  # noqa: E402

#: Formasyonlar. Aile bunların **iki varyantı** — bkz. `AILE`.
FORMASYON: dict[str, tuple[type, object]] = {
    "abcd": (Abcd, AbcdParams()),
    "gartley": (Gartley, GartleyParams()),
    "kelebek": (Kelebek, KelebekParams()),
    "uc_surus": (UcSurus, UcSurusParams()),
}

#: Aile ÖNCEDEN sabit (`docs/olcum/onkayit-harmonik-teyit.md` §5):
#: 4 formasyon × 2 varyant = **8 test**. Sonuca bakıp üye eklenmeyecek.
AILE: list[tuple[str, str]] = [
    (ad, varyant) for ad in FORMASYON for varyant in ("kor", "teyit")
]


def teyitli(
    df: pd.DataFrame, s: Signal
) -> tuple[Signal, float, float] | None:
    """KURAL-30 — bir bar bekleme tekniği. Sıfır serbest parametre.

    D'ye dokunulan bar **sinyaldir ama giriş değildir**. Bir sonraki barın
    kapanışı beklenir; o bar **işlem yönünde kapanırsa** (boğada
    `close > open`) o kapanıştan girilir, kapanmazsa işlem **hiç açılmaz**.

    Bedava değil ve bunu ön kayıt §8'de baştan kabul ettik: teyit barı
    yukarı kapandığı için boğada D'den DAHA YÜKSEK bir fiyattan girilir.
    Stop aynı yerde kaldığı için risk büyür, ödül/risk düşer. Teyidin
    isabeti bu kaybı telafi edecek kadar artırması gerekiyor.
    """
    i = df.index.get_loc(s.detected_at)
    if not isinstance(i, int) or i + 1 >= len(df):
        return None
    j = i + 1
    acilis = float(df["open"].iloc[j])
    kapanis = float(df["close"].iloc[j])
    uzun = s.direction == "long"
    if (kapanis <= acilis) if uzun else (kapanis >= acilis):
        return None  # teyit gelmedi → işlem açılmaz
    stop, hedef = float(s.payload["stop"]), float(s.payload["hedef"])
    # Teyit barı stop'un ötesinde kapandıysa işlem zaten ölü doğar.
    if (kapanis <= stop) if uzun else (kapanis >= stop):
        return None
    yeni = dataclasses.replace(
        s,
        detected_at=df.index[j],
        payload={**s.payload, "giris": kapanis, "teyit": True},
    )
    return yeni, stop, hedef


def _evren(tf: str) -> dict[str, pd.DataFrame]:
    kok = KOK / "data" / "ohlcv" / "bist"
    out: dict[str, pd.DataFrame] = {}
    for p in sorted(kok.iterdir()):
        f = p / f"{tf}.parquet"
        if not f.exists():
            continue
        df = pd.read_parquet(f)
        if len(df) < 300:
            continue
        df.attrs["timeframe"] = Timeframe(tf)
        df.attrs["symbol"] = p.name
        out[p.name] = df
    return out


def _islemler(
    sinif: type,
    params: object,
    evren: dict[str, pd.DataFrame],
    *,
    yon: str,
    varyant: str,
) -> tuple[dict[str, list[tuple[Signal, float, float]]], int]:
    """Sinyalleri (sinyal, stop, hedef) üçlülerine çevirir.

    Stop ve hedef STRATEJİNİN kendi kuralından gelir; ölçüm onları
    uydurmaz. `yon="long"` yalnız alış tarafını sayar — BIST'te açığa
    satış kısıtlı olduğu için uygulanabilir olan budur.
    """
    ded = sinif(params)
    islemler: dict[str, list[tuple[Signal, float, float]]] = {}
    atilan = 0
    for sembol, df in evren.items():
        kayit: list[tuple[Signal, float, float]] = []
        for s in ded(df).signals:
            if yon != "hepsi" and s.direction != yon:
                continue
            if varyant == "teyit":
                ucdu = teyitli(df, s)
                if ucdu is None:
                    atilan += 1
                    continue
                kayit.append(ucdu)
                continue
            stop, hedef = s.payload["stop"], s.payload["hedef"]
            giris = s.payload["giris"]
            # Sıfır riskli işlem ölçüme giremez: R tanımsızlaşır ve baz
            # saçmalaşır (Golden Zone'da +48R'lik bazlar böyle doğmuştu).
            if abs(giris - stop) <= 0:
                atilan += 1
                continue
            kayit.append((s, float(stop), float(hedef)))
        if kayit:
            islemler[sembol] = kayit
    return islemler, atilan


def _satir(ad: str, r: RResult) -> str:
    pf = r.profit_factor
    pf_s = "∞" if pf == float("inf") else f"{pf:.2f}"
    return (
        f"| `{ad}` | {r.n_trades} | {r.n_symbols} | %{r.win_rate * 100:.1f} | "
        f"**{r.mean_r:+.3f}R** | {r.baseline_mean_r:+.3f}R | "
        f"{r.mean_r - r.baseline_mean_r:+.3f}R | {pf_s} | {r.p_value:.4f} |"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--yon", default="long", choices=["long", "short", "hepsi"])
    ap.add_argument("--maliyet-kati", type=float, default=1.0)
    a = ap.parse_args()
    tf = a.zaman_dilimi

    print(f"evren yükleniyor · {tf}", flush=True)
    evren = _evren(tf)
    print(f"{len(evren)} sembol", flush=True)

    sonuc: dict[str, dict[str, RResult]] = collections.defaultdict(dict)
    kunye: list[str] = []
    for formasyon, varyant in AILE:
        sinif, params = FORMASYON[formasyon]
        ad = f"{formasyon}·{varyant}"
        kunye.append(ad)
        islemler, atilan = _islemler(
            sinif, params, evren, yon=a.yon, varyant=varyant
        )
        n = sum(len(v) for v in islemler.values())
        print(f"  {ad:18s} {n:6d} işlem "
              f"({len(islemler)} sembol, {atilan} atıldı)", flush=True)
        ufuk = int(getattr(params, "zaman_bariyeri", 40))
        for pencere in ("hepsi", "oos", "is"):
            sonuc[ad][pencere] = measure_r(
                evren,
                islemler,
                max_bars=ufuk,
                pencere=pencere,
                komisyon=VARSAYILAN_KOMISYON * a.maliyet_kati,
                kayma=VARSAYILAN_KAYMA * a.maliyet_kati,
                # Limit dolumda giriş barının kalanı canlı; teyitli girişte
                # giriş zaten bar KAPANIŞI olduğu için gereksiz.
                giris_bari_riskli=(varyant == "kor"),
            )

    p_ana = {ad: sonuc[ad]["hepsi"].p_value for ad in kunye}
    fdr = bh_fdr(p_ana, q=0.05)

    satir: list[str] = []
    y = satir.append
    y(f"# Harmonik (Pesavento) — K4 İstatistik · {tf}")
    y("")
    y(f"**Tarih:** {dt.date.today().isoformat()} · **Evren:** {len(evren)} "
      f"BIST sembolü · **Yön:** {a.yon}")
    y("")
    y("Ölçüt: **üç bariyerli R** (stop / hedef / zaman). Stop ve hedef "
      "stratejinin kendi kuralından geliyor. İşlem maliyeti dahil "
      f"(taraf başına %{VARSAYILAN_KOMISYON * a.maliyet_kati * 100:.3f} komisyon "
      f"+ %{VARSAYILAN_KAYMA * a.maliyet_kati * 100:.3f} kayma). **Aynı barda "
      "stop ve hedef birlikte vurulduysa STOP sayılır.**")
    y("")
    y("Bağımsız gözlem **sembol**, bar değil. Adil baz: aynı risk yapısıyla "
      "rastgele bar/sembol. Aile beş üyeli ve **önceden sabitlendi** — "
      "BH-FDR (q=0.05) beşine birden uygulandı.")
    y("")

    for pencere, baslik in (
        ("hepsi", "Tüm dönem — BİRİNCİL"),
        ("oos", "OOS — ikincil"),
        ("is", "IS — ikincil"),
    ):
        y(f"## {baslik}")
        y("")
        y("| künye | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |")
        y("|---|---|---|---|---|---|---|---|---|")
        for ad in kunye:
            y(_satir(ad, sonuc[ad][pencere]))
        y("")

    y("## BH-FDR (q = 0.05) — tüm dönem, 8 test")
    y("")
    y("| künye | p | FDR eşiğini geçti mi |")
    y("|---|---|---|")
    for ad in sorted(kunye, key=lambda k: p_ana[k]):
        y(f"| `{ad}` | {p_ana[ad]:.4f} | {'**✔ geçti**' if fdr[ad] else '✘'} |")
    y("")

    y("## Teyit katkı yaptı mı (ön kayıt §6, madde 4)")
    y("")
    y("Teyitli varyantın körlemesineden **daha iyi** olması gerekiyor; "
      "yoksa teyit 'işe yaradı' denemez.")
    y("")
    y("| formasyon | körlemesine fark | teyitli fark | teyidin katkısı |")
    y("|---|---|---|---|")
    for formasyon in FORMASYON:
        k = sonuc[f"{formasyon}·kor"]["hepsi"]
        t = sonuc[f"{formasyon}·teyit"]["hepsi"]
        kf = k.mean_r - k.baseline_mean_r
        tf_ = t.mean_r - t.baseline_mean_r
        y(f"| `{formasyon}` | {kf:+.3f}R | {tf_:+.3f}R | "
          f"**{tf_ - kf:+.3f}R** |")
    y("")

    y("## Çıkış kırılımı")
    y("")
    y("| formasyon | hedef | stop | zaman | ort. kazanç | ort. kayıp |")
    y("|---|---|---|---|---|---|")
    for ad in kunye:
        r = sonuc[ad]["hepsi"]
        y(f"| `{ad}` | %{r.target_rate * 100:.0f} | %{r.stop_rate * 100:.0f} | "
          f"%{r.time_rate * 100:.0f} | {r.ortalama_kazanc:+.2f}R | "
          f"{r.ortalama_kayip:+.2f}R |")
    y("")

    y("## Örneklem yeterli mi")
    y("")
    y("Pardo s.295: 30–50 işlem asgari kabul edilir. **Sembol sayısı 30'un "
      "altındaki satırın sayısı yazılır, verdikti yazılmaz.**")
    y("")
    y("| künye | sembol | yeterli mi |")
    y("|---|---|---|")
    for ad in kunye:
        n = sonuc[ad]["hepsi"].n_symbols
        y(f"| `{ad}` | {n} | {'✔' if n >= 30 else '✘ verdikt yazılmaz'} |")
    y("")

    hedef = KOK / "docs" / "olcum" / f"harmonik-pesavento-K4b-teyit-{tf}-{a.yon}.md"
    if a.maliyet_kati != 1.0:
        hedef = hedef.with_name(hedef.stem + f"-maliyet{a.maliyet_kati:g}x.md")
    hedef.write_text("\n".join(satir) + "\n", encoding="utf-8")
    print(f"\nyazıldı: {hedef.relative_to(KOK)}")
    for s in satir:
        if s.startswith("| `") or s.startswith("## "):
            print(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
