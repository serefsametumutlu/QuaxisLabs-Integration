"""ChartSpec v1 JSON Şeması — `spec.py` ve `roller.py`'den TÜRETİLİR.

Elle yazılmaz: rol listeleri doğrudan enum'lardan okunur, böylece şema ile
Python tarafı birbirinden ayrı düşemez. Şema, sözleşmenin dilden bağımsız
yüzüdür; web çizicisi ve ileride PNG çizicisi aynı dosyaya bakar.
"""

from __future__ import annotations

from typing import Any

from .roller import AlanRol, CizgiRol, EtiketRol, IsaretRol, RozetRol, SeviyeRol, Yon
from .spec import SURUM

_ID = "https://quaxislabs.dev/sema/chartspec-1.0.schema.json"


def _roller(enum) -> list[str]:
    return sorted(u.value for u in enum)


def _nokta() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["t", "fiyat"],
        "additionalProperties": False,
        "properties": {
            "t": {"type": "integer", "description": "UTC epoch saniye"},
            "fiyat": {"type": "number"},
        },
    }


def _katman(tur: str, enum, ek: dict[str, Any], zorunlu: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["tur", "rol", *zorunlu],
        "additionalProperties": False,
        "properties": {
            "tur": {"const": tur},
            "rol": {"enum": _roller(enum)},
            "panel": {"type": "string"},
            **ek,
        },
    }


def sema() -> dict[str, Any]:
    yerlesim = {"enum": ["ust", "alt"]}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _ID,
        "title": "QuaxisLabs ChartSpec",
        "description": (
            "Çizim kütüphanesinden bağımsız, versiyonlu çizim sözleşmesi. "
            "Roller kapalı bir kümedir: listede olmayan bir rol geçersizdir, "
            "sessizce varsayılana düşmez."
        ),
        "type": "object",
        "required": ["surum", "kunye", "paneller", "seriler"],
        "additionalProperties": False,
        "properties": {
            "surum": {"const": SURUM},
            "kunye": {
                "type": "object",
                "required": ["sembol", "zaman_dilimi", "strateji"],
                "additionalProperties": False,
                "properties": {
                    "sembol": {"type": "string"},
                    "ad": {"type": "string"},
                    "zaman_dilimi": {"type": "string"},
                    "strateji": {"type": "string"},
                    "strateji_adi": {"type": "string"},
                    "yon": {"enum": _roller(Yon)},
                    "durum": {"type": "string"},
                    "ornek_mi": {
                        "type": "boolean",
                        "description": "Örnek veri mi? Arayüz bunu kullanıcıya AYNEN gösterir.",
                    },
                },
            },
            "paneller": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["id", "tur", "oran"],
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string"},
                        "tur": {"enum": ["fiyat", "hacim"]},
                        "oran": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
                        "y": {
                            "type": "object",
                            "required": ["alt", "ust"],
                            "additionalProperties": False,
                            "description": (
                                "Komposerin BİLİNÇLİ yazdığı aralık. Yoksa çizici aralığı "
                                "YALNIZCA o panelin serilerinden hesaplar; katmanlar aralığı "
                                "kendiliğinden genişletemez."
                            ),
                            "properties": {
                                "alt": {"type": "number"},
                                "ust": {"type": "number"},
                                "gerekce": {"type": "string"},
                            },
                        },
                    },
                },
            },
            "seriler": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "oneOf": [
                        {
                            "type": "object",
                            "required": ["id", "tur", "panel", "veri"],
                            "additionalProperties": False,
                            "properties": {
                                "id": {"type": "string"},
                                "tur": {"const": "mum"},
                                "panel": {"type": "string"},
                                "veri": {
                                    "type": "array",
                                    "minItems": 2,
                                    "items": {
                                        "type": "object",
                                        "required": ["t", "acilis", "yuksek", "dusuk", "kapanis"],
                                        "additionalProperties": False,
                                        "properties": {
                                            "t": {"type": "integer"},
                                            "acilis": {"type": "number"},
                                            "yuksek": {"type": "number"},
                                            "dusuk": {"type": "number"},
                                            "kapanis": {"type": "number"},
                                        },
                                    },
                                },
                            },
                        },
                        {
                            "type": "object",
                            "required": ["id", "tur", "panel", "veri"],
                            "additionalProperties": False,
                            "properties": {
                                "id": {"type": "string"},
                                "tur": {"const": "hacim"},
                                "panel": {"type": "string"},
                                "veri": {
                                    "type": "array",
                                    "minItems": 2,
                                    "items": {
                                        "type": "object",
                                        "required": ["t", "hacim", "yon"],
                                        "additionalProperties": False,
                                        "properties": {
                                            "t": {"type": "integer"},
                                            "hacim": {"type": "number", "minimum": 0},
                                            "yon": {"enum": _roller(Yon)},
                                        },
                                    },
                                },
                            },
                        },
                    ]
                },
            },
            "katmanlar": {
                "type": "array",
                "items": {
                    "oneOf": [
                        _katman(
                            "seviye",
                            SeviyeRol,
                            {
                                "fiyat": {"type": "number"},
                                "etiket": {"type": "string"},
                                "baslangic": {"type": "integer"},
                            },
                            ["fiyat", "etiket"],
                        ),
                        _katman(
                            "alan",
                            AlanRol,
                            {
                                "noktalar": {"type": "array", "minItems": 3, "items": _nokta()},
                                "etiket": {"type": "string"},
                            },
                            ["noktalar"],
                        ),
                        _katman(
                            "bant",
                            AlanRol,
                            {
                                "alt": {"type": "number"},
                                "ust": {"type": "number"},
                                "etiket": {"type": "string"},
                                "baslangic": {"type": "integer"},
                            },
                            ["alt", "ust"],
                        ),
                        _katman(
                            "cizgi",
                            CizgiRol,
                            {"noktalar": {"type": "array", "minItems": 2, "items": _nokta()}},
                            ["noktalar"],
                        ),
                        _katman(
                            "isaret",
                            IsaretRol,
                            {"nokta": _nokta(), "metin": {"type": "string"}, "yerlesim": yerlesim},
                            ["nokta"],
                        ),
                        _katman(
                            "etiket",
                            EtiketRol,
                            {"nokta": _nokta(), "metin": {"type": "string"}, "yerlesim": yerlesim},
                            ["nokta", "metin"],
                        ),
                        _katman(
                            "rozet",
                            RozetRol,
                            {
                                "nokta": _nokta(),
                                "metin": {"type": "string"},
                                "yon": {"enum": _roller(Yon)},
                            },
                            ["nokta", "metin", "yon"],
                        ),
                    ]
                },
            },
        },
    }
