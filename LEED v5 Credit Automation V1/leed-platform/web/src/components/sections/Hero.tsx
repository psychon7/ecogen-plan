import Image from "next/image";
import { UserRound, Leaf } from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Button } from "@/components/ui/Button";
import { Reveal } from "@/components/ui/Reveal";

/**
 * Hero — 5/7 split with massive display H1, glass CTA, and isometric ecosystem scene.
 */
export function Hero() {
  return (
    <section className="relative isolate overflow-hidden pt-32 md:pt-40">
      <div aria-hidden className="eg-mesh pointer-events-none absolute inset-0 -z-10" />

      <div className="mx-auto grid max-w-[1320px] grid-cols-12 gap-8 px-5 md:px-8 lg:gap-12 lg:px-10">
        {/* Copy */}
        <div className="col-span-12 lg:col-span-5">
          <Reveal>
            <Kicker>LEED v5 evidence automation</Kicker>
          </Reveal>

          <Reveal delay={0.05}>
            <h1 className="mt-6 text-[clamp(44px,8vw,72px)] font-semibold leading-[1.02] tracking-[-0.03em] text-forest">
              Every LEED project.
              <br />
              <span className="text-primary">Every proof point.</span>
            </h1>
          </Reveal>

          <Reveal delay={0.12}>
            <p className="mt-6 max-w-[55ch] text-[17px] leading-[1.55] text-forest/75">
              EcoGen turns project data into traceable, reviewer-ready evidence packs for
              supported LEED v5 credits, with source citations, deterministic calculations,
              confidence flags, and named human approval before submission.
            </p>
          </Reveal>

          <Reveal delay={0.18}>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
              <Button href="#demo" size="lg">
                Book a demo
              </Button>
              <Button href="#suites" variant="secondary" size="lg" icon="right">
                Explore supported credits
              </Button>
            </div>
          </Reveal>

          <Reveal delay={0.26}>
            <div className="mt-10 flex items-start gap-3 border-t border-[rgba(15,61,35,0.08)] pt-6">
              <span className="mt-0.5 grid h-9 w-9 place-items-center rounded-full eg-icon-well">
                <UserRound className="h-4 w-4 text-forest" strokeWidth={2} />
              </span>
              <p className="max-w-[42ch] text-[13.5px] leading-[1.5] text-forest/75">
                Built for LEED consultants, sustainability project managers, and portfolio
                owners who need progress they can prove.
              </p>
            </div>
          </Reveal>
        </div>

        {/* Hero scene */}
        <div className="col-span-12 lg:col-span-7">
          <Reveal delay={0.1}>
            <div className="relative">
              <div
                aria-hidden
                className="absolute -inset-6 -z-10 rounded-[40px] eg-mesh blur-2xl opacity-70"
              />
              <Image
                src="/assets/visuals/01-hero-ecosystem-evidence-map.png"
                width={1600}
                height={1200}
                priority
                alt="Isometric LEED v5 ecosystem with evidence pack callouts"
                className="h-auto w-full select-none"
              />
            </div>
          </Reveal>
        </div>

        {/* Microcopy under visual */}
        <div className="col-span-12">
          <Reveal delay={0.2}>
            <div className="flex items-center justify-center gap-2 pt-2 pb-12 text-center text-[12.5px] tracking-[0.01em] text-forest/55">
              <Leaf className="h-3.5 w-3.5 text-primary/70" strokeWidth={2} />
              Supported workflows vary by rating system, region, source availability, and review requirements.
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
