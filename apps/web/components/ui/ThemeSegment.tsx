"use client";

import { TEMA_ETIKET, TEMA_KIPLERI, TemaKipi } from "@/lib/tema";
import { useTema } from "@/lib/tema-deposu";

const IKON: Record<TemaKipi, React.ReactNode> = {
  system: (
    <>
      <rect x="2.2" y="3" width="11.6" height="8" rx="1.3" fill="none" stroke="currentColor" strokeWidth="1.3" />
      <path d="M6 13.4h4" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
    </>
  ),
  light: (
    <>
      <circle cx="8" cy="8" r="3.1" fill="none" stroke="currentColor" strokeWidth="1.3" />
      <path
        d="M8 1.4v1.7M8 12.9v1.7M1.4 8h1.7M12.9 8h1.7M3.4 3.4l1.2 1.2M11.4 11.4l1.2 1.2M12.6 3.4l-1.2 1.2M4.6 11.4l-1.2 1.2"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinecap="round"
      />
    </>
  ),
  dark: (
    <path
      d="M13.2 9.6A5.8 5.8 0 0 1 6.4 2.8a5.8 5.8 0 1 0 6.8 6.8Z"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.3"
      strokeLinejoin="round"
    />
  ),
};

type Props = {
  /** Denetimli kullanım (vitrin). Verilmezse kök temayı yönetir. */
  value?: TemaKipi;
  onChange?: (k: TemaKipi) => void;
};

/** Üç kademeli tema anahtarı: sistem · açık · koyu. Ürün varsayılanı koyu. */
export function ThemeSegment({ value, onChange }: Props) {
  const denetimli = value !== undefined;
  return denetimli ? (
    <Seg kip={value} ata={onChange ?? (() => {})} />
  ) : (
    <KokSegment />
  );
}

function KokSegment() {
  const { kip, kipAta } = useTema();
  return <Seg kip={kip} ata={kipAta} />;
}

function Seg({ kip, ata }: { kip: TemaKipi; ata: (k: TemaKipi) => void }) {
  return (
    <div className="themeseg" role="group" aria-label="Tema">
      {TEMA_KIPLERI.map((m) => (
        <button
          key={m}
          type="button"
          title={TEMA_ETIKET[m]}
          aria-label={TEMA_ETIKET[m]}
          aria-pressed={m === kip}
          onClick={() => ata(m)}
        >
          <svg viewBox="0 0 16 16" aria-hidden="true">
            {IKON[m]}
          </svg>
        </button>
      ))}
    </div>
  );
}
