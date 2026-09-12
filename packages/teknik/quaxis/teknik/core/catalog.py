"""Gösterge kataloğu — tarayıcının gösterge paketine bağımlılığını KESEN arayüz.

Eski depoda `scanner/engine.py` ve `scanner/eod.py` doğrudan
`tlab.indicators.bootstrap`'ten `CATALOG`, `populate_registry` ve
`scaled_factory` alıyordu. Bu, katman ayrımı kuralının (README madde 2:
`Veri → Özellik → Gösterge → Tarayıcı`) tersine akan tek yeriydi: tarayıcı
somut bir gösterge paketini tanıyordu ve o paket olmadan import bile
edilemiyordu.

Burada bağımlılık tersine çevrilir. Motor artık yalnız bu ARAYÜZÜ bilir;
göstergeler (ADR-002 gereği Bölüm C'de sıfırdan yazılacak) kendi
kataloglarını kurup motora VERİR. Motorun hiçbir göstergeyi tanımaması
sayesinde altyapı, tek bir gösterge yazılmadan da test edilebilir.
"""

from __future__ import annotations

import importlib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

import pandas as pd
from quaxis.teknik.core.errors import RegistryError
from quaxis.teknik.core.indicator import Registry
from quaxis.teknik.core.indicator import registry as default_registry
from quaxis.teknik.core.types import Timeframe


@dataclass(frozen=True)
class IndicatorSpec:
    """Bir göstergenin katalog künyesi. Göstergenin KENDİSİ değil, motorun
    iş açmak için bilmesi gereken asgari bilgi."""

    name: str
    category: str
    #: `() -> BaseIndicator | UniverseIndicator`. Kesin bir union yazılmıyor:
    #: tekil / pair / universe çağıranlarının `__call__` imzaları farklı.
    factory: Any
    #: `compute(df, context)` ikinci bir sembol ister mi (pair göstergeleri).
    needs_context: bool = False
    #: Evren-geneli gösterge: motor sembol başına iş AÇMAZ, evrenin tamamını
    #: tek işte verir (bkz. `core/indicator.py::UniverseIndicator`).
    needs_universe: bool = False
    #: Göstergenin KENDİ `meta.supported_timeframes`'inin izdüşümü. Motor
    #: desteklenmeyen (gösterge, zaman dilimi) çifti için iş HİÇ AÇMAZ.
    supported_timeframes: tuple[Timeframe, ...] = ()


