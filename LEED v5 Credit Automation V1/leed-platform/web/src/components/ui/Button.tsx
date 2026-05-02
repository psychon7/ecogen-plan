"use client";

import * as React from "react";
import Link from "next/link";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { cn } from "@/lib/cn";

type Variant = "primary" | "secondary" | "ghost";

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  href?: string;
  icon?: "right" | "up-right" | "none";
  size?: "md" | "lg";
}

/**
 * EcoGen liquid-glass CTA.
 *  - primary    : forest-green capsule with nested arrow circle (Book a demo)
 *  - secondary  : frosted glass capsule with sage hover (Explore credits)
 *  - ghost      : underline-less text link with arrow shift on hover
 */
export function Button({
  variant = "primary",
  href,
  icon = "right",
  size = "md",
  className,
  children,
  ...props
}: Props) {
  const base = cn(
    "group relative inline-flex items-center gap-3 rounded-full font-semibold tracking-[0.005em]",
    "select-none whitespace-nowrap",
    size === "lg" ? "min-h-[52px] px-6 py-3.5 text-[15px]" : "min-h-[44px] px-5 py-3 text-sm"
  );

  const styles = {
    primary: cn(
      "eg-btn-primary bg-primary text-[#FFFFFC]",
      "shadow-[inset_0_1px_0_rgba(255,255,255,0.35),0_8px_24px_rgba(15,61,35,0.18)]"
    ),
    secondary: cn(
      "eg-btn-secondary eg-glass-pill text-forest"
    ),
    ghost: cn(
      "text-forest/85 hover:text-forest transition-colors px-1.5 py-1.5"
    ),
  }[variant];

  const Arrow = icon === "up-right" ? ArrowUpRight : ArrowRight;
  const renderArrow = icon !== "none";

  const innerCircle = renderArrow && variant !== "ghost" ? (
    <span
      aria-hidden
      className={cn(
        "grid h-7 w-7 place-items-center rounded-full transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)]",
        "group-hover:translate-x-0.5 group-hover:-translate-y-[1px] group-hover:scale-[1.04]",
        variant === "primary"
          ? "bg-[rgba(255,255,255,0.18)] ring-1 ring-inset ring-white/20"
          : "bg-mint ring-1 ring-inset ring-[rgba(15,61,35,0.06)]"
      )}
    >
      <Arrow className="h-3.5 w-3.5" strokeWidth={2} />
    </span>
  ) : null;

  const ghostArrow = renderArrow && variant === "ghost" ? (
    <Arrow
      aria-hidden
      className="h-4 w-4 transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] group-hover:translate-x-1"
      strokeWidth={2}
    />
  ) : null;

  const content = (
    <span className={cn(base, styles, className)}>
      <span>{children}</span>
      {innerCircle}
      {ghostArrow}
    </span>
  );

  if (href) {
    const isExternal = href.startsWith("http");
    if (isExternal) {
      return (
        <a href={href} target="_blank" rel="noopener noreferrer">
          {content}
        </a>
      );
    }
    return <Link href={href}>{content}</Link>;
  }

  return (
    <button {...props} className={cn("contents")}>
      {content}
    </button>
  );
}
