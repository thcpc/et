import { fileURLToPath, URL } from 'node:url'
import path from 'path';
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@codemirror/state': path.resolve(__dirname, 'node_modules/@codemirror/state'),
      '@codemirror/view': path.resolve(__dirname, 'node_modules/@codemirror/view'),
      '@codemirror/language': path.resolve(__dirname, 'node_modules/@codemirror/language'),
      'jquery': path.resolve(__dirname, 'src/assets/summernote/jquery-3.4.1.slim.min.js')
    },
  },
  build: {
    assetsInlineLimit: 0, // 禁止内联字体文件
  },
  optimizeDeps: {
    include: ['@codemirror/state', '@codemirror/view', '@codemirror/language']
  }
})
