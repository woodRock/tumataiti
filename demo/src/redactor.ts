import init, { defaultPolicy, redact } from "./wasm/tumataiti_wasm.js";

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
  redact(text: string, policy: Policy): Redaction;
  defaultPolicy: Policy;
}

/** Load the WebAssembly rules. This is the only network request the redactor makes. */
export async function loadRedactor(): Promise<Redactor> {
  await init();
  return {
    redact: (text, policy) => JSON.parse(redact(text, JSON.stringify(policy))),
    defaultPolicy: JSON.parse(defaultPolicy()),
  };
}
