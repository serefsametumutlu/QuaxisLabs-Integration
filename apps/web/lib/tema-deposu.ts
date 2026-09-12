"use client";

import { useCallback, useSyncExternalStore } from "react";
import {
  Aksan,
  DEPO_ANAHTARI,
  TemaKipi,
  VARSAYILAN_AKSAN,
  VARSAYILAN_TEMA,
  aksanMi,
  temaKipiMi,
} from "@/lib/tema";

/**
 * Temanın tek doğru kaynağı <html> üzerindeki niteliklerdir — React durumu
 * değil. Nitelikleri hidrasyondan önce önyükleme betiği yazar; React onları
 * `useSyncExternalStore` ile OKUR. Böylece hem sunucu çıktısı tutarlı kalır
 * (sunucu anlık görüntüsü = varsayılan) hem de efekt içinde setState
 * gerekmez.
 */
const dinleyiciler = new Set<() => void>();

function abone(f: () => void) {
  dinleyiciler.add(f);
  return () => {
    dinleyiciler.delete(f);
  };
}

function bildir() {
  dinleyiciler.forEach((f) => f());
}

function kipOku(): TemaKipi {
  const t = document.documentElement.getAttribute("data-theme");
  return temaKipiMi(t) ? t : "system";
}

function aksanOku(): Aksan {
  const a = document.documentElement.getAttribute("data-accent");
  return aksanMi(a) ? a : VARSAYILAN_AKSAN;
}

function depoyaYaz(anahtar: string, deger: string) {
  try {
    localStorage.setItem(anahtar, deger);
  } catch {
    /* özel pencere ya da kapalı site verisi — tercih kalıcı olmaz, arayüz çalışır */
  }
}

export function useTema() {
  const kip = useSyncExternalStore(abone, kipOku, () => VARSAYILAN_TEMA);
  const aksan = useSyncExternalStore(abone, aksanOku, () => VARSAYILAN_AKSAN);

  const kipAta = useCallback((k: TemaKipi) => {
    const d = document.documentElement;
    if (k === "system") d.removeAttribute("data-theme");
    else d.setAttribute("data-theme", k);
    depoyaYaz(DEPO_ANAHTARI.tema, k);
    bildir();
  }, []);

  const aksanAta = useCallback((a: Aksan) => {
    document.documentElement.setAttribute("data-accent", a);
    depoyaYaz(DEPO_ANAHTARI.aksan, a);
    bildir();
  }, []);

  return { kip, aksan, kipAta, aksanAta };
}
