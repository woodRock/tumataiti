import { useEffect, useState } from "react";

/**
 * Counts network requests the page makes after the redactor (and the model,
 * once loaded) has loaded, using the browser's own Resource Timing records. It
 * should stay at zero. The count restarts when `since` changes.
 */
export function NetworkMeter({ since: label }: { since: string }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    setCount(0);
    const since = performance.now();
    const observer = new PerformanceObserver((list) => {
      const fresh = list.getEntries().filter((e) => e.startTime >= since).length;
      if (fresh) setCount((n) => n + fresh);
    });
    observer.observe({ type: "resource", buffered: false });
    return () => observer.disconnect();
  }, [label]);

  return (
    <div className={count === 0 ? "net net-ok" : "net net-warn"} role="status">
      <span className="net-dot" aria-hidden="true" />
      <span>
        <strong>{count}</strong> network {count === 1 ? "request" : "requests"} since {label}
      </span>
    </div>
  );
}
