"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { ORNEK_TARAMA } from "@/lib/ornek-veri";
import { STRATEJILER } from "@/lib/ornek-strateji";
import { YUZEYLER } from "@/lib/yollar";

type Kayit = { tur: string; ad: string; alt?: string; yol: string };

const TR = new Intl.Collator("tr", { sensitivity: "base" });

function kayitlar(): Kayit[] {
  const semboller = ORNEK_TARAMA.map((r) => ({
    tur: "Sembol",
    ad: r.sembol,
    alt: r.ad,
    yol: `/grafik?sembol=${r.sembol}`,
  }));
  const stratejiler = STRATEJILER.map((s) => ({
    tur: "Strateji",
    ad: s.ad,
    alt: s.paket,
    yol: `/stratejiler/${s.slug}`,
  }));
  const yuzeyler = YUZEYLER.map((y) => ({ tur: "Yüzey", ad: y.ad, yol: y.yol }));
  return [...semboller, ...stratejiler, ...yuzeyler];
}

/** Türkçe arama: büyük/küçük ve aksan farkı aranan sonucu kaçırmasın. */
function esles(metin: string, sorgu: string) {
  const d = (s: string) => s.toLocaleLowerCase("tr").replaceAll("ı", "i");
  return d(metin).includes(d(sorgu));
}

/**
 * Omni — Ctrl+K / ⌘K ile açılan hızlı geçiş.
 * Sembol, strateji ve yüzeyler tek listede; ok tuşları + Enter ile gidilir.
 */
export function Omni() {
  const router = useRouter();
  const [acik, setAcik] = useState(false);
  const [sorgu, setSorgu] = useState("");
  const [secili, setSecili] = useState(0);
  const girdiRef = useRef<HTMLInputElement>(null);

  const tum = useMemo(() => kayitlar(), []);
  const sonuc = useMemo(() => {
    const q = sorgu.trim();
    const liste = q ? tum.filter((k) => esles(k.ad, q) || (k.alt ? esles(k.alt, q) : false)) : tum;
    return liste.sort((a, b) => TR.compare(a.tur, b.tur) || TR.compare(a.ad, b.ad)).slice(0, 12);
  }, [tum, sorgu]);

  useEffect(() => {
    const tus = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        // Sorgu her açılışta sıfırlanır; kapanışta ayrıca temizlemeye gerek
        // kalmaz — durumu efekt içinde sıfırlamak fazladan bir tur doğururdu.
        setSorgu("");
        setSecili(0);
        setAcik((a) => !a);
      }
      if (e.key === "Escape") setAcik(false);
    };
    window.addEventListener("keydown", tus);
    return () => window.removeEventListener("keydown", tus);
  }, []);

  // Yalnız DOM yan etkisi: açılınca odak arama kutusuna.
  useEffect(() => {
    if (acik) girdiRef.current?.focus();
  }, [acik]);

  const ac = () => {
    setSorgu("");
    setSecili(0);
    setAcik(true);
  };

  const git = (k: Kayit) => {
    setAcik(false);
    router.push(k.yol);
  };

  const listeTusu = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSecili((i) => Math.min(sonuc.length - 1, i + 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSecili((i) => Math.max(0, i - 1));
    } else if (e.key === "Enter" && sonuc[secili]) {
      e.preventDefault();
      git(sonuc[secili]);
    }
  };

  return (
    <>
      <button type="button" className="omni" onClick={ac}>
        <svg width="13" height="13" viewBox="0 0 16 16" aria-hidden="true">
          <circle cx="7" cy="7" r="4.6" fill="none" stroke="currentColor" strokeWidth="1.4" />
          <path d="M10.5 10.5 L14 14" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
        </svg>
        Sembol ya da strateji ara
        <kbd>Ctrl K</kbd>
      </button>

      {acik ? (
        <>
          <div className="omniperde" onClick={() => setAcik(false)} />
          <div className="omnikutu" role="dialog" aria-modal="true" aria-label="Hızlı geçiş">
            <div className="omnibas">
              <svg width="13" height="13" viewBox="0 0 16 16" aria-hidden="true">
                <circle cx="7" cy="7" r="4.6" fill="none" stroke="currentColor" strokeWidth="1.4" />
                <path d="M10.5 10.5 L14 14" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
              </svg>
              <input
                ref={girdiRef}
                value={sorgu}
                onChange={(e) => {
                  setSorgu(e.target.value);
                  setSecili(0);
                }}
                onKeyDown={listeTusu}
                placeholder="THYAO, Altın Bölge, Tarama…"
                aria-label="Ara"
              />
              <kbd>Esc</kbd>
            </div>
            <ul className="omnilist">
              {sonuc.map((k, i) => (
                <li key={`${k.tur}-${k.ad}`}>
                  <button
                    type="button"
                    data-secili={i === secili ? "true" : undefined}
                    onMouseEnter={() => setSecili(i)}
                    onClick={() => git(k)}
                  >
                    <span className="tur">{k.tur}</span>
                    <span className="ad">{k.ad}</span>
                    {k.alt ? <span className="alt">{k.alt}</span> : null}
                  </button>
                </li>
              ))}
              {sonuc.length === 0 ? <li className="bos">Eşleşme yok.</li> : null}
            </ul>
            <div className="omnifoot">
              <span>↑ ↓ gez · Enter aç · Esc kapat</span>
              <span className="dim">örnek veri</span>
            </div>
          </div>
        </>
      ) : null}
    </>
  );
}
