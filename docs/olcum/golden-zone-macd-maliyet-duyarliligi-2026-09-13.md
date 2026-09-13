# golden-zone-macd — Maliyet Duyarlılığı

**Tarih:** 2026-09-13 · **Koşul:** `macd_uyum` (MACD histogramı sinyal yönünde)
**Pencere:** OOS · **Grup:** B ·
**İşlem:** 2718

Tek bir maliyet düzeyinde "kenar var" demek, o düzeyin doğru olduğunu
varsaymaktır. Bu tablo bunun yerine **kenarın hangi maliyette sıfırlandığını**
söyler; karar verecek olan o eşiği kendi aracı kurum komisyonuyla
karşılaştırır.

| Gidiş-dönüş maliyet | Ort. R | Adil baz | Koşulsuz tabana ΔR | p | Verdikt |
|---|---|---|---|---|---|
| %0.00 | +0.160R | +0.076R | +0.097R | 0.0020 | kenar-var |
| %0.06 | +0.149R | +0.066R | +0.097R | 0.0020 | kenar-var |
| %0.15 | +0.133R | +0.049R | +0.096R | 0.0020 | kenar-var |
| %0.30 | +0.105R | +0.022R | +0.094R | 0.0020 | kenar-var |
| %0.45 | +0.078R | -0.005R | +0.093R | 0.0020 | kenar-var |
| %0.75 | +0.023R | -0.059R | +0.090R | 0.0020 | kenar-var |

> Maliyet **baza da** uygulanır — yalnız gerçek işlemlere uygulamak ölçümü
> stratejinin aleyhine saptırırdı.

## Nasıl okunur

`Ort. R` sıfırın altına indiği düzeyde strateji **para kaybettirir**.
Sıfırın üstünde ama `adil baz`ın altında kaldığı düzeyde kaybettirmez ama
**piyasanın kendi verdiğinin altında** kalır. İkisinin arasındaki aralık,
stratejinin yaşayabileceği maliyet penceresidir.

BIST'te aracı kurum komisyonu taraf başına %0.01–%0.15 arası değişir;
likit olmayan sembollerde spread ve kayma bunun katı olabilir. Tablodaki
eşik **kendi maliyetinle** karşılaştırılmalı.

## Ölçümün sınırları

| | |
|---|---|
| Kayma modeli | Sabit oran. Gerçekte emir büyüklüğüne ve likiditeye
bağlıdır; küçük sembollerde bu tablo iyimserdir. |
| Giriş | Limit emir varsayıldı (bölge seviyesine). Dolmama riski modellenmedi. |
| Vergi/stopaj | yok |
