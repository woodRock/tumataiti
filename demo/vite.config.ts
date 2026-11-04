import { existsSync, readFileSync } from "node:fs";
import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

// The student model is optional: `npm run model -- <exported onnx dir>` copies
// it into public/models/student/. Builds without it run the rules only.
const MANIFEST = "public/models/student/manifest.json";
const studentModel = existsSync(MANIFEST) ? JSON.parse(readFileSync(MANIFEST, "utf8")) : null;

// SPEC §7.1: the built page may only talk to its own origin. Applied at build
// time only, because the dev server relies on inline scripts for hot reload.
const CSP = [
  "default-src 'self'",
  "script-src 'self' 'wasm-unsafe-eval'",
  "style-src 'self' 'unsafe-inline'",
  "connect-src 'self'",
  "img-src 'self' data:",
  "object-src 'none'",
  "base-uri 'none'",
  "form-action 'none'",
].join("; ");

function contentSecurityPolicy(): Plugin {
  return {
    name: "tumataiti-csp",
    apply: "build",
    transformIndexHtml: (html) =>
      html.replace("<head>", `<head>\n    <meta http-equiv="Content-Security-Policy" content="${CSP}" />`),
  };
}

export default defineConfig({
  plugins: [react(), contentSecurityPolicy()],
  define: { __STUDENT_MODEL__: JSON.stringify(studentModel) },
  build: { target: "es2022" },
});
