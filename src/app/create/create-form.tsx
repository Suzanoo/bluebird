"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import styles from "./create.module.css";

const MAX_BYTES = 4_000_000;
const XLSX_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
const weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

export default function CreateForm() {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [download, setDownload] = useState<string | null>(null);
  const [warnings, setWarnings] = useState(0);
  const controller = useRef<AbortController | null>(null);
  const downloadUrl = useRef<string | null>(null);

  useEffect(() => () => {
    controller.current?.abort();
    if (downloadUrl.current) URL.revokeObjectURL(downloadUrl.current);
  }, []);

  function clearResult() {
    if (downloadUrl.current) URL.revokeObjectURL(downloadUrl.current);
    downloadUrl.current = null;
    setDownload(null); setWarnings(0); setError("");
  }

  async function generate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (controller.current) return;
    clearResult();
    const form = new FormData(event.currentTarget);
    const file = form.get("xml");
    const method = form.get("method");
    if (!(file instanceof File) || file.size === 0) { setError("Select a non-empty XML file."); return; }
    if (file.size > MAX_BYTES) { setError("XML must be at most 4 MB."); return; }
    if (method !== "Equal" && method !== "Duration") { setError("Select Equal or Duration explicitly."); return; }
    const query = new URLSearchParams({ method, cutoff: String(form.get("cutoff")), distribution: String(form.get("distribution")) });
    const abort = new AbortController(); controller.current = abort; setPending(true);
    const timeout = setTimeout(() => abort.abort(), 65_000);
    try {
      const response = await fetch(`/api/progress/convert?${query}`, {
        method: "POST", headers: { "Content-Type": "application/xml" },
        body: file, signal: abort.signal, cache: "no-store",
      });
      if (!response.ok) {
        let message = response.status === 413 ? "The upload or workbook exceeds the current size limit."
          : response.status === 504 ? "Conversion exceeded the runtime target. Try a smaller schedule."
          : "Conversion failed. Check the file or try again.";
        if (response.headers.get("content-type")?.includes("application/json")) {
          const payload = await response.json();
          // Server exposes bounded validation messages only. React renders as text.
          if (typeof payload?.error?.message === "string") message = payload.error.message;
        }
        throw new Error(message);
      }
      if (!response.headers.get("content-type")?.startsWith(XLSX_TYPE)) throw new Error("The server did not return a workbook.");
      const blob = await response.blob();
      if (!blob.size || blob.size > MAX_BYTES) throw new Error("The workbook response was empty or too large.");
      const signature = new Uint8Array(await blob.slice(0, 4).arrayBuffer());
      if (signature[0] !== 0x50 || signature[1] !== 0x4b || signature[2] !== 3 || signature[3] !== 4) throw new Error("The workbook response was invalid.");
      downloadUrl.current = URL.createObjectURL(blob);
      setDownload(downloadUrl.current);
      setWarnings(Number(response.headers.get("X-Bluebird-Warnings")) || 0);
      const link = document.createElement("a");
      link.href = downloadUrl.current; link.download = "progress.xlsx";
      document.body.appendChild(link); link.click(); link.remove();
    } catch (cause) {
      if (abort.signal.aborted) setError("The request timed out or was cancelled. No download was completed. Server processing may still be finishing.");
      else setError(cause instanceof Error ? cause.message : "Could not reach the converter.");
    } finally {
      clearTimeout(timeout); controller.current = null; setPending(false);
    }
  }

  return (
    <form className={styles.form} onSubmit={generate} onChange={clearResult} aria-busy={pending}>
      <fieldset disabled={pending} className={styles.fields}>
        <legend>Schedule and configuration</legend>
        <label htmlFor="xml">Schedule XML</label>
        <input id="xml" name="xml" type="file" accept=".xml,application/xml,text/xml" required aria-describedby="file-help" />
        <p id="file-help" className={styles.small}>Export one project from P6 or Microsoft Project. Native .mpp files are not supported.</p>
        <label htmlFor="method">Initial weighting <span className={styles.required}>Required</span></label>
        <select id="method" name="method" defaultValue="" required>
          <option value="" disabled>Choose weighting</option><option>Equal</option><option>Duration</option>
        </select>
        <div className={styles.config}>
          <div><label htmlFor="cutoff">Weekly cutoff day</label><select id="cutoff" name="cutoff" defaultValue="Friday">{weekdays.map(day => <option key={day}>{day}</option>)}</select></div>
          <div><label htmlFor="distribution">Plan distribution</label><select id="distribution" name="distribution" defaultValue="auto"><option value="auto">Auto (Progress Studio rules)</option><option value="flat">Flat</option><option value="front">Front loaded</option><option value="back">Back loaded</option><option value="bell">Bell curve</option></select></div>
        </div>
        <p className={styles.small}>Cutoff defines the reporting week. Distribution shapes the Plan over time; it does not change activity weights.</p>
        <button className="button-link" type="submit">{pending ? "Generating…" : "Generate workbook"}</button>
      </fieldset>
      <p role="status" aria-live="polite">{pending ? "Processing your schedule and preparing the workbook…" : download ? "Workbook ready. Your download has started." : ""}</p>
      {error && <p role="alert" className={styles.error}>{error}</p>}
      {download && <div className={styles.result}><a className="text-link" href={download} download="progress.xlsx">Download workbook again ↓</a><p>Open in Desktop Excel. Enter weekly Actual in Main, press F9 and save your file.</p>{warnings > 0 && <p role="status">{warnings} activities have missing plan dates. See the workbook Guide before using the Plan.</p>}</div>}
    </form>
  );
}
