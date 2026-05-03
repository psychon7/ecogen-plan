import Image from "next/image";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { Button } from "@/components/ui/Button";
import { GlassCard } from "@/components/ui/GlassCard";

const RESULTS = [
  { k: "Documentation time", v: "Days → hours", note: "Pilot baseline pending" },
  { k: "Reviewer comments", v: "Reduced rework", note: "Surfaced pre-export" },
  { k: "Manual repair items", v: "Surfaced early", note: "Confidence-flagged" },
  { k: "Approval path", v: "Named + timestamped", note: "Audit trail preserved" },
];

export function CaseStudy() {
  return (
    <section id="resources" className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <Reveal>
          <GlassCard tone="strong" radius="hero" bezel padded={false}>
            <div className="grid grid-cols-12 gap-0 overflow-hidden rounded-[26px]">
              <div className="col-span-12 lg:col-span-6">
                <div className="relative h-full min-h-[320px]">
                  <Image
                    src="/assets/visuals/07-water-efficiency-pilot.png"
                    fill
                    sizes="(max-width: 1024px) 100vw, 50vw"
                    alt="Water Efficiency pilot evidence pack"
                    className="object-contain object-center"
                  />
                </div>
              </div>
              <div className="col-span-12 border-t border-[rgba(15,61,35,0.08)] p-8 md:p-12 lg:col-span-6 lg:border-l lg:border-t-0">
                <Kicker>Pilot workflow</Kicker>
                <h3 className="mt-5 text-[clamp(28px,3.6vw,40px)] font-semibold leading-[1.1] tracking-[-0.02em] text-forest">
                  Water Efficiency evidence pack in hours, not days.
                </h3>
                <p className="mt-5 max-w-[52ch] text-[15px] leading-[1.55] text-forest/70">
                  EcoGen helps a LEED team upload fixture schedules, validate inputs, run
                  baseline and proposed-use calculations, flag missing assumptions, and
                  prepare a reviewer-ready Water Efficiency evidence pack.
                </p>

                <dl className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2">
                  {RESULTS.map((r) => (
                    <div
                      key={r.k}
                      className="rounded-2xl border border-[rgba(15,61,35,0.08)] bg-white/50 p-4"
                    >
                      <dt className="text-[11px] font-semibold uppercase tracking-[0.14em] text-forest/55">
                        {r.k}
                      </dt>
                      <dd className="mt-1.5 text-[16px] font-semibold text-forest">
                        {r.v}
                      </dd>
                      <p className="mt-1 text-[12px] text-forest/55">{r.note}</p>
                    </div>
                  ))}
                </dl>

                <div className="mt-8">
                  <Button href="#demo" variant="secondary" icon="up-right">
                    View pilot workflow
                  </Button>
                </div>
              </div>
            </div>
          </GlassCard>
        </Reveal>
      </div>
    </section>
  );
}
