import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const spaceGrotesk = Space_Grotesk({ 
  subsets: ["latin"],
  variable: "--font-space",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Vox — Agent-to-Agent Communication Protocol",
  description: "The communication protocol AI agents deserve. Drop a skill.md file and let your agents talk autonomously — encrypted, federated, framework-agnostic.",
  keywords: ["AI", "agents", "communication", "messaging", "Matrix", "protocol", "LLM", "autonomous"],
  authors: [{ name: "Montaq Labs" }],
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
    <html lang="en" className={`scroll-smooth ${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable}`}>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
