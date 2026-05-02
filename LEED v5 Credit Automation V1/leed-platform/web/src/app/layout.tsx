import type { Metadata } from "next";
import { Open_Sans, Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const openSans = Open_Sans({
  variable: "--font-open-sans",
  subsets: ["latin"],
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
  display: "swap",
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://ecogen.ai"),
  title: {
    default: "LEED v5 Automation Software for Evidence Packs | EcoGen",
    template: "%s | EcoGen",
  },
  description:
    "Automate supported LEED v5 evidence workflows with source-grounded calculations, reviewer tasks, audit trails, and demo-ready sustainability compliance reporting.",
  applicationName: "EcoGen",
  keywords: [
    "LEED v5 automation software",
    "LEED documentation software",
    "LEED evidence pack software",
    "LEED certification workflow software",
    "AI LEED documentation assistant",
    "green building certification software",
    "sustainability compliance platform",
  ],
  openGraph: {
    type: "website",
    title: "EcoGen — LEED v5 Evidence Automation",
    description:
      "Prepare traceable, reviewer-ready LEED v5 evidence packs faster, with AI-assisted workflows and human approval built in.",
    siteName: "EcoGen",
    images: [{ url: "/assets/visuals/11-og-default.png", width: 1200, height: 630 }],
  },
  twitter: {
    card: "summary_large_image",
    title: "EcoGen — LEED v5 Evidence Automation",
    description: "Traceable, reviewer-ready LEED v5 evidence packs.",
    images: ["/assets/visuals/11-og-default.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${openSans.variable} ${geistSans.variable} ${geistMono.variable}`}
    >
      <body className="min-h-screen bg-canvas font-sans text-forest antialiased">
        {children}
      </body>
    </html>
  );
}
