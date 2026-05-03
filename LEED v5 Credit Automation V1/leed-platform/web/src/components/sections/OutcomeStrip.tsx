import {
  FileCog,
  FolderArchive,
  ChartNoAxesColumnIncreasing,
  Activity,
  BadgeCheck,
} from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { GlassCard } from "@/components/ui/GlassCard";

const OUTCOMES = [
  {
    icon: FileCog,
    title: "Automate documentation",
    body: "Run repeatable credit workflows with structured inputs, source checks, and draft package generation.",
  },
  {
    icon: FolderArchive,
    title: "Centralize evidence",
    body: "Keep uploads, API data, assumptions, calculations, and reviewer notes connected to each claim.",
  },
  {
    icon: ChartNoAxesColumnIncreasing,
    title: "Track credits",
    body: "See what is draft, in review, internally approved, exported, submitted, and awarded.",
  },
  {
    icon: Activity,
    title: "Optimize performance",
    body: "Compare options, identify gaps, and surface improvements before review pressure builds.",
  },
  {
    icon: BadgeCheck,
    title: "Achieve readiness",
    body: "Export clean evidence packs only after confidence checks and human approval are complete.",
  },
];

export function OutcomeStrip() {
  return (
    <section className="relative py-20 md:py-24">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <Reveal>
          <p className="mx-auto max-w-[60ch] text-center text-[15px] leading-[1.5] text-forest/70">
            Replace scattered documents with one governed workflow from intake to export.
          </p>
        </Reveal>

        <Reveal delay={0.08}>
          <GlassCard
            tone="strong"
            radius="panel"
            bezel
            padded={false}
            className="mt-10"
          >
            <ul className="grid grid-cols-1 divide-y divide-[rgba(15,61,35,0.07)] sm:grid-cols-2 sm:divide-y-0 lg:grid-cols-5">
              {OUTCOMES.map((o, i) => {
                const Icon = o.icon;
                return (
                  <li
                    key={o.title}
                    className={`group flex flex-col gap-3 px-6 py-7 lg:px-7 ${
                      i !== OUTCOMES.length - 1
                        ? "lg:border-r lg:border-[rgba(15,61,35,0.07)]"
                        : ""
                    } ${
                      i % 2 === 1 ? "sm:border-l sm:border-[rgba(15,61,35,0.07)]" : ""
                    }`}
                  >
                    <span className="grid h-10 w-10 place-items-center rounded-full eg-icon-well">
                      <Icon className="h-4.5 w-4.5 text-forest" strokeWidth={1.75} />
                    </span>
                    <h3 className="text-[15px] font-semibold text-forest">{o.title}</h3>
                    <p className="hidden text-[13px] leading-[1.5] text-forest/65 lg:block">
                      {o.body}
                    </p>
                  </li>
                );
              })}
            </ul>
          </GlassCard>
        </Reveal>
      </div>
    </section>
  );
}
