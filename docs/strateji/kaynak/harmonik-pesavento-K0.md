# Harmonik Formasyonlar (Pesavento) — K0 Kaynak Dosyası

**Tarih:** 2026-09-13 · **Pasaport:** `docs/strateji/harmonik-pesavento.md`
**Durum:** ✅ K1/K2 kodlandı (`indicators/harmonik/`). Sıradaki kapı **K3**.

**Kaynak:** Larry Pesavento & Leslie Jouflas, *Trade What You See: How to
Profit from Pattern Recognition* (Wiley, 2007), Böl. 4–7 ve 11.
Depodaki çıkarım: `Temel Analiz/bilanco-radar/bilgi-bankasi/teknik/10_pesavento_twys.md`

---

## 0. Kapsam

Bu turda **dört** formasyon: AB=CD, Gartley "222", Butterfly, Three Drives.

Kalan dört ekol (Bat / Crab / Shark — Carney, Cypher — Oglesbee, 5-0 —
Duddella) **bu kitapta yok** ve sonraki tura bırakıldı. Toplam sekiz olacak.

---

## 1. Dördünün paylaştığı iskelet

Dört formasyon da aynı yapıyı kullanır; farkları yalnız **oran tablosu**:

```
pivot zinciri  →  D bir FİYAT HEDEFİ olarak hesaplanır  →  fiyat D'ye dokunur  →  SİNYAL
```

**D bir pivot DEĞİLDİR.** Son pivot (C ya da Drive-öncesi) kesinleştiği anda
D deterministik olarak hesaplanabilir. Fiyatın D'ye ulaşması anlık bilinir —
ileriye bakış yok.

Bu, Golden Zone'da kurduğumuz yapının aynısı: çıpalar sabitlenir, seviye
hesaplanır, fiyat seviyeye dokununca sinyal doğar.

### Pivotlar ne zaman kesinleşir

Her pivot, **kendisinden sonraki** ters yönlü hareket başlayınca kesinleşir.
Yani `bar_time` (pivotun kendi barı) ile `detected_at` (teyit barı) FARKLIDIR.

Kaynağın kendi ifadesiyle: *"kesinleşme barı A'nın KENDİ barı DEĞİL, tersine
dönüşün teyit edildiği SONRAKİ bardır."*

---

## 2. Formasyon tabloları

### FORMASYON-01 · AB=CD

