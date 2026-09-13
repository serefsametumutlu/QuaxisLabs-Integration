"""Evren geneli OHLCV indirici — K3/K4 ölçümlerinin ön koşulu.

    python tools/veri_cek.py --market bist --zaman-dilimi 1D
    python tools/veri_cek.py --market bist --evren ISCTR,TCELL --baslangic 2015-01-01

`Store.update()` artımlı çalışır: var olan parquet'in son barlarıyla
örtüşen bir pencere çeker, birleştirir. Bu yüzden araç **yeniden
koşturulabilir** — yarıda kesilirse baştan indirmez.

Hata alan sembol ATLANMAZ, SAYILIR. "Veri çekilemedi" ile "aday bulunamadı"
birbirine karışırsa K3 raporu yalan söyler: önceki projede 648/648 sembolde
sıfır aday çıkmıştı ve kimse bunun kaç tanesinin veri hatası olduğunu
bilmiyordu.
"""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))

from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.data.providers.yfinance_provider import YFinanceProvider  # noqa: E402
from quaxis.teknik.data.store import Store  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Evren geneli OHLCV indirici")
    ap.add_argument("--market", default="bist")
    ap.add_argument("--zaman-dilimi", default="1D", help="1D veya 1H (4H/1W türetilir)")
    ap.add_argument("--evren", default=None, help="virgülle ayrılmış; yoksa config'ten")
    ap.add_argument("--baslangic", default="2010-01-01")
    ap.add_argument("--atla-var-olani", action="store_true", help="dosyası olanı hiç çekme")
    ap.add_argument(
        "--rapor", action="store_true",
        help="hataların TAM dökümünü docs/olcum/ altına yaz (K3'ün 'veri hatası' satırı için)",
    )
    a = ap.parse_args()

    market = Market(a.market)
    tf = Timeframe(a.zaman_dilimi)
    if a.evren:
        evren = [s.strip() for s in a.evren.split(",") if s.strip()]
    else:
        from quaxis.teknik.data.universe import load_universe

        evren = load_universe(market)

    bas = dt.datetime.fromisoformat(a.baslangic).replace(tzinfo=dt.UTC)
    store = Store(YFinanceProvider())
    kok = KOK / "data" / "ohlcv" / market.value

    tamam, hatali = 0, []
    for i, sembol in enumerate(evren, start=1):
        if a.atla_var_olani and (kok / sembol / f"{tf.value}.parquet").exists():
            tamam += 1
            continue
        try:
            store.update(sembol, market, bas, timeframes=(tf,))
            tamam += 1
        except Exception as exc:  # sağlayıcı her türlü hatayı fırlatabilir
            hatali.append((sembol, f"{type(exc).__name__}: {exc}"))
        if i % 25 == 0 or i == len(evren):
            print(f"{i}/{len(evren)} · tamam={tamam} · hata={len(hatali)}", flush=True)

    print(f"\nBitti: {tamam} sembol hazır, {len(hatali)} sembol hata verdi.")
    if hatali:
        print("Hata alanlar (ilk 20) — K3 raporunda 'veri hatası' olarak SAYILMALI:")
        for sembol, mesaj in hatali[:20]:
            print(f"  {sembol}: {mesaj[:110]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
