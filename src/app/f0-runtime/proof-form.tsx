"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import styles from "./proof.module.css";

const MAX_BYTES = 4_000_000;
const XLSX_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
const messages: Record<string, string> = {
  invalid_xml: "The file is not valid XML.",
  invalid_method: "Select Equal or Duration.",
  missing_upload: "Select a non-empty XML file.",
  upload_too_large: "XML must be at most 4 MB.",
  output_too_large: "Workbook exceeds the 4 MB proof limit.",
  unsupported_input: "This schedule or weighting is unsupported by the proof. Duration requires usable source durations.",
  busy: "Converter is busy. Please try again shortly.",
  timeout: "Conversion exceeded the proof time target. Please try a smaller schedule.",
};

export default function ProofForm() {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);
  const controller = useRef<AbortController | null>(null);
  const downloadUrl = useRef<string | null>(null);

  useEffect(() => () => {
    controller.current?.abort();
    if (downloadUrl.current) URL.revokeObjectURL(downloadUrl.current);
  }, []);

  async function generate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (controller.current) return;
    setError("");
    setDone(false);
    const form = new FormData(event.currentTarget);
    const file = form.get("xml");
    const method = form.get("method");
    if (!(file instanceof File) || file.size === 0) {
      setError(messages.missing_upload); return;
    }
    if (file.size > MAX_BYTES) {
      setError(messages.upload_too_large); return;
    }
    if (method !== "Equal" && method !== "Duration") {
      setError(messages.invalid_method); return;
    }
    const abort = new AbortController();
    controller.current = abort;
    setPending(true);
    // Client deadline is not a guarantee that server CPU work has stopped.
    const timeout = setTimeout(() => abort.abort(), 65_000);
    try {
      const response = await fetch(`/api/f0/convert?method=${method}`, {
        method: "POST", headers: { "Content-Type": "application/xml" },
        body: file, signal: abort.signal, cache: "no-store",
      });
      if (!response.ok) {
        let message = response.status === 413 ? messages.upload_too_large
          : response.status === 504 ? messages.timeout
          : "Conversion failed. Please check the file or try again.";
        if (response.headers.get("content-type")?.includes("application/json")) {
          const payload = await response.json();
          message = messages[payload?.error?.code] ?? message;
        }
        throw new Error(message);
      }
      if (!response.headers.get("content-type")?.startsWith(XLSX_TYPE)) {
        throw new Error("The server did not return a workbook.");
      }
      const blob = await response.blob();
      if (!blob.size || blob.size > MAX_BYTES) {
        throw new Error("The workbook response was empty or too large.");
      }
      const signature = new Uint8Array(await blob.slice(0, 4).arrayBuffer());
      if (signature[0] !== 0x50 || signature[1] !== 0x4b || signature[2] !== 3 || signature[3] !== 4) {
        throw new Error("The workbook response was invalid.");
      }
      if (downloadUrl.current) URL.revokeObjectURL(downloadUrl.current);
      downloadUrl.current = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = downloadUrl.current;
      link.download = "progress-f0.xlsx";
      document.body.appendChild(link);
      link.click();
      link.remove();
      setDone(true);
    } catch (cause) {
      setError(abort.signal.aborted ? "The request timed out or was cancelled. No download was completed."
        : cause instanceof Error ? cause.message : "Could not reach the converter.");
    } finally {
      clearTimeout(timeout);
      controller.current = null;
      setPending(false);
    }
  }

  return (
    <form onSubmit={generate} className={styles.form} aria-busy={pending}>
      <fieldset disabled={pending} className={styles.fields}>
        <label htmlFor="xml">Schedule XML</label>
        <input id="xml" name="xml" type="file" accept=".xml,application/xml,text/xml" required />
        <label htmlFor="method">Initial weighting</label>
        <select id="method" name="method" defaultValue="" required>
          <option value="" disabled>Choose weighting</option>
          <option value="Equal">Equal</option>
          <option value="Duration">Duration</option>
        </select>
        <button className="button-link" type="submit">{pending ? "Generating…" : "Generate"}</button>
      </fieldset>
      <p role="status" aria-live="polite">{pending ? "Processing your schedule…" : done ? "Workbook download started." : ""}</p>
      {error && <p role="alert" className={styles.error}>{error}</p>}
    </form>
  );
}
