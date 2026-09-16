"""Tarama sonucu → web köprüsü: `results.db` okunur, derleme anında
okunacak bir JSON yazılır.

    python tools/tarama_disaktar.py
    python tools/tarama_disaktar.py --azami-yas 10 --azami-satir 500

Çıktı: `apps/web/lib/tarama-verisi.json`

## Neden derleme anında JSON, neden istek anında SQLite değil

Tarama **günde bir kere** koşuyor (kapanış sonrası). İstek anında veritabanı
okumak tazelik kazandırmaz, karşılığında iki şey kaybettirirdi: statik dışa
aktarım (`QUAXIS_EXPORT=1`, görsel kabul döngüsünün dayandığı şey) kırılır ve
web doğrudan motorun deposuna bağlanır — mimarideki tek yönlü ok
(`Veri → … → Depo → Görselleştirme`) tersine akmaya başlar.

## Verdikt rozeti nereden geliyor

Uydurulmuyor. Her satırın göstergesi, pasaport künyelerindeki `gostergeler:`
eşlemesiyle bir pasaporta bağlanır; rozet o pasaportun `verdikt` alanıdır.
`python tools/pasaport.py dogrula` katalogdaki her göstergenin TAM BİR
pasaport tarafından sahiplenildiğini denetler, yani rozetsiz satır üretmek
mümkün değil.

## Şirket adı neden yok

Evren dosyasında sembol var, şirket adı yok; başka bir kaynağımız da yok.
Maket veride "Türk Hava Yolları" yazıyordu çünkü elle yazılmıştı. Gerçek
veride elimizde olmayan bir alanı doldurmak, maket veriyi gerçek diye
sunmanın başka bir biçimi olurdu — o yüzden alan YOK, tabloda yalnız sembol
duruyor.

## Kesilen satırlar

Evren 648 sembol; bir gösterge zincirinin en güncel durumu yıllar öncesine
ait olabilir (`bars_ago` binlerce bar). Tamamını JSON'a gömmek hem gereksiz
hem büyük. `--azami-satir` ile kesilir, KESİLEN SAYI künyeye yazılır ve
arayüz onu gösterir — sessiz kırpma yasak.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "packages" / "teknik"))
sys.path.insert(0, str(KOK / "tools"))

for akis in (sys.stdout, sys.stderr):
    if hasattr(akis, "reconfigure"):
        akis.reconfigure(encoding="utf-8", errors="replace")

import pasaport as pasaport_araci  # noqa: E402
from quaxis.teknik.core.types import Market, Timeframe  # noqa: E402
from quaxis.teknik.data.providers.yfinance_provider import YFinanceProvider  # noqa: E402
from quaxis.teknik.data.store import Store  # noqa: E402
from quaxis.teknik.scanner.results import DEFAULT_DB_PATH, ResultsStore  # noqa: E402

CIKTI = KOK / "apps" / "web" / "lib" / "tarama-verisi.json"

#: Künyedeki `paket` → arayüzdeki paket adı. Sol raydaki paket listesiyle
#: aynı sözcükler; iki yerde iki ad olursa kullanıcı iki şey sanır.
PAKET_ADI = {
    "yapi": "Yapı",
    "formasyon": "Formasyon",
    "trend": "Trend & Momentum",
    "arbitraj": "İstatistiksel Arbitraj",
}

#: `SignalState` → arayüzde görünen durum. Kapalı küme: tanınmayan durum
#: sessizce geçmez, `ValueError` atar (ChartSpec rol kuralının aynısı).
DURUM_ADI = {
    "pending": "Bekliyor",
    "active": "Bölgede",
    "confirmed": "Onaylandı",
    "invalidated": "Geçersiz",
    "completed": "Tamamlandı",
    "expired": "Süre doldu",
}

#: Künyedeki `verdikt` → arayüzdeki rozet metni.
VERDIKT_ADI = {
    "olculmedi": "ölçülmedi",
    "kanitlanmadi": "kanıtlanmadı",
    "izlenen-aday": "izlenen aday",
    "kenar-var": "kenar var",
}

#: Sparkline uzunluğu — maketteki ile aynı.
SERI_BAR = 22

#: Zaman dilimi kodu → arayüzde görünen ad. Ürün Türkçe: gün "G", saat "S",
#: hafta "Hf". Kod tarafı `Timeframe` enum'unun kanonik (BÜYÜK harf) yazımını
#: kullanır; koşu kaydında küçük harfle duruyor olabilir (`run_eod` argümanı
#: öyle geliyor) ve iki yazım karşılaştırılırsa filtre HİÇBİR satırı tutmaz.
#: Bu yüzden künyeye kanonik yazım yazılır.
ZAMAN_DILIMI_ADI = {"1H": "1S", "4H": "4S", "1D": "1G", "W1": "1Hf"}


def gosterge_haritasi() -> dict[str, dict[str, str]]:
    """gösterge adı → {etiket, paket, verdikt, pasaport}.

    Kaynak pasaport künyeleridir. Bir gösterge sahipsizse burada da yoktur
    ve dışa aktarım o satırda DURUR — rozetsiz satır üretmektense gürültülü
    biçimde patlamak yeğdir.
    """
    harita: dict[str, dict[str, str]] = {}
    for pas in pasaport_araci.pasaportlar():
        paket = str(pas.kunye.get("paket", "")).strip()
        verdikt = str(pas.kunye.get("verdikt", "olculmedi")).strip()
        for ad, etiket in (pas.kunye.get("gostergeler") or {}).items():
            harita[str(ad)] = {
                "etiket": str(etiket),
                "paket": PAKET_ADI.get(paket, paket),
                "verdikt": VERDIKT_ADI.get(verdikt, verdikt),
                "pasaport": pas.slug,
            }
    return harita


def _seri_ve_fiyat(store: Store, sembol: str, tf: str, market: Market):
    """Son `SERI_BAR` kapanış + en son kapanış. Veri yoksa (None, None)."""
    try:
        df = store.get(sembol, Timeframe(tf), market)
    except (FileNotFoundError, ValueError):
        return None, None
    kapanis = df["close"].tail(SERI_BAR)
    if kapanis.empty:
        return None, None
    return [round(float(x), 4) for x in kapanis], round(float(kapanis.iloc[-1]), 4)


def disaktar(args: argparse.Namespace) -> int:
    harita = gosterge_haritasi()
    market = Market(args.market.lower())

    with ResultsStore(db_path=DEFAULT_DB_PATH) as depo:
        run_id = args.run_id or depo.latest_run(market.value)
        if run_id is None:
            print("Tamamlanmış run yok. Önce `python tools/tarama.py kos`.", file=sys.stderr)
            return 1
        kayit = depo.get_run(run_id)
        ham, toplam = depo.latest_signals(
            run_id, max_bars_ago=args.azami_yas, limit=args.azami_satir
        )
        kalite = depo.data_quality_summary(run_id)

    bilinmeyen = sorted({s["indicator"] for s in ham} - set(harita))
    if bilinmeyen:
        print(
            f"HATA: şu göstergeler hiçbir pasaportta sahiplenilmemiş: {bilinmeyen}\n"
            "`python tools/pasaport.py dogrula` bunu söyler; künyeye `gostergeler:` ekle.",
            file=sys.stderr,
        )
        return 2

    store = Store(YFinanceProvider())
    seri_onbellek: dict[str, tuple] = {}
    satirlar = []
    veri_yok = 0
    for s in ham:
        k = harita[s["indicator"]]
        # Fiyat serisi SATIRA değil SEMBOLE aittir: aynı sembolün iki
        # stratejisi aynı seriyi taşır. Satır başına gömülünce 2000 satırlık
        # çıktı 1.3 MB'a çıkıyordu ve bu dosya istemci paketine giriyor.
        anahtar = f"{s['symbol']}|{s['timeframe']}"
        if anahtar not in seri_onbellek:
            seri_onbellek[anahtar] = _seri_ve_fiyat(store, s["symbol"], s["timeframe"], market)
        seri, fiyat = seri_onbellek[anahtar]
        if seri is None:
            veri_yok += 1
            continue
        yuk = json.loads(s["payload_json"])
        durum = DURUM_ADI.get(s["state"])
        if durum is None:
            raise ValueError(f"tanınmayan sinyal durumu: {s['state']!r}")
        satirlar.append(
            {
                "id": f"{s['symbol']}-{s['timeframe']}-{s['indicator']}-{s['pattern_id']}",
                "sembol": s["symbol"],
                "zamanDilimi": s["timeframe"],
                "paket": k["paket"],
                "strateji": k["etiket"],
                "gosterge": s["indicator"],
                "pasaport": k["pasaport"],
                "yon": "up" if s["direction"] == "long" else "down",
                "durum": durum,
                "yas": s["bars_ago"],
                "fiyat": fiyat,
                "seviye": _yuvarla(yuk.get("giris")),
                "stop": _yuvarla(yuk.get("stop")),
                "hedef": _yuvarla(yuk.get("hedef")),
                "seriAnahtari": anahtar,
                "verdikt": k["verdikt"],
            }
        )

    paket_sayaci: dict[str, int] = {}
    for r in satirlar:
        paket_sayaci[r["paket"]] = paket_sayaci.get(r["paket"], 0) + 1

    # Kanonik yazım: koşu kaydındaki ("1d") ile sinyaldeki ("1D") ayrışmasın.
    zaman_dilimleri = [
        {"kod": kod, "ad": ZAMAN_DILIMI_ADI.get(kod, kod)}
        for kod in sorted({str(z).upper() for z in (kayit.timeframes if kayit else [])})
    ]
    for kod in sorted({r["zamanDilimi"] for r in satirlar}):
        if not any(z["kod"] == kod for z in zaman_dilimleri):
            zaman_dilimleri.append({"kod": kod, "ad": ZAMAN_DILIMI_ADI.get(kod, kod)})

    cikti = {
        "kunye": {
            "runId": run_id,
            "tarih": run_id.split("_", 1)[-1],
            "market": market.value,
            "zamanDilimleri": zaman_dilimleri,
            "evren": kayit.universe_size if kayit else None,
            # Evren listesi ile GERÇEKTEN taranan ayrı sayılardır: 23 sembolde
            # sağlayıcı veri döndürmüyor. "648 sembol tarandı" demek, hiç
            # bakılmayan sembolleri bakılmış göstermek olurdu.
            "taranan": len(kalite.get("ok", [])),
            "verisiGelmeyen": sorted(
                s for durum, ss in kalite.items() if durum != "ok" for s in ss
            ),
            "gitSha": kayit.git_sha if kayit else None,
            "sureSn": _sure_sn(kayit),
            "uretildi": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
            "eslesen": toplam,
            "yazilan": len(satirlar),
            "kesilen": max(toplam - len(ham), 0),
            "veriYok": veri_yok,
            "azamiYas": args.azami_yas,
        },
        "sayaclar": {"paket": paket_sayaci, "sembol": len({r["sembol"] for r in satirlar})},
        "seriler": {
            anahtar: deger[0]
            for anahtar, deger in sorted(seri_onbellek.items())
            if deger[0] is not None
        },
        "satirlar": satirlar,
    }
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    # Girintisiz: üretilen ve makine tarafından okunan bir dosya. `indent=1`
    # 22 elemanlı her seriyi 22 satıra yayıyordu ve dosyayı ikiye katlıyordu;
    # bu dosya istemci paketine giriyor.
    CIKTI.write_text(
        json.dumps(cikti, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )

    try:
        gosterilen = CIKTI.relative_to(KOK)
    except ValueError:  # depo dışına yazılmışsa (testlerde tmp_path) tam yol
        gosterilen = CIKTI
    print(f"{gosterilen} yazıldı.")
    print(f"  run: {run_id} · eşleşen {toplam} · yazılan {len(satirlar)} · kesilen "
          f"{cikti['kunye']['kesilen']} · verisi olmayan {veri_yok}")
    for paket, n in sorted(paket_sayaci.items(), key=lambda kv: -kv[1]):
        print(f"  {paket}: {n}")
    return 0


def _yuvarla(x) -> float | None:
    return None if x is None else round(float(x), 4)


def _sure_sn(kayit) -> int | None:
    """Taramanın gerçek süresi. Arayüzde "6dk 22sn" elle yazılıydı; buradan
    gelmezse orada yine bir sayı uydurulur."""
    if kayit is None or not kayit.finished_at:
        return None
    bas = dt.datetime.fromisoformat(kayit.started_at)
    son = dt.datetime.fromisoformat(kayit.finished_at)
    return int((son - bas).total_seconds())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--market", default="bist")
    ap.add_argument("--run-id", default=None, dest="run_id")
    ap.add_argument(
        "--azami-yas", type=int, default=None, dest="azami_yas",
        help="yalnız bu kadar bar içinde doğmuş sinyaller (varsayılan: sınır yok)",
    )
    ap.add_argument("--azami-satir", type=int, default=10_000, dest="azami_satir")
    return disaktar(ap.parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
