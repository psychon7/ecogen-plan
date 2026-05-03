import { Link2, ShieldCheck, ListChecks, Route, LockKeyhole } from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { GlassCard } from "@/components/ui/GlassCard";
import { cn } from "@/lib/cn";

const PILLARS = [
  {
    icon: Link2,
    title: "Source traceability",
    body: "Every important claim links back to uploaded evidence, API data, static requirement sources, or reviewer-entered assumptions.",
    span: "lg:col-span-7",
  },
  {
    icon: ShieldCheck,
    title: "Human approval",
    body: "Compliance-critical packages require named approval before they become submission-ready.",
    span: "lg:col-span-5",
  },
  {
    icon: ListChecks,
    title: "Workflow history",
    body: "Changes, fallbacks, reviewer comments, retries, approvals, and rejected outputs remain visible.",
    span: "lg:col-span-4",
  },
  {
    icon: Route,
    title: "Regional transparency",
    body: "Credit availability and automation depth change when data coverage, APIs, licensing, or local source quality change.",
    span: "lg:col-span-4",
  },
  {
    icon: LockKeyhole,
    title: "Professional boundaries",
    body: "EcoGen does not create energy models, guarantee certification points, or replace licensed professional judgment.",
    span: "lg:col-span-4",
  },
];

export function Trust() {
  return (
    <section className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="max-w-[820px]">
          <Reveal>
            <Kicker>Governance & trust</Kicker>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-5 text-[clamp(32px,4.6vw,46px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
              Built for auditability, not black-box automation.
            </h2>
          </Reveal>
          <Reveal delay={0.1}>
            <p className="mt-5 max-w-[60ch] text-[15.5px] leading-[1.55] text-forest/72">
              The platform is designed for professional workflows where the question is
              not only &ldquo;what did AI generate?&rdquo; but &ldquo;can a qualified
              reviewer trust this package?&rdquo;
            </p>
          </Reveal>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-12 lg:gap-6">
          {PILLARS.map((p, i) => {
            const Icon = p.icon;
            return (
              <Reveal key={p.title} delay={0.04 * i} className={cn(p.span)}>
                <GlassCard tone="strong" radius="panel" className="eg-card-hover h-full">
                  <span className="grid h-11 w-11 place-items-center rounded-full eg-icon-well">
                    <Icon className="h-5 w-5 text-forest" strokeWidth={1.75} />
                  </span>
                  <h3 className="mt-5 text-[17px] font-semibold text-forest">{p.title}</h3>
                  <p className="mt-2 max-w-[48ch] text-[13.5px] leading-[1.55] text-forest/68">
                    {p.body}
                  </p>
                </GlassCard>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
