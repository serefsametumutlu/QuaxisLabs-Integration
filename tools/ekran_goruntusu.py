"""Görsel kabul döngüsü — /tasarim sayfasının ekran görüntülerini alır.

README kural 5: her görsel iş ekran görüntüsüyle doğrulanır, en az 3 iterasyon.
Bu betik o döngünün "al" adımıdır; "bak ve düzelt" adımı insana/agent'a aittir.

Önce statik dışa aktarım üretilir:

    cd apps/web && npm run build:vitrin      # -> apps/web/out

Sonra bu betik `out/` klasörünü KENDİ İÇİNDE servis eder (ayrı bir geliştirme
sunucusu açmaya gerek yok), ekran görüntülerini alır ve çıkar:

    python tools/ekran_goruntusu.py --etiket i1

Üç tema × iki genişlik = altı görüntü.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import pathlib
import socketserver
import sys
import threading

from playwright.sync_api import sync_playwright

# (dosya eki, ?tema= değeri, tarayıcıya dayatılan prefers-color-scheme)
TEMALAR = [
    ("koyu", "dark", "dark"),
    ("acik", "light", "light"),
    ("sistem", "system", "light"),  # sistem açıkken koyuda kalmadığı görülsün
]

GENISLIKLER = [1440, 768]

KOK = pathlib.Path(__file__).resolve().parents[1]


class SessizSunucu(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):  # noqa: D102 - sessiz
        pass


def sunucu_ac(dizin: pathlib.Path) -> tuple[socketserver.TCPServer, int]:
    islem = functools.partial(SessizSunucu, directory=str(dizin))
    httpd = socketserver.TCPServer(("127.0.0.1", 0), islem)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kaynak", default=str(KOK / "apps" / "web" / "out"))
    ap.add_argument("--yol", default="/tasarim.html")
    ap.add_argument("--cikti", default=str(KOK / "docs" / "design" / "ui"))
    ap.add_argument("--etiket", default="i1", help="iterasyon etiketi: i1, i2, i3…")
    ap.add_argument("--ad", default="tasarim")
    ap.add_argument(
        "--pencere", action="store_true", help="tam sayfa yerine yalnız görünen pencere"
    )
    ap.add_argument(
        "--tema",
        default=None,
        choices=[t[0] for t in TEMALAR],
        help="yalnız bu temayı al (varsayılan: üçü de)",
    )
    args = ap.parse_args()

    temalar = [t for t in TEMALAR if args.tema is None or t[0] == args.tema]

    # Git Bash, "/tarama.html" gibi baştan eğik çizgili argümanları Windows
    # yoluna çevirir. Eğik çizgisiz de kabul edip burada tamamlıyoruz.
    yol = args.yol if args.yol.startswith("/") else "/" + args.yol

    kaynak = pathlib.Path(args.kaynak)
    if not (kaynak / "tasarim.html").exists():
        print(
            f"HATA: {kaynak} içinde dışa aktarım yok. "
            "Önce: cd apps/web && npm run build:vitrin",
            file=sys.stderr,
        )
        return 2

    cikti = pathlib.Path(args.cikti)
    cikti.mkdir(parents=True, exist_ok=True)

    httpd, port = sunucu_ac(kaynak)
    yazilan: list[pathlib.Path] = []
    try:
        with sync_playwright() as p:
            tarayici = p.chromium.launch()
            try:
                for ek, tema, sema in temalar:
                    for w in GENISLIKLER:
                        ctx = tarayici.new_context(
                            viewport={"width": w, "height": 900},
                            device_scale_factor=1,
                            color_scheme=sema,
                            reduced_motion="reduce",  # iskelet parıltısı kareyi bulandırmasın
                            locale="tr-TR",
                        )
                        sayfa = ctx.new_page()
                        # Yol zaten sorgu taşıyorsa tema `&` ile eklenir.
                        # `?tema=` yapıştırmak `grafik.html?f=x?tema=koyu`
                        # üretiyordu ve ikinci `?` sorgunun geri kalanını
                        # sessizce tek bir değerin içine gömüyordu.
                        ayrac = "&" if "?" in yol else "?"
                        url = f"http://127.0.0.1:{port}{yol}{ayrac}tema={tema}"
                        sayfa.goto(url, wait_until="networkidle")
                        sayfa.wait_for_timeout(400)  # font yüklemesi otursun
                        hedef = cikti / f"{args.ad}-{ek}-{w}-{args.etiket}.png"
                        sayfa.screenshot(path=str(hedef), full_page=not args.pencere)
                        yazilan.append(hedef)
                        ctx.close()
            finally:
                tarayici.close()
    finally:
        httpd.shutdown()
        httpd.server_close()

    for y in yazilan:
        print(f"{y}  ({y.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
