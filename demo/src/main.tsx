import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { loadRedactor } from "./redactor";
import "./styles.css";

const root = createRoot(document.getElementById("root")!);

loadRedactor().then(
  (redactor) =>
    root.render(
      <StrictMode>
        <App redactor={redactor} />
      </StrictMode>,
    ),
  (err: unknown) => {
    console.error(err);
    root.render(<p className="load-error">The redactor could not load in this browser.</p>);
  },
);
