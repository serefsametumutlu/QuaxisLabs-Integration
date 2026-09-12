import type { ButtonHTMLAttributes } from "react";

/**
 * `accent` — aksan dolgulu, sayfada en çok bir-iki tane (aksan kıtlığı ilkesi).
 * `solid`  — metin renginde dolgu; aksanı harcamadan ikinci bir birincil.
 * `ghost`  — yalnız kenarlık.
 */
export type ButonTuru = "accent" | "solid" | "ghost";
export type ButonBoyu = "sm" | "md" | "lg";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButonTuru;
  size?: ButonBoyu;
};

export function Button({ variant = "accent", size = "md", className, type, ...rest }: Props) {
  const cls = [
    "btn",
    variant === "accent" ? null : variant,
    size === "md" ? null : size,
    className,
  ]
    .filter(Boolean)
    .join(" ");
  return <button type={type ?? "button"} className={cls} {...rest} />;
}
