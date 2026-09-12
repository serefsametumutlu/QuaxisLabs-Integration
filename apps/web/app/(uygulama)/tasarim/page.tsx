"use client";

import { useState } from "react";
import "./tasarim.css";
import { Card, CardGrid, Eyebrow, Pill, ThemeSegment } from "@/components/ui";
import { VitrinKompakt } from "@/components/vitrin-kompakt";
import { BuyukTablo } from "@/components/buyuk-tablo";
import { StratejiKucukResim } from "@/components/strateji-kucuk-resim";
import { useTema } from "@/lib/tema-deposu";
import { AKSANLAR, AKSAN_ETIKET, TEMA_ETIKET, type Aksan, type TemaKipi } from "@/lib/tema";
import { ORNEK_KARTLAR, VERDIKT_ACIKLAMA } from "@/lib/ornek-veri";

const AKSAN_HEX: Record<Aksan, string> = { teal: "#2ED3C0", amber: "#E9A93A", blue: "#5B8CFF" };

const TOKEN_GRUPLARI = [
  { ad: "Zemin ve yüzey", tokenlar: ["--ground", "--surface", "--surface-2", "--surface-3"] },
  { ad: "Çizgi", tokenlar: ["--line", "--line-strong", "--grid"] },
  { ad: "Metin kademesi", tokenlar: ["--text", "--text-2", "--text-3"] },
  { ad: "Aksan — karara değer", tokenlar: ["--accent", "--accent-soft", "--accent-line", "--accent-ink"] },
  { ad: "Yön — semantik", tokenlar: ["--up", "--up-soft", "--down", "--down-soft"] },
  {
    ad: "Fibo merdiveni",
    tokenlar: ["--fib-0", "--fib-236", "--fib-382", "--fib-500", "--accent", "--fib-786", "--fib-1", "--fib-ext"],
  },
];

