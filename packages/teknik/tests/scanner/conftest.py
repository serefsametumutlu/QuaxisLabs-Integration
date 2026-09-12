"""`scanner/` alt klasöründeki testler de test yardımcılarını düz `import`
ile bulsun (bkz. üst klasördeki conftest)."""

from __future__ import annotations

import pathlib
import sys

TESTLER = pathlib.Path(__file__).resolve().parents[1]
if str(TESTLER) not in sys.path:
    sys.path.insert(0, str(TESTLER))
