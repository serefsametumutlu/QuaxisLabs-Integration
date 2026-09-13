# Golden Zone (ICT OTE) — K0 Kaynak Dosyası

**Tarih:** 2026-09-13 · **Pasaport:** `docs/strateji/golden-zone.md`

Bu dosya stratejinin **doğduğu yerdir**. Buradaki her kural ya bir kaynağa ya
da bir ölçüme bağlıdır. Bağlanmamış tek bir sayı yoktur.

---

## 0. Önce bir düzeltme: bu strateji harmonik formasyon DEĞİL

Faz 4'te `altin_bolge` adıyla yazılan komposer `references/HRhIeAdbcAAL2_B.png`
görselini üretiyordu. O görsel bir **XABCD harmonik formasyonu**: beş köşe,
C→D izdüşümü, tamamlanma rozeti. Golden Zone bambaşka bir şeydir:

| | Harmonik XABCD | Golden Zone (OTE) |
|---|---|---|
| Nesne | Beş köşeli **formasyon** | Tek salınımın **bölgesi** |
| Fibo neye çekilir | X→A, A→B, B→C ayrı ayrı | **Tek** yer değiştirme bacağı |
| Ne bekler | D noktasının tamamlanması | Bölgeye **dönüş** |
| Zamanlama | Formasyon kapanınca | Kırılımdan **sonra** |

Komposer Faz 7.1'de `swing_fib_abcd` olarak yeniden adlandırıldı. Golden Zone
kendi komposerini bu fazda alacak.

---

## 1. Kuralın kaynağı

Golden Zone / OTE bir **uygulayıcı geleneğidir**, akademik bir makale değil.
Bu yüzden K0 iki ayaklı kuruldu ve iki ayak farklı ağırlık taşır:

| Ayak | Ne veriyor | Ağırlığı |
|---|---|---|
| ICT/SMC uygulayıcı literatürü (internet) | **Mekanik kural**: neyin neye çekildiği, sıra, geçersizlik | Kuralı tanımlar, eşiği MEŞRULAŞTIRMAZ |
| Quant Playbook kitapları | **Ölçüm yöntemi**: nasıl etiketlenir, nasıl doğrulanır, ne zaman inanılır | Eşiğin geçerliliğini belirler |

**Kullanıcı kararı (2026-09-13): "Eşiklerin tamamı K3 ölçümünden türetilsin."**
Uygulayıcı kaynaklardaki sayılar bu yüzden *başlangıç değeri* olarak alınır,
*gerekçe* olarak değil. Gerekçe K3'ün ölçüm dosyasıdır.

### 1.1 Mekanik kural — ICT OTE

Kaynak: ictkillzone.com/ict-ote (erişim 2026-09-13), forexbee.co, innercircletrader.net

Olay sırası **zorunludur**, gevşetilemez:

```
1. likidite süpürmesi (sweep)      — önceki dip/tepe wick'le alınır
2. yer değiştirme + yapı kırılımı  (displacement + MSS/BOS)
3. bölgeye dönüş (0.62–0.79)       ← GİRİŞ BURADA
```

Fibonacci **iki uca** çekilir ve ikisi de sabittir:

| Uç | Boğa kurulumu | Ayı kurulumu |
|---|---|---|
| %100 | Süpürme mumunun **wick dibi** | Süpürme mumunun **wick tepesi** |
| %0 | Yer değiştirmenin **son mumunun tepesi** | Yer değiştirmenin **son mumunun dibi** |

> "anchor must be the sweep wick extreme — not a candle body, not an arbitrary
> preceding swing"

Seviyeler:

| Seviye | Anlamı |
|---|---|
| 0.62 | Bölgenin sığ ucu — ilk temas |
| **0.705** | "Sweet spot" — ortalama eşik |
| 0.79 | Bölgenin derin ucu — son geçerli giriş |
| 1.00 | Süpürme wick ucu — **stop referansı** |

Geçersizlik: **%100 seviyesinin ötesinde GÖVDE kapanışı.** Wick geçebilir,
gövde geçemez. Bu ayrım kodda birebir uygulanacak; "wick de geçersiz kılar"
demek sinyal sayısını sessizce yarıya indirir.

Hedef: yer değiştirmenin tepesi (%0 seviyesi — iç aralık likiditesi).

**Asimetri kurulumun kendi geometrisinden gelir.** Düzeltme TEPEDEN
ölçüldüğü için derine girmek stop'u küçültür, hedefi uzaklaştırmaz:

| Giriş | Risk (bacak oranı) | Ödül | Ödül/Risk | Başabaş isabet |
|---|---|---|---|---|
| 0.62 | 0.38 | 0.62 | **1.63** | %38 |
| 0.705 | 0.30 | 0.70 | **2.39** | %30 |
| 0.79 | 0.21 | 0.79 | **3.76** | %21 |

