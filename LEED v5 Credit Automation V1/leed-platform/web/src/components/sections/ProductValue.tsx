import {
  ScanSearch,
  Calculator,
  PackageCheck,
  ListTodo,
  Gauge,
  Route,
  Send,
  MonitorCog,
} from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { GlassCard } from "@/components/ui/GlassCard";
import { cn } from "@/lib/cn";

type Feature = {
  icon: React.ElementType;
  title: string;
  body: string;
  span?: string;
};

const FEATURES: Feature[] = [
  {
    icon: ScanSearch,
    title: "Source-grounded extraction",
    body: "Extract values from schedules, spreadsheets, PDFs, reports, API sources, and manual inputs with locators and confidence flags.",
    span: "md:col-span-8 lg:col-span-7",
  },
  {
    icon: Calculator,
    title: "Deterministic calculations",
    body: "Run tested credit calculations where formulas are explicit, versioned, and visible to reviewers.",
    span: "md:col-span-4 lg:col-span-5",
  },
  {
    icon: PackageCheck,
    title: "Evidence pack builder",
    body: "Assemble narratives, tables, calculations, source indexes, and exception reports into one review-ready package.",
    span: "md:col-span-5 lg:col-span-5",
  },
  {
    icon: ListTodo,
    title: "Workflow and tasks",
    body: "Assign reviews, track blockers, set SLAs, and route rejected packages back to the right repair step.",
    span: "md:col-span-7 lg:col-span-7",
  },
  {
    icon: Gauge,
    title: "Confidence scoring",
    body: "Separate high-confidence packages from workflows that need senior review, manual data, or specialist input.",
    span: "md:col-span-4 lg:col-span-3",
  },
  {
    icon: Route,
    title: "Regional source routing",
    body: "Show when APIs, public datasets, product certifications, or manual preparation paths vary by region.",
    span: "md:col-span-4 lg:col-span-3",
  },
  {
    icon: Send,
    title: "Reviewer-ready exports",
    body: "Prepare manual-upload packages for V1, with direct Arc or LEED Online integration reserved for verified V2 workflows.",
    span: "md:col-span-4 lg:col-span-3",
  },
  {
    icon: MonitorCog,
    title: "Portfolio visibility",
    body: "Give project managers and owners progress reporting without overstating unawarded points.",
    span: "md:col-span-12 lg:col-span-3",
  },
];

export function ProductValue() {
  return (
    <section className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="max-w-[820px]">
          <Reveal>
            <Kicker>Product capabilities</Kicker>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-5 text-[clamp(34px,5vw,52px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
              AI-assisted. <span className="text-primary">Reviewer-controlled.</span>
            </h2>
          </Reveal>
          <Reveal delay={0.1}>
            <p className="mt-5 max-w-[60ch] text-[16px] leading-[1.55] text-forest/72">
              EcoGen automates the repeatable work around LEED v5 documentation while
              keeping consultants, specialists, and project leads in control of
              compliance decisions.
            </p>
          </Reveal>
        </div>

        <div className="mt-14 grid grid-cols-1 gap-5 md:grid-cols-12 md:gap-5 lg:gap-6">
          {FEATURES.map((f, i) => {
            const Icon = f.icon;
            return (
              <Reveal key={f.title} delay={0.04 * i} className={cn("col-span-1", f.span)}>
                <GlassCard tone="strong" className="eg-card-hover h-full">
                  <span className="grid h-11 w-11 place-items-center rounded-full eg-icon-well">
                    <Icon className="h-5 w-5 text-forest" strokeWidth={1.75} />
                  </span>
                  <h3 className="mt-5 text-[17px] font-semibold leading-tight text-forest">
                    {f.title}
                  </h3>
                  <p className="mt-2 max-w-[48ch] text-[13.5px] leading-[1.55] text-forest/68">
                    {f.body}
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
