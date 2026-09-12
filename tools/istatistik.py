"""K4 koşucusu — sembol-kümelenmiş ileri getiri ölçümü ve raporu.

    python tools/istatistik.py --katalog "modul:KATALOG" --gosterge altin.bolge \\
        --slug altin-bolge --ufuk 20

    # ölçüm makinesini gösterge yokken sınamak için:
    python tools/istatistik.py --sentetik

Çıktı: `docs/olcum/<slug>-K4-<tarih>.md`

Sinyaller `payload` içinde `stop` ve `hedef` taşıyorsa rapora ayrıca
**üç bariyerli R-katsayısı** bölümü eklenir. İleri getiri tek başına
stop/hedef asimetrisini göremez; taşımıyorsa rapor bunu açıkça yazar.

**Eleme değil etiketleme.** Sonuç ne çıkarsa pasaporta ve siteye o yazılır.
Ölçüm mantığı `quaxis.teknik.olcum.ileri_getiri`'de ve kendi testleri var:
gerçek bir kenarı bulduğu, olmayan bir kenarı uydurmadığı ve yükselen piyasayı
tek başına kenar saymadığı test edilmiştir.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

import numpy as np  # noqa: E402
from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.data.providers.yfinance_provider import YFinanceProvider  # noqa: E402
from quaxis.teknik.data.store import Store  # noqa: E402
from quaxis.teknik.olcum.bariyer import RResult, measure_r  # noqa: E402
from quaxis.teknik.olcum.ileri_getiri import ForwardReturnResult, bh_fdr, measure  # noqa: E402
from quaxis.teknik.scanner import engine  # noqa: E402

OLCUM_KOK = KOK / "docs" / "olcum"


def kosu(
    katalog: str, gosterge: str, evren: list[str], tf: Timeframe, market: Market, ufuk: int
) -> tuple[ForwardReturnResult, RResult | None]:
    scan = engine.run(
        run_id=f"k4_{gosterge}_{dt.date.today().isoformat()}",
        universe=evren, timeframes=[tf], indicator_names=[gosterge],
        market=market, catalog=katalog, workers=1,
    )
    store = Store(YFinanceProvider())
    seri, sinyaller, ohlc, islemler = {}, {}, {}, {}
    for r in scan.results:
        if r.error or r.result is None:
            continue
        try:
            df = store.get(r.symbol, tf, market)
        except FileNotFoundError:
            continue
        seri[r.symbol] = df["close"]
        sinyaller[r.symbol] = r.result.signals
        # R ölçümü ancak strateji kendi stop/hedefini BİLDİRİRSE yapılır.
        # Ölçüm bunları uydurmaz; uydurursa ölçtüğü şey strateji olmaz.
        kayit = [
            (s, float(s.payload["stop"]), float(s.payload["hedef"]))
            for s in r.result.signals
            if "stop" in s.payload and "hedef" in s.payload
        ]
        if kayit:
            ohlc[r.symbol] = df
            islemler[r.symbol] = kayit

    ig = measure(seri, sinyaller, horizon=ufuk)
    rs = measure_r(ohlc, islemler, max_bars=ufuk) if islemler else None
    return ig, rs


def r_bolumu(r: RResult | None) -> str:
    if r is None:
        return """## R-katsayısı (üç bariyer)

Ölçülmedi — strateji sinyallerinde `stop` ve `hedef` bildirilmemiş.

> İleri getiri, stop/hedef asimetrisini **göremez**. %35 isabetle 3R kazandıran
> bir sistem 20 barlık ileri getiride sıfır görünür. Bir stratejinin iddiası
> asimetrik R ise, K4 bu bölüm doldurulmadan kapanamaz.
"""
    return f"""## R-katsayısı (üç bariyer: stop / hedef / zaman)

| Ölçüt | Değer |
|---|---|
| İşlem | {r.n_trades} ({r.n_symbols} sembol) |
| İsabet | %{r.win_rate * 100:.1f} |
| **İşlem başına beklenen R** | **{r.expectancy:+.3f}R** |
| Ortanca R | {r.median_r:+.3f}R |
| Adil baz (aynı risk, rastgele bar) | {r.baseline_mean_r:+.3f}R |
| Hedefte çıkış | %{r.target_rate * 100:.1f} |
| Stopta çıkış | %{r.stop_rate * 100:.1f} |
| Zamanda çıkış | %{r.time_rate * 100:.1f} |
| Permütasyon p değeri | {r.p_value:.4f} ({r.permutations} tur) |
| **Verdikt (R)** | **{r.verdict}** |

> Aynı barda hem stop hem hedef vurulduysa **stop** sayıldı. Bar içi sıralamayı
> bilmiyoruz; emin olmadığımız yerde stratejinin lehine varsaymıyoruz.
"""


def rapor(
    s: ForwardReturnResult, slug: str, gosterge: str, fdr: bool | None, r: RResult | None = None
) -> str:
    fdr_metin = "—" if fdr is None else ("geçti" if fdr else "geçemedi")
    verdikt = s.verdict if fdr is not False else "kanitlanmadi"
    ham = (
        float(np.mean([m.signal_return for m in s.measurements])) if s.measurements else 0.0
    )
    baz = (
        float(np.mean([m.baseline_return for m in s.measurements])) if s.measurements else 0.0
    )
    return f"""# {slug} — K4 İstatistik

