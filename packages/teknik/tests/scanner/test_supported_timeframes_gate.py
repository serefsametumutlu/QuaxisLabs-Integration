"""`engine.run()`'ın desteklenen-zaman-dilimi kapısı: desteklenmeyen bir
(gösterge, zaman dilimi) çifti için HİÇ İŞ AÇILMAMALI.

Bu, eski depoda ölçülmüş bir hatanın testidir: D1-only bir gösterge 4H'te
sessizce koşuyor, W1 destekleyen bir gösterge W1'i hiç görmüyordu. Kapı
sessiz kalmaz — atlanan çift `skipped_unsupported` ile RAPORLANIR.

Tamamen çevrimdışı: desteklenmeyen çift hiçbir veri çekimine ulaşmaz, bu
yüzden `universe=[]` yeterli. Göstergeler test kataloğundan gelir.
"""

from __future__ import annotations

from _ornek_katalog import KATALOG_ADRESI
from quaxis.teknik.core.types import Market, Timeframe
from quaxis.teknik.scanner import engine


def test_d1_only_gosterge_4h_te_atlanir() -> None:
    scan = engine.run(
        run_id="test_kapi", universe=[], timeframes=[Timeframe.H4],
        indicator_names=["test.rank"], market=Market.BIST,
        catalog=KATALOG_ADRESI, workers=1,
    )
    assert scan.results == []
    assert scan.skipped_unsupported == [{"indicator": "test.rank", "timeframe": "4H"}]


def test_desteklenen_zaman_diliminde_atlanmaz() -> None:
    scan = engine.run(
        run_id="test_kapi_ok", universe=[], timeframes=[Timeframe.D1],
        indicator_names=["test.rank"], market=Market.BIST,
        catalog=KATALOG_ADRESI, workers=1,
    )
    assert scan.skipped_unsupported == []


def test_karisik_zaman_dilimlerinde_yalniz_desteklenmeyen_atlanir() -> None:
    """`test.honest_sma_cross` hem D1 hem 4H destekler; `test.centered_pivot`
    yalnız D1. İkisi birlikte istendiğinde YALNIZCA ikincisinin 4H'si atlanır."""
    scan = engine.run(
        run_id="test_kapi_karisik", universe=[], timeframes=[Timeframe.D1, Timeframe.H4],
        indicator_names=["test.honest_sma_cross", "test.centered_pivot"],
        market=Market.BIST, catalog=KATALOG_ADRESI, workers=1,
    )
    assert scan.skipped_unsupported == [{"indicator": "test.centered_pivot", "timeframe": "4H"}]


def test_katalogda_olmayan_gosterge_sessizce_atlanir() -> None:
    """Katalogda olmayan bir ad iş üretmez ve patlamaz — tarama bir listeyi
    körlemesine koşabilmeli."""
    scan = engine.run(
        run_id="test_kapi_yok", universe=[], timeframes=[Timeframe.D1],
        indicator_names=["yok.boyle.bir.sey"], market=Market.BIST,
        catalog=KATALOG_ADRESI, workers=1,
    )
    assert scan.results == []
    assert scan.skipped_unsupported == []
