"""ChartSpec çıktılarını üretir: JSON şeması + örnek spec.

    python packages/chart/uret.py

Çıktılar:
  packages/chart/sema/chartspec-1.0.schema.json   dilden bağımsız sözleşme
  apps/web/ornek/thyao-swing-fib-abcd.chartspec.json web çizicisinin girdisi

Web çizicisi bu JSON'u okur — TypeScript tarafında elle kurulmuş bir nesneyi
değil. Sözleşme ancak dil sınırını geçince sözleşmedir.
"""

from __future__ import annotations

import json
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from quaxis.chart.komposer.swing_fib_abcd import bestele  # noqa: E402
from quaxis.chart.ornek.thyao_swing_fib_abcd import sonuc  # noqa: E402
from quaxis.chart.sema import sema  # noqa: E402


def main() -> int:
    sema_yolu = pathlib.Path(__file__).resolve().parent / "sema" / "chartspec-1.0.schema.json"
    sema_yolu.parent.mkdir(parents=True, exist_ok=True)
    sema_yolu.write_text(json.dumps(sema(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    spec = bestele(sonuc(), ornek_mi=True)
    spec_yolu = KOK / "apps" / "web" / "ornek" / "thyao-swing-fib-abcd.chartspec.json"
    spec_yolu.parent.mkdir(parents=True, exist_ok=True)
    spec_yolu.write_text(spec.json(), encoding="utf-8")

    for p in (sema_yolu, spec_yolu):
        print(f"{p.relative_to(KOK)}  ({p.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
