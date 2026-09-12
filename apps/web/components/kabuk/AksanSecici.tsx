"use client";

import { AKSANLAR, AKSAN_ETIKET, type Aksan } from "@/lib/tema";
import { useTema } from "@/lib/tema-deposu";

/** Maketteki hex'ler: aksanın kendisi token'dan gelir, bu üç değer yalnız
 *  DÜĞMENİN kendi örneğini boyar — seçilmemiş aksanın rengi token'da yok. */
const HEX: Record<Aksan, string> = { teal: "#2ED3C0", amber: "#E9A93A", blue: "#5B8CFF" };

export function AksanSecici() {
  const { aksan, aksanAta } = useTema();
  return (
    <div className="tset" role="group" aria-label="Aksan rengi">
      {AKSANLAR.map((a) => (
        <button
          key={a}
          type="button"
          className="sw"
          style={{ background: HEX[a], color: HEX[a] }}
          aria-pressed={a === aksan}
          aria-label={AKSAN_ETIKET[a]}
          title={AKSAN_ETIKET[a]}
          onClick={() => aksanAta(a)}
        />
      ))}
    </div>
  );
}
