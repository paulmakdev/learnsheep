import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import basicSsl from '@vitejs/plugin-basic-ssl'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), basicSsl()],
  server: {
    port: 3000,
    proxy: {
        '/api': {
            target: 'https://localhost:8000',
            secure: false, // allows self-signed cert
            changeOrigin: true
        }
    }
  }
})
