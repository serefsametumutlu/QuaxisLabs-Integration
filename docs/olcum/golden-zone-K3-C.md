# golden-zone — K3 Kalibrasyon · Katman C

**Tarih:** 2026-09-17 · **Gösterge:** `golden_zone`
**Zaman dilimi:** 1D

**Katman C:** B + likidite süpürmesi

| Ölçüt | Değer |
|---|---|
| Evren | 625 sembol |
| Toplam aday | 1524 |
| **Sıfır aday veren sembol** | **75** (%12.0) |
| Veri hatası alan sembol | 23 |
| Sembol başına ortalama | 2.44 |
| Sembol başına ortanca | 2.0 |
| Sembol başına en çok | 8 |
| Dönem | 2010-01-01 – 2026-09-11 |

## Teşhis

MAKUL: sembol başına ortalama 2.4 aday, sembollerin %12'i sıfır.

## Eşikler bu ölçümden nasıl türetildi

K0'ın eşik tablosundaki her `K3:` devri burada kapanır.

| Eşik | Değer | Bu ölçümden türetilişi |
|---|---|---|
| süpürme koşulu | açık | Adayları 13.8'den 2.4'e indiriyor ve sembollerin %12'si sıfır adaya düşüyor. Eleme çok sert; buna rağmen kalan işlemler daha iyi performans göstermiyor. |
| diğer eşikler | — | A/B ile aynı |

> **Bu tablo bir başarısızlığı kaydediyor, bir türetmeyi değil.** K0'ın planı
> "eşiklerin tamamı K3'ten türetilsin"di. Türetme, ölçümün bir yön
> göstermesini gerektirir — göstermedi. Bir kenarın olmadığı yerde eşik
> "optimize etmek", gürültüye eğri uydurmaktan başka bir şey olmazdı
> (Pardo s.291–293). Bu yüzden eşikler kaynaktaki hâliyle kaldı ve sonuç
> onlarla raporlandı.

> "Veri çekilemedi" ile "aday bulunamadı" AYRI sayılır. Önceki projede
> 648/648 sembolde sıfır aday çıkmıştı ve kimse kaçının veri hatası
> olduğunu bilmiyordu.
