import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
const inter = Inter({ subsets: ["latin"] });
export const metadata: Metadata = {
  title: "QuoteAI — Autonomous Insurance Pipeline",
  description:
    "Multi-agent AI system for autonomous insurance quote processing.",
};
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${inter.className} bg-[#09090b] text-[#fafafa] min-h-screen antialiased selection:bg-white/20/30 selection:text-white`}
      >
        {children}
      </body>
    </html>
  );
}
