/** @type {import('next').NextConfig} */
const nextConfig = {
  // Desabilitar Turbopack explicitamente
  webpack: (config) => {
    return config
  }
};

module.exports = nextConfig;
