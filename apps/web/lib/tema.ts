/** Tema ve aksan sözleşmesi — tek kaynak. */

export const TEMA_KIPLERI = ["system", "light", "dark"] as const;
export type TemaKipi = (typeof TEMA_KIPLERI)[number];

export const AKSANLAR = ["teal", "amber", "blue"] as const;
export type Aksan = (typeof AKSANLAR)[number];

/** Ürünün varsayılanı KOYU (kullanıcı kararı) — sistem yine de seçilebilir. */
export const VARSAYILAN_TEMA: TemaKipi = "dark";
export const VARSAYILAN_AKSAN: Aksan = "teal";

export const TEMA_ETIKET: Record<TemaKipi, string> = {
  system: "Sistem teması",
  light: "Açık tema",
  dark: "Koyu tema",
};

export const AKSAN_ETIKET: Record<Aksan, string> = {
  teal: "Turkuaz",
  amber: "Kehribar",
  blue: "Elektrik mavi",
};

export const DEPO_ANAHTARI = { tema: "quaxis.tema", aksan: "quaxis.aksan" } as const;

export function temaKipiMi(v: unknown): v is TemaKipi {
  return typeof v === "string" && (TEMA_KIPLERI as readonly string[]).includes(v);
}

export function aksanMi(v: unknown): v is Aksan {
  return typeof v === "string" && (AKSANLAR as readonly string[]).includes(v);
}

/**
 * Hidrasyondan ÖNCE koşan betik: seçili temayı ilk boyamadan evvel <html>
 * üzerine yazar, böylece açık tema seçili kullanıcıda koyu bir kare görünmez.
 * `?tema=` / `?aksan=` sorgu parametreleri ekran görüntüsü döngüsü içindir —
 * depolanan tercihi ezer ama kalıcı olarak değiştirmez.
 */
export const TEMA_ONYUKLEME_BETIGI = `(function(){try{
var d=document.documentElement,q=new URLSearchParams(location.search);
var t=q.get('tema')||localStorage.getItem('${DEPO_ANAHTARI.tema}')||'${VARSAYILAN_TEMA}';
var a=q.get('aksan')||localStorage.getItem('${DEPO_ANAHTARI.aksan}')||'${VARSAYILAN_AKSAN}';
if(['system','light','dark'].indexOf(t)<0)t='${VARSAYILAN_TEMA}';
if(['teal','amber','blue'].indexOf(a)<0)a='${VARSAYILAN_AKSAN}';
if(t==='system')d.removeAttribute('data-theme');else d.setAttribute('data-theme',t);
d.setAttribute('data-accent',a);
}catch(e){}})();`;
