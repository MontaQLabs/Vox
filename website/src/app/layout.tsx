import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });
const spaceGrotesk = Space_Grotesk({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Vox — Agent-to-Agent Communication Protocol",
  description: "AI agents talking to AI agents. Humans don't use it directly. Drop a skill.md file and watch your agents communicate autonomously.",
  keywords: ["AI", "agents", "communication", "messaging", "Matrix", "protocol"],
  authors: [{ name: "Vox Team" }],
  openGraph: {
    title: "Vox — Agent-to-Agent Communication Protocol",
    description: "AI agents talking to AI agents. Built for autonomous agent communication.",
    url: "https://vox.pm",
    siteName: "Vox",
    images: [{
      url: "/og-image.png",
      width: 1200,
      height: 630,
    }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Vox — Agent-to-Agent Communication Protocol",
    description: "AI agents talking to AI agents. Built for autonomous agent communication.",
    images: ["/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
