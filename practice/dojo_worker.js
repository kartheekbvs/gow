/* ============================================================================
   PyDocs Dojo — Python execution worker
   ----------------------------------------------------------------------------
   Owns the Pyodide runtime so the page never blocks: code and tests are sent
   as messages, results come back as JSON strings produced by the very same
   harness (practice/data/harness_py.js) that scripts/verify_practice.py uses
   in CPython. One runtime per tab: imported packages stay warm across runs.

   Protocol (main thread -> worker):
     { id, kind: "boot",  harness }                     -> { id, kind:"ready" }
     { id, kind: "code",  code, packages }              -> { id, kind:"result", result }
     { id, kind: "tests", code, func, tests, packages } -> { id, kind:"result", result }
     { id, kind: "reset" }                              -> { id, kind:"ready" }

   Every reply carries `ok` at the transport level; a rejected boot is fatal
   and reported as { id, kind:"error", error }.
   ========================================================================== */

const PYODIDE_VERSION = "0.26.4";
const PYODIDE_URL =
  "https://cdn.jsdelivr.net/pyodide/v" + PYODIDE_VERSION + "/full/pyodide.js";

let pyodide = null;
let harnessInstalled = false;
const loadedPackages = new Set();
let bootPromise = null;

self.onmessage = (ev) => {
  const msg = ev.data || {};
  const reply = (payload) => self.postMessage(Object.assign({ id: msg.id }, payload));
  // Boot must be serialized: later runs await the same promise.
  if (msg.kind === "boot") {
    boot(msg.harness).then(
      () => reply({ kind: "ready" }),
      (err) => reply({ kind: "error", error: String(err && err.message || err) })
    );
    return;
  }
  if (msg.kind === "reset") {
    hardReset().then(
      () => reply({ kind: "ready" }),
      (err) => reply({ kind: "error", error: String(err && err.message || err) })
    );
    return;
  }
  run(msg).then(
    (result) => reply({ kind: "result", result }),
    (err) => reply({
      kind: "result",
      result: JSON.stringify({
        ok: false, stage: "harness",
        error: "Worker failure: " + String(err && err.message || err),
        results: [], stdout: ""
      })
    })
  );
};

async function boot(harnessSource) {
  if (pyodide && harnessInstalled) return;
  if (!bootPromise) {
    bootPromise = (async () => {
      importScripts(PYODIDE_URL);
      pyodide = await loadPyodide();
      if (harnessSource) {
        pyodide.runPython(harnessSource);
        harnessInstalled = true;
      }
    })();
  }
  await bootPromise;
}

async function hardReset() {
  // A fresh runtime is the only fully reliable way to clear module state
  // after a user cell left globals dirty (e.g. redefined print or a type).
  pyodide = null;
  harnessInstalled = false;
  bootPromise = null;
  loadedPackages.clear();
}

async function ensurePackages(packages) {
  for (const name of packages || []) {
    if (name && !loadedPackages.has(name)) {
      await pyodide.loadPackage(name);
      loadedPackages.add(name);
    }
  }
}

async function run(msg) {
  await boot(null);
  await ensurePackages(msg.packages);
  const fn = pyodide.globals.get(msg.kind === "tests" ? "run_tests" : "run_code");
  try {
    if (msg.kind === "tests") {
      return fn(msg.code, msg.func, msg.tests);
    }
    return fn(msg.code);
  } finally {
    fn.destroy();
  }
}
