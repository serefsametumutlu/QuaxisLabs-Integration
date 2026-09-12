import type { HTMLAttributes, ReactNode } from "react";

type TileProps = HTMLAttributes<HTMLDivElement> & {
  /** Mono + büyük harf anahtar. */
  label: ReactNode;
  value: ReactNode;
  /** Sayı değil metin (örn. paket adı) — 27px yerine 19px. */
  textValue?: boolean;
  hint?: ReactNode;
};

/**
 * StatTile — değer her zaman mono + tabular-nums. Üçüncül metin kademesi
 * (%34) sayıya UYGULANMAZ: tarama aracında okunabilirlik eşiği yüksektir.
 */
export function StatTile({ label, value, textValue, hint, className, ...rest }: TileProps) {
  return (
    <div className={className ? `tile ${className}` : "tile"} {...rest}>
      <div className="k">{label}</div>
      <div className={textValue ? "v text" : "v"}>{value}</div>
      {hint ? <div className="d">{hint}</div> : null}
    </div>
  );
}

export function StatTileGrid({ className, ...rest }: HTMLAttributes<HTMLDivElement>) {
  return <div className={className ? `tiles ${className}` : "tiles"} {...rest} />;
}

/** `6dk 22sn` gibi değerlerde birimi üçüncül kademeye düşürür. */
export function Unit({ children }: { children: ReactNode }) {
  return <span className="unit">{children}</span>;
}
