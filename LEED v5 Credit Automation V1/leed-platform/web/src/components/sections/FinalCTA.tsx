import Image from "next/image";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { Button } from "@/components/ui/Button";

export function FinalCTA() {
  return (
    <section id="demo" className="relative overflow-hidden py-24 md:py-32">
      <div aria-hidden className="eg-mesh pointer-events-none absolute inset-0 -z-10" />
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="grid grid-cols-12 gap-10 lg:gap-12">
          <div className="col-span-12 lg:col-span-7">
            <Reveal>
              <Kicker>The certification operating system</Kicker>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-6 text-[clamp(40px,7vw,72px)] font-semibold leading-[1.02] tracking-[-0.03em] text-forest">
                Build the future of certification work
                <span className="text-primary"> with confidence.</span>
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-6 max-w-[58ch] text-[16px] leading-[1.55] text-forest/72">
                See how EcoGen prepares traceable LEED v5 evidence packs, routes review
                decisions, and gives teams a clearer path from project data to
                submission-ready documentation.
              </p>
            </Reveal>
            <Reveal delay={0.16}>
              <div className="mt-10 flex flex-col gap-3 sm:flex-row">
                <Button href="#book" size="lg">
                  Book a demo
                </Button>
                <Button href="#suites" variant="secondary" size="lg">
                  Explore supported credits
                </Button>
              </div>
            </Reveal>
            <Reveal delay={0.22}>
              <p className="mt-10 max-w-[60ch] text-[12px] leading-[1.55] text-forest/55">
                EcoGen assists with evidence preparation and workflow management. Final
                compliance decisions, certification submissions, and awarded outcomes
                remain subject to qualified human review and the applicable USGBC/GBCI
                process.
              </p>
            </Reveal>
          </div>

          <div className="col-span-12 lg:col-span-5">
            <Reveal delay={0.1}>
              <Image
                src="/assets/visuals/10-final-cta-botanical-band.png"
                width={1200}
                height={1200}
                alt="EcoGen botanical close"
                className="mx-auto h-auto w-full max-w-[520px] select-none"
              />
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}
