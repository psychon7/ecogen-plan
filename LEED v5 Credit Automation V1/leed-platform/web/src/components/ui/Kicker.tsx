import * as React from "react";
import { Leaf } from "lucide-react";
import { cn } from "@/lib/cn";

interface KickerProps extends React.HTMLAttributes<HTMLSpanElement> {
  icon?: React.ReactNode | false;
  tone?: "mint" | "glass";
}

/**
 * Soft botanical eyebrow tag.
 * Sentence case, subtle contrast, never aggressive all-caps tech.
 */
export function Kicker({
  icon,
  tone = "mint",
  className,
  children,
  ...rest
}: KickerProps) {
  const fill =
    tone === "mint"
      ? "bg-mint text-forest"
      : "eg-glass-pill text-forest";

  const renderedIcon =
    icon === false ? null : icon ?? (
      <Leaf className="h-3.5 w-3.5 text-primary" strokeWidth={2} />
    );

  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full border border-[rgba(15,61,35,0.08)] px-3 py-1 text-[13px] font-semibold leading-none",
        fill,
        className
      )}
      {...rest}
    >
      {renderedIcon}
      <span>{children}</span>
    </span>
  );
}
