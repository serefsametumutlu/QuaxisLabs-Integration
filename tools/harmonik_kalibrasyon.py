"""Harmonik K3 kalibrasyonu — eşikleri ÖLÇÜMDEN türetir.

    python tools/harmonik_kalibrasyon.py --zaman-dilimi 1D

Karar kuralı sonuçlar görülmeden yazıldı ve commit edildi:
`docs/olcum/harmonik-pesavento-K3-karar-kurali.md`. Bu araç o kuralı
UYGULAR, yeniden yorumlamaz.

## Neden burada R hesaplanmıyor

Karar kuralı §1: eşik seçimi yalnız kalibrasyona (aday sayısı, dağılım
şekli) bakar. Getiriye bakarak eşik seçmek, K4'ün ölçeceği şeyi K3'te
seçmektir; o zaman K4 "kenar var mı" sorusunu değil "seçtiğim eşik kendi
seçildiği veride iyi görünüyor mu" sorusunu cevaplar.

Bu yüzden ölçüm aracı bu dosyadan **hiç çağrılmıyor** — bakma ihtimali
bile doğmasın diye.

## Neden süreç havuzu

Dokuz yapılandırma × dört formasyon × 545 sembol tek çekirdekte ~45 dakika.
Sembol başına parquet BİR KEZ okunur ve o sembolün bütün yapılandırmaları
aynı süreçte koşar — dosya okuma dokuz kez tekrarlanmaz.
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import datetime as dt
import multiprocessing as mp
import pathlib
import statistics
import sys

import pandas as pd

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "packages" / "teknik")]
sys.stdout.reconfigure(encoding="utf-8")  # Windows cp1254 '·' üstünde ölüyordu

from quaxis.teknik.core.types import Timeframe  # noqa: E402
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

FORMASYONLAR = {
    "abcd": (Abcd, AbcdParams),
    "gartley": (Gartley, GartleyParams),
    "kelebek": (Kelebek, KelebekParams),
    "uc_surus": (UcSurus, UcSurusParams),
}

TOLERANSLAR = (0.02, 0.03, 0.05, 0.08, 0.10)
PIVOTLAR = (2, 3, 4, 5)
TABAN_TOLERANS = 0.05
TABAN_PIVOT = 3
#: `olusum_bar` dağılımı ölçülürken pencere buna açılır. Varsayılan 40 ile
#: ölçmek, ölçülecek şeyi ölçmeden önce kırpmak olurdu.
GENIS_PENCERE = 400
NL = chr(10)

#: K3'ün iki taramasından çıkan seçimler. **Ayrı ayrı** seçildiler:
#: tolerans taraması pivot=3 ile, pivot taraması tolerans=0.05 ile koştu.
#: Yani aşağıdaki BİRLEŞİMLER hiç ölçülmedi — `--dogrula` onları ölçer.
#: Birleşim iki sınırı sağlamıyorsa karar kuralı §7 işler: o formasyon
#: K4'e girmez. "Tek tek geçmişti" gerekçesi kabul edilmez.
SECIM: dict[str, dict] = {
    "abcd": {"tolerans": 0.02, "pivot_sol": 5, "pivot_sag": 5},
    "gartley": {"tolerans": 0.02, "pivot_sol": 4, "pivot_sag": 4},
    "kelebek": {"tolerans": 0.02, "pivot_sol": 4, "pivot_sag": 4},
    "uc_surus": {"tolerans": 0.05, "pivot_sol": 4, "pivot_sag": 4},
}


def yapilandirmalar() -> list[tuple[str, dict]]:
    """(etiket, parametre sözlüğü) çiftleri. Taban iki taramada da geçtiği
    için TEK kez koşar — aynı sayıyı iki kez hesaplamak yanıltıcı bir
    'tutarlılık' hissi verirdi."""
    out: list[tuple[str, dict]] = []
    for t in TOLERANSLAR:
        out.append((f"tolerans={t:.2f}", {"tolerans": t}))
    for k in PIVOTLAR:
        if k == TABAN_PIVOT:
            continue  # taban zaten tolerans taramasında var
        out.append((f"pivot={k}", {"pivot_sol": k, "pivot_sag": k}))
    out.append(("genis_pencere", {"donus_max_bar": GENIS_PENCERE}))
    return out


@dataclasses.dataclass
class Sayim:
    sinyal: int = 0
    semboller: set[str] = dataclasses.field(default_factory=set)
    bar: int = 0


def _dogrula_kos(arg: tuple[str, str, str]) -> dict:
    """Seçilen BİRLEŞİMİ ölçer: sinyal sayısı + `olusum_bar` dağılımı.

    Pencere burada da 400'e açılır, çünkü `donus_max_bar` seçimi
    tolerans/pivot değişince kayar — eski dağılımdan okunan sayıyı yeni
    ayarlara taşımak, ölçülmemiş bir eşiği ölçülmüş gibi göstermek olurdu.
    """
    kok_s, sembol, tf = arg
    try:
        df = pd.read_parquet(pathlib.Path(kok_s) / sembol / f"{tf}.parquet")
    except Exception:
        return {}
    df.attrs["timeframe"] = Timeframe(tf)
    df.attrs["symbol"] = sembol
    cikti: dict = {"bar": len(df), "sayim": {}, "olusum": {}, "yon": {}}
    for ad, (sinif, ptip) in FORMASYONLAR.items():
        kw = dict(SECIM[ad], donus_max_bar=GENIS_PENCERE)
        try:
            s = sinif(ptip(**kw))(df).signals
        except Exception:
            continue
        cikti["sayim"]["secim", ad] = len(s)
        cikti["olusum"][ad] = [x.payload["olusum_bar"] for x in s]
        cikti["yon"][ad] = sum(1 for x in s if x.direction == "long")
    return cikti


def _sembol_kos(arg: tuple[str, str, str]) -> dict:
    """Tek sembol, bütün yapılandırmalar. Süreç sınırını yalnız SONUÇ geçer."""
    kok_s, sembol, tf = arg
    yol = pathlib.Path(kok_s) / sembol / f"{tf}.parquet"
    try:
        df = pd.read_parquet(yol)
    except Exception:
        return {}
    df.attrs["timeframe"] = Timeframe(tf)
    df.attrs["symbol"] = sembol
    n = len(df)
    cikti: dict = {"bar": n, "sayim": {}, "oran": collections.defaultdict(list),
                   "olusum": collections.defaultdict(list), "yon": {}}

    for etiket, degisiklik in yapilandirmalar():
        for ad, (sinif, ptip) in FORMASYONLAR.items():
            try:
                sonuc = sinif(ptip(**degisiklik))(df)
            except Exception:
                continue
            s = sonuc.signals
            cikti["sayim"][etiket, ad] = len(s)
            if etiket == "genis_pencere":
                cikti["olusum"][ad] = [x.payload["olusum_bar"] for x in s]
            if etiket == f"tolerans={TABAN_TOLERANS:.2f}":
                cikti["olusum"]["dar:" + ad] = [x.payload["olusum_bar"] for x in s]
                cikti["yon"][ad] = sum(1 for x in s if x.direction == "long")
                for x in s:
                    for oran_ad, deger in x.payload["oranlar"].items():
                        cikti["oran"][ad, oran_ad].append(deger)
    cikti["oran"] = dict(cikti["oran"])
    cikti["olusum"] = dict(cikti["olusum"])
    return cikti


def _dilim(veri: list[float], pct: float) -> float:
    if not veri:
        return float("nan")
    s = sorted(veri)
    return s[min(len(s) - 1, int(len(s) * pct))]


def _yillik(sinyal: int, bar: int, tf: str) -> float:
    """Sembol başına YILLIK sinyal. Ham sayı kıyaslanamaz: 17 yıllık bir
    sembolle 2 yıllık bir sembol aynı torbada."""
    bar_yil = {"1D": 252.0, "1W": 52.0, "4H": 756.0}.get(tf, 252.0)
    return sinyal / (bar / bar_yil) if bar else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--islemci", type=int, default=0)
    ap.add_argument(
        "--dogrula", action="store_true",
        help="Seçilen tolerans+pivot BİRLEŞİMİNİ ölç (taramalar ayrı koştu)",
    )
    a = ap.parse_args()
    tf = a.zaman_dilimi

    veri_kok = KOK / "data" / "ohlcv" / "bist"
    semboller = sorted(
        p.name for p in veri_kok.iterdir() if (p / f"{tf}.parquet").exists()
    )
    print(f"evren: {len(semboller)} sembol · {tf}", flush=True)

    isci = a.islemci or max(1, (mp.cpu_count() or 2) - 1)
    isler = [(str(veri_kok), s, tf) for s in semboller]
    with mp.Pool(isci) as havuz:
        sonuclar = havuz.map(
            _dogrula_kos if a.dogrula else _sembol_kos, isler, chunksize=4
        )

    toplam: dict[tuple[str, str], Sayim] = collections.defaultdict(Sayim)
    oranlar: dict[tuple[str, str], list[float]] = collections.defaultdict(list)
    olusum: dict[str, list[int]] = collections.defaultdict(list)
    yon: dict[str, int] = collections.defaultdict(int)
    toplam_bar = 0

    for s, cikti in zip(semboller, sonuclar, strict=True):
        if not cikti:
            continue
        toplam_bar += cikti["bar"]
        for anahtar, adet in cikti["sayim"].items():
            t = toplam[anahtar]
            t.sinyal += adet
            t.bar += cikti["bar"]
            if adet:
                t.semboller.add(s)
        for anahtar, v in cikti.get("oran", {}).items():
            oranlar[anahtar] += v
        for ad, v in cikti["olusum"].items():
            olusum[ad] += v
        for ad, v in cikti["yon"].items():
            yon[ad] += v

    if a.dogrula:
        _dogrula_rapor(tf, toplam, olusum, yon)
        return 0
    _rapor(tf, len(semboller), toplam_bar, toplam, oranlar, olusum, yon)
    return 0


def _dogrula_rapor(tf, toplam, olusum, yon) -> None:  # noqa: ANN001
    """Birleşimin iki sınırı sağlayıp sağlamadığını YAZAR."""
    satir = [
        "",
        "## 7 · Seçilen birleşimin doğrulaması",
        "",
        "İki tarama **ayrı ayrı** koştu (tolerans taraması pivot=3 ile, pivot "
        "taraması tolerans=0.05 ile). Seçilen birleşimler böylece hiç "
        "ölçülmemiş oluyordu. Burada ölçülüyorlar; iki sınırı sağlamayan "
        "formasyon karar kuralı §7 gereği **K4'e girmez**.",
        "",
        "| formasyon | tolerans | pivot | sinyal | sembol | /sembol/yıl | "
        "≥100 | ≤3/yıl | **donus_max_bar** |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for ad in FORMASYONLAR:
        s = toplam["secim", ad]
        yil = _yillik(s.sinyal, s.bar, tf) if s.bar else 0.0
        a_ok = len(s.semboller) >= 100
        b_ok = yil <= 3.0
        v = olusum.get(ad, [])
        pencere = max(5, int(round(_dilim(v, 0.90) / 5.0) * 5)) if v else "—"
        satir.append(
            f"| `{ad}` | {SECIM[ad]['tolerans']:.2f} | {SECIM[ad]['pivot_sol']} | "
            f"{s.sinyal} | {len(s.semboller)} | {yil:.2f} | "
            f"{'✔' if a_ok else '✘'} | {'✔' if b_ok else '✘'} | **{pencere}** |"
        )
    satir += ["", "`donus_max_bar` burada YENİDEN okundu: tolerans ve pivot "
              "değişince dokunuş süresi dağılımı da kayar. Eski dağılımdan "
              "okunan sayıyı yeni ayarlara taşımak, ölçülmemiş bir eşiği "
              "ölçülmüş gibi göstermek olurdu.", ""]
    hedef = KOK / "docs" / "olcum" / f"harmonik-pesavento-K3-{tf}.md"
    metin = hedef.read_text(encoding="utf-8") + NL.join(satir) + NL
    hedef.write_text(metin, encoding="utf-8")
    print(NL.join(satir))


def _rapor(tf, evren, toplam_bar, toplam, oranlar, olusum, yon) -> None:  # noqa: ANN001
    tarih = dt.date.today().isoformat()
    satir: list[str] = []
    y = satir.append

    y(f"# Harmonik (Pesavento) — K3 Kalibrasyon · {tf}")
    y("")
    y(f"**Tarih:** {tarih} · **Evren:** {evren} BIST sembolü · "
      f"**{toplam_bar:,} bar** ({toplam_bar / 252:,.0f} sembol-yıl)".replace(",", " "))
    y("")
    y("Karar kuralı sonuçlar görülmeden yazıldı ve commit edildi: "
      "[`harmonik-pesavento-K3-karar-kurali.md`](harmonik-pesavento-K3-karar-kurali.md).")
    y("")
    y("> **Bu bir backtest DEĞİLDİR.** Hiçbir işlem simüle edilmedi, getiri "
      "hesaplanmadı. Ölçülen tek şey: formasyon gerçek veride kaç kez "
      "oluşuyor ve oranları nasıl dağılıyor. Getiri K4'ün işi.")
    y("")

    # ---------------------------------------------------------- tolerans
    y("## 1 · Tolerans taraması")
    y("")
    y("Karar kuralı: sembol ≥ 100 **ve** sembol başına yıllık sinyal ≤ 3; "
      "kalanlardan **en küçüğü**.")
    y("")
    secim_tol: dict[str, float | None] = {}
    for ad in FORMASYONLAR:
        y(f"### `{ad}`")
        y("")
        y("| tolerans | sinyal | sembol | sinyal/sembol/yıl | ≥100 sembol | ≤3/yıl |")
        y("|---|---|---|---|---|---|")
        uygun: list[float] = []
        for t in TOLERANSLAR:
            s = toplam[f"tolerans={t:.2f}", ad]
            yil = _yillik(s.sinyal, s.bar, tf) if s.bar else 0.0
            a_ok = len(s.semboller) >= 100
            b_ok = yil <= 3.0
            if a_ok and b_ok:
                uygun.append(t)
            y(f"| {t:.2f} | {s.sinyal} | {len(s.semboller)} | {yil:.2f} | "
              f"{'✔' if a_ok else '✘'} | {'✔' if b_ok else '✘'} |")
        secim_tol[ad] = min(uygun) if uygun else None
        y("")
        if uygun:
            y(f"**Seçilen: `tolerans = {min(uygun):.2f}`**")
        else:
            y("**Hiçbir değer iki sınırı birden sağlamadı → bu formasyon "
              "K4'e GİRMEZ (karar kuralı §7).**")
        y("")

    # ------------------------------------------------------------ pivot
    y("## 2 · Pivot kolu taraması")
    y("")
    y("Karar kuralı: aynı iki sınır; kalanlardan **ortanca**. "
      "(En küçük değil — dar pivot kolu gürültüyü salınım sanar.)")
    y("")
    y("| formasyon | " + " | ".join(f"kol={k}" for k in PIVOTLAR) + " | seçilen |")
    y("|---|" + "---|" * (len(PIVOTLAR) + 1))
    secim_piv: dict[str, int | None] = {}
    for ad in FORMASYONLAR:
        hucre, uygun = [], []
        for k in PIVOTLAR:
            etiket = f"tolerans={TABAN_TOLERANS:.2f}" if k == TABAN_PIVOT else f"pivot={k}"
            s = toplam[etiket, ad]
            yil = _yillik(s.sinyal, s.bar, tf) if s.bar else 0.0
            ok = len(s.semboller) >= 100 and yil <= 3.0
            if ok:
                uygun.append(k)
            hucre.append(f"{s.sinyal} / {len(s.semboller)}s {'✔' if ok else '✘'}")
        sec = uygun[len(uygun) // 2] if uygun else None
        secim_piv[ad] = sec
        y(f"| `{ad}` | " + " | ".join(hucre) + f" | **{sec if sec else '—'}** |")
    y("")
    y("Hücreler: `sinyal / sembol`.")
    y("")

    # ----------------------------------------------------- donus_max_bar
    y("## 3 · `donus_max_bar` — taranmadı, DAĞILIMDAN okundu")
    y("")
    y(f"Pencere {GENIS_PENCERE} bara açıldı ve C'nin onayından D'ye "
      "dokunuşa kadar geçen bar sayısı ölçüldü. Karar kuralı: **%90'lık "
      "dilim**, en yakın 5'e yuvarlanmış.")
    y("")
    y("> **Bu ölçümün bilinen yanlılığı:** dedektör aynı yönde ikinci bir "
      "kurulum açmıyor. Pencere 400'e açılınca uzun bekleyen bir kurulum "
      "arkasındaki kısa bekleyenleri BLOKLUYOR, yani dağılım uzun beklemeler "
      "lehine hafifçe kayıyor. Yanlılığın yönü bilindiği için 40 barlık "
      "(kırpılmış) dağılım da yanına yazıldı: ikisi birbirine yakınsa "
      "yanlılık önemsizdir.")
    y("")
    y("| formasyon | n | medyan | %75 | **%90** | %95 | azami | **seçilen** | 40-bar %90 |")
    y("|---|---|---|---|---|---|---|---|---|")
    secim_pencere: dict[str, int] = {}
    for ad in FORMASYONLAR:
        v = olusum.get(ad, [])
        if not v:
            y(f"| `{ad}` | 0 | — | — | — | — | — | — | — |")
            continue
        p90 = _dilim(v, 0.90)
        sec = max(5, int(round(p90 / 5.0) * 5))
        secim_pencere[ad] = sec
        dar = olusum.get("dar:" + ad, [])
        dar_s = f"{_dilim(dar, .90):.0f}" if dar else "—"
        y(f"| `{ad}` | {len(v)} | {statistics.median(v):.0f} | {_dilim(v, .75):.0f} | "
          f"**{p90:.0f}** | {_dilim(v, .95):.0f} | {max(v)} | **{sec}** | {dar_s} |")
    y("")

    # ------------------------------------------------------ oran dağılımı
    y("## 4 · Oranlar gerçekte nereye düşüyor")
    y("")
    y("Eşik SEÇMEZ (karar kuralı §6) — bulgu olarak yazılır.")
    y("")
    y("### Gartley'in AB bacağı gerçekten dar bir bantta mı")
    y("")
    y("K0 §3.1: kitabın iki kuralı (D = .786 XA **ve** içeride AB=CD) "
      "cebirsel olarak `AB = .786 / (2 − BC)` veriyor, yani **AB ≈ .49–.65**. "
      "Ölçüm bunu doğruluyor mu:")
    y("")
    y("| formasyon · bacak | n | en düşük | %25 | medyan | %75 | en yüksek |")
    y("|---|---|---|---|---|---|---|")
    for (ad, oran_ad), v in sorted(oranlar.items()):
        if oran_ad.endswith("_ham") or not v:
            continue
        sv = sorted(v)
        y(f"| `{ad}` · {oran_ad} | {len(v)} | {sv[0]:.3f} | {_dilim(v, .25):.3f} | "
          f"{statistics.median(v):.3f} | {_dilim(v, .75):.3f} | {sv[-1]:.3f} |")
    y("")
    y("### Hangi Fibonacci oranı kaç kez tuttu")
    y("")
    for (ad, oran_ad), v in sorted(oranlar.items()):
        if oran_ad.endswith("_ham") or not v:
            continue
        sayac = collections.Counter(round(x, 3) for x in v)
        if len(sayac) > 8:
            continue  # sürekli değer (sapma/ham oran), sayılmaz
        dagilim = " · ".join(
            f"{k}: %{n / len(v) * 100:.0f}" for k, n in sorted(sayac.items())
        )
        y(f"* `{ad}` · **{oran_ad}** — {dagilim}")
    y("")

    # ------------------------------------------------------------- yön
    y("## 5 · Boğa / ayı asimetrisi")
    y("")
    y("| formasyon | toplam | boğa | ayı | boğa oranı |")
    y("|---|---|---|---|---|")
    for ad in FORMASYONLAR:
        s = toplam[f"tolerans={TABAN_TOLERANS:.2f}", ad]
        b = yon.get(ad, 0)
        pay = f"%{b / s.sinyal * 100:.0f}" if s.sinyal else "—"
        y(f"| `{ad}` | {s.sinyal} | {b} | {s.sinyal - b} | {pay} |")
    y("")

    # ------------------------------------------------------------ karar
    y("## 6 · Uygulanacak eşikler")
    y("")
    y("| formasyon | tolerans | pivot kolu | donus_max_bar |")
    y("|---|---|---|---|")
    for ad in FORMASYONLAR:
        t = secim_tol.get(ad)
        p = secim_piv.get(ad)
        w = secim_pencere.get(ad)
        y(f"| `{ad}` | {t if t else '— (kalibre edilemedi)'} | "
          f"{p if p else '—'} | {w if w else '—'} |")
    y("")
    y("`stop_orani` (AB=CD) **kapatılmadı** — karar kuralı §5: hangi stop "
      "mesafesinin doğru olduğu bir getiri sorusudur ve getiriye bakarak "
      "eşik seçmek yasaklandı. K4'te iki ayrı künye olarak ölçülecek.")
    y("")

    hedef = KOK / "docs" / "olcum" / f"harmonik-pesavento-K3-{tf}.md"
    hedef.write_text("\n".join(satir) + "\n", encoding="utf-8")
    print(f"\nyazıldı: {hedef.relative_to(KOK)}")
    print("\n".join(satir[-14:]))


if __name__ == "__main__":
    raise SystemExit(main())
