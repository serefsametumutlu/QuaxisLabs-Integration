# Sıradaki strateji — aday araştırması

**Tarih:** 2026-09-13 · **Durum:** karar bekliyor

Golden Zone durduruldu. Bu belge, ölçüm makinesinden geçirilecek sıradaki
strateji için **kaynaklı** adayları listeler. Seçim yapılınca tam K0 yazılır.

---

## Golden Zone'dan öğrendiklerimiz — seçim ölçütleri

Bir sonraki strateji seçilirken şunlara bakıyorum:

| Ölçüt | Neden |
|---|---|
| **Kaynağında kanıt var mı** | Golden Zone'un kaynağı kuralı tarif ediyordu ama kanıt sunmuyordu. Yeni adayda yayımlanmış sonuç aranıyor. |
| **Mekanizma farklı mı** | Golden Zone "bölgeye dönüş" idi. Aynı aileden bir şey seçmek aynı duvara toslamak olur. |
| **Kalabalık mı** | Bankacılıkta (en likit, en çok izlenen) en kötü sonucu aldık. "Herkesin baktığı yerde kenar kalmaz" işareti. |
| **Günlük veriyle ölçülebilir mi** | Saatlik veri yalnız 2 yıl geriye gidiyor. Günlükte 16 yıl var. |
| **Adil baz kurulabilir mi** | BIST'in kendi sürüklenmesi pozitif; stratejinin onu YENMESİ gerek. |

> **Chan'ın kendisi de permütasyon testi kullanıyor** (s.35): "10 000 simüle
> fiyat serisinde çalıştırınca APR'nin eşit ya da büyük çıktığı yalnız 100
> seri var." Ölçüm makinemizin yöntemi kaynağın yöntemiyle aynı.

---

## Aday A · Boşluk Dönüşü (Buy-on-Gap)

**Kaynak:** Ernest Chan, *Algorithmic Trading: Winning Strategies and Their
Rationale* (2013), **s.93–95**

### Kural (kitaptan, birebir)

1. Açılışa yakın, **önceki günün dibinden bugünkü açılışa getirisi bir
   standart sapmadan düşük** olan hisseleri seç. Sapma, son 90 günün
   kapanış-kapanış getirilerinden hesaplanır. ("Aşağı boşluk açanlar.")
2. Bu listeyi daralt: **açılış fiyatı, kapanışların 20 günlük hareketli
   ortalamasının üstünde** olmalı.
3. Listedeki **en düşük getirili 10 hisseyi al.**
4. **Gün sonunda kapanışta hepsini kapat.**

### Kitabın kendi gerekçesi

> "Endeks vadelileri açılış öncesi düşükken bazı hisseler açılıştaki panik
> satışından orantısız zarar görür. Panik satışı bitince hisse gün içinde
> kademeli olarak toparlanır."

2. kural için: *"mean-reverting stratejilerde çok işe yarar: ortalamaya
dönüş stratejisinin üstüne bindirilmiş bir momentum filtresidir."* "Biraz"
düşenler "çok" düşenlerden daha iyi döner; çok düşenlerde genelde kötü haber
vardır ve haber kaynaklı düşüşler dönmez.

### Kitabın bildirdiği sonuç

| | |
|---|---|
| APR | %8.7 |
| Sharpe | 1.5 |
| Dönem | 2006-05-11 – 2012-04-24 |
| Ayna (yukarı boşlukta short) | APR %46, Sharpe 1.27 |

### ⚠ Kaynağın kendi itirafı — bu ciddiye alınmalı

> *"Açılış fiyatlarını sinyal üretmek için kullanıp yine açılış fiyatından
> nasıl dolabiliriz? Kısa cevap tabii ki: Dolamayız!"*

Chan, açılış öncesi fiyatlarla sinyal üretilebileceğini ama bunun "sinyal
gürültüsü" yaratacağını söylüyor. **BIST'te bu daha da sert bir sorun:**
açılış öncesi fiyat akışına erişimimiz yok. Ölçersek sonucun iyimser
olduğunu açıkça yazmak zorundayız.

