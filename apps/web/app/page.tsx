import Link from "next/link";
import { Eyebrow } from "@/components/ui";

/**
 * Kök sayfa — Faz 2'de yalnız bir işaret levhası.
 * Giriş ekranı ve uygulama kabuğu Faz 3'ün işi; maketteki hero, tarama,
 * grafik ve strateji yüzeyleri orada kurulacak.
 */
export default function AnaSayfa() {
  return (
    <main style={{ maxWidth: 760, margin: "0 auto", padding: "96px 22px" }}>
      <Eyebrow>QuaxisLabs · Faz 2</Eyebrow>
      <h1
        style={{
          fontFamily: "var(--f-display)",
          fontWeight: 500,
          fontSize: 38,
          letterSpacing: "-1.4px",
          lineHeight: 1.08,
          margin: "20px 0 0",
        }}
      >
        Sinyali de gösteririz,
        <br />
        <span className="mut">isabetini de.</span>
      </h1>
      <p className="mut" style={{ fontSize: 15, lineHeight: 1.62, margin: "20px 0 0", maxWidth: "60ch" }}>
        Bu turda tasarım sistemi ve bileşen kütüphanesi kuruldu. Ürün yüzeyleri — giriş ekranı,
        tarama, grafik ve strateji sayfası — Faz 3 ve Faz 4&apos;te gelecek.
      </p>
      <p style={{ margin: "26px 0 0" }}>
        <Link className="btn" href="/tasarim">
          Tasarım vitrinini aç →
        </Link>
      </p>
    </main>
  );
}
