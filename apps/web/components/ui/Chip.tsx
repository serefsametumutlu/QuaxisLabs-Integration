"use client";

import type { ButtonHTMLAttributes, HTMLAttributes, ReactNode } from "react";

type ChipProps = Omit<ButtonHTMLAttributes<HTMLButtonElement>, "aria-pressed"> & {
  pressed?: boolean;
};

/** Filtre çipi — tam hap, 30px, basılıyken metin rengi zemine döner. */
export function Chip({ pressed = false, className, type, ...rest }: ChipProps) {
  return (
    <button
      type={type ?? "button"}
      aria-pressed={pressed}
      className={className ? `chip ${className}` : "chip"}
      {...rest}
    />
  );
}

type GroupProps<T extends string> = Omit<HTMLAttributes<HTMLDivElement>, "onChange"> & {
  label?: string;
  options: readonly { value: T; label: ReactNode }[];
  value: T;
  onChange: (v: T) => void;
};

/**
 * ChipGroup — grup içinde tek seçim. `radiogroup` değil: seçenekler filtreyi
 * daraltan düğmeler, o yüzden `aria-pressed` taşıyan düğme grubu.
 */
export function ChipGroup<T extends string>({
  label,
  options,
  value,
  onChange,
  className,
  ...rest
}: GroupProps<T>) {
  return (
    <div
      role="group"
      aria-label={label}
      className={className ? `chipgroup ${className}` : "chipgroup"}
      {...rest}
    >
      {label ? <span className="lab">{label}</span> : null}
      {options.map((o) => (
        <Chip key={o.value} pressed={o.value === value} onClick={() => onChange(o.value)}>
          {o.label}
        </Chip>
      ))}
    </div>
  );
}
