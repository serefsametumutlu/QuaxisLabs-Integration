"""Segment analizi — strateji HANGİ sembollerde ve HANGİ zaman diliminde çalışıyor?

    python tools/segment_analizi.py --katalog "quaxis.teknik.indicators.katalog:KATALOG" \\
        --slug golden-zone --zaman-dilimi 1D

Çıktı: `docs/olcum/<slug>-segment-<tf>-<tarih>.md`

## Bu KEŞİFSEL bir analizdir, doğrulama değil

Önceki ön kayıtlı test şunu gösterdi: `macd_uyum` B grubu sembollerde
p=0.0025, A grubunda p=0.8166. Yani etki sembol bileşimine duyarlı. Bu araç
o duyarlılığın **haritasını** çıkarır.

Ama harita çıkarmak, haritada en parlak görünen kutuyu "bulduk" ilan etmek
değildir. Segment sayısı arttıkça birinin tesadüfen iyi görünmesi kesinleşir;
burada BH-FDR uygulanır ve **geçen segment bile "aday" sayılır, "kanıt"
değil.** Bir segmentin gerçekten çalıştığını söylemek için o segment
önceden seçilip kendi ön kayıtlı testinden geçmelidir.

## Ölçütler

| Ölçüt | Ne söyler |
|---|---|
| Sinyal / işlem sayısı | Strateji o segmentte ne sıklıkta konuşuyor |
| İsabet (win rate) | Kaç işlem artıda kapandı |
| Profit factor | Kazanç toplamı / kayıp toplamı (1.0 başabaş) |
| Ortalama R | İşlem başına beklenen getiri, risk cinsinden |
| Adil baz | Aynı risk yapısıyla rastgele girişin verdiği |

**İsabet tek başına yanıltır.** %60 isabetle para kaybettiren bir sistem
mümkündür (kazançlar küçük, kayıplar büyük); profit factor ve ortalama R
bunu ayırt eder. Üçü birlikte okunur.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import re
import sys
from dataclasses import dataclass

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

for akis in (sys.stdout, sys.stderr):
    if hasattr(akis, "reconfigure"):
        akis.reconfigure(encoding="utf-8", errors="replace")

import numpy as np  # noqa: E402
from katmanli_olcum import ASGARI_ISLEM, tara  # noqa: E402
from kosul_taramasi import KOSULLAR, _islemler, _rejim_ekle, endeks_rejimi  # noqa: E402
from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.olcum.bariyer import RResult, measure_r  # noqa: E402
from quaxis.teknik.olcum.ileri_getiri import bh_fdr  # noqa: E402

OLCUM_KOK = KOK / "docs" / "olcum"
EVREN_DOSYA = KOK / "packages" / "teknik" / "config" / "universe_bist.txt"


def sektorler() -> dict[str, str]:
    """Evren dosyasındaki `# Sektör (n)` başlıklarından sembol→sektör haritası."""
    harita: dict[str, str] = {}
    simdiki = "Tanımsız"
    for satir in EVREN_DOSYA.read_text(encoding="utf-8").splitlines():
        s = satir.strip()
        if not s:
            continue
        if s.startswith("#"):
            m = re.match(r"#\s*(.+?)\s*\(\d+\)\s*$", s)
            if m:
                simdiki = m.group(1)
            continue
        harita[s] = simdiki
    return harita


@dataclass
class Segment:
    ad: str
    aciklama: str
    semboller: set[str]
    sonuc: RResult | None = None

    @property
    def guvenilir(self) -> bool:
        return bool(self.sonuc and self.sonuc.n_trades >= ASGARI_ISLEM)


def _ciro_medyani(sinyaller: dict) -> dict[str, float]:
    """Sembol başına medyan ciro — sinyal barlarında ölçülmüş."""
    out = {}
    for sembol, liste in sinyaller.items():
        degerler = [g.payload["ciro"] for g in liste if g.payload.get("ciro") is not None]
        if degerler:
            out[sembol] = float(np.median(degerler))
    return out


def _fiyat_medyani(ohlc: dict) -> dict[str, float]:
    return {s: float(df["close"].median()) for s, df in ohlc.items() if len(df)}


def _dilim(degerler: dict[str, float], sayi: int, adlar: list[str]) -> list[Segment]:
    """Değerleri `sayi` eşit parçaya böler (çeyrekler gibi)."""
    if not degerler:
        return []
    sinir = np.quantile(list(degerler.values()), np.linspace(0, 1, sayi + 1))
    out = []
    for i in range(sayi):
        alt, ust = sinir[i], sinir[i + 1]
        uyanlar = {
            s for s, v in degerler.items()
            if (v >= alt and v < ust) or (i == sayi - 1 and v >= alt)
        }
        out.append(Segment(adlar[i], f"{alt:,.0f} – {ust:,.0f}", uyanlar))
    return out


def segmentler(ohlc: dict, sinyaller: dict) -> list[Segment]:
    ciro = _ciro_medyani(sinyaller)
    fiyat = _fiyat_medyani(ohlc)
    sek = sektorler()

    out: list[Segment] = []
    out += _dilim(ciro, 4, ["Likidite Ç1 (en ince)", "Likidite Ç2", "Likidite Ç3",
                            "Likidite Ç4 (en kalın)"])
    out += _dilim(fiyat, 3, ["Fiyat: düşük", "Fiyat: orta", "Fiyat: yüksek"])

    sayim: dict[str, set[str]] = {}
    for sembol in sinyaller:
        sayim.setdefault(sek.get(sembol, "Tanımsız"), set()).add(sembol)
    # Yalnız en az 8 sembollü sektörler: 2 sembollü bir "sektör" segmenti
    # istatistik değil anekdot olur.
    for ad, kume in sorted(sayim.items(), key=lambda x: -len(x[1])):
        if len(kume) >= 8:
            out.append(Segment(f"Sektör: {ad}", f"{len(kume)} sembol", kume))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Segment analizi")
    ap.add_argument("--katalog", required=True)
    ap.add_argument("--gosterge", default="golden_zone")
    ap.add_argument("--slug", default="golden-zone")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--kosul", default=None, help="KOSULLAR anahtarı; yoksa koşulsuz")
    ap.add_argument("--tur", type=int, default=1500)
    ap.add_argument("--evren", default=None)
    a = ap.parse_args()

    market, tf = Market(a.market), Timeframe(a.zaman_dilimi)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    ohlc, sinyaller, hatali = tara(a.katalog, a.gosterge, evren, tf, market)
    _rejim_ekle(sinyaller, endeks_rejimi(market, tf))
    kosul = KOSULLAR[a.kosul][1] if a.kosul else None
    ham = sum(len(v) for v in sinyaller.values())
    print(f"{len(ohlc)} sembol · ham sinyal {ham}", flush=True)

    bariyer = 40
    for liste in _islemler(sinyaller).values():
        bariyer = int(liste[0][0].payload.get("zaman_bariyeri", bariyer))
        break

    def olc(alt_ohlc, alt_sinyal) -> RResult:
        return measure_r(
            alt_ohlc, _islemler(alt_sinyal, kosul), max_bars=bariyer,
            pencere="oos", permutations=a.tur,
        )

    genel = olc(ohlc, sinyaller)
    cikis = (f"%{genel.target_rate * 100:.0f} / %{genel.stop_rate * 100:.0f}"
             f" / %{genel.time_rate * 100:.0f}")
    print(f"GENEL: {genel.n_trades} işlem · isabet %{genel.win_rate * 100:.1f} · "
          f"PF {genel.profit_factor:.2f} · {genel.mean_r:+.3f}R", flush=True)

    segler = segmentler(ohlc, sinyaller)
    for seg in segler:
        seg.sonuc = olc(
            {k: v for k, v in ohlc.items() if k in seg.semboller},
            {k: v for k, v in sinyaller.items() if k in seg.semboller},
        )
        r = seg.sonuc
        print(f"  {seg.ad:34} {r.n_trades:5} işlem · %{r.win_rate * 100:4.1f} · "
              f"PF {r.profit_factor:5.2f} · {r.mean_r:+.3f}R · p={r.p_value:.4f}", flush=True)

    fdr = bh_fdr({s.ad: s.sonuc.p_value for s in segler if s.guvenilir}, q=0.05)

    def satirla(kume: list[Segment]) -> str:
        return "\n".join(
            f"| {s.ad} | {s.aciklama} | {len(s.semboller)} | {s.sonuc.n_trades}"
            f"{'' if s.guvenilir else ' ⚠'} | %{s.sonuc.win_rate * 100:.1f} | "
            f"{s.sonuc.profit_factor:.2f} | {s.sonuc.mean_r:+.3f}R | "
            f"{s.sonuc.baseline_mean_r:+.3f}R | {s.sonuc.p_value:.4f} | "
            f"{'**geçti**' if fdr.get(s.ad) else '—'} |"
            for s in kume if s.sonuc
        )

    likidite = [s for s in segler if s.ad.startswith("Likidite")]
    fiyatlar = [s for s in segler if s.ad.startswith("Fiyat")]
    sektor = [s for s in segler if s.ad.startswith("Sektör")]
    gecen = [s.ad for s in segler if fdr.get(s.ad)]

    basliksatir = ("| Segment | Aralık | Sembol | İşlem | İsabet | PF | Ort. R | "
                   "Adil baz | p | BH-FDR |")
    ayrac = "|" + "---|" * 10

    OLCUM_KOK.mkdir(parents=True, exist_ok=True)
    hedef = OLCUM_KOK / f"{a.slug}-segment-{tf.value}-{dt.date.today().isoformat()}.md"
    hedef.write_text(f"""# {a.slug} — Segment Analizi · {tf.value}

