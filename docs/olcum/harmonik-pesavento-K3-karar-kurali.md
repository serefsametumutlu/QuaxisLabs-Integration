# K3 karar kuralı — Harmonik (Pesavento)

**Yazıldığı tarih:** 2026-09-13
**Durum:** ⏳ sonuçlar GÖRÜLMEDEN yazıldı ve commit edildi.

> Bu belgenin varlık sebebi: kitabın vermediği dört eşiği **sonuca bakıp
> seçme** imkânını ortadan kaldırmak.

---

## 1. Neyi seçiyoruz, neyi seçmiyoruz

Kitap dört sayı vermiyor: `tolerans`, `donus_max_bar`, `pivot_sol/sag`,
AB=CD'nin `stop_orani`. Bunlar K3'te türetilecek.

**Seçim ölçütü SADECE kalibrasyondur — aday sayısı ve dağılım şekli.**
Getiri, R, isabet, profit factor **hiçbiri bu kararda kullanılmayacak.**

Sebep somut: eşiği getiriye bakarak seçmek, K4'ün ölçeceği şeyi K3'te
seçmek demektir. O zaman K4 "kenar var mı" sorusunu değil, "seçtiğim eşik
kendi seçildiği veride iyi görünüyor mu" sorusunu cevaplar. Golden Zone'da
35 koşulluk taramanın sonucunu ancak ön kayıt kurtarmıştı.

**Bu koşuda R hesaplanmayacak.** Ölçüm aracı çağrılmayacak ki bakma
ihtimali bile doğmasın.

---

## 2. `tolerans`

Taranacak: `0.02 · 0.03 · 0.05 · 0.08 · 0.10`

**Karar kuralı — sırayla uygulanır:**

1. **Alt sınır:** formasyonun sinyal ürettiği sembol sayısı **≥ 100**
   olmalı. Altındaki değerler elenir (sembol-kümelenmiş testte bağımsız
   gözlem sembolüdür; 100'ün altı K4'ü baştan zayıflatır).
2. **Üst sınır:** sembol başına yıllık sinyal **≤ 3** olmalı. Üstü, oranın
   "tuttuğu" kavramını anlamsızlaştırır — her salınım her orana uyar.
3. Kalanlar içinden **en KÜÇÜĞÜ** seçilir.

Üçüncü madde bilinçli: eşit derecede makul iki değerden dar olanı, kitabın
oranlarına daha sadık olandır. Geniş tolerans daha çok sinyal üretir ve
daha çok sinyal *her zaman* cazip görünür — kural bu cazibeyi kesiyor.

**Dört formasyon için AYRI AYRI seçilir.** Üçü aynı çıkarsa aynı yazılır;
zorla eşitlenmez.

---

## 3. `pivot_sol` / `pivot_sag`

Taranacak: `2 · 3 · 4 · 5` (sol = sağ tutulur)

**Karar kuralı:** Aynı iki sınır (≥100 sembol, ≤3 sinyal/sembol/yıl)
uygulanır; kalanlar içinden **ortanca** değer seçilir.

Burada "en küçük" DEĞİL ortanca, çünkü küçük pivot kolu gürültüyü salınım
sanar — tolerans'takinin tersine, dar olan burada daha sadık değil daha
gevşektir.

**Golden Zone ile aynı çıkarsa (3/3) bu bir tesadüf değil avantajdır:** iki
strateji aynı pivot tanımını kullanırsa sonuçları kıyaslanabilir. Ama
kural farklı bir sayı gösterirse **kural kazanır**, kıyaslanabilirlik değil.

---

## 4. `donus_max_bar`

Ölçüm biçimi farklı: taranmaz, **dağılımdan okunur.** Pencere 400 bara
açılır ve C'nin onayından D'ye dokunuşa kadar geçen bar sayısının
(`olusum_bar`) dağılımı çıkarılır.

**Karar kuralı:** `donus_max_bar` = o dağılımın **%90'lık dilimi**, en
yakın 5'e yuvarlanmış.

Yani gerçekte olan dokunuşların onda dokuzu pencerenin içinde kalır. Geri
kalan %10, "aylar sonra tesadüfen o seviyeye değdi" vakalarıdır ve
formasyonun sonucu sayılamaz.

Dilim seçimi **şimdi** sabitlendi; sonuca bakıp %95'e çıkarılmayacak.

---

## 5. AB=CD'nin `stop_orani`

Bu **K3'te kapatılamaz** ve öyle yazılacak.

Kitap AB=CD için stop formülü vermiyor. 1.272, kitabın kendi oran
kümesinden seçilmiş bir başlangıç noktası. Hangi mesafenin doğru olduğu bir
**getiri sorusudur** — ve getiriye bakarak eşik seçmeyi §1'de yasakladık.

**Karar:** 1.272 olduğu gibi kalır, K4'te `stop_orani ∈ {1.272, 1.618}`
**iki ayrı künye** olarak ölçülür (Golden Zone'daki `yapisal` / `r_kati`
ayrımının aynısı). İki soru ayrı sorulur, biri diğerinin cevabından
seçilmez.

Bu, K3 bulgusunun kapanmadığı anlamına gelir ve `pasaport.py dogrula`
bunu bulgu olarak yazmaya devam eder — doğru davranış.

---

## 6. Ayrıca ölçülecek ama karar VERMEYECEK olanlar

Bunlar rapora girer, eşik seçmez:

* **Gartley'in AB bacağı gerçekten .49–.65 bandında mı** (K0 §3.1'in
  cebirsel tahmini). Band dışında yoğunluk çıkarsa kitabın iki kuralı
  birbiriyle çelişiyor demektir — bu bir **bulgu**, eşik değişikliği değil.
* Hangi Fibonacci oranının kaç kez tuttuğu (`bc`, `ab`, `abcd`).
* Boğa/ayı asimetrisi.
* Sıfır sinyal veren sembollerin oranı.

---

## 7. Ne zaman "kalibrasyon başarısız" denir

* Bir formasyon, taranan **hiçbir** tolerans değerinde iki sınırı birden
  sağlayamazsa → o formasyon K4'e **girmez**, "kalibre edilemedi" yazılır.
* Sembollerin %90'ından fazlası sıfır sinyal verirse → dedektör bozuktur,
  kod incelenir (eski projede `breakout_fvg` 648/648 sembolde sıfır aday
  veriyordu ve bu çok sonra fark edildi).
