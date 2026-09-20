import type { Metadata } from "next";
import ProofForm from "./proof-form";

export const metadata: Metadata = { title: "F0 workbook proof" };

export default function RuntimeProof() {
  return (
    <section className="workspace-content" aria-labelledby="proof-title">
      <header className="page-heading">
        <div>
          <p className="eyebrow">F0 experiment</p>
          <h1 id="proof-title">Generate a Progress Workbook</h1>
        </div>
      </header>
      <p>Upload MSP or P6 XML (up to 4 MB), choose weighting, then download your workbook.</p>
      <ProofForm />
    </section>
  );
}
