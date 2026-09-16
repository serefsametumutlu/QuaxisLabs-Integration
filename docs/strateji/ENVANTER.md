# Strateji Envanteri

> ✅ **2026-09-17 · Veri düzeltmesi yapıldı ve üç ailenin de ölçümü
> yenilendi.** Denetim:
> [`veri-denetimi-bist-1D.md`](../olcum/veri-denetimi-bist-1D.md) · ön kayıt
> ve sonuç: [`onkayit-veri-duzeltme.md`](../olcum/onkayit-veri-duzeltme.md).
> Hacimsiz barlar artık ne adil baza giriyor ne sinyal doğuruyor; OHLC
> ihlalinde sembol değil **bar** atılıyor, evren 544 → **625** sembole
> çıktı. **Üç ailede de verdikt değişmedi.**

**Güncelleme:** 2026-09-17 (üç ailenin ölçümü düzeltilmiş veriyle yenilendi)

Bu dosya tek bir soruya cevap verir: **elimizde ne var, hangisi ne durumda?**

---

## 1. Bu depoda GERÇEKTEN çalışan kod

| Strateji | Dedektör | Grafik | Pasaport | Ölçüldü mü | Verdikt |
|---|---|---|---|---|---|
| **Golden Zone** (ICT OTE) | ✅ | ✅ | ✅ | ✅ | `kanıtlanmadı` — ⏸ durduruldu |
| **Kesitsel Momentum** | ✅ | — | ✅ | ✅ | `kanıtlanmadı` — ⏸ durduruldu |
| Kesitsel Dönüş (ters varyant) | ✅ | — | *(momentumun içinde)* | ✅ | **reddedildi** (ön kayıtlı) |
| **Harmonik · AB=CD** | ✅ | ✅ | ✅ | ✅ | `kanıtlanmadı` — ✅ **K6 yayında** |
| **Harmonik · Gartley 222** | ✅ | ✅ | ✅ | ✅ | `kanıtlanmadı` — ✅ **K6 yayında** |
| **Harmonik · Butterfly** | ✅ | ✅ | ✅ | ✅ | `kanıtlanmadı` — ✅ **K6 yayında** |
| **Harmonik · Three Drives** | ✅ | ✅ | ✅ | ✅ | `kanıtlanmadı` — ✅ **K6 yayında** |
| **Salınım Fibo ABCD** | ❌ **YOK** | ✅ | ❌ | ❌ | — |

**Yayınlanmış (K6) strateji: 1** — harmonikler, **2026-09-17**. Projenin
yedi kapının hepsini geçen ilk stratejisi.

Kapıyı kapatan şey harmoniklerle ilgili değildi: tarama yüzeyi maket veriyle
çalışıyordu ve oraya sahte harmonik satır eklemek kapıyı kapatırdı ama yalan
olurdu. Gerçek tarama motoru evrende koştu
([ADR-003](../karar/ADR-003-tarama-koprusu.md)) ve dört formasyon da gerçek
tabloda, yanlarında `kanıtlanmadı` rozetiyle görünüyor.

**Yayınlanmış olmak "işe yarıyor" demek değildir.** Verdikt hâlâ
`kanıtlanmadı`; ürün formasyonu gösteriyor, sistem kimseye "al" demiyor ve
alarm kurulmuyor. Eleme değil etiketleme.

Dört harmonik formasyon tek pasaport altında
([`harmonik-pesavento.md`](harmonik-pesavento.md)) ama **dört ayrı künye**
ve dört ayrı ölçüm. Soru "harmonikler çalışıyor mu" değil, **hangisi**.
Cevap: **hiçbiri** — beş testin (dört formasyon + AB=CD'nin ikinci stop
varyantı) beşi de BH-FDR'yi geçemedi.

`Salınım Fibo ABCD` özel bir durum: **çizimi var, dedektörü yok.** Yani
grafiği elle girilmiş sayılarla çiziliyor; "bu formasyon ne zaman oluştu"
sorusunu cevaplayan kod yok. Harmoniklere buradan devam edilecekse ilk iş
o dedektörü yazmaktır.

### Arayüzdeki sayılar artık gerçek (2026-09-17)

Eskiden sol rayda **Yapı 4 · Formasyon 3 · Trend & Momentum 2 · İst. Arbitraj 0**
ve **Takip listem 21** yazıyordu; hiçbirinin arkasında kod yoktu.

Tarama yüzeyi gerçek çıktıya bağlandı
([ADR-003](../karar/ADR-003-tarama-koprusu.md)): tarama sayacı gün sonu
koşusundan, paket sayaçları strateji kayıt defterinden geliyor. "Takip listem"
kaldırıldı — öyle bir özellik yok.

`lib/ornek-veri.ts` silinmedi ama görevi daraldı: yalnız **tasarım vitrini**
için (bileşenleri 500 satırda göstermek, boş durumu denemek). Satır tipini
gerçek veriden alıyor, yani vitrinde çalışan bir kolon üründe kırılamaz.

Hâlâ maket olan: **strateji kütüphanesi kartlarının üçü** (`Piyasa Yapısı`,
`Arz–Talep`, `Adil Değer Boşluğu`) — arkalarında kod yok, verdiktleri
`ölçülmedi`. Ayrıca `golden-zone` ve `kesitsel-momentum` pasaportları var ama
kütüphanede kaydı yok: tarama tablosunda görünüp kütüphanede görünmüyorlar.

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

Kullanıcı kararı (2026-09-13): **Pesavento'nun dört formasyonu birlikte
kodlansın; diğer dört ekol sonra — toplam sekiz.**

Dördü kodlandı, kalibre edildi ve ölçüldü (K0→K4). **Kenar bulunamadı.**

En öğretici sayı `abcd`'nin yalnız alış satırı: +0.459R, profit factor
1.80, %41.6 isabet. Adil baz olmadan raporlansa "çalışan strateji" diye
sunulurdu. **Adil baz +0.367R** — aynı risk yapısını rastgele barlara
koyunca da neredeyse aynı sonuç çıkıyor. Kalan +0.092R, p=0.5612.

### Sonraki turda gelecek dört ekol

| Ekol | Kaynak | Not |
|---|---|---|
| Bat · Crab · Shark | Carney | **Pesavento kitabında YOK** — ayrı K0 gerekir |
| Cypher | Oglesbee | ayrı K0 |
| 5-0 | Duddella | ayrı K0 |

Kaynağı olmayan bir formasyonu Pesavento'nun altına yazmak K0'ın tek
kuralını çiğnerdi; bu yüzden ayrı tutuldular.

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
