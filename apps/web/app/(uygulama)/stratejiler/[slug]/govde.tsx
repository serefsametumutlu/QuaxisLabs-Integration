"use client";

import { useState } from "react";
import { Eyebrow, Pill, Tabs } from "@/components/ui";
import { Faz4Isareti, GrafikYeri } from "@/components/kabuk/GrafikYeri";
import { Grafik } from "@/components/grafik/Grafik";
import { HARMONIK_GARTLEY, THYAO_SWING_FIB_ABCD } from "@/lib/ornek-chartspec";
import type { ChartSpec } from "@/lib/chartspec";
import type { Strateji } from "@/lib/ornek-strateji";

const GORUNUM = [
  { value: "grafik", label: "Grafik" },
  { value: "kaynak", label: "Python kaynağı" },
] as const;

/** Slug -> gerçek ChartSpec.
 *
 * Eskiden tek bir `slug === "swing-fib-abcd"` karşılaştırmasıydı; ikinci
 * strateji eklenince o satır sessizce "spec yok" deyip örnek çizim
 * gösterirdi — sayfada gerçek levha varken. */
const SPEC: Record<string, ChartSpec> = {
  "swing-fib-abcd": THYAO_SWING_FIB_ABCD,
  "harmonik-pesavento": HARMONIK_GARTLEY,
};

/** Strateji sayfasının sekmeli üst gövdesi: grafik levhası ya da kaynak kodu. */
export function StratejiGovde({ strateji }: { strateji: Strateji }) {
  const [gorunum, setGorunum] = useState<string>("grafik");
  const tohum = strateji.slug.split("").reduce((a, c) => a + c.charCodeAt(0), 0) * 131;
  const spec = SPEC[strateji.slug] ?? null;

  return (
    <div style={{ marginBottom: 12 }}>
      <Tabs label="Görünüm" options={GORUNUM} value={gorunum} onChange={setGorunum}>
        {gorunum === "grafik" ? (
          <div className="chartframe">
            <div className="chartbar">
              {/* Künye SPEC'ten okunur. Sabit "THYAO · 1G · SAT" yazmak,
                  gerçek levhada başka bir sembol dururken şeritte başka bir
                  sembol göstermek demekti. */}
              <span className="sym">{spec ? spec.kunye.sembol : "THYAO"}</span>
              <span className="dim" style={{ fontSize: 12 }}>
                {spec ? spec.kunye.zaman_dilimi.toLocaleUpperCase("tr") : "1G"}
              </span>
              <Pill tone="acc" small>
                {strateji.ad.toLocaleLowerCase("tr")}
              </Pill>
              <Pill tone={spec?.kunye.yon === "al" ? "up" : "down"} small>
                {spec?.kunye.yon === "al" ? "AL" : "SAT"}
              </Pill>
              <span style={{ marginLeft: "auto" }} />
              {spec ? null : <Faz4Isareti />}
              <Eyebrow style={{ letterSpacing: "1.4px", fontSize: 10 }}>
                {spec && !spec.kunye.ornek_mi ? "gerçek veri" : "örnek veri"}
              </Eyebrow>
            </div>
            <div className="chartbody">
              {/* ChartSpec'i olan strateji gerçek levhayı alır; olmayan hâlâ
                  örnek çizimi gösterir ve bunu rozetle söyler. Her stratejinin
                  komposeri kendi fazında yazılacak (Bölüm C). */}
              {spec ? (
                <Grafik spec={spec} yukseklik={280} dar />
              ) : (
                <GrafikYeri
                  seed={tohum}
                  w={1060}
                  h={260}
                  bar={120}
                  son={{ fiyat: 159.49, yon: "down" }}
                  label={`${strateji.ad} stratejisinin THYAO günlük grafiğindeki örneği`}
                />
              )}
            </div>
          </div>
        ) : (
          <pre className="code">
            <span className="cm">{"# Faz 5'te packages/teknik altından gelecek — henüz yazılmadı."}</span>
            {"\n"}
            <span className="cm">{"# ADR-002: gösterge katmanı SIFIRDAN yazılıyor, eski kod taşınmıyor."}</span>
            {"\n\n"}
            <span className="kw">@dataclass</span>(frozen=<span className="kw">True</span>){"\n"}
            <span className="kw">class</span> <span className="fn">{ad(strateji.ad)}Params</span>:{"\n"}
            {strateji.parametreler.flatMap((g) => g.alanlar).map((a) => (
              <span key={a.ad}>
                {"    "}
                {a.ad}: ... = {a.varsayilan}
                {"\n"}
              </span>
            ))}
          </pre>
        )}
      </Tabs>
    </div>
  );
}

/** "Salınım Fibo ABCD" -> "SalinimFiboABCD": sınıf adı için Türkçe harfleri sadeleştirir. */
function ad(s: string) {
  const harita: Record<string, string> = {
    ı: "i", İ: "I", ğ: "g", Ğ: "G", ş: "s", Ş: "S",
    ç: "c", Ç: "C", ö: "o", Ö: "O", ü: "u", Ü: "U",
  };
  return s
    .split("")
    .map((c) => harita[c] ?? c)
    .join("")
    .replace(/[^A-Za-z0-9]/g, "");
}
