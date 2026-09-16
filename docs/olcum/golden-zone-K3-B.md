# golden-zone — K3 Kalibrasyon · Katman B

**Tarih:** 2026-09-17 · **Gösterge:** `golden_zone`
**Zaman dilimi:** 1D

**Katman B:** A + (FVG veya bölgedeki Order Block)

| Ölçüt | Değer |
|---|---|
| Evren | 625 sembol |
| Toplam aday | 8620 |
| **Sıfır aday veren sembol** | **12** (%1.9) |
| Veri hatası alan sembol | 23 |
| Sembol başına ortalama | 13.79 |
| Sembol başına ortanca | 14.0 |
| Sembol başına en çok | 28 |
| Dönem | 2010-01-01 – 2026-09-11 |

## Teşhis

MAKUL: sembol başına ortalama 13.8 aday, sembollerin %2'i sıfır.

## Eşikler bu ölçümden nasıl türetildi

K0'ın eşik tablosundaki her `K3:` devri burada kapanır.

| Eşik | Değer | Bu ölçümden türetilişi |
|---|---|---|
| `fvg_min_atr` | 0.1 | FVG/OB koşulu adayları 19.3'ten 13.8'e indiriyor (%29 eleme) — eşik ne her şeyi geçiriyor ne her şeyi kesiyor. Ama **elediği kısım kalandan daha kötü değildi**; ince ayarın anlamı yok, ayarlanacak bir sinyal bulunamadı. |
| `bolge_sig` / `bolge_derin` | 0.62 / 0.79 | A ile aynı — türetilemedi |
| `donus_max_bar` | 20 | A ile aynı |

> **Bu tablo bir başarısızlığı kaydediyor, bir türetmeyi değil.** K0'ın planı
> "eşiklerin tamamı K3'ten türetilsin"di. Türetme, ölçümün bir yön
> göstermesini gerektirir — göstermedi. Bir kenarın olmadığı yerde eşik
> "optimize etmek", gürültüye eğri uydurmaktan başka bir şey olmazdı
> (Pardo s.291–293). Bu yüzden eşikler kaynaktaki hâliyle kaldı ve sonuç
> onlarla raporlandı.

> "Veri çekilemedi" ile "aday bulunamadı" AYRI sayılır. Önceki projede
> 648/648 sembolde sıfır aday çıkmıştı ve kimse kaçının veri hatası
> olduğunu bilmiyordu.
