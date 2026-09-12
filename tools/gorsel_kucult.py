"""Ekran görüntülerini depoya girmeden önce küçültür.

Düz renkli arayüz görüntüleri 256 renge indirgendiğinde gözle ayırt edilemez
ama dosya ~4 kat küçülür. ADR-001'in dersi: depo geçmişine büyük ikili dosya
sokmak geri alınamaz bir hatadır.

    python tools/gorsel_kucult.py docs/design/ui
"""

from __future__ import annotations

import pathlib
import sys

from PIL import Image


def main() -> int:
    if len(sys.argv) < 2:
        print("kullanım: python tools/gorsel_kucult.py <klasör>", file=sys.stderr)
        return 2
    klasor = pathlib.Path(sys.argv[1])
    toplam_once = toplam_sonra = 0
    for p in sorted(klasor.glob("*.png")):
        once = p.stat().st_size
        im = Image.open(p).convert("RGB")
        kucuk = im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
        kucuk.save(p, optimize=True)
        sonra = p.stat().st_size
        toplam_once += once
        toplam_sonra += sonra
        print(f"{p.name}  {once // 1024} KB -> {sonra // 1024} KB")
    if toplam_once:
        print(f"toplam  {toplam_once // 1024} KB -> {toplam_sonra // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
