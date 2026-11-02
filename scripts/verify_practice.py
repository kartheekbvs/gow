#!/usr/bin/env python3
"""PyDocs Dojo content verifier.

Usage:
    python3 scripts/verify_practice.py                      # verify every practice/data/*.js
    python3 scripts/verify_practice.py path/to/track.js     # verify one file

What it checks
--------------
1. The Python harness (practice/data/harness_py.js) passes built-in self tests.
2. Each data file is strictly valid JSON inside the push(...) wrapper.
3. Schema: required fields, enums, id uniqueness, section links exist.
4. Pedagogy: every notebook has concept explanation cells; hints; reasoning.
5. CORRECTNESS: every reference solution must pass ALL of its tests
   (sample + hidden) when executed by the very same harness the browser uses.
6. Non-vacuity: a pass-only stub must FAIL at least one visible test, so tests
   can actually discriminate.
"""
import glob
import json
import os
import re
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "practice", "data")
HARNESS_JS = os.path.join(DATA_DIR, "harness_py.js")

DIFF_XP = {"easy": 10, "medium": 20, "hard": 35}
LEVELS = {"beginner", "intermediate", "advanced"}
ACCENTS = {"blue", "orange", "yellow", "green", "purple", "red", "cyan"}
PACKAGES = {"numpy", "pandas"}
XP_TOTAL = {}

_errors = []


def err(where, msg):
    _errors.append("[%s] %s" % (where, msg))


# ---------------------------------------------------------------- harness ----
def load_harness():
    src = open(HARNESS_JS, encoding="utf-8").read()
    if "String.raw`" not in src:
        raise SystemExit("harness_py.js: missing String.raw template")
    start = src.index("String.raw`") + len("String.raw`")
    end = src.rindex("`")
    code = src[start:end]
    if "`" in code:
        raise SystemExit("harness_py.js: backtick inside Python block")
    ns = {}
    exec(code, ns)
    return ns


