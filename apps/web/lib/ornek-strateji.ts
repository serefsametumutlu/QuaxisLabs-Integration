/**
 * ÖRNEK strateji künyeleri — Faz 3 iskeleti için.
 *
 * Gerçek künye, Strateji Pasaportu'nun (docs/strateji/) çıktısı olacak ve
 * Bölüm C'de strateji strateji doldurulacak. Buradaki metinler sayfanın
 * yapısını göstermek içindir; ÖLÇÜM bölümündeki sayılar eski depodaki tam
 * evren koşusundan gelir ve yeni kodla K4 kapısında baştan ölçülecektir.
 */

import type { Verdikt } from "./ornek-veri";

export type ParametreGrubu = {
  baslik: string;
  alanlar: { ad: string; varsayilan: string; aciklama: string }[];
};

export type KaynakKutusu = {
  etiket: string;
  govde: string;
  kod?: string;
  /** Kod cümlenin başında mı okunuyor ("min_salinim_atr = 2.0 ... yok")? */
  kodOnce?: boolean;
  /** Kapanmamış kapı: kesikli kenarlık, "burada bir şey eksik" der. */
  acik?: boolean;
};

export type Strateji = {
  slug: string;
  ad: string;
  paket: string;
  ozet: string;
  verdikt: Verdikt;
  rozetler: string[];
  tip: "fib" | "ms" | "zone" | "fvg";
  /** Grafik levhasının yanındaki dört soru — TASARIM_DILI §7. */
  notlar: { baslik: string; govde: string }[];
  parametreler: ParametreGrubu[];
  kaynak: KaynakKutusu[];
  olcum: { satirlar: [string, string][]; uyari: string; kotu?: string } | null;
  sss: { soru: string; cevap: string }[];
};

