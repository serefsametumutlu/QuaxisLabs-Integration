/** Gezinme tablosu — sol ray, üst şerit ve Ctrl+K paleti aynı kaynaktan okur.
 *
 * **Sayaçlar artık sayılıyor, yazılmıyor.** Eskiden burada `sayac: "47"`,
 * `Yapı 4 · Formasyon 3 · Trend 2` ve `Takip listem 21` elle yazılıydı;
 * hiçbirinin arkasında kod yoktu (ENVANTER.md bunu "maket veri" diye
 * işaretlemişti). Şimdi tarama sayacı gerçek koşudan, kütüphane ve paket
 * sayaçları strateji kayıt defterinden geliyor.
 *
 * "Takip listem" kaldırıldı: öyle bir özellik yok. Olmayan bir yüzeye sayaçlı
 * bir bağlantı koymak, maket satır göstermenin başka bir biçimiydi.
 */

import { STRATEJILER } from "./ornek-strateji";
import { TARAMA } from "./tarama";

export type Yuzey = {
  ad: string;
  yol: string;
  sayac?: string;
  /** Faz 3'te yalnız iskeleti var; içerik sonraki fazlarda dolacak. */
  hazir?: boolean;
};

export const YUZEYLER: Yuzey[] = [
  { ad: "Tarama", yol: "/tarama", sayac: String(TARAMA.satirlar.length), hazir: true },
  { ad: "Grafik", yol: "/grafik", hazir: true },
  {
    ad: "Strateji Kütüphanesi",
    yol: "/stratejiler",
    sayac: String(STRATEJILER.length),
    hazir: true,
  },
  { ad: "Tasarım Sistemi", yol: "/tasarim", hazir: true },
];

/** Paket başına strateji sayısı — kayıt defterinden sayılır. */
function paketSayisi(ad: string): string {
  return String(STRATEJILER.filter((s) => s.paket === ad).length);
}

export const PAKETLER = [
  { ad: "Yapı", sayac: paketSayisi("Yapı"), yol: "/stratejiler?paket=yapi" },
  { ad: "Formasyon", sayac: paketSayisi("Formasyon"), yol: "/stratejiler?paket=formasyon" },
  { ad: "Trend & Momentum", sayac: paketSayisi("Trend & Momentum"), yol: "/stratejiler?paket=trend" },
  {
    ad: "İstatistiksel Arbitraj",
    sayac: paketSayisi("İstatistiksel Arbitraj"),
    yol: "/stratejiler?paket=arbitraj",
    pasif: true,
  },
];

export const EVREN = [
  { ad: "BIST Tümü", sayac: String(TARAMA.kunye.evren ?? "—"), yol: "/tarama" },
];

export const PAZARLAMA_MENU = [
  { ad: "Tarama", yol: "/tarama" },
  { ad: "Stratejiler", yol: "/stratejiler" },
  { ad: "Grafik", yol: "/grafik" },
  { ad: "Yöntem", yol: "/#yontem" },
];
