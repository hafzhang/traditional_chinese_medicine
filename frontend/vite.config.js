import { defineConfig } from 'vite'
import uni from '@dcloudio/vite-plugin-uni'
import path from 'path'

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(process.cwd(), 'src')
    }
  },
  plugins: [
    uni()
  ],
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        timeout: 60000,
        proxyTimeout: 60000,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err);
          });
        }
      },
      '/static': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        timeout: 60000,
        proxyTimeout: 60000,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('static proxy error', err);
          });
        }
      }
    },
    open: '/#/pages/index/index'
  }
})