export const STRATEJILER: Strateji[] = [
  {
    slug: "swing-fib-abcd",
    ad: "Salınım Fibo ABCD",
    paket: "Yapı",
    ozet:
      "Baskın salınımın 0.618–0.786 düzeltme bandı. Fiyat bölgeye döner ve tutamazsa, salınımın başlangıç seviyesinin altı hedeflenir.",
    verdikt: "kanıtlanmadı",
    rozetler: ["4S · 1G", "648 sembol"],
    tip: "fib",
    notlar: [
      {
        baslik: "Nereye bak",
        govde:
          "Sağ kenardaki merdiven. 0.618–0.786 arası altın bölgedir; fiyat oraya dönüp tutamazsa X seviyesinin altı hedef olur.",
      },
      {
        baslik: "Ne ölçer",
        govde:
          "Baskın X→A salınımının düzeltme derinliğini. Baskın salınım seçimi 150 sembolde backtest edildi: en baskın %86.7, en yeni yalnızca %59.3.",
      },
      {
        baslik: "Sinyal ne zaman doğar",
        govde:
          "C oluşup fiyat 0.786'yı kapanışta aşağı kırdığında. Sinyal pivotun barını değil, onaylandığı barı taşır — sonradan değişmez.",
      },
      {
        baslik: "Değerler ne demek",
        govde:
          "1.272 = D hedefi, 1.618 = azami risk. İkisi arası kapanış, formasyonun tamamlandığı bölgedir.",
      },
    ],
    parametreler: [
      {
        baslik: "Salınım tespiti",
        alanlar: [
          {
            ad: "pivot_sol",
            varsayilan: "5",
            aciklama: "Bir tepenin pivot sayılması için solunda kaç barın daha alçak kapanması gerektiği.",
          },
          {
            ad: "pivot_sag",
            varsayilan: "5",
            aciklama:
              "Aynısı sağ taraf için. Pivot ancak bu kadar bar geçince onaylanır — sinyal o barın tarihini taşır, pivotun kendi barını değil.",
          },
          {
            ad: "min_salinim_atr",
            varsayilan: "2.0",
            aciklama: "Bir salınımın dikkate alınması için kaç ATR uzunluğunda olması gerektiği. Gürültüyü eler.",
          },
        ],
      },
      {
        baslik: "Bölge",
        alanlar: [
          { ad: "bolge_alt", varsayilan: "0.618", aciklama: "Altın bölgenin sığ ucu. Fibonacci düzeltme oranı." },
          {
            ad: "bolge_ust",
            varsayilan: "0.786",
            aciklama: "Derin ucu. Buranın altına kapanış, düzeltmenin başarısız sayıldığı eşiktir.",
          },
          {
            ad: "baskinlik",
            varsayilan: '"en_buyuk"',
            aciklama:
              "Hangi salınımın bölgeyi tanımladığı. En yeni değil en baskın — 150 sembolde ölçüldü, aradaki fark 27 puan.",
          },
        ],
      },
      {
        baslik: "Onay",
        alanlar: [
          {
            ad: "sadece_kapanis",
            varsayilan: "true",
            aciklama:
              "Fitil değmesi sinyal saymaz; seviyenin kapanışta kırılması gerekir. Açık bar asla sinyal üretmez.",
          },
          {
            ad: "max_bar",
            varsayilan: "180",
            aciklama:
              "Bir salınımın geçerli kalacağı azami süre. Sınırsız bırakılırsa yıllarca süren sahte formasyonlar doğuyor — bu ölçülmüş bir hatadır.",
          },
        ],
      },
    ],
    kaynak: [
      {
        etiket: "Birincil kaynak",
        govde: "Larry Pesavento — bilgi bankası çıkarımı. 0.618 ve 0.786 oranlarının alıntısı ve madde kodları K0 kapısında şu dosyadan girilecek:",
        kod: "bilgi-bankasi/teknik/10_pesavento_twys.md",
      },
      {
        etiket: "Ölçümle türetilen",
        govde:
          'baskinlik = "en_buyuk" — kitaptan değil backtest\'ten geldi. 150 BIST sembolü, 4159 salınım: en baskın salınım %86.7 başarı, en yeni salınım %59.3. Spearman ρ=0.24, p<0.0001, monoton.',
      },
      {
        etiket: "Açık — kapatılacak",
        govde:
          "değerinin kaynağı henüz yok. K0 kapısı kapanmadan bu alan boş bırakılamaz: ya kitaptan alıntılanacak ya da K3'te tam evren kalibrasyonuyla türetilecek.",
        kod: "min_salinim_atr = 2.0",
        kodOnce: true,
        acik: true,
      },
    ],
    olcum: {
      satirlar: [
        ["Evren", "586 sembol"],
        ["Bağımsız gözlem (sembol)", "553"],
        ["Pencere", "ilk %70 IS / son %30 OOS"],
        ["Ufuk", "20 bar"],
        ["Adil baza karşı fark", "+%0.42"],
        ["Permütasyon p değeri", "0.13"],
        ["K3 · tam evrende aday", "623 / 648 sembol"],
      ],
      kotu: "BH-FDR (q=0.05) · geçemedi",
      uyari:
        "Bu rakamlar eski depodaki tam evren koşusundan. Yeni kodla K4 kapısında baştan ölçülecek — strateji sıfırdan yazıldığı için eski ölçüm otomatik devretmez.",
    },
    sss: [
      {
        soru: "Sinyal sonradan kaybolur mu?",
        cevap:
          "Hayır. Sinyal, pivotun oluştuğu barın değil onaylandığı barın tarihini taşır ve geçmişe dönük hiçbir zaman değişmez. Her gösterge, tam seriyle farklı noktalardan kesilmiş serilerin aynı sonucu ürettiği walk-forward testinden geçmeden yayına alınamaz.",
      },
      {
        soru: "“Kanıtlanmadı” rozeti ne demek?",
        cevap:
          "Stratejinin ileriye dönük getirisi ölçüldü ve çoklu-test düzeltmesinden sonra sıfırdan ayırt edilebilir bir kenar bulunamadı. “Zarar ettiriyor” demek değil; “işe yaradığına dair elimizde kanıt yok” demek. Gizlemek yerine yazıyoruz.",
      },
      {
        soru: "Neden en yeni salınım değil en baskın salınım?",
        cevap:
          "Ölçtük. 150 sembolde 4159 salınımın nihai sonucu karşılaştırıldı: en baskın salınımın başarı oranı %86.7, en yeninin %59.3. 27 puanlık bu fark tesadüfle açıklanamaz. Bu bir tercih değil, bir bulgu.",
      },
    ],
  },
  {
    slug: "piyasa-yapisi",
    ad: "Piyasa Yapısı",
    paket: "Yapı",
    ozet:
      "HH / HL / LH / LL zinciri ve bunların kırıldığı noktalar: BOS (yapı kırılımı) ve CHoCH (karakter değişimi). Diğer yapı stratejilerinin altyapısı.",
    verdikt: "ölçülmedi",
    rozetler: ["4S · 1G", "648 sembol"],
    tip: "ms",
    notlar: [
      { baslik: "Nereye bak", govde: "Pivot zinciri ve kırılım barları. Etiketler pivotun kendi barında değil, onaylandığı barda belirir." },
      { baslik: "Ne ölçer", govde: "Ardışık tepe ve diplerin yönünü; trendin yapısal olarak sürüp sürmediğini." },
      { baslik: "Sinyal ne zaman doğar", govde: "Son korunan pivotun kapanışta kırıldığı barda. BOS trendi sürdürür, CHoCH yön değiştirir." },
      { baslik: "Değerler ne demek", govde: "Bu strateji seviye değil YAPI üretir; diğer stratejiler onun çıktısını girdi olarak kullanır." },
    ],
    parametreler: [
      {
        baslik: "Pivot",
        alanlar: [
          { ad: "pivot_sol", varsayilan: "5", aciklama: "Tepe/dip onayı için soldaki bar sayısı." },
          { ad: "pivot_sag", varsayilan: "5", aciklama: "Sağdaki bar sayısı. Non-repaint gecikmesi buradan doğar." },
        ],
      },
      {
        baslik: "Kırılım",
        alanlar: [
          { ad: "sadece_kapanis", varsayilan: "true", aciklama: "Fitil kırılımı sayılmaz." },
          { ad: "choch_dogrula", varsayilan: "true", aciklama: "Karakter değişimi için karşı yönde bir pivotun da onaylanmış olması aranır." },
        ],
      },
    ],
    kaynak: [
      {
        etiket: "Açık — kapatılacak",
        govde:
          "SMC / ICT literatürü ikincil kaynaktır; K0 kapısı birincil bir metin ve sayfa numarası ister. Bu strateji henüz K2 kapısında.",
        acik: true,
      },
    ],
    olcum: null,
    sss: [
      {
        soru: "“Ölçülmedi” ile “kanıtlanmadı” farkı ne?",
        cevap:
          "Ölçülmedi: K4 kapısı henüz açılmadı, elimizde hiç sayı yok. Kanıtlanmadı: ölçtük ve anlamlı bir kenar çıkmadı. İkisini aynı rozetle göstermek dürüst olmazdı.",
      },
    ],
  },
];

export function stratejiBul(slug: string) {
  return STRATEJILER.find((s) => s.slug === slug);
}
