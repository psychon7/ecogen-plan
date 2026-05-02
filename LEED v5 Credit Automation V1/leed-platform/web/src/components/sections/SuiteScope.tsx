"use client";

import * as React from "react";
import Image from "next/image";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import {
  ArrowRight,
  ArrowUpRight,
  Droplets,
  Snowflake,
  ClipboardCheck,
  Workflow,
  Leaf,
} from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/cn";

type Suite = {
  name: string;
  credits: string;
  icon: React.ElementType;
  body: string;
  detail: string;
  cta: string;
  href: string;
  asset: string;
};

const SUITES: Suite[] = [
  {
    name: "Water Efficiency",
    credits: "WEp2 + WEc2",
    icon: Droplets,
    body: "Indoor and outdoor water use reduction evidence workflows.",
    detail:
      "Prepare fixture schedules, baseline calculations, reduction analysis, and optimization summaries with transparent formula trails. EcoGen validates inputs, runs WEp2 baseline and WEc2 proposed-use calculations, flags missing assumptions, and assembles a reviewer-ready evidence pack.",
    cta: "View Water Efficiency workflow",
    href: "/solutions/leed-v5-water-efficiency",
    asset: "/assets/visuals/02a-suite-water-efficiency.png",
  },
  {
    name: "Refrigerant Management",
    credits: "EAp5 + EAc7",
    icon: Snowflake,
    body: "Refrigerant tracking, leak detection records, and reporting.",
    detail:
      "Parse equipment schedules, validate refrigerant identities against SNAP and AHRI references, flag high-GWP risk, calculate weighted impact, and prepare reviewer-ready refrigerant evidence with full source trails.",
    cta: "View refrigerant workflow",
    href: "/solutions/leed-v5-refrigerant-management",
    asset: "/assets/visuals/02b-suite-refrigerant-management.png",
  },
  {
    name: "Quality Plans",
    credits: "EQp1 + EQp2",
    icon: ClipboardCheck,
    body: "Construction and IAQ management plans and verification.",
    detail:
      "Draft management plans, checklist workflows, ventilation-supporting evidence, and review tasks. Structured templates ensure EQp1 and EQp2 documentation meets LEED v5 requirements with clear assignee tracking.",
    cta: "View quality plan workflow",
    href: "#",
    asset: "/assets/visuals/02c-suite-quality-plans.png",
  },
  {
    name: "Integrative Process",
    credits: "IPp1 + IPp2",
    icon: Workflow,
    body: "Early collaboration and performance analysis documentation.",
    detail:
      "Collect public-source research, organize climate and human-impact evidence, draft narratives from structured prompts, and route outputs for expert validation before the integrative process assessment is finalized.",
    cta: "View integrative workflow",
    href: "#",
    asset: "/assets/visuals/02d-suite-integrative-process.png",
  },
  {
    name: "Low-Emitting Materials",
    credits: "MRc3",
    icon: Leaf,
    body: "Material disclosure and low-emitting product evidence.",
    detail:
      "Screen product evidence against GREENGUARD, FloorScore, and VOC thresholds. Organize certifications, flag stale or missing certificates, surface exceptions, and prepare low-emitting material documentation for review.",
    cta: "View materials workflow",
    href: "/solutions/leed-v5-low-emitting-materials",
    asset: "/assets/visuals/02e-suite-low-emitting-materials.png",
  },
];

/**
 * Scroll-triggered suite showcase.
 * Left rail: suite list with active highlight.
 * Right: large glass card with crossfading image + detail.
 * On mobile: stacked cards.
 */
