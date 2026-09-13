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
  /** K3/K4 kutusu. `null` = kapıya gelmedi; sayı UYDURULMAZ, kutu boş durur.
   *
   *  `sinyal` / `baz` / `p` sütun grafiğini besler. O grafik eskiden Golden
   *  Zone'un sayılarını SABİT taşıyordu; ikinci bir ölçülmüş strateji
   *  eklenince aynı çubuklar onun sayfasında da çıkacaktı — yani yanlış
   *  strateji için doğru görünen bir grafik. */
  olcum: {
    satirlar: [string, string][];
    uyari: string;
    kotu?: string;
    sinyal: number;
    baz: number;
    p: number;
    birim: "R" | "%";
  } | null;
  sss: { soru: string; cevap: string }[];
};

export const STRATEJILER: Strateji[] = [
  {
    slug: "harmonik-pesavento",
    ad: "Harmonik Formasyonlar (Pesavento)",
    paket: "Formasyon",
    ozet:
      "Almaşık salınım uçlarından Fibonacci oranlarına uyan bir zincir bulur, D diye bir fiyat hedefi HESAPLAR ve fiyat o seviyeye dokunduğu anda sinyal üretir. Dört formasyon: AB=CD, Gartley 222, Butterfly, Three Drives.",
    verdikt: "kanıtlanmadı",
    rozetler: ["4S · 1G · 1H", "545 sembol", "5703 sembol-yıl"],
    tip: "fib",
    notlar: [
      {
        baslik: "Nereye bak",
        govde:
          "Köşeleri birleştiren zikzağa ve en sağdaki D seviyesine. Son bacak KESİK çizilir: o bacak henüz gerçekleşmedi, hesaplandı.",
      },
      {
        baslik: "Ne ölçer",
        govde:
          "Bacaklar arasındaki oranların Fibonacci sayılarına uyup uymadığını. Her bacağın üstündeki sayı ölçülen orandır — formasyonun neden formasyon olduğunu gösteren tek şey.",
      },
      {
        baslik: "Sinyal ne zaman doğar",
        govde:
          "Fiyat D seviyesine dokunduğu anda. D bir pivot DEĞİL: son köşe (C) onaylandığında hesaplanan bir fiyattır. C onaylanmadan fiyat D'ye inerse sinyal HİÇ üretilmez.",
      },
      {
        baslik: "Değerler ne demek",
        govde:
          "Giriş D'nin kendisi. Stop ve hedef formasyonun kendi geometrisinden çıkar: Gartley'de stop X'in ötesi, Kelebek'te 1.618 uzantısı; hedef ikisinde de AD salınımının .618'i.",
      },
    ],
    parametreler: [
      {
        baslik: "Pivot ve oran",
        alanlar: [
          {
            ad: "pivot_sol / pivot_sag",
            varsayilan: "AB=CD 5, diğerleri 4",
            aciklama:
              "Bir salınım ucunun solunda/sağında kaç bar olmalı. Uç ancak sağındaki barlar kapandığında BİLİNEBİLİR — non-repaint sözleşmesinin temeli. Kitapta yok, K3 ölçümünden türetildi.",
          },
          {
            ad: "tolerans",
            varsayilan: "0.02 (Three Drives 0.05)",
            aciklama:
              "Bir oranın tuttuğu sayılması için izin verilen sapma. Kitap hiçbir formasyon için pay vermiyor; K3'te sinyal sayısı taranarak seçildi.",
          },
          {
            ad: "geri_cekilme_oranlari",
            varsayilan: ".382 / .50 / .618 / .786",
            aciklama: "Geri çekilme bacaklarının uyacağı oran kümesi. Kitaptan.",
          },
        ],
      },
      {
        baslik: "Seviyeler",
        alanlar: [
          {
            ad: "d_geri_cekilme (Gartley)",
            varsayilan: "0.786",
            aciklama:
              "D, XA bacağının bu kadarını geri çeker. Kitabın bütün ticaret örneklerinde .786.",
          },
          {
            ad: "d_uzanti / stop_uzanti (Kelebek)",
            varsayilan: "1.272 / 1.618",
            aciklama:
              "Giriş ve stop uzantıları. İkisi de kitaptan; 2.618'in ötesi formasyon değildir.",
          },
          {
            ad: "hedef_orani",
            varsayilan: "0.618",
            aciklama:
              "Hedef, AD salınımının bu kadarını geri çeker. Kitap ikinci hedef olarak .786 da veriyor; biz TEK hedef ölçüyoruz — kademeli çıkış R dağılımını iyimser gösterir.",
          },
          {
            ad: "donus_max_bar",
            varsayilan: "55 / 35 / 60 / 25",
            aciklama:
              "D'ye dokunmak için tanınan azami süre. Kitapta yok; dokunuş süresi dağılımının %90'lık diliminden okundu.",
          },
        ],
      },
    ],
    kaynak: [
      {
        etiket: "KİTAP",
        govde:
          "Larry Pesavento & Leslie Jouflas, Trade What You See (Wiley, 2007), Böl. 4-7 ve 11. Oran kümeleri, Gartley'de D'nin .786'da olması, Kelebek'te stop'un 1.618'de olması ve .618 hedef doğrudan kitaptan.",
      },
      {
        etiket: "TÜRETİLEN KURAL",
        kodOnce: true,
        kod: "AB = r / (k + 1 - BC)",
        govde:
          "kitabın SÖYLEMEDİĞİ bir şeyi, söylediği iki kuraldan çıkarıyor. Gartley'de D=.786 XA ve içinde AB=CD olmalı kuralları birlikte yazılınca AB bacağı serbest kalmıyor. 2081 gerçek Gartley'de AB=.786 SIFIR kez görüldü — kitabın kuralları onu imkânsız kılıyor ve kitap bunu hiçbir yerde yazmıyor.",
      },
      {
        etiket: "KİTAPTA OLMAYAN",
        acik: true,
        govde:
          "Tolerans payı, dönüş penceresi, pivot kolu ve AB=CD'nin stop mesafesi kitapta YOK. İlk üçü K3 kalibrasyonundan türetildi — yalnız aday sayısına bakılarak, getiriye BAKILMADAN. AB=CD'nin stop'u K3'te kapatılamadı (hangi mesafenin doğru olduğu bir getiri sorusu) ve K4'te iki ayrı künye olarak ölçüldü.",
      },
      {
        etiket: "BİLİNÇLİ SAPMA",
        govde:
          "Kitabın shaded limit emri kullanılmadı: tam seviyeden dolum varsayılıp kayma işlem maliyetine yazıldı. KURAL-30 (bir bar bekleme) dedektöre gömülmedi çünkü kitap gap ve geniş bar için eşik VERMİYOR; uyarı işaretleri payload'a sayı olarak yazılıp K4'te ön kayıtla sınandı.",
      },
    ],
    olcum: {
      satirlar: [
        ["Evren", "545 sembol · 1.44M bar · 5703 sembol-yıl"],
        ["Aile", "5 test (4 formasyon + AB=CD'nin 2. stop varyantı)"],
        ["AB=CD · işlem", "622 (325 sembol)"],
        ["AB=CD · isabet", "%41.6"],
        ["AB=CD · profit factor", "1.80"],
        ["Gartley · isabet", "%35.2 (kitabın iddiası ~%70)"],
        ["Butterfly · fark", "-0.423R"],
        ["Three Drives · fark", "-0.407R"],
      ],
      uyari:
        "Tabloda AB=CD satırı var çünkü örneklemi en büyük olan o. Dördü de FDR'yi geçemedi. İkinci bir ön kayıtlı deneme (KURAL-30 bir bar bekleme) isabeti %32.8'den %45.3'e çıkardı ama p=0.0685 ile düz 0.05 eşiğini bile geçemedi — ve etkinin tamamı IS penceresindeydi, görülmemiş dönemde fark sıfırdı.",
      kotu: "evet",
      sinyal: 0.459,
      baz: 0.367,
      p: 0.5612,
      birim: "R",
    },
    sss: [
      {
        soru: "Sinyal sonradan kaybolur mu?",
        cevap:
          "Hayır. Köşeler kendi barlarından birkaç bar sonra kesinleşir ve bir daha değişmez; D onlardan hesaplanır. Bekleyen kurulum grafikte ÇİZİLMEZ — yalnız tamamlanan çizilir.",
      },
      {
        soru: "C onaylanmadan fiyat D'ye inerse ne olur?",
        cevap:
          "Sinyal ÜRETİLMEZ. O anda formasyonun varlığını bilmiyorduk; dokunuşu sinyal saymak, gerçekte verilemeyecek bir emri ölçüme eklemek olurdu. Kaçan kaçmıştır.",
      },
      {
        soru: "Kitap Gartley için ~%70 isabet diyor, siz neden %35 buldunuz?",
        cevap:
          "O sayı kitabın yazarının otuz yıllık gözlemi olarak aktarılıyor; hiçbir ölçüm dosyasına dayanmıyor. Biz 545 BIST sembolünde, işlem maliyeti dahil, aynı barda stop ve hedef birlikte vurulduğunda STOP sayarak ölçtük: yalnız alış tarafında %41.4 (n=29), iki yön birlikte %36.2 (n=58).",
      },
      {
        soru: "Kenar bulunamadıysa neden hâlâ gösteriyorsunuz?",
        cevap:
          "Çünkü eleme değil ETİKETLEME yapıyoruz. Formasyon gerçekten oluşuyor ve kullanıcı onu görmek isteyebilir; ama sistem ona al demiyor ve grafiğin künyesinde tarihsel isabet: kanıtlanmadı yazıyor.",
      },
    ],
  },
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
      sinyal: 1.18,
      baz: 0.76,
      p: 0.13,
      birim: "%",
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
