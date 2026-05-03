import Image from "next/image";
import { Clock3, UserCheck, Link2, SearchCheck } from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { GlassCard } from "@/components/ui/GlassCard";

const METRICS = [
  {
    icon: Clock3,
    value: "60–80%",
    label: "Target reduction",
    body: "Water Efficiency documentation time, after source data is available.",
    suffix: "Target",
  },
  {
    icon: UserCheck,
    value: "100%",
    label: "Human approval",
    body: "Compliance-critical exports routed through named human approval.",
    suffix: "Policy",
  },
  {
    icon: Link2,
    value: "100%",
    label: "Source-linked claims",
    body: "Factual claims tied to an upload, API, static requirement source, or reviewer entry.",
    suffix: "Policy",
  },
  {
    icon: SearchCheck,
    value: "0",
    label: "Hidden gaps",
    body: "Regional source gaps, missing data, and manual-prep items surfaced before export.",
    suffix: "Standard",
  },
];

export function Readiness() {
  return (
    <section className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="grid grid-cols-12 gap-10 lg:gap-12">
          <div className="col-span-12 lg:col-span-5">
            <Reveal>
              <Kicker>Readiness, not vanity metrics</Kicker>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-5 text-[clamp(32px,4.6vw,46px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
                Track real certification readiness.
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-5 max-w-[44ch] text-[15.5px] leading-[1.55] text-forest/72">
                EcoGen helps teams report progress without pretending pursued points are
                awarded points. Stakeholders see the difference between draft, in review,
                internally approved, exported, submitted, and awarded work.
              </p>
            </Reveal>
            <Reveal delay={0.15}>
              <div className="mt-10 hidden lg:block">
                <Image
                  src="/assets/visuals/09-audit-approval-chain.png"
                  width={900}
                  height={700}
                  alt="Audit approval chain illustration"
                  className="h-auto w-full select-none"
                />
              </div>
            </Reveal>
          </div>

          <div className="col-span-12 lg:col-span-7">
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
              {METRICS.map((m, i) => {
                const Icon = m.icon;
                return (
                  <Reveal key={m.label} delay={0.05 * i}>
                    <GlassCard tone="strong" radius="panel" className="eg-card-hover h-full">
                      <div className="flex items-center justify-between">
                        <span className="grid h-11 w-11 place-items-center rounded-full eg-icon-well">
                          <Icon className="h-5 w-5 text-forest" strokeWidth={1.75} />
                        </span>
                        <span className="rounded-full border border-[rgba(15,61,35,0.08)] bg-mint px-2.5 py-0.5 text-[10.5px] font-semibold uppercase tracking-[0.14em] text-forest">
                          {m.suffix}
                        </span>
                      </div>
                      <p className="mt-6 text-[44px] font-semibold leading-none tracking-[-0.03em] text-primary">
                        {m.value}
                      </p>
                      <h3 className="mt-3 text-[15px] font-semibold text-forest">
                        {m.label}
                      </h3>
                      <p className="mt-2 max-w-[42ch] text-[13.5px] leading-[1.55] text-forest/68">
                        {m.body}
                      </p>
                    </GlassCard>
                  </Reveal>
                );
              })}
            </div>
            <Reveal delay={0.3}>
              <p className="mt-6 text-[12px] tracking-[0.01em] text-forest/55">
                Pilot baselines and customer traction will be published only when
                verified. EcoGen does not display unverified certification or square-footage figures.
              </p>
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}
