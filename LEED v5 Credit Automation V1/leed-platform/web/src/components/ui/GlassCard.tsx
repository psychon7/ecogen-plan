import * as React from "react";
import { cn } from "@/lib/cn";

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  tone?: "strong" | "soft";
  bezel?: boolean;
  radius?: "card" | "panel" | "hero";
  padded?: boolean;
}

/**
 * Liquid-glass surface with optional outer bezel ("Doppelrand" / nested architecture).
 * Use this for every elevated panel: hero scenes, feature cards, evidence pack surfaces.
 */
export function GlassCard({
  tone = "strong",
  bezel = false,
  radius = "card",
  padded = true,
  className,
  children,
  ...rest
}: GlassCardProps) {
  const radiusMap = {
    card: { outer: "rounded-[20px]", inner: "rounded-[16px]" },
    panel: { outer: "rounded-[28px]", inner: "rounded-[22px]" },
    hero: { outer: "rounded-[36px]", inner: "rounded-[30px]" },
  } as const;

  const r = radiusMap[radius];
  const surface = tone === "strong" ? "eg-glass-strong" : "eg-glass-soft";

  if (bezel) {
    return (
      <div
        className={cn(
          "p-1.5 ring-1 ring-[rgba(15,61,35,0.06)] bg-[rgba(255,255,252,0.55)]",
          r.outer,
          "shadow-[0_18px_60px_-30px_rgba(15,61,35,0.28)]",
          className
        )}
        {...rest}
      >
        <div className={cn(surface, r.inner, padded && "p-6")}>{children}</div>
      </div>
    );
  }

  return (
    <div className={cn(surface, r.outer, padded && "p-6", className)} {...rest}>
      {children}
    </div>
  );
}
