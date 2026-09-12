"use client";

import { useId, useRef, type ReactNode } from "react";

export type SegSecenek<T extends string> = { value: T; label: ReactNode };

type SegProps<T extends string> = {
  label: string;
  options: readonly SegSecenek<T>[];
  value: T;
  onChange: (v: T) => void;
  /** Zaman dilimi gibi sayısal seçimlerde mono yüz. */
  mono?: boolean;
};

/**
 * Seg — hap içinde segment denetimi (görünüm/zaman dilimi seçici).
 * Panel değil KONTROL olduğu için tam hap.
 */
export function Seg<T extends string>({ label, options, value, onChange, mono }: SegProps<T>) {
  return (
    <div className={mono ? "seg mono" : "seg"} role="group" aria-label={label}>
      {options.map((o) => (
        <button key={o.value} type="button" aria-pressed={o.value === value} onClick={() => onChange(o.value)}>
          {o.label}
        </button>
      ))}
    </div>
  );
}

type TabsProps<T extends string> = {
  label: string;
  options: readonly SegSecenek<T>[];
  value: T;
  onChange: (v: T) => void;
  mono?: boolean;
  /** Seçili sekmenin içeriği. */
  children?: ReactNode;
};

/**
 * Tabs — Seg ile aynı görünüm, farklı anlam: burada seçim bir PANELİ
 * değiştirir, o yüzden gerçek `tablist` semantiği ve ok tuşu gezinmesi var.
 */
export function Tabs<T extends string>({ label, options, value, onChange, mono, children }: TabsProps<T>) {
  const id = useId();
  const ref = useRef<HTMLDivElement>(null);

  const tus = (e: React.KeyboardEvent<HTMLDivElement>) => {
    const i = options.findIndex((o) => o.value === value);
    let hedef: number;
    if (e.key === "ArrowRight") hedef = (i + 1) % options.length;
    else if (e.key === "ArrowLeft") hedef = (i - 1 + options.length) % options.length;
    else if (e.key === "Home") hedef = 0;
    else if (e.key === "End") hedef = options.length - 1;
    else return;
    e.preventDefault();
    onChange(options[hedef].value);
    const dugmeler = ref.current?.querySelectorAll<HTMLButtonElement>("button[role='tab']");
    dugmeler?.[hedef]?.focus();
  };

  return (
    <>
      <div
        ref={ref}
        className={mono ? "seg mono" : "seg"}
        role="tablist"
        aria-label={label}
        onKeyDown={tus}
      >
        {options.map((o) => (
          <button
            key={o.value}
            type="button"
            role="tab"
            id={`${id}-${o.value}-tab`}
            aria-controls={`${id}-${o.value}-panel`}
            aria-selected={o.value === value}
            tabIndex={o.value === value ? 0 : -1}
            onClick={() => onChange(o.value)}
          >
            {o.label}
          </button>
        ))}
      </div>
      {children !== undefined ? (
        <div
          className="tabpanel"
          role="tabpanel"
          id={`${id}-${value}-panel`}
          aria-labelledby={`${id}-${value}-tab`}
          tabIndex={0}
        >
          {children}
        </div>
      ) : null}
    </>
  );
}
