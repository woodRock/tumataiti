import { ACTIONS, CATEGORIES, hue } from "../labels";
import type { Action, Category, Policy } from "../redactor";

interface Props {
  policy: Policy;
  onChange(policy: Policy): void;
  onReset(): void;
}

const ORDER = Object.keys(CATEGORIES) as Category[];

export function PolicyPanel({ policy, onChange, onReset }: Props) {
  const setAction = (category: Category, action: Action) =>
    onChange({ ...policy, actions: { ...policy.actions, [category]: action } });

  return (
    <div className="policy">
      <label className="threshold">
        <span>
          Confidence threshold <output>{Math.round(policy.threshold * 100)}%</output>
        </span>
        <input
          type="range"
          min={0}
          max={1}
          step={0.05}
          value={policy.threshold}
          onChange={(e) => onChange({ ...policy, threshold: Number(e.target.value) })}
        />
        <span className="muted small">Anything less certain than this is flagged for review, not redacted.</span>
      </label>

      <ul className="policy-list">
        {ORDER.map((c) => (
          <li key={c} style={hue(c)} className={CATEGORIES[c].rules ? "" : "policy-later"}>
            <span className="swatch" aria-hidden="true" />
            <label htmlFor={`policy-${c}`}>{CATEGORIES[c].label}</label>
            {CATEGORIES[c].rules ? (
              <select
                id={`policy-${c}`}
                value={policy.actions[c]}
                title={ACTIONS[policy.actions[c]].hint}
                onChange={(e) => setAction(c, e.target.value as Action)}
              >
                {(Object.keys(ACTIONS) as Action[]).map((a) => (
                  <option key={a} value={a}>
                    {ACTIONS[a].label}
                  </option>
                ))}
              </select>
            ) : (
              <span className="muted small" id={`policy-${c}`}>
                needs the model
              </span>
            )}
          </li>
        ))}
      </ul>
      <button type="button" className="link" onClick={onReset}>
        Reset to defaults
      </button>
    </div>
  );
}
