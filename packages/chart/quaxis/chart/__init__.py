"""quaxis.chart — ChartSpec v1 ve strateji komposerleri.

ADR-001 §4: çizim kütüphanesinden bağımsız, versiyonlu bir JSON sözleşmesi.
Motor (packages/teknik) tipli sonuç üretir, komposer onu ChartSpec'e çevirir,
çiziciler (web / PNG) ChartSpec'i okur. Katmanlar tek yöne akar.
"""

from .roller import AlanRol, CizgiRol, EtiketRol, IsaretRol, RozetRol, SeviyeRol, Yon
from .spec import SURUM, ChartSpec

__all__ = [
    "SURUM",
    "ChartSpec",
    "SeviyeRol",
    "AlanRol",
    "CizgiRol",
    "IsaretRol",
    "EtiketRol",
    "RozetRol",
    "Yon",
]
