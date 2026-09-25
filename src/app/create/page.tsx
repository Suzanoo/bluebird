import type { Metadata } from "next";
import CreateForm from "./create-form";
import styles from "./create.module.css";

export const metadata: Metadata = { title: "Create Progress Workbook" };

export default function CreatePage() {
  return (
    <section className="workspace-content" aria-labelledby="create-title">
      <header className="page-heading">
        <div><p className="eyebrow">P6 / Microsoft Project XML</p><h1 id="create-title">Create your Progress Workbook</h1></div>
      </header>
      <div className={styles.layout}>
        <CreateForm />
        <aside className={styles.help} aria-labelledby="included-title">
          <h2 id="included-title">Ready for your weekly update</h2>
          <ul><li>Weekly Plan and Actual in Main</li><li>Monthly Summary and Progress Dashboard</li><li>Activity Amount input, with WBS grouping</li></ul>
          <h3>Choose a weighting method</h3>
          <p><strong>Equal</strong> gives each ordinary activity the same influence.</p>
          <p><strong>Duration</strong> uses source working hours. Missing or invalid durations must be corrected; no automatic fallback.</p>
          <p>Milestones have zero Progress Weight. Entered Activity Amount is allocated Contract Value and does not affect these methods.</p>
          <h3>Your files stay yours</h3>
          <p>XML is processed for this request, not saved as a cloud project. Download and keep the workbook locally. No account is needed.</p>
          <p className={styles.small}>Current limits: 4 MB XML, 2,000 activities, 260 reporting weeks and 4 MB output. The runtime target is 60 seconds, not a guaranteed completion time.</p>
        </aside>
      </div>
    </section>
  );
}
