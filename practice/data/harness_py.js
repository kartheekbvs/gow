/* ============================================================================
   PyDocs Dojo — Python execution harness (single source of truth).
   The Python source below runs identically inside Pyodide (browser worker)
   and CPython (scripts/verify_practice.py extracts and exec's it).
   RULES for editing the Python block:
     - never use the backtick character
     - never use the sequence ${   (it would break the JS template literal)
   ========================================================================== */
window.HARNESS_PY = String.raw`# ==== PyDocs Dojo test harness v1.0 ====
import json
import io
import contextlib
import traceback


def dojo_harness_version():
    return "dojo-harness-1.0"


class OpCountList(object):
    """A list stand-in that counts every element inspection.

    Used by efficiency tests: 'ops' is the number of times your algorithm
    looked at an element. Indexing costs 1 per element, iterating costs 1 per
    element, membership testing costs len(data) (a linear scan), and sorting
    is charged as len(data). len() itself is free.
    """
    __slots__ = ("_d", "ops")

    def __init__(self, data):
        self._d = list(data)
        self.ops = 0

    def __getitem__(self, i):
        if isinstance(i, slice):
            n = len(range(*i.indices(len(self._d))))
            self.ops += max(n, 1)
        else:
            self.ops += 1
        return self._d[i]

    def __iter__(self):
        for x in self._d:
            self.ops += 1
            yield x

    def __contains__(self, x):
        self.ops += len(self._d)
        return x in self._d

    def __len__(self):
        return len(self._d)

    def __eq__(self, other):
        if isinstance(other, OpCountList):
            other = other._d
        if isinstance(other, list):
            self.ops += len(self._d)
            return self._d == other
        return NotImplemented

    def __ne__(self, other):
        r = self.__eq__(other)
        if r is NotImplemented:
            return r
        return not r

    def __repr__(self):
        return repr(self._d)

    def index(self, x):
        self.ops += len(self._d)
        return self._d.index(x)

    def count(self, x):
        self.ops += len(self._d)
        return self._d.count(x)

    def sort(self, *a, **k):
        self.ops += len(self._d)
        self._d.sort(*a, **k)

    def copy(self):
        self.ops += len(self._d)
        return list(self._d)

    def to_list(self):
        return self._d


def _norm(v, _depth=0):
    """Recursively normalize a value so two 'equal' results compare equal
    regardless of set ordering, numpy/pandas wrappers, or float noise."""
    if _depth > 24:
        return "<max-depth>"
    if isinstance(v, bool):
        return ["<bool>", v]
    if v is None or isinstance(v, (int, str)):
        return v
    if isinstance(v, float):
        if v != v:
            return ["<nan>"]
        return round(v, 9)
    if isinstance(v, (set, frozenset)):
        return ["<set>", sorted((_norm(x, _depth + 1) for x in v), key=repr)]
    if isinstance(v, tuple):
        return ["<tuple>", [_norm(x, _depth + 1) for x in v]]
    if isinstance(v, list):
        return ["<list>", [_norm(x, _depth + 1) for x in v]]
    if isinstance(v, dict):
        return ["<dict>", sorted(
            ([_norm(k, _depth + 1), _norm(x, _depth + 1)] for k, x in v.items()),
            key=repr)]
    mod = getattr(type(v), "__module__", "") or ""
    if mod == "numpy" or mod.startswith("numpy."):
        import numpy as _np
        if isinstance(v, _np.ndarray):
            return ["<ndarray>", str(v.dtype), list(v.shape),
                    _norm(v.tolist(), _depth + 1)]
        if isinstance(v, _np.generic):
            return _norm(v.item(), _depth + 1)
    if mod == "pandas" or mod.startswith("pandas."):
        import pandas as _pd
        if isinstance(v, _pd.DataFrame):
            return ["<df>", sorted(
                ([_norm(c, _depth + 1), _norm(v[c].tolist(), _depth + 1)]
                 for c in v.columns), key=repr)]
        if isinstance(v, _pd.Series):
            return ["<series>", _norm(v.name, _depth + 1),
                    _norm(v.tolist(), _depth + 1)]
    try:
        return repr(v)
    except Exception:
        return "<unrepresentable>"


def _reconstruct(x):
    """Turn JSON-encoded test arguments into live Python / numpy / pandas
    objects. Special markers:
      {"__np__": {"data": [...], "dtype": "int64"}}      -> numpy array
      {"__df__": {"columns": [...], "rows": [[...]]}}    -> pandas DataFrame
      {"__ser__": {"values": [...], "name": "x"}}        -> pandas Series
      {"__opcount__": {"data": [...]}}                   -> OpCountList
      {"__set__": ["a", "b"]}                            -> set
      {"__tuple__": [1, 2]}                               -> tuple
      {"__repeat__": {"item": <any>, "times": n}}        -> item * n (str/list)
      {"__nan__": true} / {"__inf__": 1|-1}              -> float nan / inf
      {"__perm__": {"n": 9, "skip": 4}}                  -> deterministic shuffled 0..n minus skip
    """
    if isinstance(x, dict):
        if "__np__" in x:
            import numpy as _np
            spec = x["__np__"]
            return _np.array(spec["data"], dtype=spec.get("dtype"))
        if "__set__" in x:
            return set(_reconstruct(i) for i in x["__set__"])
        if "__tuple__" in x:
            return tuple(_reconstruct(i) for i in x["__tuple__"])
        if "__nan__" in x:
            return float("nan")
        if "__inf__" in x:
            return x["__inf__"] * float("inf")
        if "__perm__" in x:
            spec = x["__perm__"]
            n, skip = spec["n"], spec["skip"]
            seq = [i for i in range(n + 1) if i != skip]
            state = 123456789
            for i in range(len(seq) - 1, 0, -1):
                state = (state * 6364136223846793005
                         + 1442695040888963407) % 1152921504606846976
                j = state % (i + 1)
                seq[i], seq[j] = seq[j], seq[i]
            return seq
        if "__repeat__" in x:
            spec = x["__repeat__"]
            return _reconstruct(spec["item"]) * spec["times"]
        if "__df__" in x:
            import pandas as _pd
            spec = x["__df__"]
            return _pd.DataFrame(spec["rows"], columns=spec["columns"])
        if "__ser__" in x:
            import pandas as _pd
            spec = x["__ser__"]
            return _pd.Series(spec["values"], name=spec.get("name"))
        if "__opcount__" in x:
            return OpCountList(_reconstruct(x["__opcount__"]["data"]))
        return {k: _reconstruct(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_reconstruct(i) for i in x]
    return x


def _tail(s, n):
    s = str(s)
    return s if len(s) <= n else s[:n] + "\n... (truncated)"


def _display(v):
    """Human-readable one-line rendering for expected/got panels."""
    try:
        if isinstance(v, OpCountList):
            return repr(v.to_list())
        r = repr(v)
        return r if len(r) <= 500 else r[:500] + "..."
    except Exception:
        return "<unrepresentable>"


def run_tests(user_code, func_name, tests_json):
    """Execute user code, then run every test. Returns a JSON string:
    {"ok": bool, "stage": "compile"|"tests"|"harness", "error": str,
     "stdout": str,
     "results": [{"label": str, "hidden": bool, "passed": bool,
                  "call": str, "got": str, "expected": str,
                  "error": str, "stdout": str,
                  "ops": int, "budget": int}]}
    """
    results = []
    ns = {"__name__": "__main__"}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(user_code, ns)
    except Exception:
        return json.dumps({
            "ok": False, "stage": "compile",
            "error": _tail(traceback.format_exc(), 2000),
            "stdout": _tail(buf.getvalue(), 4000), "results": results})
    fn = ns.get(func_name)
    if not callable(fn):
        return json.dumps({
            "ok": False, "stage": "compile",
            "error": "Could not find a function named '" + str(func_name) +
                     "'. Keep the starter signature and implement it.",
            "stdout": _tail(buf.getvalue(), 4000), "results": results})
    try:
        tests = json.loads(tests_json)
    except Exception as e:
        return json.dumps({"ok": False, "stage": "harness",
                           "error": "Bad tests JSON: " + str(e),
                           "results": []})
    for t in tests:
        rec = {"label": t.get("label", "test"),
               "hidden": bool(t.get("hidden", False))}
        args = tuple(_reconstruct(a) for a in t.get("args", []))
        kwargs = {k: _reconstruct(v)
                  for k, v in (t.get("kwargs") or {}).items()}
        try:
            call_str = str(func_name) + "(" + ", ".join(
                [_display(a) for a in args] +
                [str(k) + "=" + _display(v) for k, v in kwargs.items()]) + ")"
            rec["call"] = (call_str if len(call_str) <= 300
                           else call_str[:300] + "...")
        except Exception:
            rec["call"] = str(func_name) + "(...)"
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                actual = fn(*args, **kwargs)
            rec["got"] = _display(actual)
            ok = _norm(actual) == _norm(_reconstruct(t["expected"]))
            used = None
            for a in list(args) + list(kwargs.values()):
                if hasattr(a, "ops"):
                    used = (used or 0) + a.ops
            if used is not None:
                rec["ops"] = used
            budget = t.get("max_ops")
            if ok and budget is not None:
                if used is None:
                    used = 0
                rec["budget"] = budget
                if used > budget:
                    ok = False
                    rec["error"] = ("Efficiency limit exceeded: your code "
                                    "inspected " + str(used) + " elements, "
                                    "budget is " + str(budget) + ".")
            rec["passed"] = ok
            if not ok and "error" not in rec:
                rec["expected"] = _display(_reconstruct(t["expected"]))
        except Exception:
            rec["passed"] = False
            rec["error"] = _tail(traceback.format_exc(limit=4), 1200)
        so = out.getvalue()
        if so:
            rec["stdout"] = _tail(so, 3000)
        results.append(rec)
    return json.dumps({"ok": True, "stage": "tests", "results": results})


def run_code(code):
    """Run a free-form code cell (concept demos, scratch cells). Returns a
    JSON string: {"ok": bool, "stdout": str, "error": str}"""
    ns = {"__name__": "__main__"}
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, ns)
        return json.dumps({"ok": True, "stdout": _tail(buf.getvalue(), 8000)})
    except Exception:
        return json.dumps({"ok": False, "stdout": _tail(buf.getvalue(), 4000),
                           "error": _tail(traceback.format_exc(limit=4),
                                          1500)})
`;
