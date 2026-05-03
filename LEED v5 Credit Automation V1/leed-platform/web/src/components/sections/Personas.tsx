import {
  UserRoundCheck,
  CalendarCheck2,
  GraduationCap,
  ScanSearch,
  Landmark,
} from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { GlassCard } from "@/components/ui/GlassCard";
import { cn } from "@/lib/cn";

const PERSONAS = [
  {
    icon: UserRoundCheck,
    title: "Senior LEED consultants",
    body: "Approve packages with sources, formulas, confidence, and exceptions visible before sign-off.",
    span: "lg:col-span-5",
  },
  {
    icon: CalendarCheck2,
    title: "Sustainability project managers",
    body: "Track readiness, blockers, reviewer SLAs, and client-ready progress without inflating status.",
    span: "lg:col-span-7",
  },
  {
    icon: GraduationCap,
    title: "Junior consultants",
    body: "Follow guided workflows that teach required inputs, catch gaps, and produce cleaner drafts.",
    span: "lg:col-span-4",
  },
  {
    icon: ScanSearch,
    title: "Specialist reviewers",
    body: "Review only the package elements that need expertise, with the source document and calculation trail beside the claim.",
    span: "lg:col-span-4",
  },
  {
    icon: Landmark,
    title: "Building owners",
    body: "See portfolio progress, risks, and certification blockers in language that is clear without hiding review reality.",
    span: "lg:col-span-4",
  },
];

export function Personas() {
  return (
    <section id="about" className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="max-w-[820px]">
          <Reveal>
            <Kicker>Built around the people who carry the risk</Kicker>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-5 text-[clamp(32px,4.6vw,46px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
              Designed for every role in the certification chain.
            </h2>
          </Reveal>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-12 lg:gap-6">
          {PERSONAS.map((p, i) => {
            const Icon = p.icon;
            return (
              <Reveal key={p.title} delay={0.04 * i} className={cn(p.span)}>
                <GlassCard tone="strong" className="eg-card-hover h-full">
                  <span className="grid h-11 w-11 place-items-center rounded-full eg-icon-well">
                    <Icon className="h-5 w-5 text-forest" strokeWidth={1.75} />
                  </span>
                  <h3 className="mt-5 text-[17px] font-semibold text-forest">{p.title}</h3>
                  <p className="mt-2 max-w-[44ch] text-[13.5px] leading-[1.55] text-forest/68">
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
