import type { CSSProperties } from "react";
import type { Action, Category } from "./redactor";

export interface CategoryInfo {
  label: string;
  /** OKLCH hue; lightness and chroma come from the theme. */
  hue: number;
  /** False for categories that need the model (M3). */
  rules: boolean;
  /** True for categories the current student model detects. */
  model?: boolean;
}

export const CATEGORIES: Record<Category, CategoryInfo> = {
  NZ_GOV_ID: { label: "NZ government ID", hue: 25, rules: true },
  FINANCIAL: { label: "Card or bank account", hue: 335, rules: true },
  OTHER_ID: { label: "Other ID", hue: 10, rules: false, model: true },
  SECRET: { label: "Password or API key", hue: 55, rules: true },
  EMAIL: { label: "Email", hue: 255, rules: true },
  PHONE: { label: "Phone", hue: 175, rules: true },
  URL: { label: "Web link", hue: 295, rules: true },
  IP_ADDRESS: { label: "IP address", hue: 215, rules: true },
  DATE: { label: "Birth or death date", hue: 90, rules: true },
  PERSON: { label: "Name", hue: 145, rules: false, model: true },
  ADDRESS: { label: "Address", hue: 120, rules: false, model: true },
  AFFILIATION: { label: "Iwi, hapū, marae", hue: 70, rules: false, model: true },
  HEALTH: { label: "Health", hue: 0, rules: false },
  CULTURAL_RESTRICTED: { label: "Restricted mātauranga", hue: 40, rules: false },
};

export const DETECTORS: Record<string, string> = {
  nz_ird: "IRD number",
  nz_nhi: "NHI number",
  nz_passport: "Passport number",
  nz_driver_licence: "Driver licence",
  nz_id_format: "ID-shaped code",
  payment_card: "Payment card",
  nz_bank_account: "Bank account",
  email: "Email address",
  url: "Web link",
  ipv4: "IPv4 address",
  nz_phone: "NZ phone number",
  date_of_birth: "Date of birth or death",
  anthropic_api_key: "Anthropic API key",
  openai_api_key: "OpenAI API key",
  github_token: "GitHub token",
  aws_access_key: "AWS access key",
  slack_token: "Slack token",
  google_api_key: "Google API key",
  private_key: "Private key",
  secret_assignment: "Password or secret value",
  student: "Tūmataiti model",
};

export const ACTIONS: Record<Action, { label: string; hint: string }> = {
  pseudonymise: { label: "Placeholder", hint: "Swap for [EMAIL_1]; restored in the reply" },
  generalise: { label: "Generalise", hint: "Keep a coarser value, e.g. only the year" },
  mask: { label: "Mask", hint: "Replace with the category; never restored" },
  block: { label: "Block", hint: "Refuse to send the request at all" },
  flag: { label: "Flag", hint: "Send as-is, but mark for review" },
  allow: { label: "Allow", hint: "Send as-is" },
};

/** Inline style that sets the category hue; CSS derives the colours from `--h`. */
export const hue = (category: Category) => ({ "--h": CATEGORIES[category].hue }) as CSSProperties;
