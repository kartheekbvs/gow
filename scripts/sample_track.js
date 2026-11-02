/* PyDocs Dojo — SAMPLE track data (used as the style/quality reference by
   content authors and by scripts/verify_practice.py smoke runs). This file
   lives outside practice/data/ on purpose: it is documentation, not shipped
   content. Everything about it is production-grade on purpose — mimic it. */

window.PRACTICE_TRACKS.push(
{
  "id": "sample",
  "title": "Sample Track",
  "icon": "🧪",
  "tagline": "A miniature track that demonstrates the exact data format and quality bar.",
  "accent": "cyan",
  "engine": "python",
  "packages": [],
  "notebooks": [
    {
      "id": "sample-strings",
      "title": "String Reasoning (Sample)",
      "icon": "🔤",
      "level": "beginner",
      "order": 10,
      "conceptRef": "python-basics.html#s2",
      "blurb": "Think in runs and boundaries: two pointer-free passes beat one clever pass.",
      "cells": [
        {
          "type": "concept",
          "title": "Strings are immutable — plan your builds",
          "body": "<p>Every string operation in Python returns a <b>new</b> string; the original is never edited. That single fact should shape how you design solutions: if you find yourself writing <code>s += ch</code> inside a loop over a long input, you are secretly building thousands of intermediate strings, and each concatenation may copy everything built so far.</p><p>The reasoning habit to build: when a problem is about <i>transforming</i> a sequence, decide <b>where the answer gets assembled</b> before writing any loop. A list of pieces joined once at the end (<code>''.join(pieces)</code>) keeps the total work proportional to the output size. This is the same instinct that later becomes 'build the result array and write into it' in array problems.</p>",
          "demo": {
            "code": "pieces = []\nfor ch in 'abca':\n    if ch not in pieces:\n        pieces.append(ch)\nprint(''.join(pieces))\n\n# contrast: repeated concatenation copies the prefix every time\ns = ''\nfor ch in 'abca':\n    s = s + ch\nprint(s)"
          }
        },
        {
          "type": "concept",
          "title": "Counting with a dictionary — the frequency instinct",
          "body": "<p>A huge family of string questions ('are these anagrams?', 'first unique character', 'most common word') collapse into one move: <b>count how many times each character appears</b>, then answer the real question from the counts. The counts are a small table you can inspect in any order, which is why building the table first and asking questions second is almost always simpler than trying to answer while still scanning.</p><p>Notice the pattern-shape of the data: a dict maps 'thing I care about' → 'how many times I saw it'. Once the table exists, anagram checks become table comparisons, and 'first unique' becomes one more scan that consults the table.</p>",
          "demo": {
            "code": "def counts(s):\n    table = {}\n    for ch in s:\n        table[ch] = table.get(ch, 0) + 1\n    return table\n\nprint(counts('banana'))\nprint(counts('banana') == counts('nabana'))  # anagram test"
          }
        },
        {
          "type": "exercise",
          "exercise": {
            "id": "sample-strings-1",
            "title": "Run-Length Encoding",
            "difficulty": "easy",
            "tags": ["strings", "counting"],
            "statement": "<p>A sensor reports the same reading many times in a row. To store the log compactly you want <b>run-length encoding</b>: replace each maximal run of a repeated character with the character followed by the length of the run.</p><p>Implement <code>rle(s)</code> that returns the encoded string for a non-empty input.</p>",
            "constraints": [
              "1 <= len(s) <= 10,000",
              "s consists only of lowercase letters a-z",
              "runs longer than 9 still print their full count, e.g. 'a' * 12 encodes as 'a12'"
            ],
            "examples": [
              {"call": "rle('aaabbc')", "returns": "'a3b2c1'", "why": "three a's, then two b's, then one c"},
              {"call": "rle('z')", "returns": "'z1'", "why": "a single character is a run of length one"}
            ],
            "starter": "def rle(s):\n    \"\"\"Return the run-length encoding of s.\n\n    Every maximal run of a repeated character becomes\n    the character followed by the run length.\n    \"\"\"\n    pass\n",
            "func": "rle",
            "tests": [
              {"label": "single char", "args": ["a"], "expected": "a1", "hidden": false},
              {"label": "mixed runs", "args": ["aaabbc"], "expected": "a3b2c1", "hidden": false},
              {"label": "no repeats", "args": ["abcdef"], "expected": "a1b1c1d1e1f1", "hidden": true},
              {"label": "long run (count > 9)", "args": ["aaaaaaaaaaaa"], "expected": "a12", "hidden": true},
              {"label": "alternating", "args": ["ababab"], "expected": "a1b1a1b1a1b1", "hidden": true},
              {"label": "all same", "args": ["zzzzzzzzzzzzzzzzzzzz"], "expected": "z20", "hidden": true}
            ],
            "hints": [
              "You only need to know the CURRENT run's character and how many times you have seen it so far. What tells you a run has ended?",
              "Walk left to right keeping (current_char, count). When the next character differs — or the string ends — flush the finished run to your output pieces.",
              "Build a list of pieces like 'a3' and ''.join() them once at the end. Compare each character to the PREVIOUS one to detect run boundaries."
            ],
            "reasoning": "<p>The whole problem is one boundary question: <i>when does a run end?</i> A run ends exactly when the next character differs from the previous one, or when input runs out. If you track <code>prev</code> and <code>count</code>, each character costs O(1) work: compare, increment, or flush. That gives a single left-to-right pass with a constant amount of state — the signature of a clean linear scan. Collecting pieces and joining once also keeps the building of the output linear, because each piece is created exactly once and copied exactly once.</p>",
            "solution": "def rle(s):\n    pieces = []\n    prev = s[0]\n    count = 0\n    for ch in s:\n        if ch == prev:\n            count += 1\n        else:\n            pieces.append(prev + str(count))\n            prev = ch\n            count = 1\n    pieces.append(prev + str(count))\n    return ''.join(pieces)\n"
          }
        },
        {
          "type": "exercise",
          "exercise": {
            "id": "sample-strings-2",
            "title": "First Non-Repeating Character — With a Budget",
            "difficulty": "medium",
            "tags": ["strings", "hashing", "efficiency"],
            "statement": "<p>Given a string, return the index of the first character that appears exactly once in the whole string, or <code>-1</code> if there is none.</p><p><b>Efficiency matters here.</b> The input arrives as an <code>OpCountList</code> — a list stand-in that counts how many times your code inspects an element. Your algorithm may inspect elements at most <code>3 × len(s)</code> times. A naive 'for each character, scan the whole string to count it' approach inspects about n²/2 elements and will blow the budget on the big hidden test.</p>",
            "constraints": [
              "0 <= len(s) <= 100,000",
              "s consists of lowercase letters a-z",
              "inspection budget: at most 3 × len(s) element inspections (len() itself is free)"
            ],
            "examples": [
              {"call": "first_unique('aabbcdd')", "returns": "4", "why": "'c' at index 4 is the first character that appears exactly once"},
              {"call": "first_unique(\"aabb\")", "returns": "-1", "why": "every character repeats, so there is no answer"}
            ],
            "starter": "def first_unique(s):\n    \"\"\"Return the index of the first character that appears exactly\n    once, or -1 if none does. s is an OpCountList: inspecting an\n    element costs 1, membership testing costs len(s).\n    \"\"\"\n    pass\n",
            "func": "first_unique",
            "tests": [
              {"label": "example 1", "args": [{"__opcount__": {"data": "aabbcdd"}}], "expected": 4, "hidden": false},
              {"label": "all repeat", "args": [{"__opcount__": {"data": "aabb"}}], "expected": -1, "hidden": false},
              {"label": "empty string", "args": [{"__opcount__": {"data": ""}}], "expected": -1, "hidden": true},
              {"label": "single char", "args": [{"__opcount__": {"data": "x"}}], "expected": 0, "hidden": true},
              {"label": "unique at end", "args": [{"__opcount__": {"data": "aabbccdx"}}], "expected": 6, "hidden": true},
              {"label": "big input, budget enforced", "args": [{"__opcount__": {"data": {"__repeat__": {"item": "abcabcabcabcdefg", "times": 4000}}}}], "expected": -1, "hidden": true, "max_ops": 360000}
            ],
            "hints": [
              "Scanning the whole string once per character is what breaks the budget. How could you learn ALL the counts with just one pass?",
              "Two phases: first pass builds a counts table (dict). Second pass re-walks the string and returns the first index whose count is 1.",
              "for i, ch in enumerate(s): table[ch] = table.get(ch, 0) + 1 — then a second enumerate(s) loop checking table[ch] == 1. Two passes = 2n inspections, comfortably inside 3n."
            ],
            "reasoning": "<p>The budget turns an efficiency rumor into a measurable fact: nested scanning is ~n²/2 inspections, two flat passes are exactly 2n. The counts table is what makes the second pass cheap — after one honest walk through the data, every 'how many times does ch appear?' question is answered instantly instead of re-scanning. This build-the-table-then-consult-it move is one of the most reusable ideas in coding interviews; it is the same instinct behind memoization and index maps.</p>",
            "solution": "def first_unique(s):\n    counts = {}\n    for ch in s:\n        counts[ch] = counts.get(ch, 0) + 1\n    for i, ch in enumerate(s):\n        if counts[ch] == 1:\n            return i\n    return -1\n"
          }
        },
        {
          "type": "exercise",
          "exercise": {
            "id": "sample-strings-3",
            "title": "Predict: slicing semantics",
            "difficulty": "easy",
            "tags": ["strings", "slicing"],
            "mode": "predict",
            "statement": "<p>No coding here — read the snippet and predict what it prints. Getting good at executing code in your head (and knowing exactly when Python slices wrap around) is a genuine interview skill: many debugging questions are resolved by simulating two lines like these correctly.</p>",
            "code": "s = 'abcdef'\nprint(s[2:5])\nprint(s[-2:])\nprint(s[::2])\nprint(s[5:2:-1])",
            "options": [
              "cde / ef / ace / fed",
              "bcd / ef / bdf / fed",
              "cde / de / ace / fde",
              "cde / f / abc / ecd"
            ],
            "answer": 0,
            "explain": "<p>s[2:5] takes indices 2,3,4 → 'cde'. Negative start in s[-2:] means 'from the second-to-last to the end' → 'ef'. A step of 2 takes every second character starting at index 0 → 'ace'. For s[5:2:-1] the slice walks backwards from index 5 down to (not including) index 2 → indices 5,4,3 → 'fed'. The two habits that pay off: translate negative indices immediately (len + i), and read negative-step slices as 'start, stop-when-reached, direction'.</p>"
          }
        }
      ]
    }
  ]
}
);
