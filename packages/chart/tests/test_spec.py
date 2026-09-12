"""ChartSpec sözleşmesinin testleri.

Bu testler "kod çalışıyor mu" diye sormaz; **eski mimarinin üç kanıtlanmış
hatasının yapısal olarak imkânsız olduğunu** kanıtlar (ADR-001 §4). Biri
geçmezse sözleşme delinmiş demektir.
"""

from __future__ import annotations

import pytest
from quaxis.chart.roller import AlanRol, IsaretRol, SeviyeRol, Yon, fib_rol
from quaxis.chart.spec import (
    Alan,
    ChartSpec,
    Cizgi,
    HacimBari,
    HacimSerisi,
    Isaret,
    Kunye,
    Mum,
    MumSerisi,
    Nokta,
    Panel,
    Seviye,
    YAraligi,
)

T0 = 1_760_000_000
KUNYE = Kunye(sembol="TEST", ad="Test", zaman_dilimi="1G", strateji="t", strateji_adi="T")


def _mumlar(n: int = 5) -> list[Mum]:
    return [Mum(t=T0 + i * 86400, acilis=100 + i, yuksek=102 + i, dusuk=99 + i, kapanis=101 + i) for i in range(n)]


def _spec(**degis) -> ChartSpec:
    temel = dict(
        kunye=KUNYE,
        paneller=[Panel(id="fiyat", tur="fiyat", oran=1.0)],
        seriler=[MumSerisi(id="mum", panel="fiyat", veri=_mumlar())],
        katmanlar=[],
    )
    temel.update(degis)
    return ChartSpec(**temel)


# ---------------------------------------------------------------- 1. kapalı rol


def test_bilinmeyen_rol_sessizce_griye_dusmez():
    """Eski çizici tanımadığı stili varsayılana düşürüyordu; artık atıyor."""
    with pytest.raises(ValueError) as e:
        SeviyeRol("fib_999")
    assert "bilinmeyen rol" in str(e.value).lower()
    assert "fib_618" in str(e.value)  # geçerli roller hatada listelenir


def test_tanimsiz_fibo_orani_reddedilir():
    with pytest.raises(ValueError, match="Tanımlı bir fibo oranı değil"):
        fib_rol(0.707)


def test_tanimli_fibo_orani_role_dusr():
    assert fib_rol(0.618) is SeviyeRol.FIB_618
    assert fib_rol(1.272) is SeviyeRol.FIB_1272


# -------------------------------------------------- 2. panel y aralığı disiplini


def test_acik_y_araligi_seriyi_kirpamaz():
    """Bir katman ya da elle yazılmış aralık grafiği sessizce kırpamaz."""
    with pytest.raises(ValueError, match="kırpıyor"):
        _spec(
            paneller=[Panel(id="fiyat", tur="fiyat", oran=1.0, y=YAraligi(alt=100.0, ust=103.0))]
        ).dogrula()


def test_acik_y_araligi_genisletebilir():
    """Merdiven mumların dışına taşıyorsa aralık GENİŞLETİLEBİLİR."""
    spec = _spec(
        paneller=[
            Panel(id="fiyat", tur="fiyat", oran=1.0, y=YAraligi(alt=50.0, ust=200.0, gerekce="merdiven"))
        ]
    ).dogrula()
    assert spec.paneller[0].y.alt == 50.0


def test_y_araligi_verilmezse_yalniz_seriden_gelir():
    """Varsayılan: aralık yok — çizici o panelin SERİLERİNDEN hesaplar.
    Katmanlar aralığı kendiliğinden genişletemez."""
    spec = _spec().dogrula()
    assert spec.paneller[0].y is None


def test_panelsiz_seri_reddedilir():
    with pytest.raises(ValueError, match="tanımsız panele"):
        _spec(seriler=[MumSerisi(id="mum", panel="yok", veri=_mumlar())]).dogrula()


def test_serisiz_panel_reddedilir():
    with pytest.raises(ValueError, match="hiçbir seri bağlı değil"):
        _spec(
            paneller=[
                Panel(id="fiyat", tur="fiyat", oran=0.5),
                Panel(id="hacim", tur="hacim", oran=0.5),
            ]
        ).dogrula()


# ------------------------------------------------------------- 3. tam dizi şartı


def test_iki_uca_indirgenmis_seri_reddedilir():
    with pytest.raises(ValueError, match="TAM DİZİ"):
        _spec(seriler=[MumSerisi(id="mum", panel="fiyat", veri=_mumlar(1))]).dogrula()


def test_sirasiz_zaman_reddedilir():
    m = _mumlar()
    m[1], m[3] = m[3], m[1]
    with pytest.raises(ValueError, match="artan sırada değil"):
        _spec(seriler=[MumSerisi(id="mum", panel="fiyat", veri=m)]).dogrula()


def test_tutarsiz_mum_reddedilir():
    kotu = [Mum(t=T0, acilis=100, yuksek=99, dusuk=101, kapanis=100), *_mumlar()[1:]]
    with pytest.raises(ValueError, match="Tutarsız mum"):
        _spec(seriler=[MumSerisi(id="mum", panel="fiyat", veri=kotu)]).dogrula()


# ------------------------------------------------------------------ katmanlar


def test_katman_seri_araliginin_disina_tasamaz():
    with pytest.raises(ValueError, match="seri aralığının dışında"):
        _spec(
            katmanlar=[Isaret(rol=IsaretRol.KOSE, nokta=Nokta(t=T0 - 86400, fiyat=100), metin="X")]
        ).dogrula()


def test_ucgen_olmayan_alan_reddedilir():
    with pytest.raises(ValueError, match="en az üç nokta"):
        _spec(
            katmanlar=[
                Alan(rol=AlanRol.FORMASYON, noktalar=[Nokta(T0, 100), Nokta(T0 + 86400, 101)])
            ]
        ).dogrula()


def test_tek_noktali_cizgi_reddedilir():
    with pytest.raises(ValueError, match="en az iki nokta"):
        _spec(katmanlar=[Cizgi(rol="trend", noktalar=[Nokta(T0, 100)])]).dogrula()


# ------------------------------------------------------------------ paneller


def test_panel_oranlari_bire_tamamlanmali():
    with pytest.raises(ValueError, match="toplamı 1.0"):
        _spec(
            paneller=[
                Panel(id="fiyat", tur="fiyat", oran=0.7),
                Panel(id="hacim", tur="hacim", oran=0.7),
            ],
            seriler=[
                MumSerisi(id="mum", panel="fiyat", veri=_mumlar()),
                HacimSerisi(
                    id="h",
                    panel="hacim",
                    veri=[HacimBari(t=m.t, hacim=10, yon=Yon.AL) for m in _mumlar()],
                ),
            ],
        ).dogrula()


# --------------------------------------------------------------- serileştirme


def test_json_rolleri_dizeye_indirger():
    spec = _spec(katmanlar=[Seviye(rol=SeviyeRol.FIB_618, fiyat=100.5, etiket="0.618: 100.50")]).dogrula()
    d = spec.sozluk()
    assert d["katmanlar"][0]["rol"] == "fib_618"
    assert d["surum"] == "1.0"
    assert isinstance(spec.json(), str)


def test_desteklenmeyen_surum_reddedilir():
    with pytest.raises(ValueError, match="Desteklenmeyen ChartSpec sürümü"):
        _spec(surum="0.9").dogrula()
