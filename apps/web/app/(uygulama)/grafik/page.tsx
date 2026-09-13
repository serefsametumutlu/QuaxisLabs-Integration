"use client";

import { useState } from "react";
import { Eyebrow, Pill, Seg } from "@/components/ui";
import { Grafik } from "@/components/grafik/Grafik";
import { THYAO_GOLDEN_ZONE } from "@/lib/ornek-chartspec";

const TF = [
  { value: "4s", label: "4S" },
  { value: "1g", label: "1G" },
] as const;

const SPEC = THYAO_GOLDEN_ZONE;

/** Seviye fiyatı SPEC'ten okunur — aynı sayı iki yerde yazılmaz. */
function seviye(rol: string): number | null {
  const k = (SPEC.katmanlar ?? []).find((x) => x.tur === "seviye" && x.rol === rol);
  return k && k.tur === "seviye" ? k.fiyat : null;
}

const f = (n: number | null) => (n === null ? "—" : n.toFixed(2));

const giris = seviye("fib_618");
const ortaEsik = seviye("fib_705");
const stop = seviye("fib_1");
const hedef = seviye("fib_0");
const bos = seviye("seviye");

/** Ödül/risk — iki sayıdan türetilir, elle yazılmaz. */
const rr =
  giris !== null && stop !== null && hedef !== null
    ? Math.abs(hedef - giris) / Math.abs(giris - stop)
    : null;

/**
 * Grafik yüzeyi — sinyalin nasıl doğduğunun görsel kanıtı.
 *
 * Gösterilen strateji **Golden Zone (ICT OTE)**: yedi kapıdan geçmiş,
 * K4'te ölçülmüş ve verdikti `kanıtlanmadı` çıkmış olan. Ölçülmemiş bir
 * strateji vitrine konulmaz; ölçülüp kenar bulunamayan ise **etiketiyle**
 * konur (README madde 6: eleme değil etiketleme).
 */
export default function GrafikSayfasi() {
  const [tf, setTf] = useState<string>("1g");

  return (
    <section className="board">
      <header>
        <Eyebrow>Yüzey · Grafik</Eyebrow>
        <h2>Sinyalin nasıl doğduğunun görsel kanıtı</h2>
        <p>
          Levha bir <code className="num" style={{ fontSize: 12 }}>ChartSpec</code> okuyor. Mum,
          hacim, crosshair ve zoom/pan Lightweight Charts&apos;tan; fibo seviyeleri, OTE bandı,
          çıpalar ve durum rozeti bizim SVG katmanımızdan geliyor. Spec&apos;i Python komposeri
          <b> gerçek veriden</b> üretti — <b>çizici hiçbir seviyeyi kendisi hesaplamaz.</b>
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
          {SPEC.kunye.verdikt ? (
            <Pill>tarihsel isabet · {SPEC.kunye.verdikt}</Pill>
          ) : null}
        </div>

        <div className="chartbody">
          <Grafik
            spec={SPEC}
            yukseklik={470}
            hudEk={
              <>
                {/* Dar levhada uzun HUD metni üçüncü satıra sarıyordu
                    (K5 i9, 768 bulgusu); kısaltıldı. */}
                {SPEC.kunye.strateji_adi} <span className="dim">·</span> BOS → OTE{" "}
                <span className="dim">·</span>{" "}
                {/* "hedef" ile sayısı BÖLÜNMEZ: dar levhada ikisi ayrı
                    satıra düşüp sayı sahipsiz kalıyordu (K5 i10 bulgusu). */}
                <span style={{ whiteSpace: "nowrap" }}>
                  hedef{" "}
                  <b style={{ color: SPEC.kunye.yon === "al" ? "var(--up)" : "var(--down)" }}>
                    {f(hedef)}
                  </b>
                </span>
              </>
            }
          />
        </div>

        <div className="statbox">
          <div className="r">
            <span>Kırılan yapı (BOS)</span>
            <span>{f(bos)}</span>
          </div>
          <div className="r">
            <span>Giriş (0.62)</span>
            <span style={{ color: "var(--accent)" }}>{f(giris)}</span>
          </div>
          <div className="r">
            <span>Orta eşik (0.705)</span>
            <span>{f(ortaEsik)}</span>
          </div>
          <div className="r">
            <span>Stop (1.0)</span>
            <span>{f(stop)}</span>
          </div>
          <div className="r">
            <span>Hedef (0.0)</span>
            <span style={{ color: SPEC.kunye.yon === "al" ? "var(--up)" : "var(--down)" }}>
              {f(hedef)}
            </span>
          </div>
          <div className="r">
            <span>Ödül / risk</span>
            <span>{rr === null ? "—" : `${rr.toFixed(2)} : 1`}</span>
          </div>
        </div>

        <div className="notes">
          <div className="note">
            <h5>Neden bölge burada</h5>
            <p>
              Fibonacci, süpürme ucundan (%100) yer değiştirmenin ucuna (%0) çekilir. Bölge o
              bacağın 0.62–0.79 düzeltmesidir — grafikteki kesik çizgi bacağın kendisi. O çizgi
              olmadan merdiven havada asılı kalırdı.
            </p>
          </div>
          <div className="note">
            <h5>Asimetri nereden geliyor</h5>
            <p>
              Düzeltme tepeden ölçülür: derine girmek stop&apos;u küçültür, hedefi uzaklaştırmaz.
              0.62&apos;de ödül/risk 1.63, 0.705&apos;te 2.39, 0.79&apos;da 3.76. ICT&apos;nin
              0.705&apos;e &ldquo;sweet spot&rdquo; demesinin sebebi bu aritmetik.
            </p>
          </div>
          <div className="note">
            <h5>Geçersizlik</h5>
            <p>
              %100 seviyesinin ötesinde <b>gövde</b> kapanışı kurulumu bitirir. Wick geçebilir —
              wick&apos;i de geçersiz saymak sinyal sayısını sessizce yarıya indirirdi.
            </p>
          </div>
        </div>

        <div className="verdict">
          <Pill tone="acc">K4 · İSTATİSTİK</Pill>
          <p>
            <b>Kenar kanıtlanmadı.</b> 543 BIST sembolü, 8432 işlem, sembol-kümelenmiş, IS/OOS
            ayrımlı, üç bariyerli R ölçümü: işlem başına <b className="num">+0.045R</b>, aynı risk
            yapısıyla rastgele girişin bazı <b className="num">+0.071R</b> (p=0.95). Teyit
            katmanları (FVG / order block / süpürme) değer <b>eklemedi, eksiltti.</b> Sinyal
            gösterilir, iddia edilmez — <b>ölçülmemiş bir stratejiyi &ldquo;çalışıyor&rdquo; diye
            sunmuyoruz, ölçülmüş olanın sonucunu da saklamıyoruz.</b>
          </p>
        </div>
      </div>
    </section>
  );
}
