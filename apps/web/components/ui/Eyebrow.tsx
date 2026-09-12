import type { ElementType, HTMLAttributes } from "react";

type Props = HTMLAttributes<HTMLElement> & {
  /** Varsayılan `span`; bölüm başlığı üstünde `h4` olarak da kullanılır. */
  as?: ElementType;
};

/**
 * Eyebrow — mono, 11px, +2.2px tracking, büyük harf, üçüncül kademe.
 * Başlıkta negatif tracking, etikette pozitif: bu zıtlık tasarım dilinin
 * 5. ilkesi.
 */
export function Eyebrow({ as: Tag = "span", className, ...rest }: Props) {
  return <Tag className={className ? `eyebrow ${className}` : "eyebrow"} {...rest} />;
}
