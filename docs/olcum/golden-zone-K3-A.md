# golden-zone — K3 Kalibrasyon · Katman A

**Tarih:** 2026-09-13 · **Gösterge:** `golden_zone`
**Zaman dilimi:** 1D

**Katman A:** yapı kırılımı + OTE bölgesi

| Ölçüt | Değer |
|---|---|
| Evren | 543 sembol |
| Toplam aday | 10417 |
| **Sıfır aday veren sembol** | **10** (%1.8) |
| Veri hatası alan sembol | 0 |
| Sembol başına ortalama | 19.18 |
| Sembol başına ortanca | 20.0 |
| Sembol başına en çok | 32 |
| Dönem | 2010-01-01 – 2026-09-11 |

## Teşhis

MAKUL: sembol başına ortalama 19.2 aday, sembollerin %2'i sıfır.

## Eşikler bu ölçümden nasıl türetildi

K0'ın eşik tablosundaki her `K3:` devri burada kapanır.

| Eşik | Değer | Bu ölçümden türetilişi |
|---|---|---|
| `bolge_sig` | 0.62 | **Türetilemedi.** Bölge hiçbir ayarda rastgele girişten ayrışmadı; "en iyi" değeri aramak, olmayan bir sinyalde tepe aramak olurdu. Kaynağın değeri OLDUĞU GİBİ bırakıldı ve sonuç onunla raporlandı. |
| `bolge_derin` | 0.79 | aynı — türetilemedi, kaynağın değeri korundu |
| `yer_degistirme_atr` | 1.5 | Sembol başına ortalama 19.2 aday, sembollerin yalnız %2'si sıfır aday. Kalibrasyon **MAKUL**: eşik ne evreni boğuyor ne susturuyor. Bu haliyle bırakıldı. |
| `donus_max_bar` | 20 | Aday sayısı makul aralıkta kaldığı için değiştirilmedi. |

> **Bu tablo bir başarısızlığı kaydediyor, bir türetmeyi değil.** K0'ın planı
> "eşiklerin tamamı K3'ten türetilsin"di. Türetme, ölçümün bir yön
> göstermesini gerektirir — göstermedi. Bir kenarın olmadığı yerde eşik
> "optimize etmek", gürültüye eğri uydurmaktan başka bir şey olmazdı
> (Pardo s.291–293). Bu yüzden eşikler kaynaktaki hâliyle kaldı ve sonuç
> onlarla raporlandı.

> "Veri çekilemedi" ile "aday bulunamadı" AYRI sayılır. Önceki projede
> 648/648 sembolde sıfır aday çıkmıştı ve kimse kaçının veri hatası
> olduğunu bilmiyordu.
