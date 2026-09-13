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
    if a.rapor:
        hedef = _rapor_yaz(market, tf, evren, tamam, hatali)
        print(f"\n{hedef.relative_to(KOK)} yazıldı.")
    return 0


def _sinifla(mesaj: str) -> str:
    """Hatayı K3'ün ayırt etmesi gereken türlere böler.

    "Sembol borsada yok" ile "veride bozuk tick var" aynı şey değildir:
    birincisi evren listesinin güncelliğiyle, ikincisi sağlayıcının
    kalitesiyle ilgilidir ve farklı şeyler yapmayı gerektirir.
    """
    if "veri dönmedi" in mesaj or "delisted" in mesaj or "Not Found" in mesaj:
        return "borsada yok / veri dönmedi"
    if "high >= max" in mesaj:
        return "high < gövde (bozuk tick)"
    if "low <= min" in mesaj:
        return "low > gövde (bozuk tick)"
    if "NaN" in mesaj:
        return "NaN değer"
    return "diğer"


def _rapor_yaz(
    market: Market, tf: Timeframe, evren: list[str], tamam: int, hatali: list
) -> pathlib.Path:
    from collections import Counter

    sayim = Counter(_sinifla(m) for _, m in hatali)
    kok = KOK / "docs" / "olcum"
    kok.mkdir(parents=True, exist_ok=True)
    hedef = kok / f"veri-{market.value}-{tf.value}-{dt.date.today().isoformat()}.md"

    tur_satir = "\n".join(
        f"| {tur} | {n} | %{n / len(evren) * 100:.1f} |" for tur, n in sayim.most_common()
    )
    liste = "\n".join(
        f"| `{sembol}` | {_sinifla(mesaj)} | {mesaj[:150]} |" for sembol, mesaj in sorted(hatali)
    )
    hedef.write_text(
        f"""# Veri kalitesi — {market.value.upper()} · {tf.value}

**Tarih:** {dt.date.today().isoformat()}

| | |
|---|---|
| Evren | {len(evren)} sembol |
| **Verisi hazır** | **{tamam}** (%{tamam / len(evren) * 100:.1f}) |
| Hata veren | {len(hatali)} (%{len(hatali) / len(evren) * 100:.1f}) |

## Hata türleri

| Tür | Sembol | Evrenin yüzdesi |
|---|---|---|
{tur_satir}

> "Borsada yok" ile "bozuk tick" AYRI sayılır. Birincisi evren listesinin
> güncelliğiyle ilgilidir, ikincisi sağlayıcının kalitesiyle — ve farklı
> şeyler yapmayı gerektirir.
>
> Bozuk tick'li semboller **onarılmadı, elendi.** Veriyi sessizce düzeltmek,
> ölçümün dayandığı zemini görünmez biçimde değiştirmek olurdu. Bedeli
> yukarıda yazılı ve K3/K4 raporlarının "ölçümün sınırları" bölümüne girmek
> zorunda: elenen semboller rastgele bir alt küme DEĞİL.

## Tam döküm

| Sembol | Tür | Mesaj |
|---|---|---|
{liste}
""",
        encoding="utf-8",
    )
    return hedef


if __name__ == "__main__":
    raise SystemExit(main())
