"use client";

import * as React from "react";
import Link from "next/link";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import { ChevronDown, Globe2 } from "lucide-react";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/cn";

const NAV_ITEMS: { label: string; href: string }[] = [
  { label: "Platform", href: "#platform" },
  { label: "Solutions", href: "#solutions" },
  { label: "Certifications", href: "#certifications" },
  { label: "Resources", href: "#resources" },
  { label: "About", href: "#about" },
];

/**
 * Floating glass-pill nav with fluid-island hamburger -> X morph
 * and full-screen staggered mask reveal on mobile.
 */
export function Nav() {
  const [open, setOpen] = React.useState(false);
  const [scrolled, setScrolled] = React.useState(false);
  const reduce = useReducedMotion();

  React.useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  React.useEffect(() => {
    document.documentElement.style.overflow = open ? "hidden" : "";
    return () => {
      document.documentElement.style.overflow = "";
    };
  }, [open]);

  return (
    <>
      <header
        className={cn(
          "fixed inset-x-0 top-0 z-50 flex justify-center px-4 pt-4 md:pt-6",
          "transition-[transform,opacity] duration-500"
        )}
      >
        <div
          className={cn(
            "eg-glass-pill flex w-full max-w-[1180px] items-center justify-between gap-4",
            "rounded-full px-3 py-2 md:px-4 md:py-2.5",
            scrolled && "shadow-[inset_0_1px_0_rgba(255,255,255,0.78),0_18px_40px_-18px_rgba(15,61,35,0.28)]"
          )}
        >
          <Link href="/" aria-label="EcoGen home" className="pl-2">
            <Logo />
          </Link>

          <nav className="hidden items-center gap-1 lg:flex" aria-label="Primary">
            {NAV_ITEMS.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className={cn(
                  "group inline-flex items-center gap-1 rounded-full px-3.5 py-2 text-[14px] font-medium",
                  "text-forest/80 transition-colors hover:text-forest hover:bg-mint/60"
                )}
              >
                {item.label}
                {item.label === "Solutions" || item.label === "Resources" ? (
                  <ChevronDown
                    className="h-3.5 w-3.5 opacity-60 transition-transform group-hover:translate-y-px"
                    strokeWidth={2}
                  />
                ) : null}
              </a>
            ))}
          </nav>

          <div className="hidden items-center gap-2 lg:flex">
            <button
              type="button"
              className="inline-flex items-center gap-1.5 rounded-full px-3 py-2 text-[13px] font-medium text-forest/70 transition-colors hover:text-forest"
              aria-label="Language selector"
            >
              <Globe2 className="h-4 w-4" strokeWidth={2} />
              EN
            </button>
            <a
              href="#login"
              className="rounded-full px-3.5 py-2 text-[14px] font-medium text-forest/80 transition-colors hover:text-forest"
            >
              Log in
            </a>
            <Button href="#demo" size="md">
              Book a demo
            </Button>
          </div>

          {/* Mobile cluster */}
          <div className="flex items-center gap-2 lg:hidden">
            <Button href="#demo" size="md" className="hidden sm:inline-flex">
              Book a demo
            </Button>
            <button
              aria-label={open ? "Close menu" : "Open menu"}
              aria-expanded={open}
              onClick={() => setOpen((v) => !v)}
              className={cn(
                "relative grid h-11 w-11 place-items-center rounded-full eg-glass-pill",
                "transition-transform duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]"
              )}
            >
              <span className="relative block h-3.5 w-5">
                <span
                  className={cn(
                    "absolute left-0 top-0 h-[1.6px] w-full rounded-full bg-forest transition-transform duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]",
                    open && "translate-y-[7px] rotate-45"
                  )}
                />
                <span
                  className={cn(
                    "absolute bottom-0 left-0 h-[1.6px] w-full rounded-full bg-forest transition-transform duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]",
                    open && "-translate-y-[7px] -rotate-45"
                  )}
                />
              </span>
            </button>
          </div>
        </div>
      </header>

      {/* Mobile expanded modal */}
      <AnimatePresence>
        {open && (
          <motion.div
            key="nav-overlay"
            className="fixed inset-0 z-40 lg:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
          >
            <div
              className="absolute inset-0"
              style={{
                background:
                  "radial-gradient(60% 60% at 18% 12%, rgba(207,232,214,0.85), rgba(255,255,255,0.92) 60%), rgba(255,255,255,0.92)",
                backdropFilter: "blur(28px) saturate(140%)",
                WebkitBackdropFilter: "blur(28px) saturate(140%)",
              }}
            />
            <div className="relative flex h-full flex-col px-6 pt-28 pb-10">
              <ul className="flex flex-1 flex-col gap-1">
                {NAV_ITEMS.map((item, i) => (
                  <motion.li
                    key={item.href}
                    initial={{ opacity: 0, y: reduce ? 0 : 24 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                      duration: 0.5,
                      delay: 0.1 + i * 0.05,
                      ease: [0.16, 1, 0.3, 1],
                    }}
                  >
                    <a
                      href={item.href}
                      onClick={() => setOpen(false)}
                      className="block rounded-2xl px-4 py-4 text-[34px] font-semibold leading-tight tracking-[-0.02em] text-forest hover:bg-mint/60"
                    >
                      {item.label}
                    </a>
                  </motion.li>
                ))}
              </ul>
              <motion.div
                initial={{ opacity: 0, y: reduce ? 0 : 24 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.4, ease: [0.16, 1, 0.3, 1] }}
                className="flex items-center justify-between gap-3"
              >
                <a
                  href="#login"
                  className="rounded-full px-4 py-3 text-sm font-semibold text-forest/80"
                >
                  Log in
                </a>
                <Button href="#demo" size="lg" onClick={() => setOpen(false)}>
                  Book a demo
                </Button>
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
