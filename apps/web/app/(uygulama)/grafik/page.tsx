"use client";

import { useState } from "react";
import { Eyebrow, Pill, Seg } from "@/components/ui";
import { Grafik } from "@/components/grafik/Grafik";
import { THYAO_SWING_FIB_ABCD } from "@/lib/ornek-chartspec";
import { STRATEJILER } from "@/lib/ornek-strateji";

const TF = [
  { value: "4s", label: "4S" },
  { value: "1g", label: "1G" },
] as const;

const STRATEJI = STRATEJILER[0];
const SPEC = THYAO_SWING_FIB_ABCD;

/** Seviye fiyatı SPEC'ten okunur — aynı sayı iki yerde yazılmaz. */
function seviye(rol: string): number | null {
  const k = (SPEC.katmanlar ?? []).find((x) => x.tur === "seviye" && x.rol === rol);
  return k && k.tur === "seviye" ? k.fiyat : null;
}

const f = (n: number | null) => (n === null ? "—" : n.toFixed(2));

/**
 * Grafik yüzeyi — sinyalin nasıl doğduğunun görsel kanıtı.
 *
 * Levha artık bir ChartSpec okuyor: mum, hacim, crosshair ve zoom/pan
 * Lightweight Charts'tan; fibo merdiveni, dolgulu X-A-B-C-D gövdeleri, köşe
 * rozetleri ve durum rozeti bizim SVG katmanımızdan. Sayfadaki bütün sayılar
 * spec'ten türetilir.
 */
export default function GrafikSayfasi() {
  const [tf, setTf] = useState<string>("1g");

  const a = seviye("fib_0");
  const x = seviye("fib_1");

  return (
    <section className="board">
      <header>
        <Eyebrow>Yüzey · Grafik</Eyebrow>
        <h2>Sinyalin nasıl doğduğunun görsel kanıtı</h2>
        <p>
          Levha bir <code className="num" style={{ fontSize: 12 }}>ChartSpec</code> okuyor. Mum,
          hacim, crosshair ve zoom/pan Lightweight Charts&apos;tan; fibo merdiveni, dolgulu
          X-A-B-C-D gövdeleri, köşe rozetleri ve durum rozeti bizim SVG katmanımızdan geliyor.
          Spec&apos;i Python komposeri üretti — <b>çizici hiçbir seviyeyi kendisi hesaplamaz.</b>
        </p>
      </header>

      <div className="chartframe">
        <div className="chartbar">
          <span className="sym">{SPEC.kunye.sembol}</span>
          <span className="dim" style={{ fontSize: 12 }}>
            {SPEC.kunye.ad} · BIST
          </span>
          <Seg label="Zaman dilimi" options={TF} value={tf} onChange={setTf} mono />
          <span className="sep" style={{ width: 1, height: 18, background: "var(--line)" }} />
          <Pill tone="acc">yapı · {SPEC.kunye.strateji_adi?.toLocaleLowerCase("tr")}</Pill>
          <Pill tone={SPEC.kunye.yon === "al" ? "up" : "down"}>
            {SPEC.kunye.yon === "al" ? "AL" : "SAT"}
          </Pill>
          <Pill>{SPEC.kunye.durum?.toLocaleUpperCase("tr")}</Pill>
          <span style={{ marginLeft: "auto" }} />
          {SPEC.kunye.ornek_mi ? (
            <Eyebrow style={{ letterSpacing: "1.4px", fontSize: 10 }}>örnek veri</Eyebrow>
          ) : null}
        </div>

        <div className="chartbody">
          <Grafik
            spec={SPEC}
            yukseklik={470}
            hudEk={
              <>
                {SPEC.kunye.strateji_adi} <span className="dim">·</span> baskın salınım X→A{" "}
                <span className="dim">·</span> D hedefi{" "}
                <b style={{ color: "var(--down)" }}>{f(seviye("fib_1272"))}</b>
              </>
            }
          />

        </div>

        <div className="statbox">
          <div className="r">
            <span>Baskın salınım</span>
            <span>X→A · {a !== null && x !== null ? (a - x).toFixed(2) : "—"}</span>
          </div>
          <div className="r">
            <span>Bölge (0.618–0.786)</span>
            <span>
              {f(seviye("fib_618"))} / {f(seviye("fib_786"))}
            </span>
          </div>
          <div className="r">
            <span>D hedefi (1.272)</span>
            <span style={{ color: "var(--down)" }}>{f(seviye("fib_1272"))}</span>
          </div>
          <div className="r">
            <span>Azami risk (1.618)</span>
            <span>{f(seviye("fib_1618"))}</span>
          </div>
          <div className="r">
            <span>Temas</span>
            <span style={{ color: "var(--accent)" }}>3 · tutmadı</span>
          </div>
          <div className="r">
            <span>Yön</span>
            <span style={{ color: "var(--down)" }}>Satış ▼</span>
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