**Tarih:** {dt.date.today().isoformat()}
**Gösterge:** `{gosterge}`

| Ölçüt | Değer |
|---|---|
| Evren | {s.universe} sembol |
| **Bağımsız gözlem (sembol)** | **{s.independent_observations}** |
| Toplam sinyal | {s.total_signals} |
| Pencere | ilk %{(1 - s.oos_ratio) * 100:.0f} IS / son %{s.oos_ratio * 100:.0f} OOS |
| Ufuk | {s.horizon} bar |
| Sinyal getirisi (ortalama) | %{ham * 100:+.2f} |
| Adil baz | %{baz * 100:+.2f} |
| **Adil baza karşı fark** | **%{s.mean_difference * 100:+.2f}** |
| Permütasyon p değeri | {s.p_value:.4f} ({s.permutations} tur) |
| BH-FDR (q=0.05) | {fdr_metin} |
| **Verdikt** | **{verdikt}** |

{r_bolumu(r)}
## Ne çıkarsa o

*(Sonuç olumsuzsa da aynı açıklıkla yaz. "Zarar ettiriyor" ile "işe
yaradığına dair kanıt yok" farklı şeylerdir — hangisi olduğunu söyle.
Örneklem küçükse belirt; p değerini yuvarlama.)*

## Ölçümün sınırları

| | |
|---|---|
| Dönem | *(hangi tarih aralığı)* |
| Evren | *(hangi semboller, neden)* |
| Ufuk | {s.horizon} bar — *(neden bu ufuk)* |
| Bilinen zayıflık | *(hayatta kalma yanlılığı, işlem maliyeti yok, vb.)* |

> **Bağımsız gözlem birimi sembol'dür, bar değil.** Aynı sembolün barları
> bağımsız olmadığı için bar saymak p değerini sahte küçültür.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="K4 istatistik koşucusu")
    ap.add_argument("--katalog")
    ap.add_argument("--gosterge")
    ap.add_argument("--slug")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--ufuk", type=int, default=20)
    ap.add_argument("--evren", default=None)
    ap.add_argument("--aile", default=None, help="FDR ailesi: slug=p,slug=p (bu ölçümle birlikte)")
    ap.add_argument("--sentetik", action="store_true", help="ölçüm makinesini sına")
    a = ap.parse_args()

    if a.sentetik:
        import pandas as pd
        from quaxis.teknik.core.types import Signal

        r = np.random.default_rng(5)
        seri, sinyaller = {}, {}
        for i in range(20):
            idx = pd.date_range("2024-01-01", periods=400, freq="1D", tz="UTC")
            s = pd.Series(100 + np.cumsum(r.normal(0, 1, 400)), index=idx)
            seri[f"S{i}"] = s
            barlar = r.integers(300, 380, size=5)
            sinyaller[f"S{i}"] = [
                Signal(s.index[int(b)], s.index[int(b)], "long", "confirmed", 1.0, {})
                for b in barlar
            ]
        sonuc = measure(seri, sinyaller, horizon=10, permutations=500)
        print(rapor(sonuc, "sentetik-sinama", "test.rastgele", None))
        print("Beklenen: rastgele sinyallerde kenar BULUNMAMALI.")
        return 0

    if not (a.katalog and a.gosterge and a.slug):
        ap.error("--katalog, --gosterge ve --slug zorunlu (ya da --sentetik)")

    market = Market(a.market)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    sonuc, r_sonuc = kosu(a.katalog, a.gosterge, evren, Timeframe(a.zaman_dilimi), market, a.ufuk)

    fdr: bool | None = None
    if a.aile:
        aile = {a.slug: sonuc.p_value}
        for parca in a.aile.split(","):
            ad, _, p = parca.partition("=")
            if ad.strip() and p.strip():
                aile[ad.strip()] = float(p)
        fdr = bh_fdr(aile)[a.slug]

    OLCUM_KOK.mkdir(parents=True, exist_ok=True)
    hedef = OLCUM_KOK / f"{a.slug}-K4-{dt.date.today().isoformat()}.md"
    hedef.write_text(rapor(sonuc, a.slug, a.gosterge, fdr, r_sonuc), encoding="utf-8")
    print(f"n={sonuc.independent_observations} sembol · fark %{sonuc.mean_difference * 100:+.2f} "
          f"· p={sonuc.p_value:.4f} · verdikt={sonuc.verdict}")
    if r_sonuc is None:
        print("R ÖLÇÜLMEDİ: sinyaller stop/hedef bildirmiyor — asimetri görünmez.")
    else:
        print(f"R: {r_sonuc.expectancy:+.3f}R/işlem · isabet %{r_sonuc.win_rate * 100:.1f} "
              f"· p={r_sonuc.p_value:.4f} · verdikt={r_sonuc.verdict}")
    print(f"\n{hedef.relative_to(KOK)} yazıldı.")
    print("Pasaportun K4 kapısına bağla ve künyedeki `verdikt` alanını GÜNCELLE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
