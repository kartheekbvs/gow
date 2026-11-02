#!/usr/bin/env python3
"""Calibrate intuition-track budgets: measure op counts of reference
solutions AND naive alternatives on the exact big hidden tests."""
import json
import sys

sys.path.insert(0, "scripts")
from verify_practice import load_harness  # noqa: E402

ns = load_harness()
rt = ns["run_tests"]

# ---------------- reference solutions ----------------
S = {}

S["missing_parts"] = (
    "def missing_parts(needed, available):\n"
    "    have = set(available)\n"
    "    return [p for p in needed if p not in have]\n")
S["missing_parts_naive"] = (
    "def missing_parts(needed, available):\n"
    "    out = []\n"
    "    for p in needed:\n"
    "        if p not in available:\n"
    "            out.append(p)\n"
    "    return out\n")

S["longest_safe"] = (
    "def longest_safe_stretch(rain, budget):\n"
    "    best = 0\n"
    "    total = 0\n"
    "    left = 0\n"
    "    for right in range(len(rain)):\n"
    "        total += rain[right]\n"
    "        while total > budget:\n"
    "            total -= rain[left]\n"
    "            left += 1\n"
    "        if right - left + 1 > best:\n"
    "            best = right - left + 1\n"
    "    return best\n")
S["longest_safe_naive"] = (
    "def longest_safe_stretch(rain, budget):\n"
    "    n = len(rain)\n"
    "    best = 0\n"
    "    for i in range(n):\n"
    "        total = 0\n"
    "        j = i\n"
    "        while j < n and total + rain[j] <= budget:\n"
    "            total += rain[j]\n"
    "            j += 1\n"
    "        if j - i > best:\n"
    "            best = j - i\n"
    "    return best\n")

S["missing_badge"] = (
    "def missing_badge(returns):\n"
    "    n = len(returns)\n"
    "    return n * (n + 1) // 2 - sum(returns)\n")
S["missing_badge_naive"] = (
    "def missing_badge(returns):\n"
    "    n = len(returns)\n"
    "    for cand in range(n + 1):\n"
    "        if cand not in returns:\n"
    "            return cand\n"
    "    return -1\n")

S["widest_tank"] = (
    "def widest_tank(heights):\n"
    "    left, right = 0, len(heights) - 1\n"
    "    best = 0\n"
    "    while left < right:\n"
    "        width = right - left\n"
    "        hl = heights[left]\n"
    "        hr = heights[right]\n"
    "        if hl < hr:\n"
    "            volume = hl * width\n"
    "            left += 1\n"
    "        else:\n"
    "            volume = hr * width\n"
    "            right -= 1\n"
    "        if volume > best:\n"
    "            best = volume\n"
    "    return best\n")
S["widest_tank_naive"] = (
    "def widest_tank(heights):\n"
    "    best = 0\n"
    "    n = len(heights)\n"
    "    for i in range(n):\n"
    "        for j in range(i + 1, n):\n"
    "            v = min(heights[i], heights[j]) * (j - i)\n"
    "            if v > best:\n"
    "                best = v\n"
    "    return best\n")

S["peak"] = (
    "def peak_of(temps):\n"
    "    lo, hi = 0, len(temps) - 1\n"
    "    while lo < hi:\n"
    "        mid = (lo + hi) // 2\n"
    "        if temps[mid] < temps[mid + 1]:\n"
    "            lo = mid + 1\n"
    "        else:\n"
    "            hi = mid\n"
    "    return lo\n")
S["peak_naive"] = (
    "def peak_of(temps):\n"
    "    for i in range(len(temps)):\n"
    "        if i > 0 and temps[i] < temps[i - 1]:\n"
    "            return i - 1\n"
    "    return len(temps) - 1\n")

S["meeting"] = (
    "def best_meeting_point(positions):\n"
    "    pts = sorted(positions)\n"
    "    n = len(pts)\n"
    "    median = pts[n // 2]\n"
    "    return sum(abs(p - median) for p in pts)\n")
S["meeting_naive"] = (
    "def best_meeting_point(positions):\n"
    "    best = None\n"
    "    for cand in set(positions):\n"
    "        total = sum(abs(p - cand) for p in positions)\n"
    "        if best is None or total < best:\n"
    "            best = total\n"
    "    return best\n")

# ---------------- the big tests ----------------
BLOCK5 = [1, 2, 1, 3, 2]
BLOCK8 = [4, 7, 2, 9, 1, 6, 8, 3]

BIG = [
    ("intu-ops-1 missing_parts",
     "missing_parts",
     [{"__opcount__": {"data": {"__repeat__": {"item": [3, 11, 500], "times": 20000}}}},
      {"__opcount__": {"data": {"__repeat__": {"item": [3, 11], "times": 20000}}}}],
     ["missing_parts", "missing_parts_naive"], 1),
    ("intu-ops-2 longest_safe_stretch",
     "longest_safe_stretch",
     [{"__opcount__": {"data": {"__repeat__": {"item": BLOCK5, "times": 40000}}}}, 50000],
     ["longest_safe", "longest_safe_naive"], 100),
    ("intu-ops-3 missing_badge",
     "missing_badge",
     [{"__opcount__": {"data": {"__perm__": {"n": 199999, "skip": 137}}}}],
     ["missing_badge", "missing_badge_naive"], 100),
    ("intu-ops-4 widest_tank",
     "widest_tank",
     [{"__opcount__": {"data": {"__repeat__": {"item": BLOCK8, "times": 25000}}}}],
     ["widest_tank", "widest_tank_naive"], 100),
]

