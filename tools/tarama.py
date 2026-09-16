"""Gerçek tarama koşucusu — `scanner/eod.py` boru hattının giriş kapısı.

    python tools/tarama.py kos                  # son kapalı seans, 1G, tüm evren
    python tools/tarama.py kos --zorla          # aynı gün ikinci kez koş
    python tools/tarama.py kos --evren-boyu 20  # deneme koşusu
    python tools/tarama.py ozet                 # son run'da ne çıktı

## Neden ayrı bir araç

`run_eod` Faz 5'te yazıldı ama onu çağıran tek şey bir `@pytest.mark.network`
testiydi ve o test **tek sembollük** bir evrenle koşuyordu. Depodaki tek EOD
raporunda `universe_size: 1` yazıyor: boru hattı gerçek ölçekte hiç
koşmamıştı. Arayüzdeki tarama tablosunun maket veriyle çalışmasının sebebi
motorun eksikliği değil, motoru çalıştıran bir kolun olmamasıydı.

## Varsayılan zaman dilimi neden yalnız 1G

`run_eod` varsayılanı `("4h", "1d", "w1")`. Burada **yalnız `1d`**:
stratejilerimizin üçü de 1G'de ölçüldü. 4S'te sinyal üretmek, ölçülmemiş bir
zaman diliminde sinyal gösterip yanına 1G'den gelen verdikt rozetini
koymak olurdu — rozet o sinyal hakkında hiçbir şey bilmiyor. Ayrıca sağlayıcı
saatlik veriyi yalnız son 2 yıl için veriyor (bkz.
`docs/olcum/GOLDEN-ZONE-OZET.md`), yani 4S'te ölçüm zaten yapılamıyor.

Başka bir zaman dilimi taranacaksa `--zaman-dilimi` ile açıkça istenir ve o
zaman diliminin ölçümü yoksa rozet `ölçülmedi` olur.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

for akis in (sys.stdout, sys.stderr):
    if hasattr(akis, "reconfigure"):
        akis.reconfigure(encoding="utf-8", errors="replace")

from quaxis.teknik.core.types import Market  # noqa: E402
from quaxis.teknik.data.universe import load_universe  # noqa: E402
from quaxis.teknik.scanner.eod import run_eod  # noqa: E402
from quaxis.teknik.scanner.results import DEFAULT_DB_PATH, ResultsStore  # noqa: E402

KATALOG = "quaxis.teknik.indicators.katalog:KATALOG"


def kos(args: argparse.Namespace) -> int:
    mkt = Market(args.market.lower())
    evren = None
    if args.evren_boyu:
        evren = load_universe(mkt)[: args.evren_boyu]
        print(f"DENEME KOŞUSU: evren {args.evren_boyu} sembole kırpıldı.")

    rapor = run_eod(
        market=args.market,
        date_=dt.date.fromisoformat(args.tarih) if args.tarih else None,
        force=args.zorla,
        catalog=KATALOG,
        timeframes=tuple(args.zaman_dilimi),
        universe_override=evren,
    )
    print(json.dumps(rapor, ensure_ascii=False, indent=2))
    return 0 if rapor.get("status") in ("completed", "skipped_existing") else 1


def ozet(args: argparse.Namespace) -> int:
    """Son tamamlanmış run'da gösterge başına kaç sinyal var."""
    with ResultsStore(db_path=DEFAULT_DB_PATH) as depo:
        run_id = args.run_id or depo.latest_run(args.market.lower())
        if run_id is None:
            print("Tamamlanmış run yok. Önce `python tools/tarama.py kos`.")
            return 1
        kayit = depo.get_run(run_id)
        satirlar, toplam = depo.latest_signals(run_id, limit=100_000)
        kalite = depo.data_quality_summary(run_id)

    print(f"run_id: {run_id}")
    if kayit is not None:
        print(f"evren: {kayit.universe_size} sembol · zaman dilimi: {kayit.timeframes}")
    tarandi = len(kalite.get("ok", []))
    hatali = [s for durum, ss in kalite.items() if durum != "ok" for s in ss]
    print(f"gerçekten taranan: {tarandi} sembol · verisi gelmeyen: {len(hatali)}")
    if hatali:
        print(f"  {', '.join(hatali)}")
    print(f"güncel sinyal: {toplam}")

    sayim: dict[tuple[str, str], int] = {}
    for s in satirlar:
        anahtar = (s["indicator"], s["direction"])
        sayim[anahtar] = sayim.get(anahtar, 0) + 1
    print("\n| gösterge | yön | sinyal |")
    print("|---|---|---|")
    for (gosterge, yon), n in sorted(sayim.items(), key=lambda kv: -kv[1]):
        print(f"| {gosterge} | {yon} | {n} |")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    alt = ap.add_subparsers(dest="komut", required=True)

    k = alt.add_parser("kos", help="EOD taramasını koş")
    k.add_argument("--market", default="bist")
    k.add_argument("--tarih", default=None, help="YYYY-MM-DD; yoksa son kapalı seans")
    k.add_argument("--zaman-dilimi", nargs="+", default=["1d"], dest="zaman_dilimi")
    k.add_argument("--zorla", action="store_true", help="aynı gün tamamlanmış run'ın üstüne yaz")
    k.add_argument("--evren-boyu", type=int, default=None, dest="evren_boyu")
    k.set_defaults(fn=kos)

    o = alt.add_parser("ozet", help="son run'da ne çıktı")
    o.add_argument("--market", default="bist")
    o.add_argument("--run-id", default=None, dest="run_id")
    o.set_defaults(fn=ozet)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
