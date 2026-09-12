/**
 * Rol → token eşlemesi. ChartSpec renk taşımaz; renk kararı BURADA verilir.
 *
 * Kural (TASARIM_DILI §5, bağlayıcı):
 *   · Aksan ASLA mum ölçeğinde dolu bir leke değildir — formasyon gövdesi
 *     düşük opaklıkta geniş dolgu, seviyeler 1px çizgi, rozetler hap formu.
 *   · Yön renkleri (al/sat) her zaman DOLU ve mum boyutundadır.
 *   · Hiçbir değer hardcoded renk değildir; hepsi token'dan okunur.
 *
 * Eşlemede olmayan bir rol hata atar — sessizce griye düşmek yasak.
 */

import {
  ChartSpecHatasi,
  type AlanRol,
  type CizgiRol,
  type EtiketRol,
  type IsaretRol,
  type RozetRol,
  type SeviyeRol,
  type Yon,
} from "@/lib/chartspec";

export type SeviyeStil = { token: string; kalinlik: number; kesik: string; opaklik: number; vurgulu: boolean };

const SEVIYE: Record<SeviyeRol, SeviyeStil> = {
  fib_0: { token: "--fib-0", kalinlik: 1, kesik: "6 4", opaklik: 0.72, vurgulu: false },
  fib_236: { token: "--fib-236", kalinlik: 1, kesik: "6 4", opaklik: 0.72, vurgulu: false },
  fib_382: { token: "--fib-382", kalinlik: 1, kesik: "6 4", opaklik: 0.72, vurgulu: false },
  fib_500: { token: "--fib-500", kalinlik: 1, kesik: "6 4", opaklik: 0.72, vurgulu: false },
  // 0.618 aksanın kendisidir: altın oran zaten "karara değer" seviye.
  fib_618: { token: "--accent", kalinlik: 1.4, kesik: "6 4", opaklik: 0.95, vurgulu: true },
  fib_786: { token: "--fib-786", kalinlik: 1.4, kesik: "6 4", opaklik: 0.95, vurgulu: true },
  fib_1: { token: "--fib-1", kalinlik: 1, kesik: "6 4", opaklik: 0.72, vurgulu: false },
  // D hedefi "karara değer" bir seviye: seyrek modda da gösterilir.
  fib_1272: { token: "--fib-ext", kalinlik: 1, kesik: "2 3", opaklik: 0.85, vurgulu: true },
  fib_1618: { token: "--fib-ext", kalinlik: 1, kesik: "2 3", opaklik: 0.72, vurgulu: false },
  seviye: { token: "--text-3", kalinlik: 1, kesik: "4 4", opaklik: 0.7, vurgulu: false },
  son_fiyat: { token: "--text", kalinlik: 1, kesik: "1 3", opaklik: 0.8, vurgulu: false },
};

export type AlanStil = { token: string; dolgu: number; kenar: number; kenarOpaklik: number };

const ALAN: Record<AlanRol, AlanStil> = {
  // %10 dolgu: aksan geniş ama SOLUK — mum ölçeğinde leke olmaz.
  formasyon: { token: "--accent", dolgu: 0.1, kenar: 1.3, kenarOpaklik: 0.55 },
  bolge_altin: { token: "--accent", dolgu: 0.085, kenar: 0, kenarOpaklik: 0 },
  bolge_arz: { token: "--down", dolgu: 0.16, kenar: 0, kenarOpaklik: 0 },
  bolge_talep: { token: "--up", dolgu: 0.16, kenar: 0, kenarOpaklik: 0 },
};

export type CizgiStil = { token: string; kalinlik: number; kesik: string; opaklik: number; yonDuyarli: boolean };

const CIZGI: Record<CizgiRol, CizgiStil> = {
  // İzdüşüm YÖN taşır: rengi al/sat'tan gelir, aksandan değil.
  projeksiyon: { token: "--down", kalinlik: 1.2, kesik: "3 3", opaklik: 0.85, yonDuyarli: true },
  trend: { token: "--fib-786", kalinlik: 1.2, kesik: "7 3 2 3", opaklik: 0.85, yonDuyarli: false },
  baglanti: { token: "--accent", kalinlik: 1, kesik: "", opaklik: 0.5, yonDuyarli: false },
};

export type IsaretStil = { token: string; yaricap: number; hap: boolean };

const ISARET: Record<IsaretRol, IsaretStil> = {
  kose: { token: "--accent", yaricap: 3.4, hap: true },
  temas: { token: "--accent", yaricap: 3, hap: false },
};

const ETIKET: Record<EtiketRol, string> = {
  swing_hh: "--up",
  swing_hl: "--up",
  swing_lh: "--down",
  swing_ll: "--down",
  not: "--text-3",
};

const ROZET: Record<RozetRol, { yonDuyarli: boolean; token: string }> = {
  // Tamamlanan formasyon YÖN bildirir; rengi al/sat ailesinden gelir.
  durum_tamamlandi: { yonDuyarli: true, token: "--down" },
  durum_onaylandi: { yonDuyarli: true, token: "--up" },
  durum_izleniyor: { yonDuyarli: false, token: "--accent" },
  durum_gecersiz: { yonDuyarli: false, token: "--text-3" },
};

function al<T>(tablo: Record<string, T>, rol: string, kume: string): T {
  const v = tablo[rol];
  if (v === undefined) {
    throw new ChartSpecHatasi(
      `${kume} rolü çizici tablosunda yok: ${rol}. ` +
        `Geçerli roller: ${Object.keys(tablo).join(", ")}. ` +
        `Yeni rol önce ChartSpec'e, sonra buraya eklenir — varsayılana düşmek yasak.`,
    );
  }
  return v;
}

export const seviyeStili = (r: SeviyeRol) => al(SEVIYE, r, "Seviye");
export const alanStili = (r: AlanRol) => al(ALAN, r, "Alan");
export const cizgiStili = (r: CizgiRol) => al(CIZGI, r, "Çizgi");
export const isaretStili = (r: IsaretRol) => al(ISARET, r, "İşaret");
export const etiketTokeni = (r: EtiketRol) => al(ETIKET, r, "Etiket");
export const rozetStili = (r: RozetRol) => al(ROZET, r, "Rozet");

/** Yön token'ı — al/sat dışında bir değer sözleşme ihlalidir. */
export function yonTokeni(y: Yon): string {
  if (y !== "al" && y !== "sat") {
    throw new ChartSpecHatasi(`Bilinmeyen yön: ${String(y)}. Yalnızca 'al' ve 'sat' geçerli.`);
  }
  return y === "al" ? "--up" : "--down";
}

/** `--accent` gibi bir token adını o anki temada gerçek renge çevirir. */
export function tokenRengi(kok: Element, token: string): string {
  const v = getComputedStyle(kok).getPropertyValue(token).trim();
  if (!v) throw new ChartSpecHatasi(`Token boş döndü: ${token}. tokens.css ile çizici ayrı düşmüş.`);
  return v;
}
