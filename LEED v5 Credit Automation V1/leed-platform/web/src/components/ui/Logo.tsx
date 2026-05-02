import * as React from "react";
import { cn } from "@/lib/cn";

/**
 * EcoGen leaf logo mark — coded SVG, no PNG dependency.
 */
export function Logo({
  className,
  withWordmark = true,
}: {
  className?: string;
  withWordmark?: boolean;
}) {
  return (
    <span className={cn("inline-flex items-center gap-2", className)} aria-label="EcoGen">
      <span className="grid h-9 w-9 place-items-center rounded-full eg-icon-well">
        <svg viewBox="0 0 24 24" className="h-5 w-5" aria-hidden>
          <path
            d="M20 4c-7 0-12 4-13 11-.3 2.3.4 4.3 2 5.5C10 17 13 14 19 12c-4 3-7 5-9 9 5 .5 9-2 10-7 .6-2.6.6-6 0-10z"
            fill="#1E7A3D"
            stroke="#0F3D23"
            strokeWidth="0.8"
            strokeLinejoin="round"
          />
        </svg>
      </span>
      {withWordmark && (
        <span className="text-[20px] font-semibold leading-none tracking-[-0.02em] text-forest">
          ecogen
        </span>
      )}
    </span>
  );
}
