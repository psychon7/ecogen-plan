import Image from "next/image";
import {
  FileSpreadsheet,
  FileText,
  Database,
  Globe2,
  PencilLine,
  Building2,
} from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { GlassCard } from "@/components/ui/GlassCard";

const INPUTS = [
  { icon: FileSpreadsheet, label: "Excel & CSV schedules" },
  { icon: FileText, label: "PDF certificates & reports" },
  { icon: Building2, label: "Fixture & equipment schedules" },
  { icon: Database, label: "Product & certification databases" },
  { icon: Globe2, label: "Public climate, GIS, transit datasets" },
  { icon: PencilLine, label: "Manual entries with reviewer notes" },
];

const PLANNED = [
  "Arc & LEED Online (after verified API access)",
  "WaterSense and regional fixture sources",
  "ENERGY STAR & emissions datasets",
  "EPA SNAP, AHRI, refrigerant references",
  "EC3, EPD, GREENGUARD, FloorScore",
  "Regional substitutes outside the United States",
];

export function Integrations() {
  return (
    <section className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="grid grid-cols-12 gap-10 lg:gap-12">
          <div className="col-span-12 lg:col-span-5">
            <Reveal>
              <Kicker>Sources & integrations</Kicker>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-5 text-[clamp(32px,4.6vw,46px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
                Connect the sources your evidence already depends on.
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-5 max-w-[46ch] text-[15.5px] leading-[1.55] text-forest/72">
                EcoGen works with structured files, project documents, public datasets,
                and verified third-party sources. Availability depends on credit, region,
                licensing, and API access.
              </p>
            </Reveal>
            <Reveal delay={0.16}>
              <div className="mt-10">
                <Image
                  src="/assets/visuals/08-source-routing-network.png"
                  width={900}
                  height={700}
                  alt="Regional source routing network"
                  className="h-auto w-full select-none"
                />
              </div>
            </Reveal>
          </div>

          <div className="col-span-12 lg:col-span-7">
            <Reveal>
              <GlassCard tone="strong" radius="panel" bezel>
                <h3 className="text-[12px] font-semibold uppercase tracking-[0.18em] text-primary">
                  Supported inputs
                </h3>
                <ul className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
                  {INPUTS.map((it) => {
                    const Icon = it.icon;
                    return (
                      <li
                        key={it.label}
                        className="flex items-center gap-3 rounded-2xl border border-[rgba(15,61,35,0.08)] bg-white/55 px-4 py-3"
                      >
                        <span className="grid h-9 w-9 place-items-center rounded-full eg-mint-well">
                          <Icon className="h-4 w-4 text-forest" strokeWidth={1.75} />
                        </span>
                        <span className="text-[13.5px] font-medium text-forest/85">
                          {it.label}
                        </span>
                      </li>
                    );
                  })}
                </ul>
              </GlassCard>
            </Reveal>

            <Reveal delay={0.1}>
              <GlassCard tone="soft" radius="panel" className="mt-5">
                <h3 className="text-[12px] font-semibold uppercase tracking-[0.18em] text-primary">
                  Planned & conditional
                </h3>
                <ul className="mt-4 grid grid-cols-1 gap-x-6 gap-y-2.5 sm:grid-cols-2">
                  {PLANNED.map((p) => (
                    <li key={p} className="flex items-start gap-2 text-[13.5px] leading-[1.5] text-forest/72">
                      <span className="mt-2 inline-block h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                      {p}
                    </li>
                  ))}
                </ul>
                <p className="mt-6 rounded-2xl border border-dashed border-[rgba(15,61,35,0.18)] bg-white/40 p-4 text-[12.5px] leading-[1.55] text-forest/65">
                  When a source is unavailable, EcoGen degrades visibly to assisted or
                  manual mode instead of pretending the workflow is fully automated.
                </p>
              </GlassCard>
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}
