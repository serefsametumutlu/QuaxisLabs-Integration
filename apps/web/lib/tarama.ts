/**
 * GERÇEK tarama çıktısı — `tools/tarama_disaktar.py` üretir, burada tiplenir.
 *
 * Akış: `tools/tarama.py kos` → `outputs/results.db` →
 * `tools/tarama_disaktar.py` → `tarama-verisi.json` → bu dosya → yüzey.
 *
 * JSON derleme anında okunur. Sebebi `tarama_disaktar.py`'nin başında yazılı:
 * tarama günde bir kere koşuyor, istek anında veritabanı okumak tazelik
 * kazandırmaz ama statik dışa aktarımı (görsel kabul döngüsünün dayandığı şey)
 * kırar ve web'i doğrudan motorun deposuna bağlar.
 *
 * **Verdikt uydurulmaz.** Her satırın rozeti, göstergesini sahiplenen
 * pasaportun künyesindeki `verdikt` alanıdır; `tools/pasaport.py dogrula`
 * katalogdaki her göstergenin tam bir pasaport tarafından sahiplenildiğini
 * denetler.
 *
 * **Şirket adı alanı YOK.** Evren dosyasında sembol var, ad yok. Maket veride
 * "Türk Hava Yolları" yazıyordu çünkü elle yazılmıştı; elimizde olmayan bir
 * alanı doldurmak maket veriyi gerçek diye sunmak olurdu.
 */

import ham from "./tarama-verisi.json";

export type Yon = "up" | "down";

/** Pasaport künyesindeki `verdikt` alanının insan okunur karşılığı. */
export type Verdikt = "ölçülmedi" | "kanıtlanmadı" | "izlenen aday" | "kenar var";

export type TaramaSatiri = {
  id: string;
  sembol: string;
  zamanDilimi: string;
  paket: string;
  /** Göstergenin pasaportta bildirilen görünen adı. */
  strateji: string;
  gosterge: string;
  /** Rozetin geldiği pasaportun slug'ı — kütüphane sayfasına bağlanır. */
  pasaport: string;
  yon: Yon;
  durum: string;
  /** Sinyalin doğduğu bardan bu yana kaç bar geçti. */
  yas: number | null;
  fiyat: number;
  seviye: number | null;
  stop: number | null;
  hedef: number | null;
  /** `seriler` sözlüğündeki anahtar (`SEMBOL|1D`). Fiyat serisi satıra değil
   *  SEMBOLE ait: aynı sembolün iki stratejisi aynı seriyi paylaşır. */
  seriAnahtari: string;
  verdikt: Verdikt;
};

export type TaramaKunye = {
  runId: string;
  tarih: string;
  market: string;
  /** Taranan zaman dilimleri: `kod` satırlarla eşleşen kanonik yazım
   *  ("1D"), `ad` arayüzde görünen Türkçe etiket ("1G"). */
  zamanDilimleri: { kod: string; ad: string }[];
  /** Evren dosyasındaki sembol sayısı. */
  evren: number | null;
  /** GERÇEKTEN taranan sembol — evrenle aynı değil. */
  taranan: number;
  /** Sağlayıcının veri döndürmediği semboller. Atılan veri raporlanır. */
  verisiGelmeyen: string[];
  gitSha: string | null;
  /** Taramanın gerçek süresi. Maket sürümde "6dk 22sn" elle yazılıydı. */
  sureSn: number | null;
  uretildi: string;
  /** Filtreye uyan toplam sinyal — kesmeden ÖNCE. */
  eslesen: number;
  yazilan: number;
  /** Satır sınırı yüzünden JSON'a girmeyen sinyal sayısı. Sessiz kırpma yasak. */
  kesilen: number;
  /** Sinyali olan ama fiyat serisi okunamayan sembol sayısı. */
  veriYok: number;
  azamiYas: number | null;
};

export type TaramaVerisi = {
  kunye: TaramaKunye;
  sayaclar: { paket: Record<string, number>; sembol: number };
  /** `SEMBOL|1D` → son 22 kapanış. Satır başına gömülseydi dosya iki katı olurdu. */
  seriler: Record<string, number[]>;
  satirlar: TaramaSatiri[];
};

export const TARAMA: TaramaVerisi = ham as TaramaVerisi;

export const VERDIKT_ACIKLAMA: Record<Verdikt, string> = {
  "ölçülmedi": "K4 (istatistik) kapısı henüz açılmadı",
  "kanıtlanmadı": "ölçüldü; adil baza karşı fark FDR eşiğini geçemedi",
  "izlenen aday": "ölçüldü; en az çürütülmüş grupta",
  "kenar var": "ölçüldü; FDR eşiğini geçti",
};

/** Kapanış taraması saati. Tek yerde dursun: duyuru şeridi ve üst bar okur. */
export const TARAMA_SAATI = { saat: 18, dakika: 15, metin: "18:15" } as const;

/** Kolon başlığı zaten "Yaş" diyor; "önce" eki 3 haneli yaşlarda hücreyi
 *  taşırıyor ve "135 mum ..." diye kesiliyordu. */
export function yasEtiketi(n: number | null) {
  if (n === null) return "—";
  return n === 0 ? "son mum" : `${n} mum`;
}

/** Sparkline kaç bar taşıyor — kolon başlığı bunu yazar.
 *  Başlık "20 bar" diye sabitti ama dışa aktarım 22 bar yolluyor; iki bar
 *  fark küçük ama yazan sayı ölçülen sayı değildi. */
export const SERI_BAR = Object.values(TARAMA.seriler)[0]?.length ?? 0;

/** Satırın fiyat serisi. Anahtar yoksa boş dizi — sparkline çizilmez. */
export function seri(satir: TaramaSatiri): number[] {
  return TARAMA.seriler[satir.seriAnahtari] ?? [];
}

/** Paket başına satır — sol raydaki sayaçlar bunu okur, elle sayı yazılmaz. */
export function paketSayaci(): Record<string, number> {
  return TARAMA.sayaclar.paket;
}

/**
 * Giriş ekranındaki olgu şeridi — hepsi doğrulanabilir sayılar.
 *
 * İkisi koşudan türetilir, ikisi sabittir ve kaynağı yanında yazılıdır.
 * Eskiden burada "4S + 1G" ve "586 sembolde OOS ölçümü" yazıyordu: ilki
 * taranmayan bir zaman dilimini sayıyordu, ikincisi veri düzeltmesinden
 * önceki evrendi (bkz. docs/olcum/onkayit-veri-duzeltme.md §8).
 */
export const OLGULAR = [
  { n: String(TARAMA.kunye.evren ?? "—"), t: "BIST sembolü" },
  { n: TARAMA.kunye.zamanDilimleri.map((z) => z.ad).join(" + "), t: "zaman dilimi" },
  { n: "7", t: "kapılı strateji süreci" },
  // docs/olcum/golden-zone-K4-katmanli-2026-09-17.md — A katmanında ölçülen sembol
  { n: "599", t: "sembolde OOS ölçümü" },
] as const;