| | |
|---|---|
| **Noktalar** | A, B, C, D (X yok) — 3 bacak |
| **BC/AB geri çekilmesi** | .382 · .50 · .618 · .786 (güçlü trendde tipik olarak .382) |
| **CD/AB oranı** | **1.0** (vakaların ~%40'ı, simetrik) · **1.27–2.00+** (~%60) |
| **D nerede** | C'den, AB uzunluğu × CD oranı kadar |
| **AL sinyali** | Fiyat **D seviyesine dokunduğunda** |
| **Stop** | CD/AB = **1.272** seviyesi — kitap formül VERMİYOR, gerekçe §3 |
| **Hedef** | AD salınımının **.618** geri çekilmesi |
| **Geçersiz** | BC > AB · D, B'yi aşmıyorsa |
| **Ödül/risk** | ~**3.1 : 1** (risk = AB×0.272, ödül = AD×0.618) |

### FORMASYON-02 · Gartley "222"

| | |
|---|---|
| **Noktalar** | X, A, B, C, D — 4 bacak, **içinde AB=CD barındırması ZORUNLU** |
| **B ve C oranları** | **Kitap KESİN aralık VERMİYOR** — yalnız genel liste (.382/.50/.618/.786) |
| **D nerede** | **XA bacağının .786 geri çekilmesi** ← kitabın tüm ticaret örneklerinde tutarlı |
| **AL sinyali** | Fiyat **.786 seviyesine dokunduğunda** |
| **Stop** | **X'in hemen ötesi** (XA'nın %100'ü) |
| **Hedef** | AD salınımının **.618** geri çekilmesi |
| **Ödül/risk** | ~**2.3 : 1** |
| **Geçersiz** | D, X'i aşarsa · C, A'yı aşarsa · B, X'i aşarsa |

> **Kitabın iddiası:** Gartley'in ~**%70** başarı oranı olduğu söyleniyor
> (yazarın 30 yıllık gözlemi). Kaynak çıkarımı bunu *"bir kitap iddiasıdır,
> doğrudan güvenilecek bir sayı olarak alınmamalıdır"* diye işaretlemiş.
> **Ölçeceğimiz tam olarak bu.**

### FORMASYON-03 · Butterfly

| | |
|---|---|
| **Noktalar** | X, A, B, C, D — **D, X'in ÖTESİNE geçer** (uzantı paterni) |
| **AB geri çekilmesi** | .382 · .50 · .618 · .786 (tipik .618/.786) |
| **D nerede** | XA'nın **1.272 · 1.618 · 2.00 · 2.618** uzantılarından biri |
| **AL sinyali** | Fiyat **1.272 (ya da 1.618) seviyesine dokunduğunda** |
| **Stop** | 1.272'de girildiyse **1.618'in hemen dışı** |
| **Hedef** | AD salınımının **.618** geri çekilmesi |
| **Geçersiz** | AD içinde AB=CD yoksa · **2.618'in ötesi** · B, X'i aşarsa · C, A'nın ters tarafındaysa · **D, X'i AŞMIYORSA** |

> **Uyarı (PSK-04):** Butterfly başarısız olduğunda **çok hızlı ve büyük**
> hareketle başarısız olur. Kaynak "kalp zayıfları için değil" diyor.

### FORMASYON-04 · Three Drives

| | |
|---|---|
| **Noktalar** | Drive1, A, Drive2, C, Drive3 — 5 nokta |
| **Drive uzantıları** | Her bacak **1.272 veya 1.618** (genelde aynı oran ikisinde de) |
| **A ve C geri çekilmesi** | **.618 veya .786** (.382 = güçlü trend) |
| **D nerede** | Drive3 tamamlanma seviyesi (1.272/1.618) |
| **AL sinyali** | Fiyat **Drive3 seviyesine dokunduğunda** |
| **Stop** | Son salınım dip/tepesinin hemen ötesi |
| **Hedef** | Drive3 salınımının **.618** geri çekilmesi |
| **Geçersiz** | Her drive bir öncekinden ileri olmalı · C, A'nın ters tarafındaysa · **1.618'in ötesi** · Drive3'e doğru büyük gap |

> **Uyarı (PSK-05):** Three Drives **her zaman** büyük bir dönüş sinyali
> değil — bazen trend içinde sadece bir düzeltme. Ayrıca başarısız
> örnekleri *"geriye dönük bakıldığında bile fark edilmesi zor"*.
> Bu, ölçümde **hayatta kalma yanlılığı** riski demektir.

---

## 3. Kaynağın VERMEDİĞİ üç şey — ve ne yapacağız

Bunlar K0'ın en önemli kısmı: kitap her sayıyı vermiyor ve **vermediği yeri
uydurmayacağız.**

| Eksik | Kitapta | Bizim kararımız |
|---|---|---|
| **Oran toleransı** | **YOK.** Hiçbir formasyon için "±%5" gibi bir pay verilmiyor | `K3:` ölçümünden türetilecek. Önceki projede kullanılan ±.05 bandının *"kitaptan doğrudan türetilemediği, muhtemelen Carney'den ödünç alındığı"* kaynak çıkarımında açıkça yazılı |
| **Gartley B/C oranları** | **YOK.** Yalnız genel liste, hangi oran hangi bacağa ait belirsiz | **Kitabın kendi iki kuralından TÜRETİLEBİLİYOR** — aşağıya bak |
| **AB=CD stop mesafesi** | **YOK.** "Trader'ın risk toleransı" deniyor | Kitabın KENDİ oran kümesindeki bir sonraki uzantı: 1.0'da gir, **1.272'de çık** |

### 3.1 · Gartley'in B bacağı aslında serbest değil

Kodlarken çıkan sonuç. Kitap iki şey söylüyor:

1. D, XA'nın **.786**'sında.
2. Formasyonun içinde bir **AB=CD** bulunmalı.

İkisi birden yazılınca AB bacağı **serbest kalmıyor**. `AB=CD` şartı
`CD = AB` biçiminde okunursa (simetrik hâl) cebir tek bir bağıntı veriyor:

```
AB = .786 / (2 − BC)
```

| BC | Gereken AB | Kitabın kümesine uyuyor mu |
|---|---|---|
| .382 | .486 | ✔ (.50'ye ±.014) |
| .500 | .524 | ✔ (.50'ye ±.024) |
| .618 | .569 | ~ (.618'e ±.049, sınırda) |
| .786 | .647 | ✔ (.618'e ±.029) |

Yani **AB ≈ .49–.65 bandı**. Kitabın söylemediği sayı, söylediği iki
kuraldan çıkıyor. Bunu eşik olarak sabitlemiyoruz — dedektör yine genel
kümeyi tarıyor — ama `K3:` bu bandın dışında bir yoğunluk bulursa
kuralların birbiriyle çeliştiğini bileceğiz.

### 3.2 · "İçinde AB=CD olmalı" ne demek — ölçülmüş bir hata

Bu şartı önce **`CD = AB`** (yalnız 1.0) diye kodladım. Sonuç: Kelebek'te,
D'nin XA'nın 1.272'sinde sabit olmasıyla birleşince AB bacağı **tek bir
noktaya** çöküyordu (AB=.786 **ve** BC=.382). Kitabın tarif ettiği
Kelebek'lerin neredeyse hepsi daha doğmadan eleniyordu.

Doğru okuma kitabın kendi AB=CD bölümünde: **CD, AB'ye eşit olmak zorunda
değil** — 1.0 vakaların ~%40'ı, **1.27–2.00 ise ~%60'ı**. İçerideki AB=CD
şartı bu yüzden `CD/AB ∈ {1.0, 1.272, 1.618, 2.0}` olarak kodlandı ve
hangi orana uyduğu payload'a yazılıyor (`abcd`), ki K4 "simetrik olanlar
farklı mı davranıyor" sorusunu ölçebilsin.

## 4. Kaynaktan bilinçli sapmalar

| Sapma | Gerekçe |
|---|---|
| **Kademeli çıkış YOK** | Kitap 2–3 parçalı ölçekleme öneriyor. Biz **tek stop, tek hedef** ölçüyoruz: kademeli çıkış R dağılımını iyimser gösterir (Golden Zone'da aynı kararı verdik) |
| **"Shaded" limit emir YOK** | Kitap seviyenin 0.5–1 puan ötesine emir koymayı öneriyor (dolum şansı için). Biz **tam seviyeden** dolum varsayıyoruz; kaymayı işlem maliyetiyle modelliyoruz |
| **AB=CD stop yapısal** | Kitap formül vermiyor. Sabit bir TL/puan uydurmak yerine **C'nin ötesi** kullanılacak — formasyonun kendi geometrisinden gelen tek savunulabilir nokta |
| **1-bar bekleme (KURAL-30) dedektöre GİRMEDİ** | Kitap "uyarı işareti varsa 1 bar bekle" diyor ama "büyük gap", "geniş bar" için **eşik vermiyor**. Eşiği dedektöre gömmek, o eşiği sonradan sonuca göre seçme kapısını açardı. Uyarı/teyit işaretleri payload'a **sayı** olarak yazılıyor (`gap_atr`, `aralik_atr`, `kuyruk_kapanis`, `cimbiz`); bekleme tekniği K4'te veri üstünde, **ön kayıtlı** sınanacak |
| **Three Drives'a bir nokta daha eklendi** | Kitap "A geri çekilmesi" derken bir önceki BACAĞA göre ölçüyor. O bacağın başlangıcı (`O`) olmadan A'nın oranı hesaplanamaz; `O` olmasa kuralın yarısı sessizce uygulanmamış olurdu. Formasyon bu yüzden **beş** onaylı pivot istiyor: O · S1 · A · S2 · C |
| **Three Drives'ta "büyük gap" eşiği yok** | Kitap geçersizlik sayıyor ama eşik vermiyor. `gap_atr` sayı olarak yazılıyor, eleme yapılmıyor |
| **Three Drives dahil** | Önceki projede bu formasyon Pesavento ekolüne kodlanmamıştı. Kitapta var, biz dahil ediyoruz |

---

## 5. Ölçüm tasarımı

Golden Zone'un makinesi burada **doğrudan** kullanılabilir — çünkü yapı aynı:
kurulum kendi **stop'unu ve hedefini üretiyor**.

| | |
|---|---|
| Ölçüt | **Üç bariyerli R** (`olcum/bariyer.py`) — stop/hedef/zaman |
| Giriş | D seviyesi (limit emir), barın kapanışı DEĞİL |
| İşlem maliyeti | dahil |
| Aynı barda stop+hedef | **stop** |
| Bağımsız gözlem | sembol |
| Dört formasyon | **Ayrı ayrı** ölçülecek — "harmonikler çalışıyor mu" değil, **"hangisi çalışıyor mu"** |

Dört formasyon = dört test → **BH-FDR zorunlu.**

### Beklentiyi baştan yazıyorum

Önceki projenin ölçümünde `harmonic.carney` **−%3.66 (n=68)** ile negatif
taraftaydı. O ölçüm bu makineyle yapılmadı ve n çok küçüktü — kanıt değil.
Ama harmoniklerin önceki turda **üstte değil altta** çıktığı bir gerçek ve
K0 bunu saklamıyor.

---

## 6. Ne zaman çürütülmüş sayılır

* R, adil bazın altında kalırsa → kenar yok.
* Dört formasyonun hiçbiri BH-FDR'yi geçemezse → aile çürütülmüş sayılır.
* Bir formasyon geçer ama işlem maliyeti eşiğinde sıfırlanırsa → uygulanamaz.
* Sinyal sayısı sembol başına çok düşük çıkarsa (n<30) → sayı yazılır,
  verdikt yazılmaz.

---

## 7. Eşik çıpaları

Bu kaynak çıkarımında **sayfa numarası yok** — kitabın bölüm numaraları ve
çıkarımın kendi bölüm kimlikleri (`FORMASYON-01`, `KURAL-28` …) var. Bu
yüzden pasaportun eşik tablosunda `s.123` yazılmadı: olmayan bir sayfa
numarası yazmak, K0'ın önlemek için var olduğu şeyin ta kendisidir.

Onun yerine her eşik aşağıdaki **çıpalardan** birine bağlanır.
`tools/pasaport.py` bu dosyayı açıp çıpayı arar — yani bu satırlar
denetlenir, sayfa numarası gibi kimsenin bakmadığı bir iddia değildir.

| Çıpa | Neyi sabitler | Kitaptaki yeri |
|---|---|---|
| `ESIK-GERI-CEKILME` | .382 · .50 · .618 · .786 kümesi | Böl. 3, oran tablosu |
| `ESIK-UZANTI` | 1.0 · 1.272 · 1.618 · 2.0 kümesi | Böl. 3, oran tablosu |
| `ESIK-HEDEF` | Hedef = AD salınımının .618'i | her formasyonun hedef kuralı |
| `ESIK-ABCD-ICERIDE` | İçerideki AB=CD'nin CD/AB kümesi | AB=CD bölümü (bkz. §3.2) |
| `FORMASYON-01` | AB=CD'nin BC ve CD oranları | `10_pesavento_twys.md#FORMASYON-01` |
| `FORMASYON-02` | Gartley'de D = XA'nın .786'sı, stop X'in ötesi | `…#FORMASYON-02` |
| `FORMASYON-03` | Kelebek'te D=1.272, stop=1.618, azami 2.618 | `…#FORMASYON-03` |
| `FORMASYON-04` | Three Drives'ta 1.272/1.618 sürüş uzantıları | `…#FORMASYON-04` |

### Kitapta KARŞILIĞI OLMAYAN eşikler

Bunlar çıpa almaz; `K3:` bekler ve o ölçüm dosyası diskte belirene kadar
`pasaport.py dogrula` **bulgu yazmaya devam eder**. Bu bir arıza değil,
kapının kendisi:

* `tolerans` — kitap hiçbir formasyon için pay vermiyor.
* `donus_max_bar` — kitap süre sınırı koymuyor.
* `pivot_sol` / `pivot_sag` — kitap pivot tanımı vermiyor; şimdilik Golden
  Zone ile aynı tutuldu ki iki strateji kıyaslanabilsin.
* AB=CD'nin **stop** oranı — kitap "trader'ın risk toleransı" diyor.
  1.272, kitabın kendi oran kümesinden seçilmiş bir **başlangıç
  noktasıdır**, kural değil.
