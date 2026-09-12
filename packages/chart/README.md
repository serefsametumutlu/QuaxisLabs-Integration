# quaxis.chart — ChartSpec v1 ve strateji komposerleri

Çizim kütüphanesinden bağımsız, versiyonlu bir **JSON çizim sözleşmesi** ve
strateji başına bir **komposer**. ADR-001 §4'ün karşılığıdır:

```
gösterge → TİPLİ SONUÇ → o tipe ait KOMPOSER → ChartSpec (JSON)
                                                 ├→ web çizici (apps/web)
                                                 └→ PNG çizici (rapor/Telegram, sonra)
```

**Jenerik çizici yok.** Eski mimaride 10 475 satırlık tek bir çizici 24
stratejiyi aynı primitif torbasıyla basıyordu; sonuç okunamayan, üst üste
binen, sessizce griye düşen grafiklerdi. Burada her strateji kendi
komposerine sahiptir ve komposer o stratejinin referans görselini üretmek
üzere bestelenir.

## Sözleşmenin üç yapısal güvencesi

| Eski mimarinin hatası | Nasıl imkânsız hâle geldi |
|---|---|
| Bilinmeyen stil adı sessizce griye düşüyordu | Roller **kapalı küme** (`roller.py`); tanınmayan ad `ValueError` atar. Aynı kontrol web çizicisinde de var. |
| Panel y aralığı keyfi katmanlardan hesaplanıyordu | Varsayılan aralık **yalnızca o panelin serilerinden** gelir. Komposer bilinçli genişletmek isterse `y` alanını gerekçesiyle **açıkça** yazar — ve yazdığı aralık seriyi **kırpamaz**. |
| Seriler iki uca indirgeniyordu | Her seri **tam dizi** taşır; nokta sayısı, zaman sırası ve mum tutarlılığı doğrulanır. |

Ayrıca: **ChartSpec renk taşımaz.** Yalnızca rol ve değer. Rengi çizici
tarafındaki rol tablosu verir (`apps/web/components/grafik/roller.ts`), o da
değerini tasarım token'larından okur. Hesap yapan renk seçmez, renk seçen
hesap yapmaz.

## Kullanım

```bash
cd packages/chart
python -m pytest tests -q      # 47 test
python uret.py                 # şema + örnek ChartSpec üretir
```

`uret.py` iki dosya yazar:

| Dosya | Ne |
|---|---|
| `sema/chartspec-1.0.schema.json` | Dilden bağımsız sözleşme (JSON Schema 2020-12). `sema.py` tarafından **enum'lardan türetilir** — elle yazılmaz, bu yüzden rol listeleriyle ayrı düşemez. |
| `../../apps/web/ornek/thyao-swing-fib-abcd.chartspec.json` | Web çizicisinin okuduğu örnek spec |

Web çizicisi bu JSON'u okur — TypeScript'te elle kurulmuş bir nesneyi değil.
Sözleşme ancak dil sınırını geçince sözleşmedir.

## Dizin

```
quaxis.chart/
  roller.py          kapalı rol kümesi (SeviyeRol, AlanRol, CizgiRol, …)
  spec.py            ChartSpec v1 dataclass'ları + doğrulama + JSON
  sema.py            JSON şeması, enum'lardan türetilir
  tipler.py          komposer GİRDİLERİ (göstergelerin tipli sonuçları)
  komposer/
    swing_fib_abcd.py   FibDuzeltmeSonucu → ChartSpec
  ornek/
    thyao_swing_fib_abcd.py   referans görselin sayılarıyla fikstür
tests/
  test_spec.py            sözleşmenin üç güvencesi
  test_komposer.py        referans sayıları ve non-repaint çizim kuralı
  test_sema.py            şema ile Python tarafının uyumu
  test_ciziciyle_uyum.py  Python rolleri ile web çizicisinin rolleri aynı mı
```

`test_ciziciyle_uyum.py` gerçek bir riski kapatır: biri `roller.py`'ye yeni bir
rol ekler, `apps/web`'e eklemeyi unutur. O zaman rol ChartSpec'te geçerli olur
ama ekranda hataya düşer — ya da daha kötüsü, ileride biri "hata atmasın" diye
varsayılana düşürür ve ADR-001'in yasakladığı sessiz griye dönüş geri gelir.

## Göstergeler nerede?

Henüz yok. ADR-002 gereği gösterge katmanı **sıfırdan** yazılacak ve her
strateji kendi fazında 7 kapıdan geçecek. Bu yüzden `swing_fib_abcd` komposerinin
girdisi şimdilik elle kurulan bir fikstür
(`ornek/thyao_swing_fib_abcd.py`) — sayıları `references/HRhIeAdbcAAL2_B.png`
referans görselinden okundu. Komposerin kendisi gerçek koddur ve gösterge
geldiğinde girdisi değişir, kendisi değişmez.

## Referanstaki mavi trend çizgisi neden yok?

`HRhIeAdbcAAL2_B.png`'de X'ten yukarı uzanan kesik-noktalı mavi bir çizgi var.
O çizgi **Salınım Fibo ABCD stratejisine ait değil**, ayrı bir trendline
göstergesinin çıktısı. Komposerin onu üretmesi katman ayrımını bozardı: her
komposer yalnız kendi stratejisinin çizimini üretir. `CizgiRol.TREND` rolü
sözleşmede hazır duruyor; trendline stratejisi yazıldığında kendi komposeri
onu üretecek.
