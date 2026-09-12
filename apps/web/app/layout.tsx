import type { Metadata } from "next";
import "./globals.css";
import { fontVariables } from "./fonts";
import { TEMA_ONYUKLEME_BETIGI, VARSAYILAN_AKSAN, VARSAYILAN_TEMA } from "@/lib/tema";

export const metadata: Metadata = {
  title: "QuaxisLabs",
  description: "Sinyali de gösteririz, isabetini de.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="tr"
      // Sunucu çıktısı varsayılanı taşır; önyükleme betiği ilk boyamadan önce
      // kullanıcının tercihini yazar, bu yüzden nitelik uyuşmazlığı bekleniyor.
      data-theme={VARSAYILAN_TEMA}
      data-accent={VARSAYILAN_AKSAN}
      suppressHydrationWarning
      className={fontVariables}
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: TEMA_ONYUKLEME_BETIGI }} />
      </head>
      <body>
        {children}
      </body>
    </html>
  );
}
