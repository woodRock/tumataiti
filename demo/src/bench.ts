/**
 * In-browser latency of the shipped student (dev server only; see the
 * `bench` plugin in vite.config.ts). Runs the rules alone, the student alone,
 * and the rules merged with the student on every held-out NZ document
 * (test_full), exactly as the demo does: ONNX Runtime Web, WebAssembly, one
 * thread. POSTs the per-document timings to /bench/result, which writes
 * ml/results/browser_latency.json.
 */
import { loadRedactor } from "./redactor";

/** Documents run first and not timed, so JIT compilation and allocation settle. */
const WARMUP = 10;

const log = (s: string) => {
  document.getElementById("log")!.textContent = s;
};

function quantile(xs: number[], q: number): number {
  const s = [...xs].sort((a, b) => a - b);
  const i = (s.length - 1) * q;
  const lo = Math.floor(i);
  return s[lo] + (s[Math.ceil(i)] - s[lo]) * (i - lo);
}

async function main() {
  const docs: { id: string; text: string }[] = (await (await fetch("/bench/docs")).text())
    .trim()
    .split("\n")
    .map((l) => JSON.parse(l));
  const redactor = await loadRedactor();
  const t0 = performance.now();
  const { loadStudent } = await import("./student");
  const student = await loadStudent(() => {});
  const loadMs = performance.now() - t0;
  const policy = redactor.defaultPolicy;

  for (const d of docs.slice(0, WARMUP)) redactor.redact(d.text, policy, await student.detect(d.text));

  const rules: number[] = [];
  const model: number[] = [];
  const total: number[] = [];
  for (const [i, d] of docs.entries()) {
    let t = performance.now();
    redactor.redact(d.text, policy);
    rules.push(performance.now() - t);
    t = performance.now();
    const spans = await student.detect(d.text);
    const m = performance.now() - t;
    redactor.redact(d.text, policy, spans);
    total.push(performance.now() - t);
    model.push(m);
    if (i % 50 === 0) log(`${i} / ${docs.length}: median ${quantile(total, 0.5).toFixed(1)} ms`);
  }
  const summary = (xs: number[]) => ({ median: quantile(xs, 0.5), p90: quantile(xs, 0.9), mean: xs.reduce((a, b) => a + b, 0) / xs.length });
  const result = {
    docs: docs.length,
    warmup: WARMUP,
    model: student.info,
    runtime: { library: "onnxruntime-web", backend: "wasm", threads: 1 },
    browser: { userAgent: navigator.userAgent, hardwareConcurrency: navigator.hardwareConcurrency, visibility: document.visibilityState },
    load_ms: loadMs,
    ms: { rules: summary(rules), student: summary(model), rules_student: summary(total) },
    per_doc_ms: { rules, student: model, rules_student: total },
  };
  await fetch("/bench/result", { method: "POST", body: JSON.stringify(result) });
  log(`done: ${docs.length} documents, median ${result.ms.rules_student.median.toFixed(1)} ms (rules + student)`);
  (window as unknown as { benchResult: unknown }).benchResult = result.ms;
}

main().catch((e) => log(`error: ${e}`));
