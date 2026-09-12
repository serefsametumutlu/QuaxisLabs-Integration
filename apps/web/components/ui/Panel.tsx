import type { HTMLAttributes, ReactNode } from "react";

type Props = HTMLAttributes<HTMLDivElement> & {
  /** Üst şerit: sembol, rozetler, sağa yaslı "örnek veri" etiketi vb. */
  head?: ReactNode;
  /** Gövdeyi kendi dolgusuyla saran kabuk; grafik/tablo için `false`. */
  padded?: boolean;
  children?: ReactNode;
};

/**
 * Panel — gölgesiz yüzey: bir tık açık zemin + saç teli inceliğinde kenarlık.
 * Yarıçap 2px (panel/kart keskin, kontrol tam hap).
 */
export function Panel({ head, padded = true, className, children, ...rest }: Props) {
  return (
    <div className={className ? `panel ${className}` : "panel"} {...rest}>
      {head ? <div className="panelhead">{head}</div> : null}
      {padded ? <div className="panelbody">{children}</div> : children}
    </div>
  );
}
