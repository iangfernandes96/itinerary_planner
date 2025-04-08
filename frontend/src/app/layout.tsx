import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Travel Itinerary Planner",
  description: "Plan your perfect trip with our AI-powered travel itinerary generator",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main className="min-h-screen bg-background">
          <div className="container mx-auto py-8 px-4">
            {children}
          </div>
        </main>
      </body>
    </html>
  );
}