def self_test_harness(ns):
    rt = ns["run_tests"]
    label = "HARNESS SELF-TEST"

    def run(solution, tests):
        return json.loads(rt(solution, tests[1], json.dumps(tests[0])))

    # 1. basic pass/fail
    tests = ([{"label": "t1", "args": [4], "expected": 16, "hidden": False}],
             "square")
    r = run("def square(x):\n    return x * x\n", tests)
    assert r["ok"] and r["results"][0]["passed"], "self-test 1 failed"

    # 2. wrong answer detected
    r = run("def square(x):\n    return x + x\n", tests)
    assert r["ok"] and not r["results"][0]["passed"], "self-test 2 failed"
    assert r["results"][0].get("expected") == "16", "self-test 2 expected panel"

    # 3. bool is strict (True != 1)
    t3 = ([{"label": "t3", "args": [], "expected": True, "hidden": False}],
          "f")
    r = run("def f():\n    return 1\n", t3)
    assert not r["results"][0]["passed"], "self-test 3 failed (bool vs int)"

    # 4. int/float leniency (2 == 2.0) and float noise absorbed
    t4 = ([{"label": "t4", "args": [0.1, 0.2], "expected": 0.3,
             "hidden": False}], "add")
    r = run("def add(a, b):\n    return a + b\n", t4)
    assert r["results"][0]["passed"], "self-test 4 failed (float noise)"

    # 5. set order-insensitivity (sets expressed via the __set__ marker)
    t5 = ([{"label": "t5", "args": ["abc"],
            "expected": {"__set__": ["a", "b", "c"]}, "hidden": False}],
          "letters")
    r = run("def letters(s):\n    return set(s)\n", t5)
    assert r["results"][0]["passed"], "self-test 5 failed (set order)"

    # 6. kwargs work
    t6 = ([{"label": "t6", "args": [1], "kwargs": {"k": 2}, "expected": 3,
             "hidden": False}], "sm")
    r = run("def sm(a, k=0):\n    return a + k\n", t6)
    assert r["results"][0]["passed"], "self-test 6 failed (kwargs)"

    # 7. numpy marker + ndarray comparison (dtype & shape aware)
    try:
        import numpy  # noqa: F401
        t7 = ([{"label": "t7",
                "args": [{"__np__": {"data": [[1, 2], [3, 4]],
                                     "dtype": "int64"}}],
                "expected": {"__np__": {"data": [[2, 4], [6, 8]],
                                        "dtype": "int64"}},
                "hidden": False}], "double")
        r = run("import numpy as np\ndef double(a):\n    return a * 2\n", t7)
        assert r["results"][0]["passed"], "self-test 7 failed (numpy)"
        r = run("import numpy as np\ndef double(a):\n    return a + a\n", t7)
        assert r["results"][0]["passed"], "self-test 7b failed (numpy)"
    except ImportError:
        print("  (numpy not installed locally - numpy self-tests skipped)")

    # 8. pandas marker + value comparison
    try:
        import pandas  # noqa: F401
        t8 = ([{"label": "t8",
                "args": [{"__df__": {"columns": ["a", "b"],
                                     "rows": [[1, 2], [3, 4]]}}],
                "expected": {"__df__": {"columns": ["a", "b"],
                                        "rows": [[1, 2], [3, 4]]}},
                "hidden": False}], "copy_df")
        r = run("import pandas as pd\ndef copy_df(df):\n    return df\n", t8)
        assert r["results"][0]["passed"], "self-test 8 failed (pandas)"
    except ImportError:
        print("  (pandas not installed locally - pandas self-tests skipped)")

    # 9. OpCountList: membership charges len, budget enforced
    t9 = ([{"label": "t9", "args": [{"__opcount__": {"data": [1, 2, 3, 4]}}],
            "expected": True, "hidden": False, "max_ops": 4}], "has")
    r = run("def has(xs):\n    return 3 in xs\n", t9)
    assert r["results"][0]["passed"], "self-test 9 failed (opcount in-budget)"
    assert r["results"][0].get("ops") == 4, "self-test 9 ops != 4"
    t9b = ([{"label": "t9b",
             "args": [{"__opcount__": {"data": [1, 2, 3, 4]}}],
             "expected": True, "hidden": False, "max_ops": 3}], "has")
    r = run("def has(xs):\n    return 3 in xs\n", t9b)
    assert not r["results"][0]["passed"], "self-test 9b failed (over budget)"
    t9c = ([{"label": "t9c",
             "args": [{"__opcount__": {"data": [1, 2, 3, 4]}}],
             "expected": 10, "hidden": False}], "sm")
    r = run("def sm(xs):\n    t = 0\n    for x in xs:\n        t += x\n    return t\n", t9c)
    assert r["results"][0]["passed"] and r["results"][0].get("ops") == 4, \
        "self-test 9c failed (iteration counts 4)"

    # 10. compile error reported, not crashed
    r = run("def broken(:\n", tests)
    assert not r["ok"] and r["stage"] == "compile", "self-test 10 failed"

    # 11. runtime exception captured per test
    r = run("def square(x):\n    return x[0]\n", tests)
    assert r["ok"] and not r["results"][0]["passed"] and "error" in r["results"][0], \
        "self-test 11 failed"

    # 12. run_code works and captures stdout
    rc = json.loads(ns["run_code"]("print('hi')\n42"))
    assert rc["ok"] and rc["stdout"].strip() == "hi", "self-test 12 failed"

    # 13. nan/inf markers + tuple/set recursion
    t13 = ([{"label": "t13", "args": [{"__nan__": True}],
             "expected": {"__nan__": True}, "hidden": False}], "pass_through")
    r = run("def pass_through(x):\n    return x\n", t13)
    assert r["ok"] and r["results"][0]["passed"], \
        "self-test 13 failed (nan marker)"
    t13b = ([{"label": "t13b", "args": [],
              "expected": {"__tuple__": [1, {"__set__": ["a", "b"]}]},
              "hidden": False}], "mk")
    r = run("def mk():\n    return (1, {'a', 'b'})\n", t13b)
    assert r["ok"] and r["results"][0]["passed"], \
        "self-test 13b failed (nested tuple/set markers)"

    print("  harness self-tests: OK (13 groups)")


# ------------------------------------------------------------------ files ----
def load_track(path):
    src = open(path, encoding="utf-8").read()
    marker = "window.PRACTICE_TRACKS.push("
    i = src.find(marker)
    if i < 0:
        raise ValueError("missing '%s' marker" % marker)
    start = src.find("(", i) + 1
    end = src.rfind(");")
    if end < 0:
        raise ValueError("missing closing ');'")
    payload = src[start:end].strip()
    return json.loads(payload)


