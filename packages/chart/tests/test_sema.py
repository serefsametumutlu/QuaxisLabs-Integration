"""JSON şeması ile Python tarafı birbirinden ayrı düşmemeli."""

from __future__ import annotations

import copy

import jsonschema
import pytest
from quaxis.chart.komposer.swing_fib_abcd import bestele
from quaxis.chart.ornek.thyao_swing_fib_abcd import sonuc
from quaxis.chart.sema import sema


@pytest.fixture(scope="module")
def dogrulayici():
    s = sema()
    jsonschema.Draft202012Validator.check_schema(s)
    return jsonschema.Draft202012Validator(s)


@pytest.fixture(scope="module")
def belge():
    return bestele(sonuc(), ornek_mi=True).sozluk()


def test_ornek_spec_semaya_uyar(dogrulayici, belge):
    hatalar = sorted(dogrulayici.iter_errors(belge), key=lambda e: e.path)
    assert not hatalar, "\n".join(f"{list(h.path)}: {h.message}" for h in hatalar[:5])


def test_sema_bilinmeyen_rolu_reddeder(dogrulayici, belge):
    kotu = copy.deepcopy(belge)
    seviye = next(k for k in kotu["katmanlar"] if k["tur"] == "seviye")
    seviye["rol"] = "fib_999"
    assert list(dogrulayici.iter_errors(kotu)), "Şema bilinmeyen rolü kabul etti."


def test_sema_fazladan_alani_reddeder(dogrulayici, belge):
    kotu = copy.deepcopy(belge)
    kotu["katmanlar"][0]["renk"] = "#ff0000"
    hatalar = list(dogrulayici.iter_errors(kotu))
    assert hatalar, "Şema renk alanını kabul etti — ChartSpec renk TAŞIMAZ."


def test_sema_tek_noktali_seriyi_reddeder(dogrulayici, belge):
    kotu = copy.deepcopy(belge)
    kotu["seriler"][0]["veri"] = kotu["seriler"][0]["veri"][:1]
    assert list(dogrulayici.iter_errors(kotu))
