import { useEffect } from "react";

export function DynamicBackdrop() {
  useEffect(() => {
    const root = document.documentElement;
    const handleMove = (event: PointerEvent) => {
      root.style.setProperty("--cursor-x", `${event.clientX}px`);
      root.style.setProperty("--cursor-y", `${event.clientY}px`);
    };

    window.addEventListener("pointermove", handleMove, { passive: true });
    return () => window.removeEventListener("pointermove", handleMove);
  }, []);

  return (
    <div className="dynamic-backdrop" aria-hidden="true">
      <span className="aurora aurora-a" />
      <span className="aurora aurora-b" />
      <span className="aurora aurora-c" />
      <span className="neural-node node-a" />
      <span className="neural-node node-b" />
      <span className="neural-node node-c" />
      <span className="neural-node node-d" />
    </div>
  );
}
