import type { Metadata } from "next";
import Link from "next/link";
import styles from "./create/create.module.css";

export const metadata: Metadata = { title: "Home" };

export default function Home() {
  return (
    <div className="home-content">
      <section className="intro" aria-labelledby="home-title">
        <p className="eyebrow">From schedule to progress</p>
        <h1 id="home-title">Your schedule.<br />Ready for Excel.</h1>
        <p className="intro-copy">
          Turn your Primavera P6 or Microsoft Project XML into a Progress Workbook.
          Plan, record weekly progress and prepare your next project update in Desktop Excel.
        </p>
        <Link className="button-link" href="/create">
          Create Progress Workbook <span aria-hidden="true">↗</span>
        </Link>
      </section>
      <aside className={styles.presentation} aria-labelledby="preview-title">
        <span className="small-label">One workbook. Your project.</span>
        <h2 id="preview-title">The weekly update,<br />without the setup.</h2>
        <ol className={styles.steps}>
          <li><span>01</span><div><strong>Upload your schedule</strong><p>P6 XML or MSP XML</p></div></li>
          <li><span>02</span><div><strong>Set your progress basis</strong><p>Equal or Duration, your cutoff and plan curve</p></div></li>
          <li><span>03</span><div><strong>Take your workbook with you</strong><p>Weekly Main, Monthly Summary and S-curves</p></div></li>
        </ol>
        <span className="preview-badge">Free to use · No account needed</span>
      </aside>
    </div>
  );
}
