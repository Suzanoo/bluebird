import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Workspace preview",
  description: "An empty Bluebird Project Workspace preview. No project has been created.",
};

export default function WorkspacePreview() {
  return (
    <div className="workspace-content">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Bluebird / Preview</p>
          <h1>Project workspace</h1>
        </div>
        <span className="preview-badge">Preview only</span>
      </div>
      <section className="empty-workspace" aria-labelledby="empty-title">
        <div className="empty-mark" aria-hidden="true">b.</div>
        <p className="small-label">An empty workspace</p>
        <h2 id="empty-title">Room to begin.</h2>
        <p>
          You’re viewing the Project Workspace shell.<br className="desktop-break" />
          No project has been created and no project data is stored here.
        </p>
        <Link className="text-link" href="/">
          <span aria-hidden="true">←</span> Back to Bluebird home
        </Link>
      </section>
    </div>
  );
}
