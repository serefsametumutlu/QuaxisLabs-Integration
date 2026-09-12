import type { HTMLAttributes } from "react";

/**
 * `up` / `down` YÖN demek, `acc` KARARA DEĞER demek. Ayrı token aileleri —
 * karıştırılmaz (TASARIM_DILI §3, §5).
 */
export type PillTonu = "nötr" | "up" | "down" | "acc";

const SINIF: Record<PillTonu, string> = {
  nötr: "pill",
  up: "pill up",
  down: "pill down",
  acc: "pill acc",
};

type Props = HTMLAttributes<HTMLSpanElement> & {
  tone?: PillTonu;
  /** Grafik çubuğu gibi sıkışık yerlerde 19px yükseklik. */
  small?: boolean;
};

export function Pill({ tone = "nötr", small, className, ...rest }: Props) {
  const cls = [SINIF[tone], small ? "sm" : null, className].filter(Boolean).join(" ");
  return <span className={cls} {...rest} />;
}
