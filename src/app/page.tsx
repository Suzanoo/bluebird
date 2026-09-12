import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = { title: "Home" };

export default function Home() {
  return (
    <div className="home-content">
      <section className="intro" aria-labelledby="home-title">
        <p className="eyebrow">Construction management</p>
        <h1 id="home-title">A clear place<br />to begin.</h1>
        <p className="intro-copy">
          Welcome to Bluebird. Explore the first outline of your project workspace.
        </p>
        <Link className="button-link" href="/workspace">
          Open workspace preview <span aria-hidden="true">↗</span>
        </Link>
      </section>
      <aside className="preview-note" aria-labelledby="preview-title">
        <span className="small-label">A first look</span>
        <h2 id="preview-title">Space for what comes next.</h2>
        <p>
          This is an early application preview. The workspace is empty;
          no project has been created.
        </p>
        <span className="preview-badge">Preview only</span>
      </aside>
    </div>
  );
}
