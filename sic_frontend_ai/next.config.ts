import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: "/api/:path*", // Ruta en el frontend
        destination: "http://127.0.0.1:8000/:path*", // Ruta del backend
      },
    ];
  },
};

export default nextConfig;