| Artı | Eksi |
|---|---|
| Yalnız günlük OHLC gerekir | Gerçekte açılışta dolmak mümkün olmayabilir |
| Kural net, eşikler sayısal | Günlük tutma → işlem maliyeti ağır basar |
| Mekanizma Golden Zone'dan tamamen farklı | Kaynak 2006–2012; 2012 sonrası bilinmiyor |
| Momentum filtresi fikri ayrıca öğretici | Portföy stratejisi (günde 10 hisse), tek sinyal değil |

---

## Aday B · Kesitsel Momentum (Cross-Sectional Momentum)

**Kaynak:** Chan (2013), **s.145**; asıl çalışma Daniel & Moskowitz (2011)

### Kural

Her gün evrendeki hisselerin **12 aylık (252 gün) getirisini sırala**.
En yüksek getirili grubu **al**, en düşük getirili grubu **sat**, pozisyonu
**1 ay (25 gün)** tut.

### Kitabın bildirdiği sonuç

| | |
|---|---|
| APR | %18, Sharpe 1.37 (emtia, 2005-06 – 2007-12) |
| **Kriz dönemi** | **APR −%33** (2008-01 – 2009-12) |
| Kapsam | Daniel & Moskowitz: dünya endeksleri, dövizler, uluslararası hisseler ve ABD hisseleri — "güneşin altındaki hemen her şey" |

### Neden ilgi çekici

Akademik literatürün **en iyi belgelenmiş anomalisi**. Ve bizim
`UniverseIndicator` sözleşmemiz tam da böyle evren-geneli stratejiler için
yazılmış, henüz hiç kullanılmadı.

**Bilinen çöküş modu belgeli:** momentum krizlerde sert çöker. Bunu
*ölçebiliriz* — BIST'te 2018 ve 2020 kırılmalarında ne olduğu somut bir soru.

| Artı | Eksi |
|---|---|
| Literatürde en sağlam anomali | Bizim R makinemize doğrudan oturmuyor (stop/hedef yok) |
| Yalnız günlük kapanış gerekir | Portföy stratejisi: ölçüm yöntemi uyarlanmalı |
| Çöküş modu belgeli ve ölçülebilir | BIST'te short kısıtları var (açığa satış) |
| Mekanizma tamamen farklı | 1 ay tutuş → sinyal sayısı az |

---

## Aday C · Eşleşme Ticareti / Kointegrasyon

**Kaynak:** Chan (2013), Bölüm 3–5 (s.63–131)

Kointegre olan iki menkul bulup aralarındaki farkın ortalamaya dönüşünü
ticarete konu etmek. Arayüzdeki "İstatistiksel Arbitraj" paketi bunun için
duruyor (şu an 0 strateji).

| Artı | Eksi |
|---|---|
| Sağlam istatistiksel temel (kointegrasyon testi) | Çift seçimi başlı başına bir arama problemi = ciddi çoklu test riski |
| Piyasa yönünden bağımsız — BIST sürüklenmesini yenmek zorunda değil | Açığa satış gerekir; BIST'te kısıtlı |
| Golden Zone'dan tamamen farklı | En karmaşık altyapı |

---

## Karar için sorular

1. **Hangi aday?** A (boşluk dönüşü) · B (kesitsel momentum) · C (eşleşme)
2. **Açığa satış** BIST'te bizim için gerçekçi mi? B ve C'nin yarısı buna
   dayanıyor; değilse ikisi de "yalnız alış" hâline indirgenir ve beklenen
   getiri düşer.
3. **Portföy stratejisi ölçümü:** A ve B tek sinyal değil, günde N hisse
   seçiyor. Ölçüm makinesini portföy düzeyine genişletmemi ister misin,
   yoksa sinyal başına ölçüp portföy etkisini sonraya mı bırakalım?
