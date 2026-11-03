import { useLayoutEffect, useRef } from "react";
import { hue } from "../labels";
import type { Finding } from "../redactor";

interface Props {
  value: string;
  findings: Finding[];
  onChange(value: string): void;
}

/**
 * A textarea over a mirror div. The mirror repeats the text with transparent
 * glyphs and coloured marks, so highlights sit exactly under the typed text.
 */
export function Editor({ value, findings, onChange }: Props) {
  const area = useRef<HTMLTextAreaElement>(null);

  useLayoutEffect(() => {
    const el = area.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${el.scrollHeight}px`;
  }, [value]);

  const parts: React.ReactNode[] = [];
  let cursor = 0;
  findings.forEach((f) => {
    parts.push(value.slice(cursor, f.start));
    const flagged = f.action === "flag" || f.action === "allow";
    parts.push(
      <mark key={`${f.start}:${f.end}:${f.category}`} className={flagged ? "hl hl-weak" : "hl"} style={hue(f.category)}>
        {value.slice(f.start, f.end)}
      </mark>,
    );
    cursor = f.end;
  });
  // Trailing newline needs a character after it to take up height.
  parts.push(value.slice(cursor) + " ");

  return (
    <div className="editor">
      <div className="editor-mirror" aria-hidden="true">
        {parts}
      </div>
      <textarea
        ref={area}
        className="editor-input"
        value={value}
        spellCheck={false}
        aria-label="Text to redact"
        placeholder="Type or paste something with an email, phone number, IRD number…"
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
