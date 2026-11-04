import { useEffect, useMemo, useRef, useState } from "react";
import { CloudView } from "./components/CloudView";
import { Editor } from "./components/Editor";
import { Findings } from "./components/Findings";
import { NetworkMeter } from "./components/NetworkMeter";
import { PolicyPanel } from "./components/PolicyPanel";
import { StudentPanel, type StudentState } from "./components/StudentPanel";
import { PRESETS } from "./presets";
import type { Policy, Redactor } from "./redactor";
import type { ModelSpan } from "./student";

const SETTLE_MS = 450;

export function App({ redactor }: { redactor: Redactor }) {
  const [text, setText] = useState(PRESETS[0].text);
  const [settled, setSettled] = useState(text);
  const [policy, setPolicy] = useState<Policy>(redactor.defaultPolicy);
  const [preset, setPreset] = useState<string | null>(PRESETS[0].id);
  const [run, setRun] = useState(0);
  const [stagger, setStagger] = useState(true);
  const [copied, setCopied] = useState(false);
  const [student, setStudent] = useState<StudentState>({ status: "off" });
  const [detected, setDetected] = useState<{ text: string; spans: ModelSpan[] } | null>(null);
  const model = student.status === "ready" ? student.model : null;
  // A preset settles at once and replays its animation once the model (if on) has run.
  const presetPending = useRef(false);

  // The outbound view waits for typing to pause, and for the model if it is on,
  // so it changes once per edit and never shows names the model has yet to find.
  useEffect(() => {
    if (settled === text && (!model || detected?.text === text)) return;
    let cancelled = false;
    const delay = presetPending.current || settled === text ? 0 : SETTLE_MS;
    const t = setTimeout(async () => {
      if (model) {
        try {
          const spans = await model.detect(text);
          if (cancelled) return;
          setDetected({ text, spans });
        } catch (err) {
          console.error(err);
          if (!cancelled) setStudent({ status: "error", message: "The model stopped working in this browser." });
          return;
        }
      }
      setSettled(text);
      if (presetPending.current) {
        presetPending.current = false;
        replay();
      }
    }, delay);
    return () => {
      cancelled = true;
      clearTimeout(t);
    };
  }, [text, settled, model, detected]);

  const spansFor = (t: string) => (model && detected?.text === t ? detected.spans : undefined);
  const live = useMemo(() => redactor.redact(text, policy, spansFor(text)), [redactor, text, policy, model, detected]);
  const outbound = useMemo(
    () => redactor.redact(settled, policy, spansFor(settled)),
    [redactor, settled, policy, model, detected],
  );

  const replay = () => {
    setStagger(true);
    setRun((r) => r + 1);
  };

  const loadPreset = (id: string) => {
    const p = PRESETS.find((p) => p.id === id)!;
    setPreset(id);
    setText(p.text);
    if (model) {
      presetPending.current = true;
    } else {
      setSettled(p.text);
      replay();
    }
  };

  const edit = (value: string) => {
    setPreset(null);
    setStagger(false);
    setText(value);
  };

  const copy = async () => {
    await navigator.clipboard.writeText(outbound.output);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const active = PRESETS.find((p) => p.id === preset);
  const counts = {
    redacted: live.findings.filter((f) => f.replacement !== null).length,
    flagged: live.findings.filter((f) => f.action === "flag").length,
  };

  return (
    <>
      <header className="top">
        <div className="brand">
          <span className="logo" aria-hidden="true">
            <i />
            <i />
          </span>
          <span>
            <strong>Tūmataiti</strong>
            <span className="muted"> · local redaction for Atamai</span>
          </span>
        </div>
        <NetworkMeter since={model ? "the model loaded" : "the redactor loaded"} />
      </header>

      <main>
        <section className="intro">
          <h1>Redact it before it leaves your device.</h1>
          <p className="lede">
            Type or paste below. Every check runs here in your browser, compiled from Rust to WebAssembly. Nothing you
            type is sent anywhere, so the cloud model only ever sees the right-hand side.
          </p>
        </section>

        <nav className="presets" aria-label="Examples">
          {PRESETS.map((p) => (
            <button
              key={p.id}
              type="button"
              className={p.id === preset ? "chip chip-on" : "chip"}
              aria-pressed={p.id === preset}
              onClick={() => loadPreset(p.id)}
            >
              {p.title}
            </button>
          ))}
        </nav>
        <p className="preset-note muted">{active ? `Shows: ${active.shows}.` : "Your own text."}</p>

        <StudentPanel state={student} onChange={setStudent} />

        <div className="panes">
          <section className="pane">
            <header className="pane-head">
              <h2>Your text</h2>
              <span className="muted small">stays on this device</span>
            </header>
            <Editor value={text} findings={live.findings} onChange={edit} />
            <footer className="pane-foot muted small">
              {counts.redacted} redacted · {counts.flagged} flagged for review
            </footer>
          </section>

          <section className="pane pane-cloud">
            <header className="pane-head">
              <h2>What the cloud would see</h2>
              <span className="pane-actions">
                <button type="button" className="ghost" onClick={replay} aria-label="Replay the redaction animation">
                  ↻ Replay
                </button>
                <button type="button" className="ghost" onClick={copy} disabled={outbound.blocked}>
                  {copied ? "Copied" : "Copy"}
                </button>
              </span>
            </header>
            <CloudView text={settled} redaction={outbound} run={run} stagger={stagger} />
          </section>
        </div>

        <div className="lower">
          <section>
            <h2>What was found</h2>
            <Findings findings={live.findings} />
          </section>
          <aside>
            <h2>Policy</h2>
            <PolicyPanel
              policy={policy}
              model={model !== null}
              onChange={setPolicy}
              onReset={() => setPolicy(redactor.defaultPolicy)}
            />
          </aside>
        </div>

        <section className="trust">
          <h2>How do I know nothing is sent?</h2>
          <div className="cards">
            <article>
              <h3>It runs in your browser</h3>
              <p>
                The rules are Rust compiled to WebAssembly, and the optional model runs with ONNX Runtime in the page.
                Once they have loaded, redaction needs no server. You can switch your wifi off and keep typing.
              </p>
            </article>
            <article>
              <h3>The page is locked down</h3>
              <p>
                A Content-Security-Policy forbids the page from contacting any other site. There is no analytics, no
                backend and no storage of what you type.
              </p>
            </article>
            <article>
              <h3>Check it yourself</h3>
              <p>
                Open your browser's developer tools, go to the Network tab and type. Nothing appears. The counter at the
                top uses the browser's own records of every request.
              </p>
            </article>
          </div>
        </section>
      </main>

      <footer className="bottom muted small">
        <p>
          Deterministic rules for structured identifiers, plus an optional small model (milestone 3) for names,
          addresses and iwi, hapū and marae. Health details and restricted mātauranga are not detected yet. The model is
          a research prototype trained on synthetic data. All examples are synthetic. Part of the Hiringa Te Mahara
          Atamai research programme.
        </p>
        {__STUDENT_MODEL__?.repo && (
          <p>
            The model is{" "}
            <a href={`https://huggingface.co/${__STUDENT_MODEL__.repo}`}>{__STUDENT_MODEL__.repo}</a>, fine-tuned from
            DeBERTa-v3-small (Microsoft, MIT) on synthetic data including{" "}
            <a href="https://huggingface.co/datasets/nvidia/Nemotron-PII">Nemotron-PII</a> (NVIDIA, CC BY 4.0) and{" "}
            <a href="https://huggingface.co/datasets/gretelai/gretel-pii-masking-en-v1">gretel-pii-masking-en-v1</a>{" "}
            (Gretel, Apache-2.0).
          </p>
        )}
      </footer>
    </>
  );
}
