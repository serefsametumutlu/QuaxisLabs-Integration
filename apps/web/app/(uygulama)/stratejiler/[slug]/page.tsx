import { notFound } from "next/navigation";
import { Eyebrow, Faq, Pill } from "@/components/ui";
import { STRATEJILER, stratejiBul } from "@/lib/ornek-strateji";
import { StratejiGovde } from "./govde";

export function generateStaticParams() {
  return STRATEJILER.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const s = stratejiBul(slug);
  return { title: s ? `${s.ad} · QuaxisLabs` : "QuaxisLabs" };
}

/**
 * Strateji sayfası — bir stratejinin tam künyesi.
 *
 * İskelet LuxAlgo'nun gösterge sayfasından alındı. İki bölüm bizi ayırıyor:
 * KAYNAK ("bu eşik nereden geldi?") ve ÖLÇÜM ("işe yarıyor mu?"). Rakipler 874
 * gösterge yayınlıyor ve hiçbirinin ileriye dönük getirisini göstermiyor.
 */
export default async function StratejiSayfasi({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const s = stratejiBul(slug);
  if (!s) notFound();

  return (
    <section className="board">
      <header>
        <Eyebrow>Yüzey · Strateji sayfası</Eyebrow>
      </header>

      <div className="stratHead">
        <div>
          <Eyebrow>{s.paket} paketi</Eyebrow>
          <h2>{s.ad}</h2>
          <p>{s.ozet}</p>
        </div>
        <div className="rt">
          {s.rozetler.map((r) => (
            <Pill key={r}>{r}</Pill>
          ))}
          <Pill>{s.verdikt}</Pill>
        </div>
      </div>

      <StratejiGovde strateji={s} />

      {/* ── PARAMETRELER ── */}
      <div className="sect">
        <h3>
          Parametreler <span className="gate">K1 · SÖZLEŞME</span>
        </h3>
        <p className="lede">
          Hepsi <code className="num" style={{ fontSize: 12 }}>frozen dataclass</code> alanı; sonuç
          kaydı bir <code className="num" style={{ fontSize: 12 }}>params_hash</code> taşır. Aynı
          veri + aynı parametre = bit bit aynı sonuç.
        </p>
        <div className="params">
          {s.parametreler.map((g) => (
            <div key={g.baslik}>
              <h4>{g.baslik}</h4>
              <dl>
                {g.alanlar.map((a) => (
                  <div key={a.ad}>
                    <dt>
                      {a.ad} <span className="def">{a.varsayilan}</span>
                    </dt>
                    <dd>{a.aciklama}</dd>
                  </div>
                ))}
              </dl>
            </div>
          ))}
        </div>
      </div>

      {/* ── KAYNAK ── */}
      <div className="sect">
        <h3>
          Kaynak <span className="gate">K0 · KAYNAK</span>
        </h3>
        <p className="lede">
          Her eşiğin nereden geldiği burada yazar. <b>Ezberden sayı yazmak yasak</b> — kitapta
          yoksa, ölçümle türetildiği belirtilir.
        </p>
        <div className="src">
          {s.kaynak.map((k) => (
            <div className={k.acik ? "srcbox gap" : "srcbox"} key={k.etiket}>
              <div className="k">{k.etiket}</div>
              <p>
                {k.kodOnce && k.kod ? (
                  <>
                    <code>{k.kod}</code>{" "}
                  </>
                ) : null}
                {k.govde}
                {!k.kodOnce && k.kod ? (
                  <>
                    {" "}
                    <code>{k.kod}</code>
                  </>
                ) : null}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* ── ÖLÇÜM ── */}
      <div className="sect">
        <h3>
          Ölçüm <span className="gate">K3 · K4</span>
        </h3>
        <p className="lede">
          Bu bölüm rakiplerde yok. Stratejinin işe yarayıp yaramadığı burada yazar — <b>ne çıkarsa o.</b>
        </p>

        {s.olcum ? (
          <div className="measure">
            <div>
              <table className="mtable">
                <thead>
                  <tr>
                    <th colSpan={2}>K4 · Sembol-kümelenmiş OOS testi</th>
                  </tr>
                </thead>
                <tbody>
                  {s.olcum.satirlar.map(([k, v]) => (
                    <tr key={k}>
                      <td>{k}</td>
                      <td>{v}</td>
                    </tr>
                  ))}
                  {s.olcum.kotu ? (
                    <tr>
                      <td>BH-FDR (q=0.05)</td>
                      <td style={{ color: "var(--down)" }}>geçemedi</td>
                    </tr>
                  ) : null}
                </tbody>
              </table>
              <p className="dim" style={{ fontSize: 12, margin: "12px 0 0", lineHeight: 1.55 }}>
                {s.olcum.uyari}
              </p>
            </div>
            <div>
              <Eyebrow>20 bar ileri getiri · ortalama</Eyebrow>
              <svg
                viewBox="0 0 340 132"
                role="img"
                style={{ width: "100%", height: "auto", marginTop: 10 }}
                aria-label="Gösterge sinyalleri ortalama yüzde 1.18, yön-ağırlıklı adil baz yüzde 0.76, aradaki fark yüzde 0.42 ve istatistiksel olarak anlamlı değil"
              >
                <line x1="8" y1="104" x2="332" y2="104" stroke="var(--line-strong)" strokeWidth="1" />
                <rect x="42" y="34" width="76" height="70" fill="var(--accent)" opacity=".8" />
                <text x="80" y="26" fill="var(--accent)" fontFamily="var(--f-mono)" fontSize="13" textAnchor="middle">
                  +%1.18
                </text>
                <text x="80" y="120" fill="var(--text-2)" fontFamily="var(--f-mono)" fontSize="10" textAnchor="middle">
                  sinyaller
                </text>
                <rect x="164" y="59" width="76" height="45" fill="var(--text-3)" opacity=".6" />
                <text x="202" y="51" fill="var(--text-2)" fontFamily="var(--f-mono)" fontSize="13" textAnchor="middle">
                  +%0.76
                </text>
                <text x="202" y="120" fill="var(--text-2)" fontFamily="var(--f-mono)" fontSize="10" textAnchor="middle">
                  adil baz
                </text>
                <line x1="266" y1="34" x2="266" y2="59" stroke="var(--text-3)" strokeWidth="1" />
                <line x1="262" y1="34" x2="270" y2="34" stroke="var(--text-3)" strokeWidth="1" />
                <line x1="262" y1="59" x2="270" y2="59" stroke="var(--text-3)" strokeWidth="1" />
                <text x="278" y="44" fill="var(--text-2)" fontFamily="var(--f-mono)" fontSize="11">
                  +%0.42
                </text>
                <text x="278" y="58" fill="var(--text-3)" fontFamily="var(--f-mono)" fontSize="9.5">
                  p = 0.13
                </text>
              </svg>
              <p className="dim" style={{ fontSize: 12, margin: "10px 0 0", lineHeight: 1.55 }}>
                Adil baz, aynı sembollerde rastgele barların sinyallerin kendi al/sat oranıyla
                ağırlıklandırılmış hâli — düz “piyasa yükseldi” etkisi ayıklanmış olur.
              </p>
            </div>
          </div>
        ) : (
          <div className="srcbox gap">
            <div className="k">Ölçüm yok</div>
            <p>
              Bu strateji K4 kapısına gelmedi. <b>Sayı uydurmuyoruz</b>: kutu doldurulana kadar boş
              durur ve kütüphanedeki rozeti “ölçülmedi” kalır.
            </p>
          </div>
        )}
      </div>

      {/* ── SSS ── */}
      <div className="sect">
        <h3>Sık sorulanlar</h3>
        {s.sss.map((f, i) => (
          <Faq key={f.soru} question={f.soru} open={i === 0}>
            {f.cevap}
          </Faq>
        ))}
      </div>
    </section>
  );
}
