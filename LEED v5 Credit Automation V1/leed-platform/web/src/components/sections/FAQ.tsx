"use client";

import * as React from "react";
import { Plus } from "lucide-react";
import { Kicker } from "@/components/ui/Kicker";
import { Reveal } from "@/components/ui/Reveal";
import { cn } from "@/lib/cn";

const FAQS = [
  {
    q: "Does EcoGen fully automate LEED certification?",
    a: "No. EcoGen automates repeatable documentation, calculation, extraction, and evidence-pack workflows for supported credits. Consultants and qualified reviewers still make compliance decisions and approve packages before submission.",
  },
  {
    q: "What does \u201Creviewer-ready\u201D mean?",
    a: "A reviewer-ready package includes the credit narrative, source index, calculation trail, evidence matrix, confidence flags, exceptions, and human approval record needed for serious internal review.",
  },
  {
    q: "Which credits are supported first?",
    a: "The first commercial wedge is Water Efficiency, followed by Refrigerant Management, Quality Plans, Integrative Process Assessment, and Low-Emitting Materials as production suite workflows.",
  },
  {
    q: "Can EcoGen connect directly to Arc or LEED Online?",
    a: "V1 focuses on manual-upload evidence exports. Direct Arc or LEED Online submission belongs in V2 after API access, permissions, schema requirements, terms, and final approval flows are verified.",
  },
  {
    q: "How does EcoGen handle regional data gaps?",
    a: "EcoGen shows credit-specific source availability by region. If APIs or public datasets are weak, the workflow switches to assisted or manual mode and surfaces the gap before export.",
  },
  {
    q: "Does EcoGen replace specialist reviewers?",
    a: "No. Specialist reviewers remain responsible for expert-heavy work such as energy model outputs, LCA assumptions, GIS interpretation, material certification exceptions, and project-specific compliance judgment.",
  },
  {
    q: "How is AI output checked?",
    a: "AI-generated content is tied to sources, confidence flags, deterministic calculations where applicable, requirement-to-evidence matrices, and human review tasks.",
  },
  {
    q: "Is EcoGen only for LEED v5?",
    a: "The current product story focuses on LEED v5. Future support for other certification systems will be added only when source requirements, workflows, and review boundaries are clearly defined.",
  },
  {
    q: "Who is EcoGen for?",
    a: "EcoGen is built for LEED consultants, sustainability project managers, specialist reviewers, and owners who need faster documentation without losing evidence integrity.",
  },
];

export function FAQ() {
  const [open, setOpen] = React.useState<number | null>(0);

  return (
    <section className="relative py-20 md:py-28">
      <div className="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
        <div className="grid grid-cols-12 gap-10 lg:gap-16">
          <div className="col-span-12 lg:col-span-4">
            <Reveal>
              <Kicker>FAQ</Kicker>
            </Reveal>
            <Reveal delay={0.05}>
              <h2 className="mt-5 text-[clamp(32px,4.6vw,44px)] font-semibold leading-[1.05] tracking-[-0.025em] text-forest">
                Questions LEED teams ask before they trust AI.
              </h2>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-5 max-w-[42ch] text-[14.5px] leading-[1.55] text-forest/65">
                Direct answers, written for reviewers — not marketing teams.
              </p>
            </Reveal>
          </div>

          <div className="col-span-12 lg:col-span-8">
            <Reveal>
              <ul className="border-t border-[rgba(15,61,35,0.1)]">
                {FAQS.map((f, i) => {
                  const isOpen = open === i;
                  return (
                    <li key={f.q} className="border-b border-[rgba(15,61,35,0.1)]">
                      <button
                        type="button"
                        onClick={() => setOpen(isOpen ? null : i)}
                        aria-expanded={isOpen}
                        className="group flex w-full items-center justify-between gap-6 py-6 text-left"
                      >
                        <span className="text-[16px] font-semibold leading-snug text-forest md:text-[17px]">
                          {f.q}
                        </span>
                        <span
                          className={cn(
                            "grid h-9 w-9 shrink-0 place-items-center rounded-full eg-glass-soft transition-transform duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]",
                            isOpen && "rotate-45 bg-mint"
                          )}
                        >
                          <Plus className="h-4 w-4 text-forest" strokeWidth={2} />
                        </span>
                      </button>
                      <div
                        className={cn(
                          "grid overflow-hidden transition-[grid-template-rows,opacity] duration-500 ease-[cubic-bezier(0.16,1,0.3,1)]",
                          isOpen ? "grid-rows-[1fr] opacity-100 pb-6" : "grid-rows-[0fr] opacity-0"
                        )}
                      >
                        <div className="min-h-0">
                          <p className="max-w-[68ch] pr-12 text-[14.5px] leading-[1.6] text-forest/72">
                            {f.a}
                          </p>
                        </div>
                      </div>
                    </li>
                  );
                })}
              </ul>
            </Reveal>
          </div>
        </div>
      </div>
    </section>
  );
}
