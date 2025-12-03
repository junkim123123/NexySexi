/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  
  // Render 배포 최적화: standalone 모드로 빌드하여 더 작은 이미지 크기와 빠른 시작 시간 제공
  output: 'standalone',
  
  webpack: (config, { isServer }) => {
    // Fix module resolution for uuid and other packages
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    
    // Ensure uuid is resolved from root node_modules
    config.resolve.alias = {
      ...config.resolve.alias,
      uuid: require.resolve('uuid'),
    };
    
    return config;
  },
}

module.exports = nextConfig

