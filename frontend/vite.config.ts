import { fileURLToPath, URL } from "node:url";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

/**
 * Vite configuration.
 *
 * - The `@` alias maps to `src/` for clean absolute imports.
 * - During development, requests to `/api` are proxied to the FastAPI backend
 *   so the frontend and backend can run on different ports without CORS pain.
 */
export default defineConfig({
  // Base public path. Defaults to "/" for local dev and the FastAPI-backed
  // build; the GitHub Pages workflow sets VITE_BASE=/pi_theorem/ so assets and
  // data resolve under the project-page sub-path.
  base: process.env.VITE_BASE || "/",
  plugins: [react()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
