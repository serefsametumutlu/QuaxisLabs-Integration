"""Salınım pivotları ve ALMAŞIK zincir — harmonik formasyonların iskeleti.

Harmonik bir formasyon, birbirini izleyen ve yönü sırayla değişen salınım
uçlarından ibarettir: tepe → dip → tepe → dip. Bu modül o zinciri kurar.

## Neden ayrı bir zincir

Ham pivot listesi almaşık DEĞİLDİR: art arda iki tepe (arada onaylı bir dip
olmadan) çıkabilir. Formasyon oranları ise `(C-B)/(A-B)` gibi **yön
değiştiren bacaklara** dayanır; almaşık olmayan bir listede bu oranlar
anlamsızdır. Zincir, art arda gelen aynı türden pivotlardan yalnız **en
uç olanı** tutar.

## Non-repaint

Zincir **ileri doğru** kurulur ve geçmişi asla düzeltmez:

* Bir pivot ancak `onay_i` barında zincire GİREBİLİR (`i + sag`).
* `onay_i = i + sag` sabit kaydırma olduğu için pivotlar `i` sırasıyla
  onaylanır; zincir kurulum sırası veriden bağımsızdır.
* Aynı türden daha uç bir pivot geldiğinde zincirin SON halkası değişir —
  ama bu değişim yalnız o pivotun onay barında ve sonrasında görünür.
  `t` barında yeniden hesaplandığında aynı zincir çıkar.

Bu yüzden `t` anında kurulan bir formasyon geriye dönük "aslında şuradaydı"
diye kaydırılamaz.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Pivot:
    """Onaylı bir salınım ucu."""

    i: int
    """Ucun KENDİ barı — grafikte buraya çizilir."""
    fiyat: float
    tepe: bool
    onay_i: int
    """Ucun BİLİNEBİLİR olduğu bar. Bundan önce kullanmak repaint'tir."""


def _tek_yon(seri: np.ndarray, sol: int, sag: int, *, tepe: bool) -> list[Pivot]:
    out: list[Pivot] = []
    n = len(seri)
    for i in range(sol, n - sag):
        pencere = seri[i - sol : i + sag + 1]
        uc = seri[i]
        if (tepe and uc == pencere.max()) or (not tepe and uc == pencere.min()):
            out.append(Pivot(i, float(uc), tepe, i + sag))
    return out


def pivotlar(yuksek: np.ndarray, dusuk: np.ndarray, sol: int, sag: int) -> list[Pivot]:
    """Tepe ve dip pivotları, onay sırasına göre birleştirilmiş.

    Aynı barda hem tepe hem dip oluşabilir (dar aralıklı bir bar iki
    pencerenin de ucu olabilir). Sıralama `(i, tepe)` ile deterministik
    yapılır — aksi hâlde aynı veri iki farklı zincir üretebilirdi.
    """
    hepsi = _tek_yon(yuksek, sol, sag, tepe=True) + _tek_yon(dusuk, sol, sag, tepe=False)
    hepsi.sort(key=lambda p: (p.i, p.tepe))
    return hepsi


def zincire_ekle(zincir: list[Pivot], p: Pivot) -> bool:
    """Pivotu almaşık zincire ekler. Zincir DEĞİŞTİYSE True döner.

    Üç durum:

    * Zincir boş → eklenir.
    * Son halka TERS türden → eklenir (almaşıklık korunur).
    * Son halka AYNI türden → yalnız daha uçtaysa halkayı DEĞİŞTİRİR.
      Daha uç değilse hiçbir şey olmaz; iç içe geçmiş bir salınım yeni bir
      bacak yaratmaz.
    """
    if not zincir:
        zincir.append(p)
        return True
    son = zincir[-1]
    if son.tepe != p.tepe:
        zincir.append(p)
        return True
    daha_uc = p.fiyat > son.fiyat if p.tepe else p.fiyat < son.fiyat
    if daha_uc:
        zincir[-1] = p
        return True
    return False
