"""K3 koşucusu — tam evrende aday sayısını ölçer ve raporu yazar.

    python tools/kalibrasyon.py --katalog "modul:KATALOG" --gosterge swing.fib.abcd \\
        --slug swing-fib-abcd --zaman-dilimi 1D

    # gösterge yokken boru hattını sınamak için:
    python tools/kalibrasyon.py --sentetik

Çıktı: `docs/olcum/<slug>-K3-<tarih>.md`

Rapor **her zaman** kaç sembolün sıfır aday verdiğini taşır. Önceki projede
`breakout_fvg` ve `flag_pennant` 4S'te 648/648 sembolde sıfır aday veriyordu ve
tarama "başarıyla tamamlandı" diyordu — hata yoktu, yalnızca sonuç yoktu.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.olcum.kalibrasyon import CalibrationResult, calibrate  # noqa: E402
from quaxis.teknik.scanner import engine  # noqa: E402

OLCUM_KOK = KOK / "docs" / "olcum"


def kosu(
    katalog: str, gosterge: str, evren: list[str], tf: Timeframe, market: Market
) -> CalibrationResult:
    scan = engine.run(
        run_id=f"k3_{gosterge}_{dt.date.today().isoformat()}",
        universe=evren,
        timeframes=[tf],
        indicator_names=[gosterge],
        market=market,
        catalog=katalog,
        workers=1,
    )
    sembol_basina: dict[str, int] = {}
    hatali = 0
    for r in scan.results:
        if r.error:
            hatali += 1
            continue
        sembol_basina[r.symbol] = len(r.result.signals) if r.result else 0
    return calibrate(gosterge, tf.value, sembol_basina, error_symbols=hatali)


def rapor(sonuc: CalibrationResult, slug: str) -> str:
    return f"""# {slug} — K3 Kalibrasyon

**Tarih:** {dt.date.today().isoformat()}
**Gösterge:** `{sonuc.indicator}` · **Zaman dilimi:** {sonuc.timeframe}

| Ölçüt | Değer |
|---|---|
| Evren | {sonuc.universe} sembol |
| Toplam aday | {sonuc.total_candidates} |
| **Sıfır aday veren sembol** | **{sonuc.zero_candidate_symbols}** (%{sonuc.zero_ratio * 100:.1f}) |
| Veri hatası alan sembol | {sonuc.error_symbols} |
| Sembol başına ortalama | {sonuc.per_symbol_mean:.2f} |
| Sembol başına ortanca | {sonuc.per_symbol_median:.1f} |
| Sembol başına en çok | {sonuc.per_symbol_max} |

## Teşhis

{sonuc.diagnosis}

## Ne yapıldı

*(Eşik değiştirildiyse hangisi, hangi değere ve neden — pasaportun K0
tablosundaki `K3:` devirleri burada kapanır.)*
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="K3 kalibrasyon koşucusu")
    ap.add_argument("--katalog", help='katalog adresi: "modul.yolu:NITELIK"')
    ap.add_argument("--gosterge")
    ap.add_argument("--slug")
    ap.add_argument("--zaman-dilimi", default="1D")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--evren", default=None, help="virgülle ayrılmış; yoksa config'ten")
    ap.add_argument(
        "--sentetik", action="store_true",
        help="gösterge yokken boru hattını sına (örnek katalog + sentetik veri)",
    )
    a = ap.parse_args()

    if a.sentetik:
        print("Sentetik sınama: örnek katalog + sentetik sağlayıcı.")
        print("Gerçek koşu için --katalog ve --gosterge ver.")
        from quaxis.teknik.olcum.kalibrasyon import calibrate as _c

        ornek = _c("test.ornek", "1D", {f"S{i}": (i % 5) for i in range(648)})
        print(rapor(ornek, "sentetik-sinama"))
        return 0

    if not (a.katalog and a.gosterge and a.slug):
        ap.error("--katalog, --gosterge ve --slug zorunlu (ya da --sentetik)")

    market = Market(a.market)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    sonuc = kosu(a.katalog, a.gosterge, evren, Timeframe(a.zaman_dilimi), market)
    OLCUM_KOK.mkdir(parents=True, exist_ok=True)
    hedef = OLCUM_KOK / f"{a.slug}-K3-{dt.date.today().isoformat()}.md"
    hedef.write_text(rapor(sonuc, a.slug), encoding="utf-8")
    print(sonuc.diagnosis)
    print(f"\n{hedef.relative_to(KOK)} yazıldı.")
    print("Pasaportun K3 kapısına kanıt olarak bağla ve `pasaport.py dogrula` koştur.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
