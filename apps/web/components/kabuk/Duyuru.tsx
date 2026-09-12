"use client";

import { useEffect, useState } from "react";
import { TARAMA_SAATI } from "@/lib/ornek-veri";

/** Bir sonraki kapanış taramasına kalan süre. Saat 18:15. */
function kalanSure(simdi: Date) {
  const sonraki = new Date(simdi);
  sonraki.setHours(TARAMA_SAATI.saat, TARAMA_SAATI.dakika, 0, 0);
  if (sonraki <= simdi) sonraki.setDate(sonraki.getDate() + 1);
  const s = Math.floor((sonraki.getTime() - simdi.getTime()) / 1000);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${p(Math.floor(s / 3600))}sa ${p(Math.floor(s / 60) % 60)}dk ${p(s % 60)}sn`;
}

/**
 * Duyuru şeridi — geri sayım.
 *
 * Sunucuda boş (—) çizilir, sayaç yalnız istemcide döner: sunucu saati ile
 * tarayıcı saati arasındaki fark hidrasyon uyuşmazlığı doğurur, ayrıca
 * tarama saati kullanıcının kendi saat diliminde anlamlıdır.
 */
export function Duyuru() {
  const [kalan, setKalan] = useState<string | null>(null);

  useEffect(() => {
    const tik = () => setKalan(kalanSure(new Date()));
    tik();
    const id = setInterval(tik, 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="announce">
      <span className="dotlive" aria-hidden="true" />
      <span>
        Kapanış taraması her gün <b>{TARAMA_SAATI.metin}</b>&apos;te koşuyor
      </span>
      <span className="lab">sonraki tarama</span>
      <span className="cd">{kalan ?? "—"}</span>
    </div>
  );
}
