# Strateji Envanteri

**Güncelleme:** 2026-09-13

Bu dosya tek bir soruya cevap verir: **elimizde ne var, hangisi ne durumda?**

---

## 1. Bu depoda GERÇEKTEN çalışan kod

| Strateji | Dedektör | Grafik | Pasaport | Ölçüldü mü | Verdikt |
|---|---|---|---|---|---|
| **Golden Zone** (ICT OTE) | ✅ | ✅ | ✅ | ✅ | `kanıtlanmadı` — ⏸ durduruldu |
| **Kesitsel Momentum** | ✅ | — | ✅ | ✅ | `kanıtlanmadı` — ⏸ durduruldu |
| Kesitsel Dönüş (ters varyant) | ✅ | — | *(momentumun içinde)* | ✅ | **reddedildi** (ön kayıtlı) |
| **Salınım Fibo ABCD** | ❌ **YOK** | ✅ | ❌ | ❌ | — |

**Yayınlanmış (K6) strateji: 0.**

`Salınım Fibo ABCD` özel bir durum: **çizimi var, dedektörü yok.** Yani
grafiği elle girilmiş sayılarla çiziliyor; "bu formasyon ne zaman oluştu"
sorusunu cevaplayan kod yok. Harmoniklere buradan devam edilecekse ilk iş
o dedektörü yazmaktır.

### Arayüzdeki sayılar gerçek değil

Sol raydaki **Yapı 4 · Formasyon 3 · Trend & Momentum 2 · İst. Arbitraj 0**
maket verisidir (`apps/web/lib/ornek-veri.ts`). Karşılığı olan kod yoktur.

---

## 2. Önceki projeden devralınan havuz (27 gösterge)

ADR-002 gereği **hiçbiri taşınmadı**; hepsi sıfırdan yazılacak. Eski kod
referans değil, yalnız karşılaştırma içindir.

| Aile | Adet | Not |
|---|---|---|
| `patterns.*` | 7 | çift tepe/dip, genişleyen, takoz, bayrak-flama, OBO, üçgen, FVG kırılımı |
| `structure.*` | 4 | piyasa yapısı (HH-HL-LH-LL, BOS/CHoCH), altın bölge, arz-talep, hacim profili |
| `trend.*` | 4 | `ewmac`, `ma_systems`, `breakouts`, `weekly_channel` |
| `momentum.*` | 2 | `alpha_rank`, `momentum_rank` (evren-geneli) |
| `pair.*` | 2 | göreli momentum, çift sağlığı |
| `harmonic.*` | **8 ekol** | XABCD aileleri (Gartley, Bat, Butterfly, Crab, …) |

### ⚠ Önceki ölçümün harmonikler hakkında söylediği

Eski depoda yapılan sembol-kümelenmiş ölçümde:

| Gösterge | Sonuç |
|---|---|
| `trend.ewmac` | +%1.59, p=0.034 (n=559) — **en az çürütülmüş**, yine de FDR'yi geçemedi |
| `structure.golden_zone` | en az çürütülmüş üçlüde — **bu depoda ölçtük, kenar yok** |
| `trend.ma_systems` | en az çürütülmüş üçlüde |
| **`harmonic.carney`** | **−%3.66 (n=68)** — negatif tarafta |
| `patterns.broadening` | −%1.86 (n=102) — negatif tarafta |

Ayrıca ilk turda "anlamlı" çıkan üç gösterge (`broadening` +%30,
`wedge` +%79, `five_zero` +%68) **üçü de sahte** çıktı: `wedge`'in 10
"sinyali" aslında 2 hisseydi; ANELE tek başına aynı hareketi 5 kez
tekrarlıyordu. Sembol düzeyinde kümeleme yapılınca hepsi çöktü.

**Bu, harmoniklerin işe yaramadığının kanıtı değil** — o ölçüm bu depodaki
makineyle yapılmadı, n=68 zayıf, ve harmoniklerin nasıl kodlandığı
bilinmiyor. Ama **beklentiyi yönetmesi gereken bir uyarı**: harmonikler
önceki turda üstte değil, altta çıkmıştı.

---

## 3. Sıradaki karar

Kullanıcı kararı: **harmoniklerden devam.** Başlamadan önce şunlar
netleşmeli (bir sonraki turda tabloyla gelecek):

1. Hangi harmonik(ler) — 8 ekolün hepsi mi, biriyle mi başlanacak
2. Her birinin **tam Fibonacci oranları** ve tolerans payı
3. **AL sinyali tam olarak hangi barın kapanışında** doğuyor
4. Stop ve hedef nereye
5. Ne zaman geçersiz oluyor
6. Kaynak: Pesavento / Carney, sayfa numarasıyla

---

## 4. Ölçüm makinesi — stratejilerden bağımsız varlık

İki strateji elendi ama makine kaldı ve her turda sertleşti:

| Yetenek | Nerede |
|---|---|
| Üç bariyerli R (stop/hedef/zaman) | `olcum/bariyer.py` |
| İleri getiri + adil baz | `olcum/ileri_getiri.py` |
| İşlem maliyeti + maliyet duyarlılığı | ikisinde de · `tools/maliyet_duyarliligi.py` |
| IS/OOS + sembol bölmesi | `tools/kosul_taramasi.py` |
| Çoklu test düzeltmesi (BH-FDR) | `olcum/ileri_getiri.py::bh_fdr` |
| Ön kayıt disiplini | `tools/onkayit_testi.py` |
| Koşul taraması (35 koşul) | `tools/kosul_taramasi.py` |
| Segment analizi (likidite/fiyat/sektör) | `tools/segment_analizi.py` |
| Profit factor, isabet, çıkış kırılımı | `olcum/bariyer.py::RResult` |
| Kalibrasyon (aday sayımı) | `olcum/kalibrasyon.py` |
| Non-repaint testi | `testing/repaint.py` |
| Pasaport doğrulayıcı (7 kapı) | `tools/pasaport.py` |

**Yeni bir strateji bu makineye takılıp bir turda ölçülebilir.** İki
stratejinin bedeli buydu ve karşılığında bu kaldı.
