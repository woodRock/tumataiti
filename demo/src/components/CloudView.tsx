import { useEffect, useState } from "react";
import { DETECTORS, hue } from "../labels";
import type { Finding, Redaction } from "../redactor";

const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

interface MarkProps {
  finding: Finding;
  delayMs: number;
}

/** One redaction: highlight, a black bar sweeps across, then the replacement pops in. */
function RedactionMark({ finding, delayMs }: MarkProps) {
  const [animate] = useState(() => !reducedMotion());
  const [swept, setSwept] = useState(!animate);
  // Fallback in case animationend never fires (e.g. a throttled background tab),
  // so the original text is never left showing in the outbound view.
  useEffect(() => {
    if (swept) return;
    const t = setTimeout(() => setSwept(true), delayMs + 1200);
    return () => clearTimeout(t);
  }, [swept, delayMs]);
  const style = { ...hue(finding.category), "--delay": `${delayMs}ms` } as React.CSSProperties;
  const label = DETECTORS[finding.detector] ?? finding.detector;

  if (!swept) {
    return (
      <span className="rd rd-sweep" style={style}>
        {finding.text}
        <span className="rd-bar" onAnimationEnd={() => setSwept(true)} />
      </span>
    );
  }
  return (
    <span className={`rd rd-${finding.action}${animate ? " rd-pop" : ""}`} style={style} title={label}>
      {finding.replacement}
    </span>
  );
}

interface Props {
  text: string;
  redaction: Redaction;
  /** Changes on preset load and replay, re-running every animation with a stagger. */
  run: number;
  stagger: boolean;
}

export function CloudView({ text, redaction, run, stagger }: Props) {
  if (redaction.blocked) {
    const reasons = redaction.findings.filter((f) => f.action === "block");
    return (
      <div className="blocked" key={`blocked-${run}`}>
        <div className="blocked-icon" aria-hidden="true">⊘</div>
        <p className="blocked-title">Nothing would be sent.</p>
        <p>The request is blocked because it contains:</p>
        <ul className="blocked-reasons">
          {reasons.map((f, i) => (
            <li key={i} style={hue(f.category)}>
              {DETECTORS[f.detector] ?? f.detector}
            </li>
          ))}
        </ul>
        <p>Remove these and try again.</p>
      </div>
    );
  }

  // Keys follow the entity, not its offset, so earlier edits don't replay later marks.
  const seen = new Map<string, number>();
  const parts: React.ReactNode[] = [];
  let cursor = 0;
  let animated = 0;
  for (const f of redaction.findings) {
    parts.push(text.slice(cursor, f.start));
    cursor = f.end;
    const id = `${f.text}|${f.replacement}|${f.action}`;
    const nth = (seen.get(id) ?? 0) + 1;
    seen.set(id, nth);
    const key = `${run}|${id}|${nth}`;

    if (f.replacement !== null) {
      const delay = stagger ? Math.min(animated++, 10) * 110 : 0;
      parts.push(<RedactionMark key={key} finding={f} delayMs={delay} />);
    } else if (f.action === "flag") {
      parts.push(
        <span key={key} className="rd-flag" style={hue(f.category)} title="Sent as-is. Needs review.">
          {f.text}
        </span>,
      );
    } else {
      parts.push(f.text);
    }
  }
  parts.push(text.slice(cursor));

  return <div className="cloud-text">{parts}</div>;
}
