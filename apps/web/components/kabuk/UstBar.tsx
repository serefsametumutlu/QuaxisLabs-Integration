"use client";

import { Eyebrow, Pill, ThemeSegment } from "@/components/ui";
import { TARAMA_SAATI } from "@/lib/tarama";
import { AksanSecici } from "./AksanSecici";
import { Marka } from "./Marka";
import { Omni } from "./Omni";

/** Uygulama üst şeridi — yapışkan, 52px. Kabuğun her yüzeyde sabit kalan parçası. */
export function UstBar() {
  return (
    <header className="topbar">
      <Marka href="/tarama" />
      <Omni />
      <span className="spacer" />
      <Pill className="gizlenir">BIST</Pill>
      <Eyebrow className="gizlenir" style={{ letterSpacing: "1.4px" }}>
        son tarama {TARAMA_SAATI.metin}
      </Eyebrow>
      <AksanSecici />
      <ThemeSegment />
    </header>
  );
}
