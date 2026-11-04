import init, { defaultPolicy, redact, redactWith } from "./wasm/tumataiti_wasm.js";
import type { ModelSpan } from "./student";

export type Category =
  | "PERSON"
  | "ADDRESS"
  | "EMAIL"
  | "PHONE"
  | "URL"
  | "IP_ADDRESS"
  | "DATE"
  | "NZ_GOV_ID"
  | "FINANCIAL"
  | "SECRET"
  | "AFFILIATION"
  | "HEALTH"
  | "CULTURAL_RESTRICTED";

export type Action = "allow" | "flag" | "pseudonymise" | "generalise" | "mask" | "block";

export interface Finding {
  /** UTF-16 offsets into the input string. */
  start: number;
  end: number;
  text: string;
  category: Category;
  confidence: number;
  source: "rule" | "model" | "gazetteer";
  detector: string;
  checksum: "valid" | "invalid" | "none";
  note?: string;
  action: Action;
  replacement: string | null;
}

export interface Redaction {
  output: string;
  findings: Finding[];
  blocked: boolean;
}

export interface Policy {
  actions: Record<Category, Action>;
  threshold: number;
}

export interface Redactor {
  /** Rules only, or rules merged with the student model's spans for `text`. */
  redact(text: string, policy: Policy, model?: ModelSpan[]): Redaction;
  defaultPolicy: Policy;
}

/** Load the WebAssembly rules. The student model is loaded separately, on request (student.ts). */
export async function loadRedactor(): Promise<Redactor> {
  await init();
  return {
    redact: (text, policy, model) =>
      JSON.parse(
        model
          ? redactWith(text, JSON.stringify(policy), JSON.stringify(model), "student")
          : redact(text, JSON.stringify(policy)),
      ),
    defaultPolicy: JSON.parse(defaultPolicy()),
  };
}
