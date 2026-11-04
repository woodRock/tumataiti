import { existsSync, readFileSync, writeFileSync } from "node:fs";
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

// Latency benchmark (bench.html, src/bench.ts), dev server only: serves the
// held-out NZ documents and writes the timings to ml/results/.
const BENCH_DOCS = "../ml/data/v1/nz_test_full.jsonl";
const BENCH_OUT = "../ml/results/browser_latency.json";

function bench(): Plugin {
  return {
    name: "tumataiti-bench",
    apply: "serve",
    configureServer(server) {
      server.middlewares.use("/bench/docs", (_req, res) => {
        res.setHeader("Content-Type", "application/x-ndjson");
        res.end(readFileSync(BENCH_DOCS));
      });
      server.middlewares.use("/bench/result", (req, res) => {
        let body = "";
        req.on("data", (c) => (body += c));
        req.on("end", () => {
          writeFileSync(BENCH_OUT, JSON.stringify(JSON.parse(body), null, 2) + "\n");
          res.end("ok");
        });
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), contentSecurityPolicy(), bench()],
  define: { __STUDENT_MODEL__: JSON.stringify(studentModel) },
  build: { target: "es2022" },
});
