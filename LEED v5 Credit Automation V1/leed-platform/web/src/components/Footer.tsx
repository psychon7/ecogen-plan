import { Logo } from "@/components/ui/Logo";

const COLUMNS = [
  {
    title: "Platform",
    items: ["Overview", "Features", "Evidence packs", "Integrations", "Security"],
  },
  {
    title: "Solutions",
    items: [
      "By building type",
      "For LEED consultants",
      "For project managers",
      "For owners",
      "For specialist reviewers",
    ],
  },
  {
    title: "Certifications",
    items: [
      "LEED v5",
      "Water Efficiency",
      "Refrigerant Management",
      "Low-Emitting Materials",
      "Quality Plans",
    ],
  },
  {
    title: "Resources",
    items: ["Guides", "Case studies", "Webinars", "Blog", "Help center"],
  },
  {
    title: "About",
    items: ["Mission", "Team", "Partners", "Careers"],
  },
];

export function Footer() {
  return (
    <footer className="relative border-t border-[rgba(15,61,35,0.08)] bg-white/60">
      <div className="mx-auto max-w-[1200px] px-5 py-16 md:px-8 lg:px-10">
        <div className="grid grid-cols-12 gap-10">
          <div className="col-span-12 lg:col-span-4">
            <Logo />
            <p className="mt-5 max-w-[36ch] text-[13.5px] leading-[1.55] text-forest/65">
              AI-assisted sustainability compliance for buildings and portfolios.
            </p>
          </div>

          <div className="col-span-12 grid grid-cols-2 gap-8 sm:grid-cols-3 md:grid-cols-5 lg:col-span-8">
            {COLUMNS.map((c) => (
              <div key={c.title}>
                <h4 className="text-[11.5px] font-semibold uppercase tracking-[0.18em] text-forest/65">
                  {c.title}
                </h4>
                <ul className="mt-4 space-y-2.5">
                  {c.items.map((it) => (
                    <li key={it}>
                      <a
                        href="#"
                        className="text-[13.5px] leading-[1.5] text-forest/75 transition-colors hover:text-forest"
                      >
                        {it}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-14 flex flex-col gap-4 border-t border-[rgba(15,61,35,0.08)] pt-6 text-[12px] text-forest/55 md:flex-row md:items-center md:justify-between">
          <p>
            &copy; {new Date().getFullYear()} EcoGen. LEED is a trademark of the U.S.
            Green Building Council. EcoGen is an independent software platform and is not
            affiliated with, endorsed by, or sponsored by USGBC or GBCI.
          </p>
          <div className="flex items-center gap-5">
            <a href="#" className="hover:text-forest">Privacy</a>
            <a href="#" className="hover:text-forest">Terms</a>
            <a href="#" className="hover:text-forest">Security</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
