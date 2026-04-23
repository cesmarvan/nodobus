import babel from '@rolldown/plugin-babel'
import tailwindcss from '@tailwindcss/vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import { defineConfig } from 'vite'


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    babel({ presets: [reactCompilerPreset()] }),
    tailwindcss(),
  ],
  server: {
    middlewareMode: false,
    proxy: {
      '/api/tussam': {
        target: 'https://reddelineas.tussam.es',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/tussam/, '/API/infotus-ui/buses'),
      }
    }
  },
  preview: {
    port: 3000,
  },
  appType: 'spa',
})