def page_section_ids(page):
    p = os.path.join(ROOT, page)
    if not os.path.exists(p):
        return None
    html = open(p, encoding="utf-8").read()
    return set(re.findall(r'id="(s\d+)"', html))


_html_tag = re.compile(r"<[^>]+>")


def text_len(html):
    return len(_html_tag.sub("", html))


def check_exercise(ex, nb_id, seen_ids):
    where = ex.get("id", "<no id>")
    for field in ("id", "title", "difficulty", "tags", "statement"):
        if field not in ex or not ex[field]:
            err(where, "missing field '%s'" % field)
            return
    if ex["id"] in seen_ids:
        err(ex["id"], "duplicate exercise id (already seen)")
    seen_ids.add(ex["id"])
    if not ex["id"].startswith(nb_id + "-"):
        err(ex["id"], "exercise id must start with '%s-'" % nb_id)
    if ex["difficulty"] not in DIFF_XP:
        err(ex["id"], "difficulty must be one of %s" % sorted(DIFF_XP))
    tags = ex["tags"]
    if not (isinstance(tags, list) and 1 <= len(tags) <= 4
            and all(isinstance(t, str) and t for t in tags)):
        err(ex["id"], "tags must be a list of 1-4 non-empty strings")
    if text_len(ex["statement"]) < 80:
        err(ex["id"], "statement too short (<80 chars of text)")

    if ex.get("mode") == "predict":
        check_predict(ex)
        return

    for field in ("examples", "starter", "func", "tests", "hints",
                  "reasoning", "solution"):
        if field not in ex:
            err(ex["id"], "missing field '%s'" % field)
            return
    if "def " + ex["func"] + "(" not in ex["starter"].replace("  ", " "):
        # allow def with different spacing
        if not re.search(r"def\s+%s\s*\(" % re.escape(ex["func"]),
                         ex["starter"]):
            err(ex["id"], "starter does not define function '%s'"
                % ex["func"])
    if not re.search(r"def\s+%s\s*\(" % re.escape(ex["func"]), ex["solution"]):
        err(ex["id"], "solution does not define function '%s'" % ex["func"])
    if "pass" not in ex["starter"]:
        err(ex["id"], "starter should contain 'pass' so it runs unimplemented")
    exs = ex["examples"]
    if not (isinstance(exs, list) and len(exs) >= 1):
        err(ex["id"], "needs >=1 worked example")
    for e in exs:
        if not e.get("call") or "returns" not in e:
            err(ex["id"], "example needs 'call' and 'returns'")
    hints = ex["hints"]
    if not (isinstance(hints, list) and len(hints) == 3
            and all(isinstance(h, str) and len(h) >= 20 for h in hints)):
        err(ex["id"], "hints must be exactly 3 strings (>=20 chars each)")
    if text_len(ex["reasoning"]) < 120:
        err(ex["id"], "reasoning too short (<120 chars) — teach the WHY")
    cons = ex.get("constraints", [])
    if not isinstance(cons, list) or not all(isinstance(c, str) for c in cons):
        err(ex["id"], "constraints must be a list of strings")

    tests = ex["tests"]
    if not isinstance(tests, list) or len(tests) < 5:
        err(ex["id"], "needs >=5 tests")
        return
    visible = [t for t in tests if not t.get("hidden")]
    hidden = [t for t in tests if t.get("hidden")]
    if len(visible) < 2:
        err(ex["id"], "needs >=2 visible (sample) tests")
    if len(hidden) < 3:
        err(ex["id"], "needs >=3 hidden tests")
    labels = set()
    for t in tests:
        if not t.get("label"):
            err(ex["id"], "every test needs a label")
        if t["label"] in labels:
            err(ex["id"], "duplicate test label '%s'" % t["label"])
        labels.add(t["label"])
        if "expected" not in t:
            err(ex["id"], "test '%s' missing expected" % t.get("label"))
        if "args" not in t:
            err(ex["id"], "test '%s' missing args (use [] if none)" % t.get("label"))
    # hidden tests must not be identical to visible ones (anti-overfit)
    for h in hidden:
        for v in visible:
            if (h.get("args") == v.get("args")
                    and h.get("kwargs") == v.get("kwargs")):
                err(ex["id"], "hidden test '%s' duplicates visible test '%s' "
                              "(hidden tests must probe DIFFERENT inputs)"
                    % (h.get("label"), v.get("label")))


