import { Eyebrow } from "@/components/ui";
import type { Strateji } from "@/lib/ornek-strateji";

type Olcum = NonNullable<Strateji["olcum"]>;

/**
 * Strateji · adil baz karşılaştırması.
 *
 * **Neden ayrı bir bileşen.** Bu grafik sayfanın içinde SABİT sayılarla
 * duruyordu: `+%1.18`, `+%0.76`, `p = 0.13`. Tek ölçülmüş strateji varken
 * göze batmıyordu; ikinci strateji (harmonikler) eklendiğinde aynı
 * çubuklar onun sayfasında da çıkacaktı — yani **yanlış stratejinin
 * sayfasında doğru görünen bir grafik.** Ölçüm verisinin sayfada iki
 * yerde (tabloda ve grafikte) yaşaması, ikisinin er geç ayrışması
 * demektir.
 *
 * Şimdi tek kaynak var: `strateji.olcum`.
 */
export function OlcumSutunlari({ olcum }: { olcum: Olcum }) {
  const { sinyal, baz, p, birim } = olcum;
  const fark = sinyal - baz;

  // Sütunlar en büyük değere göre ölçeklenir; negatif değer de olabilir
  // (bir strateji adil bazın ALTINDA kalabilir ve bunu göstermek şart).
  const tepe = Math.max(Math.abs(sinyal), Math.abs(baz)) || 1;
  const TABAN = 104;
  const AZAMI = 70;
  const yukseklik = (v: number) => Math.max(3, (Math.abs(v) / tepe) * AZAMI);
  const tepeY = (v: number) => (v >= 0 ? TABAN - yukseklik(v) : TABAN);

  const yaz = (v: number) =>
    birim === "R" ? `${v >= 0 ? "+" : "−"}${Math.abs(v).toFixed(3)}R` : `${v >= 0 ? "+" : "−"}%${Math.abs(v).toFixed(2)}`;

  const baslik =
    birim === "R" ? "İşlem başına R · ortalama" : "20 bar ileri getiri · ortalama";

  return (
    <div>
      <Eyebrow>{baslik}</Eyebrow>
      <svg
        viewBox="0 0 340 132"
        role="img"
        style={{ width: "100%", height: "auto", marginTop: 10 }}
        aria-label={`Strateji sinyalleri ortalama ${yaz(sinyal)}, adil baz ${yaz(
          baz,
        )}, aradaki fark ${yaz(fark)}, permütasyon p değeri ${p.toFixed(4)}`}
      >
        <line x1="8" y1={TABAN} x2="332" y2={TABAN} stroke="var(--line-strong)" strokeWidth="1" />

        <rect x="42" y={tepeY(sinyal)} width="76" height={yukseklik(sinyal)} fill="var(--accent)" opacity=".8" />
        <text x="80" y={tepeY(sinyal) - 8} fill="var(--accent)" fontFamily="var(--f-mono)" fontSize="13" textAnchor="middle">
          {yaz(sinyal)}
        </text>
        <text x="80" y="120" fill="var(--text-2)" fontFamily="var(--f-mono)" fontSize="10" textAnchor="middle">
          sinyaller
        </text>

        <rect x="164" y={tepeY(baz)} width="76" height={yukseklik(baz)} fill="var(--text-3)" opacity=".6" />
        <text x="202" y={tepeY(baz) - 8} fill="var(--text-2)" fontFamily="var(--f-mono)" fontSize="13" textAnchor="middle">
          {yaz(baz)}
        </text>
        <text x="202" y="120" fill="var(--text-2)" fontFamily="var(--f-mono)" fontSize="10" textAnchor="middle">
          adil baz
        </text>

        {/* Fark çubuğu: iki sütunun tepesi arasındaki mesafe. Sıfıra yakınsa
            çizgi de kısa olur — "aradaki fark yok" görsel olarak da görünür. */}
        <line x1="266" y1={tepeY(sinyal)} x2="266" y2={tepeY(baz)} stroke="var(--text-3)" strokeWidth="1" />
        <line x1="262" y1={tepeY(sinyal)} x2="270" y2={tepeY(sinyal)} stroke="var(--text-3)" strokeWidth="1" />
        <line x1="262" y1={tepeY(baz)} x2="270" y2={tepeY(baz)} stroke="var(--text-3)" strokeWidth="1" />
        <text x="278" y={(tepeY(sinyal) + tepeY(baz)) / 2 - 2} fill="var(--text-2)" fontFamily="var(--f-mono)" fontSize="11">
          {yaz(fark)}
        </text>
        <text x="278" y={(tepeY(sinyal) + tepeY(baz)) / 2 + 12} fill="var(--text-3)" fontFamily="var(--f-mono)" fontSize="9.5">
          p = {p.toFixed(p < 0.01 ? 4 : 2)}
        </text>
      </svg>
      <p className="dim" style={{ fontSize: 12, margin: "10px 0 0", lineHeight: 1.55 }}>
        Adil baz, <b>aynı risk yapısıyla</b> (aynı stop ve hedef mesafesi) rastgele barlarda
        açılan işlemlerin ortalaması — düz &ldquo;piyasa yükseldi&rdquo; etkisi böyle ayıklanır.
        İki sütun birbirine yakınsa strateji, rastgeleden ayırt edilemiyor demektir.
      </p>
    </div>
  );
}
