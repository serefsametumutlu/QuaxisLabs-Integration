# references/ — hedeflenen görsel çıktının tanımı

Bu klasör bir ilham panosu **değil**. Buradaki her görsel, bir stratejinin
K5 (Görsel) kapısında **yan yana konulacak hedeftir**. "Güzel oldu" demek
yerine "bu dosyaya benziyor mu" diye sorulacak.

## Grafik referansları

Kaynak: `Desktop\Teknik Analiz\önemli\` + repo kökündeki örnekler.
Hepsi kullanıcının kendi seçtiği/onayladığı çıktılar.

| Dosya | Karşıladığı strateji görseli |
|---|---|
| `HRhIeAdbcAAL2_B.png` | **XABCD harmonik + fibo merdiveni** — dolgulu XAB/BCD üçgenleri, sağ kenarda oran-renkli fibo seviyeleri (`0.618: 185.00`), `D: 159.40 [TAMAMLANDI]` kutulu etiketi, HH/HL/LH/LL swing etiketleri. **En yüksek çıta budur.** |
| `HRdEu6qaoAEaHIT.png` | A-B-C-D salınımı + teorik/gerçek D; birleşik hover kutusu (`hovermode="x unified"` benzeri) |
| `HRjNKRZWAAAhfSy.png` | Yatay aralık (range box) — destek/direnç + numaralı temaslar |
| `HRihBa2WIAIZjP_.png` | Üçgen — sınır çizgisi temasları **numaralı dairelerle** (`U1,U2,U3` / `L1,L2,L3`) |
| `HRiPy4qbUAA1bKc.png` | Simetrik / alçalan üçgen |
| `HRiOTwUbQAA9WKw.png` | Yükselen/alçalan paralel kanal; `3A / 6A / 1Y / Tümü` zaman aralığı düğmeleri |
| `HRaULXwaEAA60Z5.png` | Bayrak / flama (direk + konsolidasyon + kırılım) |
| `HRhMNlYbwAACrVs.png` | Üç itiş (three drives) — **yalnızca üç etiket, başka hiçbir şey yok** |
| `HRcUk75bgAApv6n.png` | Çift sağlığı (pair health) paneli — normalize fiyat, z-skoru, tutulan dönem gölgeleri |
| `HRb_x7YWYAA750T.png` | Likidite radarı (Corwin–Schultz spread + sigma) |
| `HRt3uuwaEAAWAgK.png` | İstatistik tablosu — METRİK / DEĞER / DURUM, pozitif-negatif satır rengi |
| `ornek1.png` | Piyasa yapısı — HH / LH / HL / LL üçgenleri, BOS / CHoCH |
| `TOBO.png` | OBO / TOBO — boyun çizgisi, hologram, uç üçgenleri |
| `ornek2.png`, `yeni strateji.png` | *(kullanıcıya sorulacak — hangi stratejiyi karşıladığı belgelenmedi)* |

### Bu görsellerden çıkarılan ortak kural

Hiçbiri jenerik bir çizicinin çıktısı değil. Her biri **o stratejiye özel
bestelenmiş**: farklı etiket biçimi, farklı vurgu, farklı sadelik derecesi.
Three Drives'ta üç etiketten başka hiçbir şey yokken, harmonikte tam bir fibo
merdiveni var. Bu yüzden mimaride tek renderer değil, **strateji başına
komposer** var (bkz. `docs/karar/ADR-001-yeniden-insa.md`).

## Arayüz referansları

`referans_token_olcumleri.json` — kullanıcının verdiği dört sitenin
(dovetail.com, slash.com, v7labs.com, luxalgo.com) gerçek `getComputedStyle`
ölçümleri. Sentezi: [`docs/design/TASARIM_DILI.md`](../docs/design/TASARIM_DILI.md).
