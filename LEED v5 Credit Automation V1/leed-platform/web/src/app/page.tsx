import { Nav } from "@/components/Nav";
import { Footer } from "@/components/Footer";
import { Hero } from "@/components/sections/Hero";
import { OutcomeStrip } from "@/components/sections/OutcomeStrip";
import { SuiteScope } from "@/components/sections/SuiteScope";
import { ProblemSection } from "@/components/sections/ProblemSection";
import { ProductValue } from "@/components/sections/ProductValue";
import { EvidencePack } from "@/components/sections/EvidencePack";
import { HowItWorks } from "@/components/sections/HowItWorks";
import { Typologies } from "@/components/sections/Typologies";
import { Readiness } from "@/components/sections/Readiness";
import { CaseStudy } from "@/components/sections/CaseStudy";
import { Personas } from "@/components/sections/Personas";
import { Integrations } from "@/components/sections/Integrations";
import { Trust } from "@/components/sections/Trust";
import { FAQ } from "@/components/sections/FAQ";
import { FinalCTA } from "@/components/sections/FinalCTA";

export default function Page() {
  // FAQ JSON-LD for AEO
  const faqJsonLd = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: [
      ["Does EcoGen fully automate LEED certification?", "No. EcoGen automates repeatable documentation, calculation, extraction, and evidence-pack workflows for supported credits. Consultants and qualified reviewers still make compliance decisions and approve packages before submission."],
      ["Which LEED v5 credits does EcoGen support first?", "EcoGen's production MVP focuses on suite-based workflows: Water Efficiency, Refrigerant Management, Quality Plans, Integrative Process Assessment, and Low-Emitting Materials. The first commercial wedge is Water Efficiency."],
      ["Can EcoGen connect directly to Arc or LEED Online?", "V1 focuses on manual-upload evidence exports. Direct Arc or LEED Online submission belongs in V2 after API access, permissions, schema requirements, terms, and final approval flows are verified."],
      ["Does EcoGen replace LEED consultants?", "No. EcoGen automates repetitive evidence preparation, calculations, extraction, and reporting tasks. LEED consultants and qualified reviewers remain responsible for strategy, review, approval, and submission decisions."],
    ].map(([q, a]) => ({
      "@type": "Question",
      name: q,
      acceptedAnswer: { "@type": "Answer", text: a },
    })),
  };

  const orgJsonLd = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "EcoGen",
    url: "https://ecogen.ai",
    description:
      "AI-assisted LEED v5 evidence automation platform that prepares traceable, reviewer-ready evidence packs.",
  };

  return (
    <>
      <Nav />
      <main className="relative">
        <Hero />
        <OutcomeStrip />
        <SuiteScope />
        <ProblemSection />
        <ProductValue />
        <EvidencePack />
        <HowItWorks />
        <Typologies />
        <Readiness />
        <CaseStudy />
        <Personas />
        <Integrations />
        <Trust />
        <FAQ />
        <FinalCTA />
      </main>
      <Footer />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }}
      />
    </>
  );
}
