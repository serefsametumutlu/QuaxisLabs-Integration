import path from "node:path";
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Depo kökü ev dizini DEĞİL; Turbopack'in kökü bu uygulamaya sabitlenmezse
  // C:\Users\Samet altındaki yabancı package-lock.json'ı bulup uyarı veriyor.
  turbopack: { root: path.resolve(import.meta.dirname) },
};

export default nextConfig;
