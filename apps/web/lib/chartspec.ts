/**
 * ChartSpec v1 — TypeScript yüzü.
 *
 * Kaynak sözleşme `packages/chart/sema/chartspec-1.0.schema.json`; buradaki
 * tipler onun karşılığıdır. Roller KAPALI kümedir: listede olmayan bir rol
 * sessizce varsayılana düşmez, `ChartSpecHatasi` atar (ADR-001 §4).
 *
 * Bu dosya renk BİLMEZ. Rol → token eşlemesi çizicinin işidir
 * (`components/grafik/roller.ts`).
 */

export const CHARTSPEC_SURUM = "1.0";

export class ChartSpecHatasi extends Error {
  constructor(mesaj: string) {
    super(mesaj);
    this.name = "ChartSpecHatasi";
  }
}

export const SEVIYE_ROLLERI = [
  "fib_0",
  "fib_236",
  "fib_382",
  "fib_500",
  "fib_618",
  "fib_786",
  "fib_1",
  "fib_1272",
  "fib_1618",
  "seviye",
  "son_fiyat",
] as const;
export type SeviyeRol = (typeof SEVIYE_ROLLERI)[number];

export const ALAN_ROLLERI = ["formasyon", "bolge_altin", "bolge_arz", "bolge_talep"] as const;
export type AlanRol = (typeof ALAN_ROLLERI)[number];

export const CIZGI_ROLLERI = ["projeksiyon", "trend", "baglanti"] as const;
export type CizgiRol = (typeof CIZGI_ROLLERI)[number];

export const ISARET_ROLLERI = ["kose", "temas"] as const;
export type IsaretRol = (typeof ISARET_ROLLERI)[number];

export const ETIKET_ROLLERI = ["swing_hh", "swing_hl", "swing_lh", "swing_ll", "not"] as const;
export type EtiketRol = (typeof ETIKET_ROLLERI)[number];

export const ROZET_ROLLERI = [
  "durum_tamamlandi",
  "durum_onaylandi",
  "durum_izleniyor",
  "durum_gecersiz",
] as const;
export type RozetRol = (typeof ROZET_ROLLERI)[number];

export type Yon = "al" | "sat";

export type Nokta = { t: number; fiyat: number };

export type Kunye = {
  sembol: string;
  ad?: string;
  zaman_dilimi: string;
  strateji: string;
  strateji_adi?: string;
  yon?: Yon;
  durum?: string;
  /** Örnek veri mi? Arayüz bunu kullanıcıya AYNEN gösterir. */
  ornek_mi?: boolean;
};

export type YAraligi = { alt: number; ust: number; gerekce?: string };

export type Panel = {
  id: string;
  tur: "fiyat" | "hacim";
  oran: number;
  /** Komposerin bilinçli yazdığı aralık. Yoksa çizici SADECE o panelin
   *  serilerinden hesaplar — katmanlar aralığı kendiliğinden genişletemez. */
  y?: YAraligi;
};

export type Mum = { t: number; acilis: number; yuksek: number; dusuk: number; kapanis: number };
export type HacimBari = { t: number; hacim: number; yon: Yon };

export type MumSerisi = { id: string; tur: "mum"; panel: string; veri: Mum[] };
export type HacimSerisi = { id: string; tur: "hacim"; panel: string; veri: HacimBari[] };
export type Seri = MumSerisi | HacimSerisi;

export type Seviye = {
  tur: "seviye";
  rol: SeviyeRol;
  fiyat: number;
  etiket: string;
  panel?: string;
  baslangic?: number;
};
export type Alan = { tur: "alan"; rol: AlanRol; noktalar: Nokta[]; panel?: string; etiket?: string };
export type Bant = {
  tur: "bant";
  rol: AlanRol;
  alt: number;
  ust: number;
  panel?: string;
  etiket?: string;
  baslangic?: number;
};
export type Cizgi = { tur: "cizgi"; rol: CizgiRol; noktalar: Nokta[]; panel?: string };
export type Isaret = {
  tur: "isaret";
  rol: IsaretRol;
  nokta: Nokta;
  metin?: string;
  yerlesim?: "ust" | "alt";
  panel?: string;
};
export type Etiket = {
  tur: "etiket";
  rol: EtiketRol;
  nokta: Nokta;
  metin: string;
  yerlesim?: "ust" | "alt";
  panel?: string;
};
export type Rozet = {
  tur: "rozet";
  rol: RozetRol;
  nokta: Nokta;
  metin: string;
  yon: Yon;
  panel?: string;
};