**Tarih:** {dt.date.today().isoformat()} ·
**Koşul:** `{a.kosul or "koşulsuz"}` · **Pencere:** OOS

> **Bu KEŞİFSEL bir analizdir.** Haritada en parlak görünen kutuyu "bulduk"
> ilan etmek, haritayı çıkarmakla aynı şey değildir. BH-FDR uygulandı ama
> geçen segment bile **aday** sayılır, kanıt değil: gerçekten çalıştığını
> söylemek için o segment önceden seçilip kendi ön kayıtlı testinden
> geçmelidir.

## Genel tablo

| | |
|---|---|
| Sembol | {len(ohlc)} (veri hatası: {hatali}) |
| Ham sinyal | {ham} |
| OOS işlem | {genel.n_trades} |
| İsabet | %{genel.win_rate * 100:.1f} |
| **Profit factor** | **{genel.profit_factor:.2f}** |
| Ortalama R | {genel.mean_r:+.3f}R |
| Adil baz | {genel.baseline_mean_r:+.3f}R |
| Ortalama kazanç / kayıp | {genel.ortalama_kazanc:+.2f}R / {genel.ortalama_kayip:+.2f}R |
| Hedef / stop / zaman çıkışı | {cikis} |

## Likiditeye göre

{basliksatir}
{ayrac}
{satirla(likidite)}