def check_predict(ex):
    if not (isinstance(ex.get("options"), list) and len(ex["options"]) == 4):
        err(ex["id"], "predict exercise needs exactly 4 options")
        return
    if not isinstance(ex.get("answer"), int) or not 0 <= ex["answer"] <= 3:
        err(ex["id"], "predict answer must be index 0-3")
    if not ex.get("code"):
        err(ex["id"], "predict exercise needs a 'code' snippet to reason about")
    if text_len(ex.get("explain", "")) < 100:
        err(ex["id"], "predict 'explain' too short (<100 chars)")


def run_solution_checks(ex, harness):
    rt = harness["run_tests"]
    tests_json = json.dumps(ex["tests"])
    try:
        res = json.loads(rt(ex["solution"], ex["func"], tests_json))
    except Exception:
        err(ex["id"], "solution crashed the harness:\n"
            + traceback.format_exc()[-400:])
        return
    if not res["ok"]:
        err(ex["id"], "solution does not even run: %s"
            % str(res.get("error", ""))[:300])
        return
    for r in res["results"]:
        if not r["passed"]:
            err(ex["id"], "solution FAILS test '%s': got=%s expected=%s %s"
                % (r["label"], r.get("got"), r.get("expected"),
                   r.get("error", "")[:150]))
    # non-vacuity: stub must fail at least one visible test
    stub = "def %s(*args, **kwargs):\n    pass\n" % ex["func"]
    res2 = json.loads(rt(stub, ex["func"], tests_json))
    if res2["ok"]:
        vis = [r for r in res2["results"] if not r["hidden"]]
        if all(r["passed"] for r in vis):
            err(ex["id"], "tests are vacuous: a pass-only stub passes every "
                          "visible test (make functions return checkable "
                          "values)")