export type Katman = Seviye | Alan | Bant | Cizgi | Isaret | Etiket | Rozet;

export type ChartSpec = {
  surum: string;
  kunye: Kunye;
  paneller: Panel[];
  seriler: Seri[];
  katmanlar?: Katman[];
};

const ROL_KUMESI: Record<Katman["tur"], readonly string[]> = {
  seviye: SEVIYE_ROLLERI,
  alan: ALAN_ROLLERI,
  bant: ALAN_ROLLERI,
  cizgi: CIZGI_ROLLERI,
  isaret: ISARET_ROLLERI,
  etiket: ETIKET_ROLLERI,
  rozet: ROZET_ROLLERI,
};

/**
 * Çizicinin ilk işi: sözleşmeyi doğrulamak.
 *
 * Python tarafı zaten doğruluyor; burada bir kez daha doğrulanır çünkü
 * ChartSpec bir DOSYA olarak da elden ele geçebilir ve çizici, kaynağına
 * güvenerek çizmez.
 */
export function dogrula(x: unknown): ChartSpec {
  const s = x as ChartSpec;
  if (!s || typeof s !== "object") throw new ChartSpecHatasi("ChartSpec bir nesne değil.");
  if (s.surum !== CHARTSPEC_SURUM) {
    throw new ChartSpecHatasi(
      `Desteklenmeyen ChartSpec sürümü: ${String(s.surum)} (beklenen ${CHARTSPEC_SURUM}).`,
    );
  }
  if (!Array.isArray(s.paneller) || s.paneller.length === 0) {
    throw new ChartSpecHatasi("ChartSpec en az bir panel taşımalı.");
  }
  if (!Array.isArray(s.seriler) || s.seriler.length === 0) {
    throw new ChartSpecHatasi("ChartSpec en az bir seri taşımalı.");
  }

  const panelIdler = new Set(s.paneller.map((p) => p.id));
  for (const seri of s.seriler) {
    if (!panelIdler.has(seri.panel)) {
      throw new ChartSpecHatasi(`'${seri.id}' serisi tanımsız panele bağlı: ${seri.panel}`);
    }
    if (seri.veri.length < 2) {
      throw new ChartSpecHatasi(
        `'${seri.id}' serisi ${seri.veri.length} nokta taşıyor. Seriler TAM DİZİ taşır.`,
      );
    }
  }

  for (const k of s.katmanlar ?? []) {
    const kume = ROL_KUMESI[k.tur];
    if (!kume) throw new ChartSpecHatasi(`Bilinmeyen katman türü: ${String(k.tur)}`);
    if (!kume.includes(k.rol)) {
      throw new ChartSpecHatasi(
        `'${k.tur}' için bilinmeyen rol: ${String(k.rol)}. ` +
          `Geçerli roller: ${kume.join(", ")}. Sessizce varsayılana düşmek yasak.`,
      );
    }
  }

  return s;
}

/** Panelin varsayılan y aralığı — YALNIZCA o panele bağlı serilerden. */
export function panelAraligi(spec: ChartSpec, panelId: string): { alt: number; ust: number } {
  const panel = spec.paneller.find((p) => p.id === panelId);
  if (panel?.y) return { alt: panel.y.alt, ust: panel.y.ust };

  const kendi = spec.seriler.filter((s) => s.panel === panelId);
  if (kendi.length === 0) throw new ChartSpecHatasi(`'${panelId}' paneline seri bağlı değil.`);

  let alt = Infinity;
  let ust = -Infinity;
  for (const s of kendi) {
    if (s.tur === "mum") {
      for (const m of s.veri) {
        alt = Math.min(alt, m.dusuk);
        ust = Math.max(ust, m.yuksek);
      }
    } else {
      for (const h of s.veri) {
        alt = Math.min(alt, 0);
        ust = Math.max(ust, h.hacim);
      }
    }
  }
  return { alt, ust };
}
