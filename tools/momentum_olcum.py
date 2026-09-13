"""Kesitsel Momentum K3+K4 koşucusu.

    python tools/momentum_olcum.py --katalog "quaxis.teknik.indicators.katalog:KATALOG" \\
        --gosterge kesitsel_momentum --slug kesitsel-momentum

Çıktı: `docs/olcum/<slug>-K3K4-<tarih>.md`

## Neden ayrı bir koşucu

`katmanli_olcum.py` üç bariyerli R ölçer; o ölçüt **stop/hedef bildiren**
stratejiler içindir. Kesitsel momentumda stop YOK: pozisyon `tutus` bar
tutulur ve kapanır (Chan s.146). Zorla bir stop uydurmak stratejiyi
değiştirmek olurdu — o yüzden ölçüt `olcum/ileri_getiri.py`'nin ufuk
getirisidir ve **ufuk stratejinin kendi `tutus` parametresinden** gelir,
araç onu uydurmaz.

## Adil baz bu stratejide her zamankinden kritik

Yalnız alış olduğu için strateji BIST'in kendi sürüklenmesini üstleniyor.
"Yükseldi" ile "yükselenleri seçmek işe yarıyor" ayrı şeyler; ikisini
ayıran tek şey, aynı barda **rastgele** sembol seçen baz.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

for akis in (sys.stdout, sys.stderr):
    if hasattr(akis, "reconfigure"):
        akis.reconfigure(encoding="utf-8", errors="replace")

import numpy as np  # noqa: E402
from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.data.providers.yfinance_provider import YFinanceProvider  # noqa: E402
from quaxis.teknik.data.store import Store  # noqa: E402
from quaxis.teknik.olcum.ileri_getiri import ForwardReturnResult, measure  # noqa: E402
from quaxis.teknik.olcum.kalibrasyon import calibrate  # noqa: E402
from quaxis.teknik.scanner import engine  # noqa: E402

OLCUM_KOK = KOK / "docs" / "olcum"


def kosu(katalog: str, gosterge: str, evren: list[str], tf: Timeframe, market: Market):
    scan = engine.run(
        run_id=f"km_{gosterge}_{dt.date.today().isoformat()}",
        universe=evren, timeframes=[tf], indicator_names=[gosterge],
        market=market, catalog=katalog, workers=1,
    )
    store = Store(YFinanceProvider())
    seri, sinyaller = {}, {}
    hatali = 0
    for r in scan.results:
        if r.error or r.result is None:
            hatali += 1
            continue
        try:
            seri[r.symbol] = store.get(r.symbol, tf, market)["close"]
        except FileNotFoundError:
            hatali += 1
            continue
        sinyaller[r.symbol] = list(r.result.signals)
    return seri, sinyaller, hatali


def rapor(
    s: ForwardReturnResult, kalib, slug: str, gosterge: str, tf: Timeframe,
    ufuk: int, ham: int, donem: str,
) -> str:
    ham_getiri = (
        float(np.mean([m.signal_return for m in s.measurements])) if s.measurements else 0.0
    )
    baz = (
        float(np.mean([m.baseline_return for m in s.measurements])) if s.measurements else 0.0
    )
    kazanan = sum(1 for m in s.measurements if m.signal_return > 0)
    return f"""# {slug} — K3 + K4 · {tf.value}

**Tarih:** {dt.date.today().isoformat()} · **Gösterge:** `{gosterge}`
**Dönem:** {donem} · **Yön:** yalnız alış

## K3 · Kalibrasyon

| | |
|---|---|
| Evren | {kalib.universe} sembol |
| Toplam sinyal | {ham} |
| Sıfır sinyal veren sembol | {kalib.zero_candidate_symbols} (%{kalib.zero_ratio * 100:.1f}) |
| Veri hatası | {kalib.error_symbols} |
| Sembol başına ortalama | {kalib.per_symbol_mean:.1f} |
| Sembol başına ortanca | {kalib.per_symbol_median:.0f} |

{kalib.diagnosis}

> Sinyaller **örtüşmüyor**: bir sembol için yeni sinyal, öncekinin
> {ufuk} barlık tutuşu bitmeden üretilmiyor (Chan s.151).