def check_track(track, path, seen_track_ids, seen_nb_ids, seen_ex_ids,
                harness):
    fid = os.path.basename(path)
    for field in ("id", "title", "icon", "tagline", "accent", "engine",
                  "notebooks"):
        if field not in track:
            err(fid, "track missing field '%s'" % field)
            return
    if track["id"] in seen_track_ids:
        # same track split across files is allowed (parts merged by id),
        # but meta must match the first part
        first = seen_track_ids[track["id"]]
        for k in ("title", "icon", "accent"):
            if track[k] != first[k]:
                err(fid, "track '%s' meta mismatch on '%s' across files"
                    % (track["id"], k))
    else:
        seen_track_ids[track["id"]] = track
    if track["accent"] not in ACCENTS:
        err(fid, "accent must be one of %s" % sorted(ACCENTS))
    if track["engine"] != "python":
        err(fid, "engine must be 'python' (predict handled per exercise)")
    pkgs = track.get("packages", [])
    if not isinstance(pkgs, list) or any(p not in PACKAGES for p in pkgs):
        err(fid, "packages must be subset of %s" % sorted(PACKAGES))

    nbs = track["notebooks"]
    if not isinstance(nbs, list) or not nbs:
        err(fid, "track needs at least one notebook")
        return
    for nb in nbs:
        nbid = nb.get("id", "<no id>")
        if nb["id"] in seen_nb_ids:
            err(nbid, "duplicate notebook id")
        seen_nb_ids.add(nb["id"])
        for field in ("id", "title", "icon", "level", "order", "conceptRef",
                      "blurb", "cells"):
            if field not in nb:
                err(nbid, "notebook missing field '%s'" % field)
                continue
        if nb.get("level") not in LEVELS:
            err(nbid, "level must be one of %s" % sorted(LEVELS))
        if not isinstance(nb.get("order"), int):
            err(nbid, "order must be an int (sorts notebooks within track)")
        # conceptRef must point to a real page + section
        ref = nb.get("conceptRef", "")
        if ref:
            page = ref.split("#")[0]
            ids = page_section_ids(page)
            if ids is None:
                err(nbid, "conceptRef page '%s' does not exist" % page)
            elif "#" in ref and ref.split("#")[1] not in ids:
                err(nbid, "conceptRef section '%s' not found in %s"
                    % (ref.split("#")[1], page))
        cells = nb.get("cells", [])
        concepts = [c for c in cells if c.get("type") == "concept"]
        exercises = [c for c in cells if c.get("type") == "exercise"]
        if not concepts:
            err(nbid, "notebook has NO concept cells — every concept needs "
                      "an explanation (user requirement)")
        for c in concepts:
            if text_len(c.get("body", "")) < 200:
                err(nbid, "concept cell '%s' body too short (<200 chars) — "
                          "write a real explanation"
                    % c.get("title", "?"))
            d = c.get("demo")
            if d is not None:
                if not d.get("code"):
                    err(nbid, "concept demo needs 'code'")
                else:
                    try:
                        rc = json.loads(harness["run_code"](d["code"]))
                        if not rc["ok"]:
                            err(nbid, "concept demo '%s' CRASHES: %s"
                                % (c.get("title", "?"),
                                   str(rc.get("error", ""))[-300:]))
                        elif not rc.get("stdout", "").strip():
                            err(nbid, "concept demo '%s' prints nothing — "
                                      "demos must show output"
                                % c.get("title", "?"))
                    except Exception:
                        err(nbid, "concept demo '%s' could not be executed"
                            % c.get("title", "?"))
        if not exercises:
            err(nbid, "notebook has NO exercises")
        for c in exercises:
            ex = c.get("exercise")
            if not ex:
                err(nbid, "exercise cell missing 'exercise' object")
                continue
            check_exercise(ex, nb["id"], seen_ex_ids)
            if ex.get("mode") != "predict":
                run_solution_checks(ex, harness)
            XP_TOTAL[ex["id"]] = DIFF_XP.get(ex.get("difficulty"), 0)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args:
        files = [os.path.abspath(a) for a in args]
    else:
        files = sorted(glob.glob(os.path.join(DATA_DIR, "*.js")))
        files = [f for f in files
                 if not os.path.basename(f).startswith("harness")]
    if not files:
        print("no data files found")
        return 1

    print("loading harness:", os.path.relpath(HARNESS_JS, ROOT))
    harness = load_harness()
    self_test_harness(harness)
    print()

    seen_track_ids, seen_nb_ids, seen_ex_ids = {}, set(), set()
    total_nb, total_ex, total_concepts = 0, 0, 0
    for f in files:
        rel = os.path.relpath(f, ROOT)
        try:
            track = load_track(f)
        except json.JSONDecodeError as e:
            err(rel, "INVALID JSON: %s (line %s col %s)"
                % (e.msg, e.lineno, e.colno))
            continue
        except Exception as e:
            err(rel, "cannot load: %s" % e)
            continue
        before = len(_errors)
        check_track(track, f, seen_track_ids, seen_nb_ids, seen_ex_ids,
                    harness)
        nbs = len(track.get("notebooks", []))
        exs = sum(len([c for c in nb.get("cells", [])
                       if c.get("type") == "exercise"])
                  for nb in track.get("notebooks", []))
        cns = sum(len([c for c in nb.get("cells", [])
                       if c.get("type") == "concept"])
                  for nb in track.get("notebooks", []))
        total_nb += nbs
        total_ex += exs
        total_concepts += cns
        status = "OK" if len(_errors) == before else "ERRORS"
        print("%-34s track=%-18s notebooks=%-3d exercises=%-3d "
              "concepts=%-3d  %s"
              % (rel, track.get("id", "?"), nbs, exs, cns, status))

    print()
    print("=" * 70)
    print("TOTALS: %d tracks-parts, %d notebooks, %d concept cells, "
          "%d exercises, %d XP"
          % (len(files), total_nb, total_concepts, total_ex,
             sum(XP_TOTAL.values())))
    if _errors:
        print()
        print("ERRORS (%d):" % len(_errors))
        for e in _errors:
            print("  ✗", e)
        print()
        print("FIX THESE BEFORE SHIPPING.")
        return 1
    print("ALL CHECKS PASSED ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
