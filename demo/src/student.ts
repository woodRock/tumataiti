import * as ort from "onnxruntime-web/wasm";
import ortWasmUrl from "onnxruntime-web/ort-wasm-simd-threaded.wasm?url";
import initStudent, { Student } from "./wasm-student/tumataiti_student.js";

/** A span from the student model, with UTF-16 offsets. */
export interface ModelSpan {
  start: number;
  end: number;
  label: string;
  confidence: number;
}

export interface StudentInfo {
  /** Backbone name, e.g. `deberta-v3-small`. */
  name: string;
  /** How the weights were quantised, e.g. `int8 embeddings, int4 encoder`. */
  precision: string;
  bytes: number;
  /** The model file in order: it is stored in parts because GitHub refuses files over 100 MB. */
  parts: string[];
  /** Hugging Face repo of a published model, e.g. `woodrock/tumataiti-deberta-v3-small-open`. */
  repo: string | null;
}

export interface StudentModel {
  info: StudentInfo;
  /** Spans for `text`; runs one window at a time on this device. */
  detect(text: string): Promise<ModelSpan[]>;
}

const BASE = `${import.meta.env.BASE_URL}models/student/`;
/** Decoding threshold on P(not O), as in training and evaluation. */
const THRESHOLD = 0.5;

async function download(url: string, onBytes: (n: number) => void): Promise<Uint8Array> {
  const res = await fetch(url);
  if (!res.ok || !res.body) throw new Error(`${url}: ${res.status}`);
  const chunks: Uint8Array[] = [];
  const reader = res.body.getReader();
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    onBytes(value.length);
  }
  const out = new Uint8Array(chunks.reduce((n, c) => n + c.length, 0));
  let at = 0;
  for (const c of chunks) {
    out.set(c, at);
    at += c.length;
  }
  return out;
}

function join(chunks: Uint8Array[]): Uint8Array {
  const out = new Uint8Array(chunks.reduce((n, c) => n + c.length, 0));
  let at = 0;
  for (const c of chunks) {
    out.set(c, at);
    at += c.length;
  }
  return out;
}

/**
 * Download the student model from this site and start it. Everything after
 * this runs on the device: the files are static, and no text is ever sent.
 * `onProgress` gets the fraction downloaded. Import this module dynamically,
 * so ONNX Runtime only loads when the model is switched on.
 */
export async function loadStudent(onProgress: (fraction: number) => void): Promise<StudentModel> {
  const info = __STUDENT_MODEL__;
  if (!info) throw new Error("this build has no model");
  let got = 0;
  const tick = (n: number) => onProgress(Math.min(1, (got += n) / info.bytes));
  const text = async (f: string) => new TextDecoder().decode(await download(BASE + f, tick));
  const [tokenizer, config, weights] = await Promise.all([
    text("tokenizer.json"),
    text("config.json"),
    Promise.all(info.parts.map((p) => download(BASE + p, tick))).then(join),
    initStudent(),
  ]);
  const student = new Student(tokenizer, config);

  // Single-threaded: threads need cross-origin isolation headers, which a
  // static host such as GitHub Pages cannot set.
  ort.env.wasm.wasmPaths = { wasm: ortWasmUrl };
  ort.env.wasm.numThreads = 1;
  const session = await ort.InferenceSession.create(weights, { executionProviders: ["wasm"] });
  const tags = student.numTags();

  // One document at a time: ONNX Runtime Web runs one session call at a time.
  let queue: Promise<unknown> = Promise.resolve();
  const run = async (input: string): Promise<ModelSpan[]> => {
    const windows = student.windows(input);
    try {
      for (let i = 0; i < windows.count(); i++) {
        const ids = windows.ids(i);
        const shape = [1, ids.length];
        const out = await session.run({
          input_ids: new ort.Tensor("int64", ids, shape),
          attention_mask: new ort.Tensor("int64", new BigInt64Array(ids.length).fill(1n), shape),
        });
        const logits = out.logits.data as Float32Array;
        if (logits.length !== ids.length * tags) throw new Error("unexpected logits shape");
        windows.addLogits(student, i, logits, THRESHOLD);
      }
      return JSON.parse(windows.spans());
    } finally {
      windows.free();
    }
  };

  return {
    info,
    detect(input) {
      const result = queue.then(() => run(input));
      queue = result.catch(() => undefined);
      return result;
    },
  };
}
