import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    open: false,
    cors: true,
    allowedHosts: true
  },
  preview: {
    host: '0.0.0.0',
    port: 3000,
    open: false,
    cors: true,
    allowedHosts: true
  },
  build: {
    emptyOutDir: false
  }
});
