import type { Metadata } from "next";
import Link from "next/link";
import Navigation from "./_components/navigation";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Bluebird", template: "%s | Bluebird" },
  description: "Bluebird construction management — application preview.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>
        <a className="skip-link" href="#main-content">Skip to content</a>
        <header className="site-header">
          <div className="header-inner">
            <Link className="brand" href="/" aria-label="Bluebird home">
              <span className="brand-mark" aria-hidden="true">b.</span>
              <span>bluebird<span className="brand-dot" aria-hidden="true">.</span></span>
            </Link>
            <Navigation />
          </div>
        </header>
        <main id="main-content" tabIndex={-1} className="main-content">
          {children}
        </main>
        <footer className="site-footer">
          <span>Bluebird</span>
          <span>Application preview · No project data</span>
        </footer>
      </body>
    </html>
  );
}
