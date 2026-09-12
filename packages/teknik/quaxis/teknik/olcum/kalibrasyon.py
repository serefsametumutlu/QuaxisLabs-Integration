"""K3 — kalibrasyon: tam evrende aday sayısı.

Bir göstergenin eşikleri oturmuş mu? İki yönlü bozulma var ve ikisi de
sessizdir:

- **Sıfıra yakın aday** → gösterge bozuk. Önceki projede `breakout_fvg` ve
  `flag_pennant` 4S'te **648/648 sembolde sıfır aday** veriyordu ve bu çok
  sonra fark edildi. Tarama "başarıyla tamamlandı" diyordu çünkü hata yoktu —
  yalnızca sonuç yoktu.
- **On binlerce aday** → eşik çok gevşek; her şey sinyal olunca hiçbir şey
  sinyal değildir.

Bu yüzden rapor **her zaman** sıfır aday veren sembol sayısını taşır.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CalibrationResult:
    indicator: str
    timeframe: str
    universe: int
    total_candidates: int
    zero_candidate_symbols: int
    error_symbols: int
    per_symbol_mean: float
    per_symbol_median: float
    per_symbol_max: int

    @property
    def zero_ratio(self) -> float:
        return self.zero_candidate_symbols / self.universe if self.universe else 1.0

    @property
    def diagnosis(self) -> str:
        """Düz Türkçe teşhis — rapora olduğu gibi yazılır."""
        if self.universe == 0:
            return "Evren boş; ölçüm yapılmadı."
        if self.zero_ratio >= 0.95:
            return (
                f"BOZUK: sembollerin %{self.zero_ratio * 100:.0f}'i sıfır aday verdi. "
                f"Gösterge tam evrende neredeyse hiç çalışmıyor — eşikler ya da "
                f"zaman dilimi ölçeklemesi gözden geçirilmeli."
            )
        if self.per_symbol_mean > 50:
            return (
                f"ÇOK GEVŞEK: sembol başına ortalama {self.per_symbol_mean:.1f} aday. "
                f"Her şey sinyal olunca hiçbir şey sinyal değildir; eşik sıkılaştırılmalı."
            )
        if self.zero_ratio >= 0.5:
            return (
                f"DAR: sembollerin %{self.zero_ratio * 100:.0f}'i sıfır aday verdi. "
                f"Kabul edilebilir olabilir ama gerekçesi pasaporta yazılmalı."
            )
        return (
            f"MAKUL: sembol başına ortalama {self.per_symbol_mean:.1f} aday, "
            f"sembollerin %{self.zero_ratio * 100:.0f}'i sıfır."
        )


def calibrate(
    indicator: str,
    timeframe: str,
    per_symbol: dict[str, int],
    *,
    error_symbols: int = 0,
) -> CalibrationResult:
    """`per_symbol`: {sembol: aday sayısı}. Hata alan semboller ayrı sayılır —
    sıfır aday ile "veri çekilemedi" aynı şey değildir."""
    sayilar = np.array(list(per_symbol.values()), dtype=float) if per_symbol else np.array([0.0])
    return CalibrationResult(
        indicator=indicator,
        timeframe=timeframe,
        universe=len(per_symbol),
        total_candidates=int(sayilar.sum()),
        zero_candidate_symbols=int((sayilar == 0).sum()),
        error_symbols=error_symbols,
        per_symbol_mean=float(sayilar.mean()),
        per_symbol_median=float(np.median(sayilar)),
        per_symbol_max=int(sayilar.max()),
    )
