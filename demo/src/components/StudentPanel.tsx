import type { StudentModel } from "../student";

/** The bundled model's manifest, or null for a rules-only build (vite.config.ts). */
const MODEL_SHIPPED = __STUDENT_MODEL__;

export type StudentState =
  | { status: "off" }
  | { status: "loading"; progress: number }
  | { status: "ready"; model: StudentModel }
  | { status: "error"; message: string };

const mb = (bytes: number) => `${Math.round(bytes / 1e6)} MB`;

/** Opt-in switch for the student model, with download progress. */
export function StudentPanel({ state, onChange }: { state: StudentState; onChange(s: StudentState): void }) {
  if (!MODEL_SHIPPED) {
    return (
      <p className="student muted small">
        This build runs the rules only, so names and addresses are not detected. The name model is not published yet.
      </p>
    );
  }

  const start = async () => {
    onChange({ status: "loading", progress: 0 });
    try {
      const { loadStudent } = await import("../student");
      const model = await loadStudent((progress) => onChange({ status: "loading", progress }));
      onChange({ status: "ready", model });
    } catch (err) {
      console.error(err);
      onChange({ status: "error", message: "The model could not load in this browser." });
    }
  };

  switch (state.status) {
    case "off":
      return (
        <div className="student">
          <button type="button" className="chip chip-on" onClick={start}>
            Add the name model
          </button>
          <span className="muted small">
            Finds names, addresses and iwi. Downloads {mb(MODEL_SHIPPED.bytes)} from this site once, then runs on this
            device. Your text is never uploaded.
          </span>
        </div>
      );
    case "loading":
      return (
        <div className="student" role="status">
          <progress value={state.progress} max={1} aria-label="Model download" />
          <span className="muted small">
            Downloading the model: {mb(state.progress * MODEL_SHIPPED.bytes)} of {mb(MODEL_SHIPPED.bytes)}
          </span>
        </div>
      );
    case "ready":
      return (
        <p className="student student-ready small" role="status">
          <span className="student-on" aria-hidden="true" /> Model on: {state.model.info.name} (
          {state.model.info.precision}), running on this device.
        </p>
      );
    case "error":
      return (
        <div className="student">
          <span className="small">{state.message} Redaction continues with the rules only.</span>
          <button type="button" className="ghost" onClick={start}>
            Try again
          </button>
        </div>
      );
  }
}
