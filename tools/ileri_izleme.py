"""İleriye dönük izleme — kural DONDURULDU, veri henüz yok.

    python tools/ileri_izleme.py

Çıktı: `docs/olcum/ileri-izleme-abcd-teyit.md`

## Neden bu araç var

`abcd·teyit` (AB=CD + KURAL-30 bir bar bekleme) ön kayıtlı ölçümde
p=0.0685 ile **reddedildi**. Reddedilmesinin sebebi sayının büyüklüğü
değil, nerede olduğuydu: etkinin tamamı IS penceresindeydi, görülmemiş
dönemde fark sıfırdı.

Geçmişte arama yapmak bitti. Bir kuralın gerçekten çalıştığını gösteren
tek meşru yol, **kural donduktan SONRA gelen veride** ölçmektir — çünkü o
veriye bakarak kimse hiçbir seçim yapmadı.

## Dondurma anı

`DONMA_TARIHI` bu aracın sözleşmesidir. Bu tarihten ÖNCEKİ hiçbir sinyal
rapora girmez; girseydi izleme, ölçülmüş ve reddedilmiş veriyi yeniden
sayıyor olurdu.

Parametreler de dondu: `AbcdParams()` varsayılanları K3'ten geldi ve
**değiştirilmeyecek**. Değiştirilirse bu dosya artık aynı kuralı
izlemiyor demektir; o zaman yeni bir dondurma tarihi ve yeni bir dosya
gerekir.

## Ne zaman karar verilir

Asgari **30 sembol** birikmeden verdikt yazılmaz (Pardo s.295). O eşiğe
gelindiğinde ölçüm `tools/harmonik_olcum.py` ile aynı makinede, aynı
maliyet varsayımlarıyla koşulur.
"""

from __future__ import annotations

import datetime as dt
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "packages" / "teknik")]
sys.stdout.reconfigure(encoding="utf-8")

import pandas as pd  # noqa: E402
from quaxis.teknik.core.types import Timeframe  # noqa: E402
from quaxis.teknik.indicators.harmonik import Abcd, AbcdParams  # noqa: E402

#: Kuralın donduğu an. `e5556aa` commit'i bu tarihte atıldı ve ön kayıt
#: `f989bf6` ile sonuç görülmeden yazılmıştı.
DONMA_TARIHI = dt.date(2026, 9, 14)

#: Verdikt yazılabilmesi için asgari bağımsız gözlem (sembol).
ASGARI_SEMBOL = 30


def teyitli_giris(df: pd.DataFrame, s) -> tuple[pd.Timestamp, float] | None:  # noqa: ANN001
    """KURAL-30: D'ye dokunulan bar sinyaldir, giriş DEĞİLDİR.

    `tools/harmonik_olcum.py::teyitli` ile AYNI kural. İki yerde iki farklı
    tanım olsaydı izleme, ölçtüğünü sandığı şeyi ölçmezdi.
    """
    i = df.index.get_loc(s.detected_at)
    if not isinstance(i, int) or i + 1 >= len(df):
        return None
    j = i + 1
    acilis, kapanis = float(df["open"].iloc[j]), float(df["close"].iloc[j])
    uzun = s.direction == "long"
    if (kapanis <= acilis) if uzun else (kapanis >= acilis):
        return None
    stop = float(s.payload["stop"])
    if (kapanis <= stop) if uzun else (kapanis >= stop):
        return None
    return df.index[j], kapanis


def main() -> int:
    kok = KOK / "data" / "ohlcv" / "bist"
    ded = Abcd(AbcdParams())
    esik = pd.Timestamp(DONMA_TARIHI, tz="UTC")

    kayitlar: list[tuple[str, pd.Timestamp, float, float, float]] = []
    veri_sonu: pd.Timestamp | None = None
    sembol_sayisi = 0

    for p in sorted(kok.iterdir()):
        f = p / "1D.parquet"
        if not f.exists():
            continue
        df = pd.read_parquet(f)
        if len(df) < 300:
            continue
        sembol_sayisi += 1
        df.attrs["timeframe"] = Timeframe.D1
        df.attrs["symbol"] = p.name
        veri_sonu = df.index[-1] if veri_sonu is None else max(veri_sonu, df.index[-1])
        for s in ded(df).signals:
            if s.direction != "long" or s.detected_at < esik:
                continue
            ucdu = teyitli_giris(df, s)
            if ucdu is None:
                continue
            t, giris = ucdu
            kayitlar.append(
                (p.name, t, giris, float(s.payload["stop"]), float(s.payload["hedef"]))
            )

    semboller = {k[0] for k in kayitlar}
    satir = [
        "# İleriye dönük izleme — `abcd·teyit`",
        "",
        f"**Koşu tarihi:** {dt.date.today().isoformat()} · "
        f"**Kuralın donduğu an:** {DONMA_TARIHI.isoformat()}",
        "",
        "Kural `docs/olcum/onkayit-harmonik-teyit.md`'de donduruldu ve "
        "`e5556aa` ile commit edildi. Bu rapor **yalnızca o tarihten sonra "
        "doğan** sinyalleri sayar.",
        "",
        "> Geçmişte arama yapmak bitti. Bir kuralın çalıştığını gösteren tek",
        "> meşru yol, kural donduktan SONRA gelen veride ölçmektir — o veriye",
        "> bakarak kimse hiçbir seçim yapmadı.",
        "",
        "| | |",
        "|---|---|",
        f"| Evren | {sembol_sayisi} BIST sembolü, 1G |",
        f"| Veri son barı | {veri_sonu.date() if veri_sonu is not None else '—'} |",
        f"| Dondurmadan sonraki sinyal | **{len(kayitlar)}** |",
        f"| Bağımsız gözlem | **{len(semboller)}** sembol |",
        f"| Verdikt için gereken | {ASGARI_SEMBOL} sembol (Pardo s.295) |",
        "",
    ]

    if len(semboller) < ASGARI_SEMBOL:
        satir += [
            "## Durum: **VERDİKT YOK**",
            "",
            f"Birikmiş gözlem {len(semboller)} sembol, eşik {ASGARI_SEMBOL}. "
            "Sayı yazılır, verdikt yazılmaz.",
            "",
            "Bu bir arıza değil, tasarım: kural bugün donduruldu ve veri "
            "henüz o tarihten sonrasını içermiyor. Eşik dolana kadar bu "
            "rapor boş kalacak ve **boş kalması doğru davranıştır.**",
            "",
        ]
    else:
        satir += [
            "## Durum: ölçüme hazır",
            "",
            "Eşik doldu. Ölçüm `tools/harmonik_olcum.py` ile AYNI makinede, "
            "aynı maliyet varsayımlarıyla koşulmalı; bu araç sinyal toplar, "
            "verdikt vermez.",
            "",
            "| sembol | giriş barı | giriş | stop | hedef |",
            "|---|---|---|---|---|",
        ]
        satir += [
            f"| {a} | {t.date()} | {g:.2f} | {s:.2f} | {h:.2f} |"
            for a, t, g, s, h in kayitlar[:50]
        ]
        satir.append("")

    hedef = KOK / "docs" / "olcum" / "ileri-izleme-abcd-teyit.md"
    hedef.write_text("\n".join(satir) + "\n", encoding="utf-8")
    print("\n".join(satir))
    print(f"\nyazıldı: {hedef.relative_to(KOK)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