## K4 · İstatistik

| | |
|---|---|
| **Bağımsız gözlem (sembol)** | **{s.independent_observations}** |
| Ölçülen sinyal | {s.total_signals} |
| Pencere | ilk %{(1 - s.oos_ratio) * 100:.0f} IS / son %{s.oos_ratio * 100:.0f} OOS |
| Ufuk | {s.horizon} bar (stratejinin kendi tutuş süresi) |
| **Sinyal getirisi** | **%{ham_getiri * 100:+.2f}** |
| **Adil baz** (rastgele sembol) | **%{baz * 100:+.2f}** |
| **Fark** | **%{s.mean_difference * 100:+.2f}** |
| Kazanan sembol | {kazanan}/{s.independent_observations} |
| Permütasyon p değeri | {s.p_value:.4f} ({s.permutations} tur) |
| **Verdikt** | **{s.verdict}** |

İşlem maliyeti **dahil**: taraf başına %0.05 komisyon + %0.05 kayma.
Giriş de çıkış da piyasa emri sayıldı — sıralama barının kapanışında
alınıyor, tutuş bitince kapanışta satılıyor.

## Ne çıkarsa o

*(Sonuç olumsuzsa da aynı açıklıkla yazılır.)*

## Ölçümün sınırları

| | |
|---|---|
| Yalnız alış | Kaynak uzun/kısa kuruyor; yalnız alış piyasa yönünü nötrlemez |
| Portföy etkisi | Sinyal başına ölçüldü; eş zamanlı pozisyon sayısı
ve sermaye dağıtımı modellenmedi |
| Hayatta kalma yanlılığı | Evren bugünkü listeden |
| Momentum çöküşü | Chan s.152: krizden sonra yıllarca kötü. Dönem kırılımı ayrıca ölçülmeli |
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Kesitsel momentum K3+K4")
    ap.add_argument("--katalog", required=True)
    ap.add_argument("--gosterge", default="kesitsel_momentum")
    ap.add_argument("--slug", default="kesitsel-momentum")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--tur", type=int, default=2000)
    ap.add_argument("--evren", default=None)
    a = ap.parse_args()

    market, tf = Market(a.market), Timeframe(a.zaman_dilimi)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    print(f"Tarama: {len(evren)} sembol · {tf.value}", flush=True)
    seri, sinyaller, hatali = kosu(a.katalog, a.gosterge, evren, tf, market)
    ham = sum(len(v) for v in sinyaller.values())
    print(f"{len(seri)} sembol · ham sinyal {ham} · veri hatası {hatali}", flush=True)
    if ham == 0:
        print("Hiç sinyal yok.")
        return 1

    # Ufuk STRATEJİNİN kendi parametresinden gelir; araç uydurmaz.
    ufuk = 25
    for liste in sinyaller.values():
        if liste:
            ufuk = int(liste[0].payload.get("tutus", ufuk))
            break

    kalib = calibrate(
        a.gosterge, tf.value, {s: len(v) for s, v in sinyaller.items()}, error_symbols=hatali
    )
    print(kalib.diagnosis, flush=True)

    sonuc = measure(seri, sinyaller, horizon=ufuk, permutations=a.tur)
    print(f"n={sonuc.independent_observations} sembol · fark "
          f"%{sonuc.mean_difference * 100:+.2f} · p={sonuc.p_value:.4f} "
          f"· {sonuc.verdict}", flush=True)

    ilk = min(s.index[0] for s in seri.values())
    son = max(s.index[-1] for s in seri.values())
    donem = f"{ilk.date()} – {son.date()}"

    OLCUM_KOK.mkdir(parents=True, exist_ok=True)
    hedef = OLCUM_KOK / f"{a.slug}-K3K4-{tf.value}-{dt.date.today().isoformat()}.md"
    hedef.write_text(
        rapor(sonuc, kalib, a.slug, a.gosterge, tf, ufuk, ham, donem), encoding="utf-8"
    )
    print(f"\n{hedef.relative_to(KOK)} yazıldı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