export default function TasarimSayfasi() {
  const { aksan, aksanAta } = useTema();

  // Üç sütun bağımsız: her biri kendi temasını gösterir ve kendi anahtarıyla
  // değiştirilebilir. Kök tema üstteki anahtarla yönetilir.
  const [sutun, setSutun] = useState<TemaKipi[]>(["system", "light", "dark"]);
  const sutunAta = (i: number, k: TemaKipi) => setSutun((s) => s.map((v, j) => (j === i ? k : v)));

  return (
    <div className="tsayfa">
      <header className="tust">
        <div>
          <Eyebrow>Tasarım Sistemi · iç vitrin</Eyebrow>
          <h1>Token&apos;lar ve bileşenler</h1>
        </div>
        {/* Tema ve aksan anahtarları kabuğun üst şeridinde; burada yalnız
            aksanın hex'i okunabilsin diye adlı seçici duruyor. */}
        <div className="sag">
          <span className="swatchrow">
            {AKSANLAR.map((a) => (
              <button
                key={a}
                type="button"
                className="swatch"
                aria-pressed={a === aksan}
                onClick={() => aksanAta(a)}
              >
                <i style={{ background: AKSAN_HEX[a] }} />
                {AKSAN_ETIKET[a]} <span className="hex">{AKSAN_HEX[a]}</span>
              </button>
            ))}
          </span>
        </div>
      </header>

      <p className="mut" style={{ fontSize: 13, margin: "12px 0 0", maxWidth: "80ch" }}>
        Dört referans sitenin ölçülmüş ortak dili. Gölge yok; yüzeyler bir tık açık zemin + saç teli
        inceliğinde kenarlıkla ayrılıyor. Ağırlık 400 varsayılan, 500 yalnızca vurgu, 700 hiç yok.
        Hiyerarşi boyutla değil opaklıkla kuruluyor. Sayfadaki bütün veriler{" "}
        <b className="dim">örnektir</b>.
      </p>

      {/* ══════════ ÜÇ TEMA YAN YANA ══════════ */}
      <section className="tbolum" id="tasarim-temalar">
        <header>
          <Eyebrow>Bölüm 01</Eyebrow>
          <h2>On beş bileşen, üç temada yan yana</h2>
          <p>
            Her sütun kendi <code className="num" style={{ fontSize: 12 }}>data-theme</code> kapsamını
            taşır; token&apos;lar kapsamlanabilir olduğu için aynı sayfada üç tema birden çizilebiliyor.
            Sütun başlığındaki anahtar yalnızca o sütunu değiştirir — sayfanın kendi teması üstteki
            anahtarda.
          </p>
        </header>

        <div className="temalar">
          {sutun.map((kip, i) => (
            <div className="temakutu" data-theme={kip} key={i}>
              <div className="bas">
                <span className="ad">{TEMA_ETIKET[kip]}</span>
                <ThemeSegment value={kip} onChange={(k) => sutunAta(i, k)} />
              </div>
              <div className="ic">
                <VitrinKompakt />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ══════════ DATATABLE ══════════ */}
      <section className="tbolum" id="tasarim-tablo">
        <header>
          <Eyebrow>Bölüm 02</Eyebrow>
          <h2>DataTable — 500 satır, sanallaştırılmış</h2>
          <p>
            Tablo bizde birinci sınıf bir bileşen: referans sitelerin hiçbirinde{" "}
            <code className="num" style={{ fontSize: 12 }}>&lt;table&gt;</code> yok, çünkü onlar
            pazarlama sitesi. Sıralanabilir kolonlar, sabit yükseklikli sanal pencere, mono +
            tabular-nums sayılar, satır-üzeri kancası ve tam klavye gezinmesi.
          </p>
        </header>
        <BuyukTablo />
      </section>

      {/* ══════════ TOKEN'LAR ══════════ */}
      <section className="tbolum" id="tasarim-tokenlar">
        <header>
          <Eyebrow>Bölüm 03</Eyebrow>
          <h2>Token&apos;lar</h2>
          <p>
            Hepsi <code className="num" style={{ fontSize: 12 }}>app/tokens.css</code>&apos;te,
            maketten birebir taşınmış hâlde. Hardcoded renk yasak; bu sayfadaki her örnek kutusu bile
            değerini token&apos;dan okur.
          </p>
        </header>

        <div className="tokenlar">
          {TOKEN_GRUPLARI.map((g) => (
            <div className="tokenkart" key={g.ad}>
              <div className="ad">{g.ad}</div>
              <div className="sira">
                {g.tokenlar.map((t) => (
                  <div key={t} className="ornek" style={{ background: `var(${t})` }} title={t} />
                ))}
              </div>
              <div className="alt">{g.tokenlar.join(" · ")}</div>
            </div>
          ))}
        </div>

        <div className="specgrid" style={{ marginTop: 14 }}>
          <div className="spec">
            <h5>Renk ayrımı</h5>
            <ul className="scale">
              <li>
                <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <i style={{ width: 22, height: 14, borderRadius: 2, background: "var(--accent)", display: "block" }} />
                  Aksan · karara değer
                </span>
                <code>~173°</code>
              </li>
              <li>
                <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <i style={{ width: 22, height: 14, borderRadius: 2, background: "var(--up)", display: "block" }} />
                  Yükseliş · yön
                </span>
                <code>~100°</code>
              </li>
              <li>
                <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <i style={{ width: 22, height: 14, borderRadius: 2, background: "var(--down)", display: "block" }} />
                  Düşüş · yön
                </span>
                <code>~356°</code>
              </li>
            </ul>
            <p className="note">
              Aksan ile yükseliş arası <b>73°</b>. Aksanı değiştirirsen bu mesafe yeniden ölçülmeli —
              gözle onaylanmaz.
            </p>
          </div>

          <div className="spec">
            <h5>Tipografi ölçeği</h5>
            <ul className="scale">
              <li>
                <span style={{ fontFamily: "var(--f-display)", fontSize: 19, letterSpacing: "-.5px" }}>
                  Levha başlığı
                </span>
                <code>19 / -0.5</code>
              </li>
              <li>
                <span style={{ fontSize: 14 }}>Gövde</span>
                <code>14 / 400</code>
              </li>
              <li>
                <span style={{ fontSize: 13 }}>Tablo satırı</span>
                <code>13 / 400</code>
              </li>
              <li>
                <Eyebrow>Eyebrow</Eyebrow>
                <code>11 / +2.2</code>
              </li>
            </ul>
            <p className="note">Başlıkta negatif tracking, etikette pozitif.</p>
          </div>

          <div className="spec">
            <h5>Türkçe glifler · üç yüz</h5>
            <div className="stack" style={{ gap: 7 }}>
              <span style={{ fontFamily: "var(--f-display)", fontSize: 17, letterSpacing: "-.4px" }}>
                İıĞğŞşÇçÖöÜü — Şişecam İğne
              </span>
              <span style={{ fontFamily: "var(--f-ui)", fontSize: 15 }}>
                İıĞğŞşÇçÖöÜü — Şişecam İğne
              </span>
              <span className="num" style={{ fontSize: 15 }}>
                İıĞğŞşÇçÖöÜü — 0123456789
              </span>
            </div>
            <p className="note">
              Archivo · Inter · JetBrains Mono — üçü de <b>yerel</b>, CDN bağımlılığı yok.
            </p>
          </div>

          <div className="spec">
            <h5>Yarıçap ikiliği</h5>
            <div className="yaricap">
              <figure>
                <div className="kutu" style={{ borderRadius: "var(--r-panel)" }} />
                <figcaption>panel · 2px</figcaption>
              </figure>
              <figure>
                <div className="kutu" style={{ borderRadius: "var(--r-media)" }} />
                <figcaption>medya · 8px</figcaption>
              </figure>
              <figure>
                <div className="kutu" style={{ borderRadius: "var(--r-pill)" }} />
                <figcaption>kontrol · hap</figcaption>
              </figure>
            </div>
            <p className="note">Ara değer yok. Her şeye yuvarlak köşe vermek bu dilin dışında.</p>
          </div>

          <div className="spec">
            <h5>Sayı dizgisi</h5>
            <ul className="scale num">
              <li>
                <span>THYAO</span>
                <span>209.10</span>
              </li>
              <li>
                <span>ASELS</span>
                <span>78.45</span>
              </li>
              <li>
                <span>EREGL</span>
                <span>1 204.75</span>
              </li>
              <li>
                <span>KCHOL</span>
                <span>9.08</span>
              </li>
            </ul>
            <p className="note">
              Mono + <code>tabular-nums</code> — ondalıklar hizalanır. Üçüncül kademe sayıya
              uygulanmaz.
            </p>
          </div>

          <div className="spec">
            <h5>Hareket</h5>
            <p className="note" style={{ margin: 0 }}>
              Kaydırma tetikli açılış animasyonu <b>yok</b>: sayfa ilk boyamada eksiksiz okunur.
              Geçişler yalnız durum değişiminde ve 120 ms. <code>prefers-reduced-motion</code>{" "}
              altında animasyon ve geçiş tamamen kapanır — iskelet parıltısı dahil.
            </p>
          </div>
        </div>
      </section>

      {/* ══════════ KARTLAR ══════════ */}
      <section className="tbolum" id="tasarim-kartlar">
        <header>
          <Eyebrow>Bölüm 04</Eyebrow>
          <h2>Kart ızgarası</h2>
          <p>
            Kartın yüzü gerçek bir grafik olacak (Faz 4). Altında kaynağı, pasaport kapısı ve
            istatistik verdikti. <b className="dim">Buradaki grafikler örnektir.</b>
          </p>
        </header>
        <CardGrid>
          {ORNEK_KARTLAR.map((k) => (
            <Card
              key={k.ad}
              thumb={<StratejiKucukResim tip={k.tip} />}
              meta={`${k.kaynak} · ${k.kapi}`}
              title={k.ad}
              foot={
                <>
                  <Pill tone="acc">{k.paket}</Pill>
                  <Pill title={VERDIKT_ACIKLAMA[k.verdikt]}>{k.verdikt}</Pill>
                  <a href="#tasarim-kartlar">Stratejiyi aç →</a>
                </>
              }
            >
              {k.ozet}
            </Card>
          ))}
        </CardGrid>
      </section>
    </div>
  );
}
