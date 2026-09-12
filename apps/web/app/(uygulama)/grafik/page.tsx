"use client";

import { useState } from "react";
import { Eyebrow, Pill, Seg } from "@/components/ui";
import { Faz4Isareti, GrafikYeri } from "@/components/kabuk/GrafikYeri";
import { STRATEJILER } from "@/lib/ornek-strateji";

const TF = [
  { value: "4s", label: "4S" },
  { value: "1g", label: "1G" },
] as const;

const STRATEJI = STRATEJILER[0];

/**
 * Grafik yüzeyi — sinyalin nasıl doğduğunun görsel kanıtı.
 * Levhanın çevresi (çubuk, HUD, durum kutusu, dört not, K4 verdikti) burada
 * kurulur; levhanın İÇİ Faz 4'te ChartSpec ile doldurulacak.
 */
export default function GrafikSayfasi() {
  const [tf, setTf] = useState<string>("1g");

  return (
    <section className="board">
      <header>
        <Eyebrow>Yüzey · Grafik</Eyebrow>
        <h2>Sinyalin nasıl doğduğunun görsel kanıtı</h2>
        <p>
          Levhanın çerçevesi, HUD&apos;u, durum kutusu ve altındaki dört not bu fazda kuruldu.
          Levhanın içi — dolgulu X-A-B-C-D gövdesi, oran-renkli fibo merdiveni, numaralı temas
          daireleri, crosshair — <b>Faz 4</b>&apos;te <code className="num" style={{ fontSize: 12 }}>ChartSpec</code>{" "}
          ile bağlanacak.
        </p>
      </header>

      <div className="chartframe">
        <div className="chartbar">
          <span className="sym">THYAO</span>
          <span className="dim" style={{ fontSize: 12 }}>
            Türk Hava Yolları · BIST
          </span>
          <Seg label="Zaman dilimi" options={TF} value={tf} onChange={setTf} mono />
          <span className="sep" style={{ width: 1, height: 18, background: "var(--line)" }} />
          <Pill tone="acc">yapı · altın bölge</Pill>
          <Pill tone="down">SAT</Pill>
          <Pill>TAMAMLANDI</Pill>
          <span style={{ marginLeft: "auto" }} />
          <Faz4Isareti />
          <Eyebrow style={{ letterSpacing: "1.4px", fontSize: 10 }}>örnek veri</Eyebrow>
        </div>

        <div className="chartbody">
          <GrafikYeri
            w={1180}
            h={470}
            bar={140}
            /* HUD ve durum kutusu üstte duruyor: seri onların ALTINDAN
               başlar, sağdaki pay yalnız fiyat oluğu kadar. Böylece ne son
               barlar ne de fiyat rozeti bir katmanın arkasında kalır. */
            padUst={124}
            padSag={96}
            son={{ fiyat: 159.49, yon: "down" }}
            label="THYAO günlük grafik — örnek seri; strateji çizimleri Faz 4'te eklenecek"
          />

          <div className="hud">
            <div className="l1">
              THYAO <span className="dim">·</span> BIST <span className="dim">·</span>{" "}
              {tf === "1g" ? "1G" : "4S"}
            </div>
            <div className="l2">
              Altın Bölge <span className="dim">·</span> baskın salınım X→A{" "}
              <span className="dim">·</span> D hedefi{" "}
              <b style={{ color: "var(--down)" }}>159.49</b>
            </div>
          </div>

          <div className="statbox">
            <div className="h">
              <span>ALTIN BÖLGE</span>
              <span>DURUM</span>
            </div>
            {[
              ["Baskın salınım", "X→A · 39.00"],
              ["Bölge (0.618–0.786)", "185.00 / 178.45"],
              ["Doğduğu bar", "18 bar önce"],
            ].map(([k, v]) => (
              <div className="r" key={k}>
                <span>{k}</span>
                <span>{v}</span>
              </div>
            ))}
            <div className="r">
              <span>Temas</span>
              <span style={{ color: "var(--accent)" }}>3 · tutmadı</span>
            </div>
            <div className="r">
              <span>Yön</span>
              <span style={{ color: "var(--down)" }}>Satış ▼</span>
            </div>
          </div>
        </div>

        <div className="notes">
          {STRATEJI.notlar.map((n) => (
            <div className="note" key={n.baslik}>
              <h5>{n.baslik}</h5>
              <p>{n.govde}</p>
            </div>
          ))}
        </div>

        <div className="verdict">
          <Pill tone="acc">K4 · İSTATİSTİK</Pill>
          <p>
            <b>Kenar kanıtlanmadı.</b> 586 sembol, sembol-kümelenmiş, IS/OOS ayrımlı, permütasyon +
            BH-FDR ölçümünde bu strateji q=0.05 eşiğini geçemedi (n=553 sembol, fark +%0.42, p=0.13).
            Sinyal gösterilir, iddia edilmez — <b>ölçülmemiş bir stratejiyi “çalışıyor” diye
            sunmuyoruz.</b>
          </p>
        </div>
      </div>
    </section>
  );
}
