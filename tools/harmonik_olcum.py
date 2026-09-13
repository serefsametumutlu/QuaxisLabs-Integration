"""Harmonik K4 — üç bariyerli R ölçümü, sembol-kümelenmiş, BH-FDR ile.

    python tools/harmonik_olcum.py --zaman-dilimi 1D

## Aile burada tanımlanır

Beş test: dört formasyon + AB=CD'nin ikinci stop varyantı. Aile
**önceden** sabitlendi (K3 karar kuralı §5) ve sonuca bakıp
genişletilmeyecek. BH-FDR bu beşine uygulanır.

AB=CD'nin iki stop varyantı olmasının sebebi kitap: AB=CD için stop
formülü **vermiyor**. Hangi mesafenin doğru olduğu bir getiri sorusu
olduğu için K3'te kapatılamadı; iki seçenek de ölçülüp aileye dahil
ediliyor. "İkisini dene, iyi olanı raporla" tuzağına düşmemenin yolu
ikisini de aynı düzeltmeye sokmaktır.

## Neden hem IS hem OOS yazılıyor

`measure_r`'ın uyarısı şu: bir koşulu IS'te ARAYIP yine IS'te doğrulamak
cevabı bildiğin sınava girmektir. Burada **getiride hiçbir arama
yapılmadı** — eşikler kalibrasyondan (sinyal sayısı, oran dağılımı)
geldi, R'ye bakılmadı. Bu yüzden IS ayrı bir pencere olarak meşru ve
tutarlılık kontrolü sağlıyor. Yine de **birincil sayı OOS'unkidir**;
ikisi ayrışırsa bu bir bulgudur, seçim hakkı değil.
"""

from __future__ import annotations

import argparse
import collections
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

#: Aile ÖNCEDEN sabit. Sonuca bakıp üye eklenmeyecek.
AILE: dict[str, tuple[type, object]] = {
    "abcd_stop1272": (Abcd, AbcdParams(stop_orani=1.272)),
    "abcd_stop1618": (Abcd, AbcdParams(stop_orani=1.618)),
    "gartley": (Gartley, GartleyParams()),
    "kelebek": (Kelebek, KelebekParams()),
    "uc_surus": (UcSurus, UcSurusParams()),
}


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
    sinif: type, params: object, evren: dict[str, pd.DataFrame], *, yon: str
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
    islem_sayisi: dict[str, int] = {}
    for ad, (sinif, params) in AILE.items():
        islemler, atilan = _islemler(sinif, params, evren, yon=a.yon)
        islem_sayisi[ad] = sum(len(v) for v in islemler.values())
        print(f"  {ad:16s} {islem_sayisi[ad]:6d} işlem "
              f"({len(islemler)} sembol, {atilan} atıldı)", flush=True)
        ufuk = int(getattr(params, "zaman_bariyeri", 40))
        for pencere in ("oos", "is"):
            sonuc[ad][pencere] = measure_r(
                evren,
                islemler,
                max_bars=ufuk,
                pencere=pencere,
                komisyon=VARSAYILAN_KOMISYON * a.maliyet_kati,
                kayma=VARSAYILAN_KAYMA * a.maliyet_kati,
            )

    p_oos = {ad: sonuc[ad]["oos"].p_value for ad in AILE}
    fdr = bh_fdr(p_oos, q=0.05)

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

    for pencere, baslik in (("oos", "OOS — birincil"), ("is", "IS — tutarlılık")):
        y(f"## {baslik}")
        y("")
        y("| formasyon | işlem | sembol | isabet | beklenen R | adil baz | fark | PF | p |")
        y("|---|---|---|---|---|---|---|---|---|")
        for ad in AILE:
            y(_satir(ad, sonuc[ad][pencere]))
        y("")

    y("## BH-FDR (q = 0.05) — OOS penceresi")
    y("")
    y("| formasyon | p | FDR eşiğini geçti mi |")
    y("|---|---|---|")
    for ad in sorted(AILE, key=lambda k: p_oos[k]):
        y(f"| `{ad}` | {p_oos[ad]:.4f} | {'**✔ geçti**' if fdr[ad] else '✘'} |")
    y("")

    y("## Çıkış kırılımı")
    y("")
    y("| formasyon | hedef | stop | zaman | ort. kazanç | ort. kayıp |")
    y("|---|---|---|---|---|---|")
    for ad in AILE:
        r = sonuc[ad]["oos"]
        y(f"| `{ad}` | %{r.target_rate * 100:.0f} | %{r.stop_rate * 100:.0f} | "
          f"%{r.time_rate * 100:.0f} | {r.ortalama_kazanc:+.2f}R | "
          f"{r.ortalama_kayip:+.2f}R |")
    y("")

    y("## Örneklem yeterli mi")
    y("")
    y("Pardo s.295: 30–50 işlem asgari kabul edilir. **Sembol sayısı 30'un "
      "altındaki satırın sayısı yazılır, verdikti yazılmaz.**")
    y("")
    y("| formasyon | OOS sembol | yeterli mi |")
    y("|---|---|---|")
    for ad in AILE:
        n = sonuc[ad]["oos"].n_symbols
        y(f"| `{ad}` | {n} | {'✔' if n >= 30 else '✘ verdikt yazılmaz'} |")
    y("")

    hedef = KOK / "docs" / "olcum" / f"harmonik-pesavento-K4-{tf}-{a.yon}.md"
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
