"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import styles from "./create.module.css";

const MAX_BYTES = 4_000_000;
const XLSX_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
const weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
type AmountField = { identity: string; name: string; source: string; data_type: string; native_name: string };
type AmountPreview = {
  field: AmountField; valid: boolean; ordinary_count: number; milestone_count: number;
  positive_count: number; zero_count: number; ordinary_total: string;
  errors: string[]; warnings: string[];
  rows: { key: string; activity_id: string; name: string; raw_values: (string | null)[]; value: string | null; status: string }[];
};

export default function CreateForm() {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [download, setDownload] = useState<string | null>(null);
  const [warnings, setWarnings] = useState(0);
  const [fields, setFields] = useState<AmountField[] | null>(null);
  const [amountField, setAmountField] = useState("");
  const [preview, setPreview] = useState<AmountPreview | null>(null);
  const [sourceHash, setSourceHash] = useState("");
  const [method, setMethod] = useState("");
  const formRef = useRef<HTMLFormElement | null>(null);
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

  function resetAmount() {
    setFields(null); setAmountField(""); setPreview(null); setSourceHash("");
    if (method === "Amount") setMethod("");
  }

  async function inspectAmount(selected = "") {
    if (controller.current || !formRef.current) return;
    clearResult(); setPreview(null);
    if (method === "Amount") setMethod("");
    const file = new FormData(formRef.current).get("xml");
    if (!(file instanceof File) || !file.size || file.size > MAX_BYTES) {
      resetAmount(); setError("Select a non-empty XML file of at most 4 MB."); return;
    }
    const abort = new AbortController(); controller.current = abort; setPending(true);
    const timeout = setTimeout(() => abort.abort(), 65_000);
    try {
      const query = new URLSearchParams();
      if (selected) query.set("amount_field", selected);
      const response = await fetch(`/api/progress/amount-preview?${query}`, {
        method: "POST", headers: { "Content-Type": "application/xml" },
        body: file, signal: abort.signal, cache: "no-store",
      });
      if (!response.headers.get("content-type")?.includes("application/json")) {
        throw new Error("Amount inspection did not return a valid response. Try again.");
      }
      const payload = await response.json();
      if (!response.ok) throw new Error(payload?.error?.message || "Amount inspection failed.");
      setFields(payload.fields); setSourceHash(payload.source_hash); setPreview(payload.preview);
    } catch (cause) {
      setError(abort.signal.aborted ? "Amount inspection timed out or was cancelled. Try again."
        : cause instanceof Error ? cause.message : "Amount inspection failed.");
    } finally {
      clearTimeout(timeout); controller.current = null; setPending(false);
    }
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
    if (method !== "Equal" && method !== "Duration" && method !== "Amount") { setError("Select a weighting method explicitly."); return; }
    const query = new URLSearchParams({ method, cutoff: String(form.get("cutoff")), distribution: String(form.get("distribution")) });
    if (method === "Amount") {
      if (!preview?.valid || preview.field.identity !== amountField || !sourceHash) {
        setError("Validate the selected Amount field before Generate."); return;
      }
      query.set("amount_field", amountField); query.set("source_hash", sourceHash);
    }
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
    <form ref={formRef} className={styles.form} onSubmit={generate} onChange={clearResult} aria-busy={pending}>
      <fieldset disabled={pending} className={styles.fields}>
        <legend>Schedule and configuration</legend>
        <label htmlFor="xml">Schedule XML</label>
        <input id="xml" name="xml" type="file" accept=".xml,application/xml,text/xml" required aria-describedby="file-help" onChange={resetAmount} />
        <p id="file-help" className={styles.small}>Export one project from P6 or Microsoft Project. Native .mpp files are not supported.</p>
        <details className={styles.amount}>
          <summary>Use XML Amount weighting (optional)</summary>
          <p className={styles.small}>Select a declared numeric field containing allocated Contract Value on one consistent monetary basis. No currency conversion or automatic field selection.</p>
          <button type="button" onClick={() => { setAmountField(""); void inspectAmount(); }}>Inspect Amount fields</button>
          {fields?.length === 0 && <p role="status">No supported declared numeric Amount fields found. Equal and Duration remain available; no values are invented.</p>}
          {!!fields?.length && <>
            <label htmlFor="amount-field">XML Amount source</label>
            <select id="amount-field" value={amountField} onChange={event => {
              setAmountField(event.target.value); setPreview(null);
              if (method === "Amount") setMethod("");
            }}>
              <option value="">Choose a field explicitly</option>
              {fields.map((field, index) => <option key={`${field.identity}-${index}`} value={field.identity}>{field.name} / {field.native_name || field.source} [{field.identity}; {field.data_type}]</option>)}
            </select>
            <button type="button" disabled={!amountField} onClick={() => void inspectAmount(amountField)}>Validate selected Amount</button>
          </>}
          {preview && <div aria-live="polite">
            <p>{preview.valid ? "Amount ready — choose Amount below." : "Amount not ready. Correct the listed source values."}</p>
            <p className={styles.small}>Ordinary activities: {preview.ordinary_count}; positive: {preview.positive_count}; zero: {preview.zero_count}; milestones: {preview.milestone_count}. Ordinary weighting basis total (excludes milestones): {preview.ordinary_total}.</p>
            {preview.errors.length > 0 && <ul className={styles.error}>{preview.errors.map((message, i) => <li key={i}>{message}</li>)}</ul>}
            {preview.warnings.length > 0 && <ul className={styles.warning}>{preview.warnings.map((message, i) => <li key={i}>{message}</li>)}</ul>}
            <div className={styles.previewTable} tabIndex={0} role="region" aria-label="Amount values preview">
              <table><caption>Source Amount values (before Excel numeric conversion)</caption><thead><tr><th>Activity ID / Name</th><th>Raw Amount</th><th>Status</th></tr></thead><tbody>
                {preview.rows.map(row => <tr key={row.key}><td>{row.activity_id} / {row.name}</td><td>{row.raw_values.length ? row.raw_values.map(v => v === null ? "(missing)" : v === "" ? "(blank)" : v).join(" | ") : "(missing)"}</td><td>{row.status}</td></tr>)}
              </tbody></table>
            </div>
          </div>}
        </details>
        <label htmlFor="method">Initial weighting <span className={styles.required}>Required</span></label>
        <select id="method" name="method" value={method} onChange={event => setMethod(event.target.value)} required>
          <option value="" disabled>Choose weighting</option><option>Equal</option><option>Duration</option><option disabled={!preview?.valid || preview.field.identity !== amountField}>Amount</option>
        </select>
        <div className={styles.config}>
          <div><label htmlFor="cutoff">Weekly cutoff day</label><select id="cutoff" name="cutoff" defaultValue="Friday">{weekdays.map(day => <option key={day}>{day}</option>)}</select></div>
          <div><label htmlFor="distribution">Plan distribution</label><select id="distribution" name="distribution" defaultValue="auto"><option value="auto">Auto (Progress Studio rules)</option><option value="flat">Flat</option><option value="front">Front loaded</option><option value="back">Back loaded</option><option value="bell">Bell curve</option></select></div>
        </div>
        <p className={styles.small}>Cutoff defines the reporting week. Distribution shapes the Plan over time; it does not change activity weights.</p>
        <button className="button-link" type="submit">{pending ? "Generating…" : "Generate workbook"}</button>
      </fieldset>
      <p role="status" aria-live="polite">{pending ? "Processing your schedule…" : download ? "Workbook ready. Your download has started." : ""}</p>
      {error && <p role="alert" className={styles.error}>{error}</p>}
      {download && <div className={styles.result}><a className="text-link" href={download} download="progress.xlsx">Download workbook again ↓</a><p>Open in Desktop Excel. Enter weekly Actual in Main, press F9 and save your file.</p>{warnings > 0 && <p role="status">{warnings} input warnings. See the workbook Guide for missing plan dates or missing milestone Amount.</p>}</div>}
    </form>
  );
}