export function SuiteScope() {
  const [active, setActive] = React.useState(0);
  const sectionRef = React.useRef<HTMLDivElement>(null);
  const triggerRefs = React.useRef<(HTMLDivElement | null)[]>([]);
  const reduce = useReducedMotion();

  /* IntersectionObserver — each scroll-trigger sets active index */
  React.useEffect(() => {
    const observers: IntersectionObserver[] = [];
    triggerRefs.current.forEach((el, i) => {
      if (!el) return;
      const obs = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) setActive(i);
        },
        { rootMargin: "-40% 0px -40% 0px", threshold: 0 }
      );
      obs.observe(el);
      observers.push(obs);
    });
    return () => observers.forEach((o) => o.disconnect());
  }, []);

  const current = SUITES[active];
  const Icon = current.icon;

  return (
    <section id="suites" className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        {/* Header */}
        <Reveal>
          <h2 className="text-[clamp(28px,4vw,40px)] font-semibold leading-[1.1] tracking-[-0.025em] text-forest">
            Automate the credits that are ready for automation.
          </h2>
        </Reveal>
        <Reveal delay={0.05}>
          <p className="mt-3 max-w-[64ch] text-[15px] leading-[1.55] text-forest/65">
            We start with the high-confidence LEED v5 suites most ready for
            AI-assisted workflows.
          </p>
        </Reveal>

        {/* ──────── Desktop: scroll-triggered sticky showcase ──────── */}
        <div
          ref={sectionRef}
          className="mt-14 hidden lg:grid lg:grid-cols-12 lg:gap-10"
        >
          {/* Left rail — scroll triggers */}
          <div className="col-span-5">
            <div className="space-y-2">
              {SUITES.map((s, i) => {
                const SIcon = s.icon;
                const isActive = active === i;
                return (
                  <div
                    key={s.name}
                    ref={(el) => { triggerRefs.current[i] = el; }}
                    className="min-h-[180px]"
                  >
                    <button
                      type="button"
                      onClick={() => setActive(i)}
                      className={cn(
                        "group w-full rounded-2xl p-5 text-left transition-all duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]",
                        isActive
                          ? "eg-glass-strong shadow-[0_12px_40px_-18px_rgba(15,61,35,0.28)]"
                          : "hover:bg-mint/30"
                      )}
                    >
                      <div className="flex items-center gap-3">
                        <span
                          className={cn(
                            "grid h-10 w-10 shrink-0 place-items-center rounded-full transition-colors duration-500",
                            isActive ? "eg-icon-well" : "bg-mist"
                          )}
                        >
                          <SIcon
                            className={cn(
                              "h-4.5 w-4.5 transition-colors duration-500",
                              isActive ? "text-forest" : "text-forest/50"
                            )}
                            strokeWidth={1.75}
                          />
                        </span>
                        <div>
                          <h3
                            className={cn(
                              "text-[16px] font-semibold leading-snug transition-colors duration-300",
                              isActive ? "text-forest" : "text-forest/55"
                            )}
                          >
                            {s.name}
                          </h3>
                          <p
                            className={cn(
                              "mt-0.5 text-[12px] font-semibold tracking-[0.02em] transition-colors duration-300",
                              isActive ? "text-primary" : "text-primary/40"
                            )}
                          >
                            {s.credits}
                          </p>
                        </div>
                      </div>
                      <p
                        className={cn(
                          "mt-3 max-w-[38ch] text-[13.5px] leading-[1.55] transition-colors duration-300",
                          isActive ? "text-forest/70" : "text-forest/40"
                        )}
                      >
                        {s.body}
                      </p>
                    </button>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right — sticky large glass card */}
          <div className="col-span-7">
            <div className="sticky top-32">
              <div
                className={cn(
                  "rounded-[28px] p-2",
                  "ring-1 ring-[rgba(15,61,35,0.06)] bg-[rgba(255,255,252,0.5)]",
                  "shadow-[0_24px_64px_-28px_rgba(15,61,35,0.32)]"
                )}
              >
                <div className="eg-glass-strong overflow-hidden rounded-[22px]">
                  {/* Image area — white bg, large */}
                  <div className="relative flex items-center justify-center bg-white px-8 py-10">
                    <AnimatePresence mode="wait">
                      <motion.div
                        key={active}
                        initial={reduce ? false : { opacity: 0, scale: 0.96, filter: "blur(8px)" }}
                        animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
                        exit={{ opacity: 0, scale: 0.96, filter: "blur(8px)" }}
                        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                        className="flex items-center justify-center"
                      >
                        <Image
                          src={current.asset}
                          width={800}
                          height={560}
                          alt={`${current.name} isometric illustration`}
                          className="h-[340px] w-auto select-none object-contain"
                          priority
                        />
                      </motion.div>
                    </AnimatePresence>
                  </div>

                  {/* Detail strip */}
                  <div className="border-t border-[rgba(15,61,35,0.08)] p-7">
                    <AnimatePresence mode="wait">
                      <motion.div
                        key={active}
                        initial={reduce ? false : { opacity: 0, y: 12 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -8 }}
                        transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                      >
                        <div className="flex items-center gap-3">
                          <span className="grid h-11 w-11 place-items-center rounded-full eg-icon-well">
                            <Icon className="h-5 w-5 text-forest" strokeWidth={1.75} />
                          </span>
                          <div>
                            <h3 className="text-[20px] font-semibold leading-tight text-forest">
                              {current.name}
                            </h3>
                            <p className="mt-0.5 text-[13px] font-semibold tracking-[0.02em] text-primary">
                              {current.credits}
                            </p>
                          </div>
                        </div>
                        <p className="mt-4 max-w-[56ch] text-[14.5px] leading-[1.6] text-forest/72">
                          {current.detail}
                        </p>
                        <a
                          href={current.href}
                          className="group mt-5 inline-flex items-center gap-2 text-[14px] font-semibold text-primary transition-colors hover:text-forest"
                        >
                          {current.cta}
                          <ArrowUpRight className="h-4 w-4 transition-transform duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] group-hover:translate-x-0.5 group-hover:-translate-y-[1px]" strokeWidth={2} />
                        </a>
                      </motion.div>
                    </AnimatePresence>
                  </div>
                </div>
              </div>

              {/* Progress dots */}
              <div className="mt-5 flex items-center justify-center gap-2">
                {SUITES.map((_, i) => (
                  <button
                    key={i}
                    aria-label={`Go to ${SUITES[i].name}`}
                    onClick={() => setActive(i)}
                    className={cn(
                      "h-2 rounded-full transition-all duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]",
                      active === i
                        ? "w-8 bg-primary"
                        : "w-2 bg-forest/15 hover:bg-forest/30"
                    )}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* ──────── Mobile: stacked full-width cards ──────── */}
        <div className="mt-10 space-y-4 lg:hidden">
          {SUITES.map((s, i) => {
            const SIcon = s.icon;
            return (
              <Reveal key={s.name} delay={0.04 * i}>
                <a
                  href={s.href}
                  className={cn(
                    "eg-card-hover group block rounded-[24px]",
                    "p-1.5 ring-1 ring-[rgba(15,61,35,0.06)] bg-[rgba(255,255,252,0.55)]",
                    "shadow-[0_12px_40px_-20px_rgba(15,61,35,0.24)]"
                  )}
                >
                  <div className="eg-glass-strong overflow-hidden rounded-[20px]">
                    <div className="flex items-center justify-center bg-white px-6 py-8">
                      <Image
                        src={s.asset}
                        width={600}
                        height={400}
                        alt={`${s.name} isometric illustration`}
                        className="h-[200px] w-auto select-none object-contain sm:h-[260px]"
                      />
                    </div>
                    <div className="border-t border-[rgba(15,61,35,0.08)] p-5">
                      <div className="flex items-center gap-3">
                        <span className="grid h-10 w-10 place-items-center rounded-full eg-icon-well">
                          <SIcon className="h-4.5 w-4.5 text-forest" strokeWidth={1.75} />
                        </span>
                        <div>
                          <h3 className="text-[17px] font-semibold text-forest">{s.name}</h3>
                          <p className="text-[12px] font-semibold tracking-[0.02em] text-primary">
                            {s.credits}
                          </p>
                        </div>
                      </div>
                      <p className="mt-3 text-[14px] leading-[1.55] text-forest/70">
                        {s.detail}
                      </p>
                      <div className="mt-4 flex items-center gap-1.5 text-[13px] font-semibold text-primary">
                        {s.cta}
                        <ArrowRight className="h-3.5 w-3.5 transition-transform group-hover:translate-x-1" strokeWidth={2} />
                      </div>
                    </div>
                  </div>
                </a>
              </Reveal>
            );
          })}
        </div>

        {/* Footer */}
        <div className="mt-10 flex flex-col items-start justify-between gap-6 border-t border-[rgba(15,61,35,0.08)] pt-8 md:flex-row md:items-center">
          <p className="max-w-[58ch] text-[13px] leading-[1.55] text-forest/55">
            Scope notes: Credit support varies by rating system, region, version,
            and source availability. See platform for details.
          </p>
          <Button href="#demo">Book a demo</Button>
        </div>
      </div>
    </section>
  );
}
