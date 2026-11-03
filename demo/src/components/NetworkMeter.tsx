import { useEffect, useState } from "react";

/**
 * Counts network requests the page makes after the redactor has loaded, using
 * the browser's own Resource Timing records. It should stay at zero.
 */
export function NetworkMeter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const since = performance.now();
    const observer = new PerformanceObserver((list) => {
      const fresh = list.getEntries().filter((e) => e.startTime >= since).length;
      if (fresh) setCount((n) => n + fresh);
    });
    observer.observe({ type: "resource", buffered: false });
    return () => observer.disconnect();
  }, []);

  return (
    <div className={count === 0 ? "net net-ok" : "net net-warn"} role="status">
      <span className="net-dot" aria-hidden="true" />
      <span>
        <strong>{count}</strong> network {count === 1 ? "request" : "requests"} since the redactor loaded
      </span>
    </div>
  );
}
