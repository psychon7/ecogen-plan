import Image from "next/image";
import {
  Building2,
  UploadCloud,
  Workflow,
  ClipboardCheck,
  PackageCheck,
} from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { Button } from "@/components/ui/Button";
import { GlassCard } from "@/components/ui/GlassCard";

const STEPS = [
  {
    icon: Building2,
    title: "Set up the project",
    body: "Choose rating system context, region, building type, pursued credits, team roles, and available source paths.",
  },
  {
    icon: UploadCloud,
    title: "Upload or connect evidence",
    body: "Add schedules, product lists, reports, model outputs, spreadsheets, and manual data where APIs are unavailable.",
  },
  {
    icon: Workflow,
    title: "Run supported workflows",
    body: "EcoGen extracts fields, runs calculations, drafts narratives, and builds a traceable evidence pack for review.",
  },
  {
    icon: ClipboardCheck,
    title: "Review with confidence",
    body: "Consultants and specialists inspect sources, formulas, exceptions, and AI-generated content before approval.",
  },
  {
    icon: PackageCheck,
    title: "Export the package",
    body: "Export reviewer-ready documentation for manual upload, with the approval record and audit trail preserved.",
  },
];

export function HowItWorks() {
  return (
    <section className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="grid grid-cols-12 gap-8 lg:gap-12">
          <div className="col-span-12 lg:col-span-5">
            <Reveal>
              <Kicker>From data to export</Kicker>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-5 text-[clamp(34px,5vw,52px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
                From project data to reviewer-ready export.
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-5 max-w-[44ch] text-[15.5px] leading-[1.55] text-forest/72">
                Five governed steps. Source-grounded at every stage. Human approval
                before the package leaves the workspace.
              </p>
            </Reveal>
            <Reveal delay={0.15}>
              <div className="mt-8">
                <Button href="#demo">Book a demo</Button>
              </div>
            </Reveal>
            <Reveal delay={0.22}>
              <div className="mt-12 hidden lg:block">
                <Image
                  src="/assets/visuals/05-master-workflow-flow.png"
                  width={900}
                  height={700}
                  alt="Master workflow diagram"
                  className="h-auto w-full select-none"
                />
              </div>
            </Reveal>
          </div>

          <div className="col-span-12 lg:col-span-7">
            <ol className="relative space-y-4">
              {STEPS.map((s, i) => {
                const Icon = s.icon;
                return (
                  <Reveal key={s.title} delay={0.05 * i} as="div">
                    <GlassCard tone="strong" radius="panel" className="eg-card-hover">
                      <div className="flex items-start gap-5">
                        <div className="flex flex-col items-center gap-3">
                          <span className="grid h-12 w-12 place-items-center rounded-full eg-icon-well">
                            <Icon className="h-5 w-5 text-forest" strokeWidth={1.75} />
                          </span>
                          <span className="text-[11px] font-semibold tracking-[0.18em] text-primary/80">
                            STEP {String(i + 1).padStart(2, "0")}
                          </span>
                        </div>
                        <div className="flex-1 pt-1">
                          <h3 className="text-[19px] font-semibold leading-tight text-forest">
                            {s.title}
                          </h3>
                          <p className="mt-2 max-w-[58ch] text-[14px] leading-[1.55] text-forest/70">
                            {s.body}
                          </p>
                        </div>
                      </div>
                    </GlassCard>
                  </Reveal>
                );
              })}
            </ol>
          </div>

          <div className="col-span-12 lg:hidden">
            <Reveal>
              <Image
                src="/assets/visuals/05-master-workflow-flow.png"
                width={1200}
                height={800}
                alt="Master workflow diagram"
                className="h-auto w-full select-none"
              />
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}
