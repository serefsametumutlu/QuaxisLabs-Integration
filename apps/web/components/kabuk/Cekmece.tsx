"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import { Button, Pill } from "@/components/ui";
import { VERDIKT_ACIKLAMA, yasEtiketi, type TaramaSatiri } from "@/lib/ornek-veri";
import { Faz4Isareti, GrafikYeri } from "./GrafikYeri";

type Props = {
  satir: TaramaSatiri | null;
  kapat: () => void;
};

/**
 * Sağdan açılan grafik çekmecesi.
 * Tarama tablosunda satıra tıklamak SAYFA DEĞİŞTİRMEZ — tarama sonucu ve
 * filtreler yerinde kalır, grafik yanda açılır. Esc ve perde kapatır, odak
 * çekmeceye alınır ve kapanınca geldiği yere döner.
 */
export function Cekmece({ satir, kapat }: Props) {
  const kutuRef = useRef<HTMLDivElement>(null);
  const oncekiOdak = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!satir) return;
    oncekiOdak.current = document.activeElement as HTMLElement | null;
    kutuRef.current?.focus();
    const tus = (e: KeyboardEvent) => {
      if (e.key === "Escape") kapat();
    };
    window.addEventListener("keydown", tus);
    return () => {
      window.removeEventListener("keydown", tus);
      oncekiOdak.current?.focus?.();
    };
  }, [satir, kapat]);

  if (!satir) return null;

  const tohum = satir.sembol.split("").reduce((a, c) => a + c.charCodeAt(0), 0) * 977;

  return (
    <>
      <div className="cekmece-perde" onClick={kapat} />
      <div
        className="cekmece"
        role="dialog"
        aria-modal="true"
        aria-label={`${satir.sembol} grafik çekmecesi`}
        ref={kutuRef}
        tabIndex={-1}
      >
        <header>
          <span className="sym">{satir.sembol}</span>
          <span className="dim" style={{ fontSize: 12 }}>
            {satir.ad}
          </span>
          <Pill tone="acc" small>
            {satir.strateji}
          </Pill>
          <Pill tone={satir.yon} small>
            {satir.yon === "up" ? "AL" : "SAT"}
          </Pill>
          <button type="button" className="kapat" onClick={kapat} aria-label="Çekmeceyi kapat">
            ✕
          </button>
        </header>

        <div className="govde">
          <div className="chartframe">
            <div className="chartbar">
              <span className="sym">{satir.sembol}</span>
              <span className="dim" style={{ fontSize: 12 }}>
                1G
              </span>
              <span className="spacer" style={{ marginLeft: "auto" }} />
              <Faz4Isareti />
            </div>
            <div className="chartbody">
              <GrafikYeri
                seed={tohum}
                w={720}
                h={280}
                bar={90}
                son={{ fiyat: satir.fiyat, yon: satir.yon }}
                label={`${satir.sembol} örnek günlük seri — grafik motoru Faz 4'te bağlanacak`}
              />
            </div>
          </div>

          <div className="satirlar">
            <div>
              <div className="k">Fiyat</div>
              <div className="v">{satir.fiyat.toFixed(2)}</div>
            </div>
            <div>
              <div className="k">Seviye</div>
              <div className="v">{satir.seviye.toFixed(2)}</div>
            </div>
            <div>
              <div className="k">Durum</div>
              <div className="v" style={{ fontSize: 13 }}>
                {satir.durum}
              </div>
            </div>
            <div>
              <div className="k">Yaş</div>
              <div className="v" style={{ fontSize: 13 }}>
                {yasEtiketi(satir.yas)}
              </div>
            </div>
          </div>

          <div className="verdict">
            <Pill tone="acc">K4 · İSTATİSTİK</Pill>
            <p>
              <b>{satir.verdikt}</b> — {VERDIKT_ACIKLAMA[satir.verdikt]}. Sinyal gösterilir, iddia
              edilmez: ölçülmemiş bir stratejiyi “çalışıyor” diye sunmuyoruz.
            </p>
          </div>

          <div className="row" style={{ gap: 8 }}>
            <Link className="btn ghost" href={`/grafik?sembol=${satir.sembol}`}>
              Tam grafikte aç →
            </Link>
            <Button variant="ghost" onClick={kapat}>
              Kapat
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}
