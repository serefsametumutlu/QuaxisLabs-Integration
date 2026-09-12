"""Ekran görüntüsünden bölge kırpar — görsel kabul döngüsünün "yakından bak" adımı.

Tam sayfa görüntüler küçültülerek okunduğu için ince kusurlar (glif eksikliği,
1px hizasızlık, kontrast) görünmez. Bu betik ilgili bölgeyi 1:1 ya da
büyütülmüş olarak ayrı bir dosyaya yazar.

    python tools/kirp.py docs/design/ui/tasarim-koyu-1440-i1.png 0 300 1440 900 --olcek 1
"""

from __future__ import annotations

import argparse
import pathlib
import sys

from PIL import Image

CIKTI = pathlib.Path(__file__).resolve().parents[1] / "docs" / "design" / "_gecici"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("kaynak")
    ap.add_argument("x", type=int)
    ap.add_argument("y", type=int)
    ap.add_argument("w", type=int)
    ap.add_argument("h", type=int)
    ap.add_argument("--olcek", type=float, default=1.0)
    ap.add_argument("--ad", default=None)
    args = ap.parse_args()

    CIKTI.mkdir(parents=True, exist_ok=True)
    im = Image.open(args.kaynak)
    kutu = (args.x, args.y, min(args.x + args.w, im.width), min(args.y + args.h, im.height))
    parca = im.crop(kutu)
    if args.olcek != 1.0:
        boy = (int(parca.width * args.olcek), int(parca.height * args.olcek))
        parca = parca.resize(boy, Image.LANCZOS)

    ad = args.ad or f"{pathlib.Path(args.kaynak).stem}-{args.x}x{args.y}.png"
    hedef = CIKTI / ad
    parca.save(hedef)
    print(f"{hedef}  {parca.width}x{parca.height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