@dataclass
class Catalog:
    """Adlandırılmış gösterge künyeleri + ölçekli örnek üretimi.

    Motor bunu bir ARGÜMAN olarak alır; global bir modülden okumaz. Böylece
    testler kendi küçük kataloglarını verebilir ve tarama motoru gerçek
    göstergeler olmadan da uçtan uca koşabilir.
    """

    specs: dict[str, IndicatorSpec] = field(default_factory=dict)

    # ------------------------------------------------------------- kurulum
    @classmethod
    def of(cls, specs: Iterable[IndicatorSpec] | Mapping[str, IndicatorSpec]) -> Catalog:
        if isinstance(specs, Mapping):
            return cls(dict(specs))
        return cls({s.name: s for s in specs})

    def add(self, spec: IndicatorSpec) -> None:
        if spec.name in self.specs:
            raise RegistryError(f"'{spec.name}' katalogda zaten var")
        self.specs[spec.name] = spec

    # -------------------------------------------------------------- okuma
    def get(self, name: str) -> IndicatorSpec | None:
        return self.specs.get(name)

    def names(self, category: str | None = None) -> list[str]:
        if category is None:
            return sorted(self.specs)
        return sorted(n for n, s in self.specs.items() if s.category == category)

    def __contains__(self, name: object) -> bool:
        return name in self.specs

    def __len__(self) -> int:
        return len(self.specs)

    # ------------------------------------------------------------- üretim
    def create(self, name: str, timeframe: Timeframe) -> Any:
        """Göstergeyi kurar ve parametrelerini zaman dilimine göre ÖLÇEKLER.

        Ölçeklemenin TEK yeri burasıdır. Eski depoda bunun gerekçesi şuydu:
        "grafikle tarama AYNI sonucu üretmeli" — iki çağıranın ayrı ayrı
        ölçeklemesi sessizce ayrışmaya yol açıyordu.

        Parametreyi yeni bir örnekle DEĞİŞTİRİR (fabrika imzasına dokunmaz):
        göstergelerin constructor imzaları birbirinden farklı olabilir,
        `params` ise hepsinde sıradan bir örnek özniteliğidir.
        """
        spec = self.specs.get(name)
        if spec is None:
            mevcut = ", ".join(sorted(self.specs)) or "(katalog boş)"
            raise RegistryError(f"'{name}' katalogda yok. Mevcut: {mevcut}")
        indicator = spec.factory()
        indicator.params = indicator.params.for_timeframe(timeframe)
        return indicator

    # ------------------------------------------------------------ registry
    def populate_registry(
        self,
        sample_df: pd.DataFrame,
        *,
        sample_context: dict[str, pd.DataFrame] | None = None,
        target: Registry | None = None,
    ) -> None:
        """Katalogdaki her göstergeyi repaint doğrulamasından geçirip
        registry'ye kaydeder; zaten kayıtlıysa sessizce atlar.

        Evren-geneli göstergeler generic `repaint_test`'e giremez (farklı
        sözleşme) — onlar `register_verified_elsewhere` ile kaydedilir ve
        non-repaint sözleşmeleri kendi hedefli testlerinde doğrulanır.
        """
        reg = target if target is not None else default_registry
        for spec in self.specs.values():
            instance = spec.factory()
            try:
                if spec.needs_universe:
                    reg.register_verified_elsewhere(instance)
                elif spec.needs_context:
                    reg.register(instance, sample_df, sample_context)
                else:
                    reg.register(instance, sample_df)
            except RegistryError as exc:
                if "zaten kayıtlı" in str(exc):
                    continue
                raise


#: Gösterge paketi henüz yok (ADR-002: Bölüm C'de sıfırdan yazılacak).
#: Motor boş katalogla da import edilebilir ve test edilebilir olmalı.
EMPTY_CATALOG = Catalog()

#: `load_catalog` için boş katalogun adresi.
EMPTY_CATALOG_REF = "quaxis.teknik.core.catalog:EMPTY_CATALOG"

_CACHE: dict[str, Catalog] = {}


def load_catalog(ref: str) -> Catalog:
    """`"modul.yolu:nitelik"` adresini `Catalog`'a çözer.

    Motorun işçileri AYRI SÜREÇLERDE koşar ve fabrikalar closure olabildiği
    için `Catalog` nesnesi pickle edilemez. Süreçler arasında yalnız bu ADRES
    taşınır; her süreç kataloğu kendi içinde bir kez çözüp önbelleğe alır.
    """
    onbellekli = _CACHE.get(ref)
    if onbellekli is not None:
        return onbellekli
    if ":" not in ref:
        raise RegistryError(
            f"Katalog adresi 'modul.yolu:nitelik' biçiminde olmalı, alınan: {ref!r}"
        )
    modul_yolu, nitelik = ref.split(":", 1)
    try:
        modul = importlib.import_module(modul_yolu)
    except ImportError as exc:
        raise RegistryError(f"Katalog modülü bulunamadı: {modul_yolu!r} ({exc})") from exc
    try:
        katalog = getattr(modul, nitelik)
    except AttributeError as exc:
        raise RegistryError(f"{modul_yolu!r} içinde {nitelik!r} yok") from exc
    if not isinstance(katalog, Catalog):
        raise RegistryError(f"{ref!r} bir Catalog değil: {type(katalog).__name__}")
    _CACHE[ref] = katalog
    return katalog
