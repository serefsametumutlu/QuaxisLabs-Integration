"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui";

/**
 * Giriş ekranındaki sembol arama kutusu.
 * Sahte bir kutu değil: girilen metin taramaya sorgu olarak taşınır. Gerçek
 * sembol çözümlemesi veri katmanı geldiğinde (Faz 5) burada yapılacak.
 */
export function HeroForm() {
  const router = useRouter();
  const [q, setQ] = useState("");

  return (
    <form
      className="heroform"
      onSubmit={(e) => {
        e.preventDefault();
        const t = q.trim();
        router.push(t ? `/tarama?q=${encodeURIComponent(t)}` : "/tarama");
      }}
    >
      <input
        type="text"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Sembol ara: THYAO, ASELS, EREGL…"
        aria-label="Sembol ara"
      />
      <Button type="submit">Taramayı aç</Button>
    </form>
  );
}
