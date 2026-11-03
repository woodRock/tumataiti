import { ACTIONS, CATEGORIES, DETECTORS, hue } from "../labels";
import type { Finding } from "../redactor";

const CHECKSUM = {
  valid: { mark: "✓", text: "Check digit valid" },
  invalid: { mark: "✗", text: "Check digit fails" },
  none: { mark: "–", text: "No check digit" },
} as const;

export function Findings({ findings }: { findings: Finding[] }) {
  if (findings.length === 0) {
    return <p className="muted empty">Nothing detected yet.</p>;
  }
  return (
    <div className="table-wrap">
      <table className="findings">
        <thead>
          <tr>
            <th>Found</th>
            <th>Detector</th>
            <th className="num">Confidence</th>
            <th>Check</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {findings.map((f, i) => (
            <tr key={i} style={hue(f.category)}>
              <td>
                <span className="swatch" aria-hidden="true" />
                <code className="found">{f.text}</code>
                {f.note && <div className="note">{f.note}</div>}
              </td>
              <td>
                {DETECTORS[f.detector] ?? f.detector}
                <div className="muted small">{CATEGORIES[f.category].label}</div>
              </td>
              <td className="num">
                <span className="meter" style={{ "--v": f.confidence } as React.CSSProperties} aria-hidden="true" />
                {Math.round(f.confidence * 100)}%
              </td>
              <td>
                <span className={`check check-${f.checksum}`} title={CHECKSUM[f.checksum].text}>
                  {CHECKSUM[f.checksum].mark}
                </span>
                <span className="sr-only">{CHECKSUM[f.checksum].text}</span>
              </td>
              <td>
                <span className={`pill pill-${f.action}`}>{ACTIONS[f.action].label}</span>
                {f.replacement && <code className="arrow">→ {f.replacement}</code>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
