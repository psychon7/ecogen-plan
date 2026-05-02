import Image from "next/image";
import { FolderArchive, Gauge, ScanSearch, ListTodo } from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { GlassCard } from "@/components/ui/GlassCard";

const PAINS = [
  {
    icon: FolderArchive,
    title: "Evidence is scattered",
    body: "Uploads, calculations, product certificates, and reviewer comments live in different places.",
  },
  {
    icon: Gauge,
    title: "Status is unclear",
    body: "Teams confuse draft progress with true submission readiness.",
  },
  {
    icon: ScanSearch,
    title: "AI feels risky",
    body: "Consultants cannot approve a claim unless they can inspect the source, formula, assumption, and reviewer history.",
  },
  {
    icon: ListTodo,
    title: "Rework is expensive",
    body: "Missing evidence, inconsistent calculations, and late reviewer comments turn documentation into repeated manual cleanup.",
  },
];

export function ProblemSection() {
  return (
    <section id="platform" className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="grid grid-cols-12 gap-8 lg:gap-12">
          <div className="col-span-12 lg:col-span-8">
            <Reveal>
              <Kicker>The cost of fragmented documentation</Kicker>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-5 max-w-[18ch] text-[clamp(34px,5vw,52px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
                LEED teams do not need more spreadsheets.
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-6 max-w-[58ch] text-[16px] leading-[1.55] text-forest/72">
                Certification work is high-trust work, but most teams still manage
                evidence inside fragmented folders, inboxes, calculators, PDFs, and
                trackers. That creates hidden risk: numbers drift, sources disappear,
                review tasks stall, and &ldquo;almost ready&rdquo; packages reach
                submission too late.
              </p>
            </Reveal>

            <Reveal delay={0.15}>
              <GlassCard tone="soft" radius="panel" bezel className="mt-10" padded={false}>
                <div className="eg-glass-soft rounded-[22px] p-2">
                  <Image
                    src="/assets/visuals/03-fragmented-evidence-risk.png"
                    width={1400}
                    height={900}
                    alt="Fragmented evidence risk diagram"
                    className="h-auto w-full select-none rounded-[18px]"
                  />
                </div>
              </GlassCard>
            </Reveal>
          </div>

          <div className="col-span-12 lg:col-span-4">
            <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-1">
              {PAINS.map((p, i) => {
                const Icon = p.icon;
                return (
                  <Reveal key={p.title} delay={0.06 * i} as="div">
                    <GlassCard tone="strong" className="eg-card-hover h-full">
                      <span className="grid h-10 w-10 place-items-center rounded-full eg-icon-well">
                        <Icon className="h-4.5 w-4.5 text-forest" strokeWidth={1.75} />
                      </span>
                      <h3 className="mt-4 text-[16px] font-semibold text-forest">{p.title}</h3>
                      <p className="mt-2 text-[13.5px] leading-[1.55] text-forest/68">
                        {p.body}
                      </p>
                    </GlassCard>
                  </Reveal>
                );
              })}
            </ul>
          </div>
        </div>

        <Reveal delay={0.2}>
          <p className="mt-12 max-w-[60ch] text-[18px] leading-[1.4] font-semibold text-forest">
            EcoGen treats evidence as a governed workflow, not a folder of files.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