## Fiyat ölçeğine göre

{basliksatir}
{ayrac}
{satirla(fiyatlar)}

## Sektöre göre (en az 8 sembollü)

{basliksatir}
{ayrac}
{satirla(sektor)}

⚠ = {ASGARI_ISLEM} işlemin altı; sayı yazılır, verdikt yazılmaz (Pardo s.295).

## BH-FDR'yi geçen segmentler

{", ".join(f"**{g}**" for g in gecen) if gecen else "**Hiçbiri.**"}

## Nasıl okunur

**İsabet tek başına yanıltır.** %60 isabetle para kaybettiren sistem
mümkündür (kazançlar küçük, kayıplar büyük). Üç sayı birlikte okunur:

* **Profit factor < 1.0** → kayıplar kazançları yiyor.
* **Ortalama R ≤ adil baz** → strateji piyasanın kendi verdiğinin altında.
* **p > 0.05** → aradaki fark gürültüden ayırt edilemiyor.

## Ölçümün sınırları

| | |
|---|---|
| Keşifsel | Segmentler önceden tanımlandı, ama SEÇİM sonuca bakılarak
yapılırsa geçerlilik kaybolur |
| Segment sayısı | {len(segler)} — her biri bir test; FDR bu yüzden zorunlu |
| İşlem maliyeti | dahil (taraf başına %0.05 + çıkışta %0.05 kayma) |
| Likidite dilimi | Sinyal barlarındaki medyan ciro; sembolün genel likiditesi değil |
| Sektör | Evren dosyasındaki Fintables sınıflaması (2026-08-13) |
""", encoding="utf-8")
    print(f"\n{hedef.relative_to(KOK)} yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
