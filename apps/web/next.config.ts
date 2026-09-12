import path from "node:path";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Depo kökü ev dizini DEĞİL; Turbopack'in kökü bu uygulamaya sabitlenmezse
  // C:\Users\Samet altındaki yabancı package-lock.json'ı bulup uyarı veriyor.
  turbopack: { root: path.resolve(import.meta.dirname) },

  // Görsel kabul döngüsü için statik dışa aktarım: QUAXIS_EXPORT=1 npm run build
  // `out/` üretir, tools/ekran_goruntusu.py onu kendi içinde servis edip
  // ekran görüntüsünü alır. Normal derlemeyi etkilemez.
  ...(process.env.QUAXIS_EXPORT ? { output: "export" as const } : {}),
};

export default nextConfig;