ICT'nin 0.705'e "sweet spot", derin girişe "optimal" demesinin sebebi bu
aritmetiktir — mistik bir oran değil.

**Bu kurulum kendi stop'unu ve hedefini KENDİ üretir.** Ölçüm bunları
uydurmaz — Faz 7.1'de K4'e eklenen üç bariyerli R ölçümünün çalışması için
gereken tam olarak buydu.

### 1.2 Uygulayıcı literatürün kendi iddiası — ve onun sınırı

Satıcı tarafı: EUR/USD 2021–2024, Londra/New York seansları, **üç koşul aynı
anda sağlandığında** 0.705 isabeti %55–65 olarak bildiriliyor (4S trend BOS ile
teyitli + 0.618–0.705 bölgesine dönüş + M5'te FVG ya da Order Block). Aynı
kaynak, kill zone dışında bu oranın belirgin düştüğünü söylüyor.

Bağımsız taraf: geniş bir yapay zekâ destekli çalışma, kavram başına güven
aralıklarının **sıfırı kestiğini** buldu; üst zaman dilimi eğilimi dışında
hiçbir tekil ICT kavramı istatistiksel olarak "kenar" sayılamadı. Aynı çalışma
**teyitli varyantların** (OTE + FVG) risk-ayarlı ölçütleri iyileştirdiğini, ama
işlem sıklığını düşürdüğünü bildiriyor.

**K0'ın buradan çıkardığı sonuç şudur:** iki taraf çelişmiyor. İkisi de aynı
şeyi söylüyor — *tek başına bölge kenar değil; teyit katmanı kenar üretiyor
olabilir, bedeli örneklem.* Bu bir hipotezdir ve Faz 7.1 tam olarak bunu
ölçecek. Hangi katmanın kenar **eklediği** ölçülmeden hiçbiri kanıtlanmış
sayılmaz.

---

## 2. Ölçüm yöntemi — kitaplardan, sayfa numarasıyla

### 2.1 Etiketleme: üç bariyer

**López de Prado, *Advances in Financial Machine Learning*, s.45**
(`Quant Playbook/books/Group 1…/MD formatı/Advances In Financial Machine Learning.md`)

> "I call it the triple-barrier method because it labels an observation
> according to the first barrier touched out of three barriers. … If the
> vertical barrier is touched first, we have two choices: the sign of the
> return, or a 0."

Uygulanışı: `packages/teknik/quaxis/teknik/olcum/bariyer.py`. Dikey bariyerde
getirinin işareti alındı (kitabın kendi tercihi). **İleri getiri tek başına
yetmez** — Golden Zone'un bütün iddiası asimetrik R'dir; zaman bazlı çıkış onu
görmez. ICT'yi "kenar yok" diye bulan geniş çalışmanın yapısal kusuru buydu.

### 2.2 Katmanlama: meta-etiketleme

**López de Prado, s.50–53**

> "I call this problem meta-labeling because we want to build a secondary ML
> model that learns how to use a primary exogenous model." (s.50)

> "First, we build a model that achieves high recall, even if the precision is
> not particularly high. Second, we correct for the low precision by applying
> meta-labeling to the positives predicted by the primary model." (s.51–53)

Bu, katmanlı ölçümün **kitaptaki karşılığıdır**:

| Katman | Meta-etiketlemedeki rolü |
|---|---|
| A · BOS + OTE bölgesi | **Birincil model** — yönü belirler; yüksek recall / düşük precision beklenir |
| B · + FVG ya da Order Block | **İkincil model** — "gireyim mi?" sorusunu yanıtlar, precision'ı düzeltir |
| C · + likidite süpürmesi | İkinci bir precision filtresi |

Ölçülecek soru katman başına **"kenar var mı"** değil, **"kenar EKLİYOR mu"**.

### 2.3 Katmanlamanın bedeli: serbestlik derecesi

**Pardo, *The Evaluation and Optimization of Trading Strategies*, s.291–293**
(`Quant Playbook/books/Group 4…/MD formatı/The Evaluation And Optimization Of Trading Strategies.md`)

> "It is a cardinal rule of statistical analysis that too many constraints—or
> too few degrees of freedom—on a data sample will lead to untrustworthy
> results." (s.292)

Her teyit katmanı bir kural daha, bir serbestlik derecesi daha ve daha küçük
bir örneklemdir. Katman ekledikçe "iyileşen" bir ölçüt, iyileşmeyi kenardan
değil örneklem küçülmesinden alıyor olabilir. Bu yüzden katman tablosunda R'nin
yanında **her zaman** işlem sayısı durur.

### 2.4 Ne zaman sayıya inanılır

**Pardo, s.295**

> "Thirty to 50 trades is an adequate minimum."

**K0 kuralı:** bir katman 30 işlemin altına düşüyorsa o katmanın R sayısı
**rapora yazılır ama verdikt üretmez**.

---

## 3. Eşikler ve kaynakları

| Eşik | Başlangıç değeri | Nereden | Nihai kaynak |
|---|---|---|---|
| Bölge sığ ucu | 0.62 | ICT OTE mekaniği | `K3:` ölçümünden türetilecek |
| Bölge derin ucu | 0.79 | ICT OTE mekaniği | `K3:` ölçümünden türetilecek |
| Sweet spot | 0.705 | ICT OTE mekaniği | `K3:` ölçümünden türetilecek |
| Yer değiştirme eşiği (asgari bacak) | ölçülecek | — | `K3:` |
| Süpürme toleransı | ölçülecek | — | `K3:` |
| FVG asgari boşluğu | ölçülecek | — | `K3:` |
| Bölgeye dönüş için azami bar | ölçülecek | — | `K3:` |
| Stop tamponu | 0 (wick ucu) | ICT: "beyond this level" | `K3:` |
| Hedef | %0 seviyesi | ICT: displacement high | sabit, kuraldan |
| Zaman bariyeri | ölçülecek | — | `K3:` |

**Kullanıcı kararı gereği hiçbir eşik kitaptan alıntıyla meşrulaştırılmıyor.**
ICT sayıları sadece aramanın başlangıç noktası. K3 koşulmadan K1/K2'de bu
değerler **varsayılan** olarak durur, **gerekçeli** değil — pasaportun K0
tablosundaki `K3:` devirleri K3 raporu yazılınca kapanır.

---

## 4. Kaynaktan sapmalar

| Sapma | Gerekçe |
|---|---|
| Kill zone (seans) filtresi **yok** | BIST ve NASDAQ günlük/4S taranıyor; ICT'nin seans penceresi FX intraday'e özgü. Filtre eklenirse ayrı bir katman olarak ölçülür, sessizce varsayılmaz. |
| "Daily bias" adımı **yok** | Öznel; kodlanabilir bir kural değil. Yerine BOS yönü kullanılıyor — ölçülebilir ve non-repaint. |
| Kademeli kâr alma / breakeven'a çekme **yok** | Ölçümde tek hedef, tek stop. Kademeli çıkış R dağılımını iyimser gösterir ve önceki projenin motorunda düzeltilen kusurlardan biriydi. Kaynakta displacement tepesi **T1**'dir ve koşucu ötedeki likiditeye gider; biz koşucuyu ölçmüyoruz, yani bu mod stratejinin LEHİNE değil aleyhine muhafazakârdır. |
| Hedef ayrıca sabit R katıyla da ölçülecek | Yapısal modda hedef mesafesi giriş derinliğiyle değişir (0.62'de 1.63R, 0.79'da 3.76R), yani farklı derinlikteki işlemler farklı risk profili taşır. `hedef_modu="r_kati"` hepsini aynı profile sabitler ve "bölgenin kendisi öngörü taşıyor mu" sorusunu derinlikten arındırır. İkisi AYRI sorular. |
| Aynı barda stop ve hedef → **stop** | Bar içi sıralama bilinmiyor. Emin olunmayan yerde stratejinin lehine varsaymak backtest'i yalancı yapar. |

---

## 5. Non-repaint gerekçesinin kaynağı

Her iki fibo ucu da giriş barından **kesinlikle önce** sabitlenir:

- %100 ucu → süpürme mumunun wick'i (geçmişte, kapanmış)
- %0 ucu → yer değiştirmenin son mumu (bölgeye dönüş başladığı anda kesinleşir)

Bu yüzden `detected_at` = fiyatın bölgeye **ilk girdiği barın kapanışı**;
`bar_time` = yer değiştirme bacağının bittiği bar. İkisi farklıdır ve fark
kaydedilir. Bacağın "en iyi" ucunu sonradan seçmek — ileriye bakıp daha yüksek
bir tepe bulunca çıpayı oraya kaydırmak — repaint'in ta kendisidir ve K2'nin
walk-forward testi bunu yakalayacak.

---

## Kaynaklar

- López de Prado, M. (2018). *Advances in Financial Machine Learning*, s.45, 50–53.
- Pardo, R. (2008). *The Evaluation and Optimization of Trading Strategies*, s.291–293, 295.
- [ICT OTE — The 62–79% Optimal Trade Entry Zone](https://www.ictkillzone.com/ict-ote)
- [ICT Optimal Trade Entry (OTE) Strategy: The 62–79% Fib Zone](https://forexbee.co/ict-optimal-trade-entry-ote-strategy/)
- [ICT Fibonacci Settings — OTE 70.5%](https://innercircletrader.net/tutorials/ict-fibonacci-levels/)
- [ICT Fibonacci and Golden Pocket: Finding the Optimal Trade Entry](https://backtrex.com/en/blog/ict-fibonacci-golden-pocket-ote-setup)
- [Is ICT Strategy Profitable? — bağımsız backtest](https://offbeatforex.com/is-ict-strategy-profitable/)