for name, func, args, sols, naive_scale in BIG:
    print("=" * 64)
    print(name)
    for key in sols:
        use_args = args
        if "naive" in key and naive_scale > 1:
            # shrink repeated data by naive_scale so the naive run finishes
            use_args = json.loads(json.dumps(args))
            for a in use_args:
                if isinstance(a, dict) and "__opcount__" in a:
                    d = a["__opcount__"]["data"]
                    if isinstance(d, dict) and "__repeat__" in d:
                        d["__repeat__"]["times"] = max(1, d["__repeat__"]["times"] // naive_scale)
                    elif isinstance(d, dict) and "__perm__" in d:
                        d["__perm__"]["n"] = max(4, d["__perm__"]["n"] // naive_scale)
        test = {"label": "big", "args": use_args, "expected": None, "hidden": True, "max_ops": 10**9}
        res = json.loads(rt(S[key], func, json.dumps([test])))
        r = res["results"][0]
        got = r.get("got")
        ops = r.get("ops", "-")
        note = ""
        if "naive" in key and naive_scale > 1:
            note = "  (at 1/%d scale -> extrapolated ~%s ops at full size)" % (
                naive_scale, ops if ops == "-" else format(int(str(ops)) * naive_scale * naive_scale, ","))
        print("  %-24s got=%-14s ops=%s%s" % (key, got, ops, note))

# ---- small-case cross-checks: reference vs naive give the same answer ----
print("=" * 64)
print("cross-checks on small inputs")
import itertools  # noqa: E402

# widest_tank small
import random  # noqa: E402
random.seed(7)
for trial in range(300):
    h = [random.randint(0, 12) for _ in range(random.randint(2, 9))]
    t1 = {"label": "x", "args": [h], "expected": 0, "hidden": False}
    a = json.loads(rt(S["widest_tank"], "widest_tank", json.dumps([t1])))["results"][0]["got"]
    b = json.loads(rt(S["widest_tank_naive"], "widest_tank", json.dumps([t1])))["results"][0]["got"]
    assert a == b, (h, a, b)
print("widest_tank: 300 random cross-checks OK")

for trial in range(300):
    rain = [random.randint(0, 6) for _ in range(random.randint(0, 12))]
    budget = random.randint(0, 20)
    t1 = {"label": "x", "args": [rain, budget], "expected": 0, "hidden": False}
    a = json.loads(rt(S["longest_safe"], "longest_safe_stretch", json.dumps([t1])))["results"][0]["got"]
    b = json.loads(rt(S["longest_safe_naive"], "longest_safe_stretch", json.dumps([t1])))["results"][0]["got"]
    assert a == b, (rain, budget, a, b)
print("longest_safe_stretch: 300 random cross-checks OK")

# meeting point: median total vs brute force
for trial in range(300):
    pos = [random.randint(-50, 50) for _ in range(random.randint(1, 10))]
    t1 = {"label": "x", "args": [pos], "expected": 0, "hidden": False}
    a = json.loads(rt(S["meeting"], "best_meeting_point", json.dumps([t1])))["results"][0]["got"]
    b = json.loads(rt(S["meeting_naive"], "best_meeting_point", json.dumps([t1])))["results"][0]["got"]
    assert a == b, (pos, a, b)
print("best_meeting_point: 300 random cross-checks OK")

# peak: binary search vs linear on bitonic arrays
for trial in range(300):
    n = random.randint(1, 30)
    peak_at = random.randint(0, n - 1)
    rising = list(range(1, peak_at + 2))
    falling = list(range(peak_at + 1 - 1, 0, -1)) if peak_at + 1 - 1 > 0 else []
    arr = rising + falling
    t1 = {"label": "x", "args": [arr], "expected": 0, "hidden": False}
    a = json.loads(rt(S["peak"], "peak_of", json.dumps([t1])))["results"][0]["got"]
    b = json.loads(rt(S["peak_naive"], "peak_of", json.dumps([t1])))["results"][0]["got"]
    assert a == b == peak_at, (arr, a, b, peak_at)
print("peak_of: 300 random bitonic cross-checks OK")

# ---- peak finder on a large bitonic literal: measure op counts ----
print("=" * 64)
n = 4096
peak_idx = int(n * 0.7)
big_bitonic = (list(range(1, peak_idx + 2))
               + list(range(peak_idx, 0, -1)))
print("bitonic len:", len(big_bitonic), "peak at:", peak_idx,
      "value:", big_bitonic[peak_idx])
for key in ("peak", "peak_naive"):
    t1 = {"label": "big", "args": [{"__opcount__": {"data": big_bitonic}}], "expected": peak_idx, "hidden": True, "max_ops": 10**9}
    res = json.loads(rt(S[key], "peak_of", json.dumps([t1])))
    r = res["results"][0]
    print("  %-14s got=%-8s ops=%s" % (key, r.get("got"), r.get("ops", "-")))

# ---- meeting point big test: measure ----
print("=" * 64)
pos_block = [3, -7, 12, 100, -40, 55, 2, 8]
big_pos = pos_block * 25000  # 200k
for key in ("meeting", "meeting_naive"):
    t1 = {"label": "big", "args": [{"__opcount__": {"data": {"__repeat__": {"item": pos_block, "times": 25000}}}}],
          "expected": 0, "hidden": True, "max_ops": 10**9}
    res = json.loads(rt(S[key], "best_meeting_point", json.dumps([t1])))
    r = res["results"][0]
    print("  %-14s got=%-12s ops=%s" % (key, r.get("got"), r.get("ops", "-")))
