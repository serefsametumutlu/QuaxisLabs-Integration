# golden-zone — Maliyet Duyarlılığı

**Tarih:** 2026-09-13 · **Koşul:** `oynaklik_dusuk` (ATR14/ATR50 < 1 — sakin rejim)
**Pencere:** OOS · **İşlem:** 5329

Tek bir maliyet düzeyinde "kenar var" demek, o düzeyin doğru olduğunu
varsaymaktır. Bu tablo bunun yerine **kenarın hangi maliyette sıfırlandığını**
söyler; karar verecek olan o eşiği kendi aracı kurum komisyonuyla
karşılaştırır.

| Gidiş-dönüş maliyet | Ort. R | Adil baz | Koşulsuz tabana ΔR | p | Verdikt |
|---|---|---|---|---|---|
| %0.00 | +0.069R | +0.028R | +0.024R | 0.0093 | kenar-var |
| %0.06 | +0.056R | +0.016R | +0.022R | 0.0093 | kenar-var |
| %0.15 | +0.038R | -0.003R | +0.019R | 0.0093 | kenar-var |
| %0.30 | +0.006R | -0.034R | +0.014R | 0.0093 | kenar-var |
| %0.45 | -0.025R | -0.065R | +0.009R | 0.0093 | kanıtlanmadı |
| %0.75 | -0.089R | -0.127R | -0.002R | 0.0093 | kanıtlanmadı |

> Maliyet **baza da** uygulanır — yalnız gerçek işlemlere uygulamak ölçümü
> stratejinin aleyhine saptırırdı.

## p değeri neden hiç değişmiyor

Bütün satırlarda p=0.0093. Tesadüf değil: maliyet hem sinyali hem adil bazı
**neredeyse aynı kadar** aşağı çeker, aradaki fark sabit kalır. p o farkı
sınar, kârlılığı değil.

Bunun anlamı önemli: **"rastgeleden iyi" ile "para kazandırır" ayrı iki
sorudur.** p birincisini yanıtlar; bu tablonun `Ort. R` sütunu ikincisini.

## Nasıl okunur

`Ort. R` sıfırın altına indiği düzeyde strateji **para kaybettirir**.
Sıfırın üstünde ama `adil baz`ın altında kaldığı düzeyde kaybettirmez ama
**piyasanın kendi verdiğinin altında** kalır. İkisinin arasındaki aralık,
stratejinin yaşayabileceği maliyet penceresidir.

**Bu ölçümde eşik ~%0.30.** Gidiş-dönüş maliyetin %0.30'un altındaysa koşullu
kurulum pozitif kalıyor; üstündeyse para kaybettiriyor. %0.30, taraf başına
%0.10 komisyon + %0.10 kayma demektir — BIST'te düşük ama imkânsız değil.

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
