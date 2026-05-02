import Image from "next/image";
import {
  FileCheck2,
  ListChecks,
  Calculator,
  ShieldCheck,
  Gauge,
  ScanSearch,
  Link2,
  CheckCircle2,
} from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { Button } from "@/components/ui/Button";
import { GlassCard } from "@/components/ui/GlassCard";

const COMPONENTS = [
  { icon: FileCheck2, label: "Credit summary and rating-system metadata" },
  { icon: ListChecks, label: "Input inventory: uploads, APIs, manual fields, assumptions" },
  { icon: Link2, label: "Source index with locators, retrieval dates, versions, hashes" },
  { icon: ScanSearch, label: "Extracted data with field-level confidence" },
  { icon: Calculator, label: "Calculation workbook with formulas and intermediate values" },
  { icon: FileCheck2, label: "Generated narrative or compliance rationale" },
  { icon: ListChecks, label: "Requirement-to-evidence matrix" },
  { icon: Gauge, label: "Confidence tier with missing data and degradation reasons" },
  { icon: ShieldCheck, label: "Workflow, audit history, and named human review record" },
];

export function EvidencePack() {
  return (
    <section id="certifications" className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="grid grid-cols-12 gap-10 lg:gap-12">
          {/* Visual — 7 cols */}
          <div className="order-2 col-span-12 lg:order-1 lg:col-span-7">
            <Reveal>
              <GlassCard tone="strong" radius="hero" bezel padded={false}>
                <div className="relative">
                  <Image
                    src="/assets/visuals/04-evidence-pack-product-illustration.png"
                    width={1600}
                    height={1100}
                    alt="EcoGen evidence pack interface"
                    className="h-auto w-full select-none rounded-[26px]"
                  />
                  <span className="absolute right-5 top-5 inline-flex items-center gap-1.5 rounded-full eg-glass-pill px-3 py-1.5 text-[12px] font-semibold text-forest">
                    <CheckCircle2 className="h-3.5 w-3.5 text-primary" strokeWidth={2} />
                    Reviewer-ready
                  </span>
                </div>
              </GlassCard>
            </Reveal>
          </div>

          {/* Copy — 5 cols */}
          <div className="order-1 col-span-12 lg:order-2 lg:col-span-5 lg:pt-6">
            <Reveal>
              <Kicker>One traceable artifact</Kicker>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-5 text-[clamp(32px,4.6vw,46px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
                One evidence pack. Every source, formula, and approval.
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-5 max-w-[52ch] text-[15.5px] leading-[1.55] text-forest/72">
                Every supported workflow produces an evidence pack designed for serious
                review. Not just faster documents — every compliance claim is
                inspectable.
              </p>
            </Reveal>

            <Reveal delay={0.15}>
              <ul className="mt-8 space-y-2.5">
                {COMPONENTS.map((c) => {
                  const Icon = c.icon;
                  return (
                    <li
                      key={c.label}
                      className="flex items-start gap-3 rounded-2xl px-3 py-2.5 transition-colors hover:bg-mint/40"
                    >
                      <span className="mt-0.5 grid h-7 w-7 shrink-0 place-items-center rounded-full eg-mint-well">
                        <Icon className="h-3.5 w-3.5 text-forest" strokeWidth={2} />
                      </span>
                      <span className="text-[13.5px] leading-[1.5] text-forest/80">
                        {c.label}
                      </span>
                    </li>
                  );
                })}
              </ul>
            </Reveal>

            <Reveal delay={0.22}>
              <div className="mt-8">
                <Button href="#demo">See an evidence pack demo</Button>
              </div>
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}
