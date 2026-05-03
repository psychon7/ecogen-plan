import Image from "next/image";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { GlassCard } from "@/components/ui/GlassCard";
import { cn } from "@/lib/cn";

const TYPOLOGIES = [
  {
    name: "Data centers",
    body: "High-performance facilities with complex systems and documentation burden.",
    asset: "/assets/visuals/06a-typology-data-center.png",
    span: "lg:col-span-7",
  },
  {
    name: "Hospitals",
    body: "Tightly reviewed projects where specialist accountability matters.",
    asset: "/assets/visuals/06b-typology-hospital.png",
    span: "lg:col-span-5",
  },
  {
    name: "Schools",
    body: "Clear tasking and progress visibility for teams with many stakeholders.",
    asset: "/assets/visuals/06c-typology-school.png",
    span: "lg:col-span-4",
  },
  {
    name: "Offices",
    body: "Repeatable workflows for common LEED v5 documentation paths.",
    asset: "/assets/visuals/06d-typology-office.png",
    span: "lg:col-span-4",
  },
  {
    name: "Campuses",
    body: "Portfolio visibility across projects, blockers, and reviewer queues.",
    asset: "/assets/visuals/06e-typology-campus.png",
    span: "lg:col-span-4",
  },
  {
    name: "Sites & masterplans",
    body: "Assisted workflows where GIS, regional data, and manual review are explicit.",
    asset: "/assets/visuals/06f-typology-sites-masterplans.png",
    span: "lg:col-span-12",
  },
];

export function Typologies() {
  return (
    <section id="solutions" className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="max-w-[820px]">
          <Reveal>
            <Kicker>Building typologies</Kicker>
          </Reveal>
          <Reveal delay={0.05}>
            <h2 className="mt-5 text-[clamp(34px,5vw,52px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
              Designed for every building typology.
            </h2>
          </Reveal>
          <Reveal delay={0.1}>
            <p className="mt-5 text-[15.5px] leading-[1.55] text-forest/72">
              EcoGen supports LEED teams across project types, while still respecting
              rating-system rules, regional source availability, and credit-specific
              review requirements.
            </p>
          </Reveal>
        </div>

        <div className="mt-12 grid grid-cols-1 gap-5 md:grid-cols-2 lg:grid-cols-12 lg:gap-6">
          {TYPOLOGIES.map((t, i) => (
            <Reveal key={t.name} delay={0.04 * i} className={cn(t.span)}>
              <GlassCard
                tone="strong"
                radius="panel"
                padded={false}
                className="eg-card-hover group h-full overflow-hidden"
              >
                <div className="relative h-44 overflow-hidden md:h-52">
                  <Image
                    src={t.asset}
                    fill
                    sizes="(max-width: 1024px) 100vw, 50vw"
                    alt={`${t.name} typology illustration`}
                    className="object-contain object-center transition-transform duration-700 ease-[cubic-bezier(0.16,1,0.3,1)] group-hover:scale-[1.03]"
                  />
                </div>
                <div className="border-t border-[rgba(15,61,35,0.08)] p-6">
                  <h3 className="text-[17px] font-semibold text-forest">{t.name}</h3>
                  <p className="mt-2 max-w-[44ch] text-[13.5px] leading-[1.55] text-forest/68">
                    {t.body}
                  </p>
                </div>
              </GlassCard>
            </Reveal>
          ))}
        </div>

        <Reveal delay={0.2}>
          <p className="mt-10 text-[12.5px] tracking-[0.01em] text-forest/55">
            Project eligibility and rating-system selection should be confirmed against USGBC guidance before registration.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
