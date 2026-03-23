"""Generate python-basics.html — 15 deep-dive topics"""
import os

OUT = r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\python-basics.html"

def page_shell(title, subtitle, topics_count, toc_items, body):
    toc = "\n".join(
        f'<a class="toc-link" href="#s{i+1}"><span class="toc-num">{i+1:02d}</span>{t}</a>'
        for i, t in enumerate(toc_items)
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — PyDocs</title>
<meta name="description" content="{subtitle}">
<link rel="stylesheet" href="style.css">
<script src="shared.js" defer></script>
</head>
<body>
<div class="page-hero">
  <div class="breadcrumb"><a href="index.html">PyDocs</a> › {title}</div>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  <span class="topic-count">📚 {topics_count} Topics</span>
</div>
<div class="toc-container">
  <h2>Table of Contents</h2>
  <div class="toc-grid">{toc}</div>
</div>
{body}
<div class="page-nav">
  <a href="index.html">← Home</a>
  <a href="numpy.html">NumPy →</a>
</div>
</body></html>"""

def code_block(title, lang, code, output=None):
    out_html = ""
    if output:
        lines = "\n".join(f'<div class="out-line">{l}</div>' for l in output)
        out_html = f'<div class="output-block"><div class="out-label">Output</div>{lines}</div>'
    return f"""<div class="code-block">
  <div class="code-header">
    <span class="code-lang">● {lang}</span>
    <span class="code-title">{title}</span>
    <button class="copy-btn">Copy</button>
  </div>
  <div class="code-body"><pre><code>{code}</code></pre></div>
  {out_html}
</div>"""

def section(num, title, intro, content):
    return f"""<div class="content-section" id="s{num}">
  <div class="section-header">
    <span class="section-num">{num:02d}</span>
    <h2>{title}</h2>
  </div>
  <p class="section-intro">{intro}</p>
  {content}
</div>"""

def params(rows):
    trs = "".join(f"<tr><td>{p}</td><td>{t}</td><td>{d}</td><td>{desc}</td></tr>" for p,t,d,desc in rows)
    return f"""<div class="params-card"><div class="params-card-header">Parameters</div>
<table class="params-table"><thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>{trs}</tbody></table></div>"""

def callout(kind, icon, title, body):
    return f'<div class="callout {kind}"><span class="callout-icon">{icon}</span><div class="callout-body"><strong>{title}</strong><p>{body}</p></div></div>'

def ret(type_, desc):
    return f'<div class="return-box"><div class="ret-label">Returns</div><span class="ret-type">{type_}</span><div class="ret-desc">{desc}</div></div>'

# ── Section 1: Variables & Data Types ─────────────────────────────────────────
s1 = section(1, "Variables &amp; Data Types",
  "Python is dynamically typed — variables are just labels on objects. Every value has a type, an identity (memory address), and a value. Understanding types is foundational to all Python code.",
  code_block("All Literal Types + type() + isinstance() + id()", "Python",
"""# ── Integer ──────────────────────────────────────────────────────────
x = 42
big = 1_000_000          # underscores for readability (PEP 515)
neg = -17
binary = 0b1010          # 10  (binary literal)
octal  = 0o17            # 15  (octal literal)
hexval = 0xFF            # 255 (hex literal)

# ── Float ────────────────────────────────────────────────────────────
pi   = 3.14159265358979
sci  = 1.5e-3            # 0.0015
inf  = float('inf')
nan  = float('nan')

# ── String ───────────────────────────────────────────────────────────
s    = "hello"
raw  = r"C:\\Users\\no\\escape"
byte = b"raw bytes"
multi= """line one
line two"""

# ── Boolean ──────────────────────────────────────────────────────────
t, f = True, False      # bool is a subclass of int (True==1, False==0)
print(True + True)       # 2

# ── None ─────────────────────────────────────────────────────────────
nothing = None
print(nothing is None)   # True (use 'is', not ==)

# ── type() → exact type ───────────────────────────────────────────────
print(type(42))           # &lt;class 'int'&gt;
print(type(3.14))         # &lt;class 'float'&gt;
print(type("hi"))         # &lt;class 'str'&gt;
print(type(True))         # &lt;class 'bool'&gt;
print(type(None))         # &lt;class 'NoneType'&gt;

# ── isinstance() → type check (respects inheritance) ─────────────────
print(isinstance(True, int))      # True  (bool IS-A int)
print(isinstance(3.14, (int, float))) # True, checks multiple types

# ── id() → memory address (CPython implementation) ───────────────────
a = 256; b = 256
print(id(a) == id(b))    # True  (small int caching: -5 to 256)
a = 1000; b = 1000
print(id(a) == id(b))    # False (new objects above 256)

# ── Type Coercion ─────────────────────────────────────────────────────
print(int("42"))          # 42
print(int(3.99))          # 3   (truncates, does NOT round)
print(int("0xFF", 16))    # 255 (base conversion)
print(float("1.5e2"))     # 150.0
print(str(42))            # '42'
print(bool(0))            # False (falsy: 0, 0.0, '', [], {}, None)
print(bool(""))           # False
print(bool([1]))          # True""",
["2", "True", "<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'bool'>",
 "<class 'NoneType'>", "True", "True", "True", "False", "42", "3", "255",
 "150.0", "'42'", "False", "False", "True"]) +
callout("note","ℹ️","CPython Integer Caching","CPython caches small integers from -5 to 256. Variables pointing to same small int share identical id(). For larger integers, each variable gets a new object, so id() differs even if value is equal.") +
callout("warning","⚠️","int() truncates, doesn't round","<code>int(3.9)</code> → 3, NOT 4. Use <code>round(3.9)</code> → 4 if you need rounding. Also <code>int('-5')</code> works but <code>int('3.14')</code> raises ValueError — use <code>int(float('3.14'))</code>.")
)

# ── Section 2: String Methods ─────────────────────────────────────────────────
s2 = section(2, "String Methods",
  "Strings in Python are immutable sequences of Unicode characters. All string methods return a NEW string — the original is unchanged. Python has 47+ built-in string methods.",
  code_block("Case, Strip, Find, Replace", "Python",
"""s = "  Hello, World!  "

# Case methods
print(s.upper())          # '  HELLO, WORLD!  '
print(s.lower())          # '  hello, world!  '
print(s.title())          # '  Hello, World!  '
print(s.swapcase())       # '  hELLO, wORLD!  '
print(s.capitalize())     # '  hello, world!  '

# Stripping whitespace
print(s.strip())          # 'Hello, World!'
print(s.lstrip())         # 'Hello, World!  '
print(s.rstrip())         # '  Hello, World!'

# Find & Index (find returns -1 on miss; index raises ValueError)
t = "abcabcabc"
print(t.find("bc"))       # 1
print(t.rfind("bc"))      # 7
print(t.index("bc"))      # 1
print(t.count("bc"))      # 3

# Replace
print("aabbcc".replace("b","X"))      # 'aaXXcc'
print("aabbcc".replace("b","X", 1))   # 'aaXbcc' (max 1 replacement)

# Starts/Ends
print("hello".startswith("he"))   # True
print("world".endswith(("d","x")))# True  (tuple of options)

# Split & Join
parts = "a,b,c".split(",")       # ['a','b','c']
print(",".join(parts))            # 'a,b,c'
print("a  b".split())             # ['a','b']  (splits on any whitespace)
lines = "line1\\nline2\\nline3"
print(lines.splitlines())         # ['line1','line2','line3']
print("line1\\nline2\\nline3".splitlines(keepends=True)) # ['line1\\n','line2\\n','line3']

# Format
print("{} {}".format("Hello","World"))
print("{name} is {age}".format(name="Ada", age=36))
# f-strings (fastest, PEP 498)
name, age = "Turing", 41
print(f"{name} is {age} years old")
print(f"{3.14159:.2f}")           # '3.14'
print(f"{1000000:,}")             # '1,000,000'
print(f"{'center':^20}")          # '       center       '
print(f"{42:#010x}")              # '0x0000002a'""",
["'  HELLO, WORLD!  '","'  hello, world!  '","'  Hello, World!  '","'  hELLO, wORLD!  '",
 "'  hello, world!  '","'Hello, World!'","'Hello, World!  '","'  Hello, World!'",
 "1","7","1","3","'aaXXcc'","'aaXbcc'","True","True",
 "['a','b','c']","'a,b,c'","['a','b']","['line1','line2','line3']",
 "Hello World","Ada is 36","Turing is 41 years old","3.14","1,000,000","       center       ","0x0000002a"]) +
code_block("Padding, Encoding, Validation Methods", "Python",
"""# Padding
print("42".zfill(6))       # '000042'
print("hi".center(10,"*")) # '****hi****'
print("left".ljust(10,"-"))# 'left------'
print("right".rjust(10))   # '     right'

# Validation — all return bool
print("123".isdigit())     # True
print("12.3".isdigit())    # False  (no decimal point)
print("abc".isalpha())     # True
print("abc123".isalnum())  # True
print("   ".isspace())     # True
print("Title Case".istitle())  # True
print("UPPER".isupper())   # True
print("lower".islower())   # True

# Encoding
encoded = "héllo".encode("utf-8")   # b'h\\xc3\\xa9llo'
print(type(encoded))                  # &lt;class 'bytes'&gt;
decoded = encoded.decode("utf-8")    # 'héllo'

# String slicing: s[start:stop:step]
s = "abcdefghij"
print(s[2:7])      # 'cdefg'   start inclusive, stop exclusive
print(s[:4])       # 'abcd'
print(s[::2])      # 'acegi'   every other character
print(s[::-1])     # 'jihgfedcba'  reverse string
print(s[-3:])      # 'hij'  last 3 chars

# maketrans + translate (character mapping)
tbl = str.maketrans("aeiou", "12345")
print("hello world".translate(tbl))  # 'h2ll4 w4rld'

# partition (splits into 3-tuple)
print("key=value".partition("="))    # ('key', '=', 'value')""",
["'000042'","'****hi****'","'left------'","'     right'",
 "True","False","True","True","True","True","True","True",
 "<class 'bytes'>","'cdefg'","'abcd'","'acegi'","'jihgfedcba'","'hij'",
 "'h2ll4 w4rld'","('key', '=', 'value')"])
)

# ── Section 3: List Methods ────────────────────────────────────────────────────
s3 = section(3, "List Methods",
  "Lists are ordered, mutable, heterogeneous sequences. They are the workhorse of Python data structures. All mutating methods operate IN-PLACE and return None; non-mutating methods return new objects.",
  code_block("All List Methods + Builtins", "Python",
"""lst = [3, 1, 4, 1, 5, 9, 2, 6]

# Mutating methods (return None, modify in-place)
lst.append(7)           # [3,1,4,1,5,9,2,6,7]   — O(1)
lst.extend([8, 9])      # adds iterable elements  — O(k)
lst.insert(0, 0)        # insert at index 0       — O(n)
lst.remove(1)           # removes first 1         — O(n)
popped = lst.pop()      # removes & returns last  — O(1)
popped2 = lst.pop(2)    # removes & returns index 2 — O(n)
lst.sort()              # in-place sort (Timsort) — O(n log n)
lst.sort(reverse=True)  # descending
lst.sort(key=lambda x: -x)  # custom key
lst.reverse()           # in-place reverse        — O(n)
lst.clear()             # empties list            — O(n)

# Non-mutating methods (return value, original unchanged)
lst = [3, 1, 4, 1, 5, 9]
idx = lst.index(4)      # 2  — O(n), raises ValueError if not found
cnt = lst.count(1)      # 2  — O(n)
cpy = lst.copy()        # shallow copy            — O(n)

# Built-in functions on lists
print(len(lst))         # 6
print(min(lst))         # 1
print(max(lst))         # 9
print(sum(lst))         # 23
print(sorted(lst))      # [1,1,3,4,5,9]  new list, original unchanged
print(sorted(lst, key=lambda x:-x))  # [9,5,4,3,1,1] descending

# List Comprehensions
squares   = [x**2 for x in range(1, 6)]          # [1,4,9,16,25]
evens     = [x for x in range(10) if x % 2 == 0]  # [0,2,4,6,8]
flat      = [x for row in [[1,2],[3,4]] for x in row]  # [1,2,3,4]
matrix    = [[i*j for j in range(1,4)] for i in range(1,4)]

# Unpacking
a, b, c = [1, 2, 3]
first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)  # 1 [2, 3, 4] 5

# Operators
print([1, 2] + [3, 4])  # [1, 2, 3, 4]
print([0] * 5)           # [0, 0, 0, 0, 0]
print(3 in [1, 2, 3])    # True""",
["6","1","9","23","[1, 1, 3, 4, 5, 9]","[9, 5, 4, 3, 1, 1]",
 "1 [2, 3, 4] 5","[1, 2, 3, 4]","[0, 0, 0, 0, 0]","True"])
)

# ── Section 4: Dictionary Methods ─────────────────────────────────────────────
s4 = section(4, "Dictionary Methods",
  "Dictionaries are hash maps — O(1) average for get/set/delete. Since Python 3.7 they preserve insertion order. Keys must be hashable (immutable).",
  code_block("All Dict Methods + Comprehensions + Merging", "Python",
"""d = {"a": 1, "b": 2, "c": 3}

# Basic access
print(d["a"])             # 1       (raises KeyError if missing)
print(d.get("z", 0))     # 0       (safe, returns default)
d.setdefault("d", 4)     # adds "d":4 only if "d" missing

# Views (live, reflect mutations)
print(d.keys())           # dict_keys(['a','b','c','d'])
print(d.values())         # dict_values([1,2,3,4])
print(d.items())          # dict_items([('a',1),('b',2),('c',3),('d',4)])

# Mutating
d.update({"e": 5, "a": 99})  # merges; existing keys overwritten
removed = d.pop("c")          # removes 'c', returns 3
last = d.popitem()            # removes & returns last (k,v) pair in 3.7+
copied = d.copy()             # shallow copy
d.clear()                     # empties dict

# fromkeys — create dict with same default value
keys = ["x", "y", "z"]
empty = dict.fromkeys(keys, 0)    # {'x':0, 'y':0, 'z':0}
none_vals = dict.fromkeys(keys)   # {'x':None,'y':None,'z':None}

# Dict Comprehension
sq = {x: x**2 for x in range(1, 6)}       # {1:1, 2:4, 3:9, 4:16, 5:25}
filtered = {k: v for k, v in sq.items() if v > 9}  # {4:16, 5:25}

# Python 3.9+ merge operator
a = {"x": 1, "y": 2}
b = {"y": 99, "z": 3}
merged = a | b          # {'x':1, 'y':99, 'z':3}  new dict
a |= b                  # update a in-place

# Collections extras
from collections import defaultdict, OrderedDict, Counter

# defaultdict — missing keys get default value automatically
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
print(dd)  # defaultdict(<class 'list'>, {'fruits': ['apple', 'banana']})

# Counter — counts hashable items
c = Counter("abracadabra")
print(c.most_common(3))       # [('a', 5), ('b', 2), ('r', 2)]
print(c["a"])                 # 5
c2 = Counter({"a": 1, "b": 3})
print(c + c2)                 # combined counts
print(c - c2)                 # subtract (keeps only positives)""",
["1","0","dict_keys(['a','b','c','d'])","{'x':0,'y':0,'z':0}",
 "{1:1,2:4,3:9,4:16,5:25}","{4:16,5:25}","{'x':1,'y':99,'z':3}",
 "defaultdict(<class 'list'>, {'fruits': ['apple', 'banana']})","[('a', 5), ('b', 2), ('r', 2)]","5"])
)

# ── Section 5: Set Methods ─────────────────────────────────────────────────────
s5 = section(5, "Set Methods",
  "Sets are unordered collections of unique hashable elements backed by a hash table. O(1) add/remove/membership. Use frozenset for immutable variant.",
  code_block("All Set Operations", "Python",
"""s = {1, 2, 3, 4, 5}

# Mutating methods
s.add(6)            # adds single element       O(1)
s.remove(6)         # removes; raises KeyError if missing
s.discard(99)       # removes; NO error if missing
p = s.pop()         # removes & returns arbitrary element
s2 = s.copy()       # shallow copy

# Set algebra (return NEW set)
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A | B)                # {1,2,3,4,5,6}  union
print(A.union(B))           # same
print(A & B)                # {3,4}          intersection
print(A.intersection(B))    # same
print(A - B)                # {1,2}          difference (in A not B)
print(A.difference(B))      # same
print(A ^ B)                # {1,2,5,6}      symmetric diff
print(A.symmetric_difference(B))  # same

# Relationship tests
print({1,2}.issubset({1,2,3}))    # True
print({1,2,3}.issuperset({1,2}))  # True
print({1,2}.isdisjoint({3,4}))    # True (no elements in common)

# frozenset — hashable set (can be dict key)
fs = frozenset([1,2,3])
d = {fs: "frozen"}   # legal, frozenset is hashable

# Set comprehension
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # {0, 4, 16, 36, 64}

# Update methods (in-place equivalents)
A.update(B)          # A = A | B  in-place
A.intersection_update(B)   # A = A & B  in-place
A.difference_update(B)     # A = A - B  in-place
A.symmetric_difference_update(B)  # A = A^B in-place""",
["{1,2,3,4,5,6}","{3,4}","{1,2}","{1,2,5,6}","True","True","True","{0,4,16,36,64}"])
)

# ── Section 6: Tuple Methods ─────────────────────────────────────────────────
s6 = section(6, "Tuple Methods",
  "Tuples are immutable ordered sequences. They only have 2 methods but are widely used for multiple return values, dictionary keys, and named tuples.",
  code_block("Tuple Methods + namedtuple + Unpacking", "Python",
"""t = (3, 1, 4, 1, 5, 9, 2, 6, 5)

# Only 2 methods
print(t.count(1))    # 2  — count occurrences
print(t.index(5))    # 4  — first occurrence index (raises ValueError if missing)

# Named Tuples (like lightweight classes)
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)      # 3 4
print(p[0], p[1])    # 3 4  (still supports indexing)
print(p._asdict())   # {'x': 3, 'y': 4}
p2 = p._replace(x=10)   # immutable — returns new
print(p2)            # Point(x=10, y=4)

# Python 3.6+ typed variant
from typing import NamedTuple

class Color(NamedTuple):
    red:   int
    green: int
    blue:  int = 0   # default value

c = Color(255, 128)
print(c)             # Color(red=255, green=128, blue=0)

# Tuple Unpacking
a, b, c = (1, 2, 3)
first, *rest = (10, 20, 30, 40)
print(first, rest)   # 10 [20, 30, 40]
*head, last = (10, 20, 30, 40)
print(head, last)    # [10, 20, 30] 40

# Nested unpacking
(a, b), c = (1, 2), 3
print(a, b, c)       # 1 2 3

# Tuple vs List
# Tuple: immutable, hashable, slightly faster iteration
# List:  mutable, not hashable as dict key
# When to use tuple: multiple return values, fixed records, dict keys
print((1,2,3) == [1,2,3])  # False (different types)""",
["2","4","3 4","3 4","{'x': 3, 'y': 4}","Point(x=10, y=4)","Color(red=255, green=128, blue=0)","10 [20, 30, 40]","[10, 20, 30] 40","1 2 3","False"])
)

# ── Section 7: Control Flow ───────────────────────────────────────────────────
s7 = section(7, "Control Flow",
  "Python control flow: if/elif/else, ternary operators, for/while loops, break/continue/pass, loop else clause, and Python 3.10+ match/case structural pattern matching.",
  code_block("if / elif / else / ternary / match-case", "Python",
"""# ── if / elif / else ─────────────────────────────────────────────────
score = 87
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print(grade)   # 'B'

# ── Ternary (conditional expression) ──────────────────────────────────
x = 10
parity = "even" if x % 2 == 0 else "odd"
print(parity)  # 'even'

# ── for loop with range ────────────────────────────────────────────────
for i in range(0, 10, 2):   # start, stop(excl), step
    print(i, end=" ")        # 0 2 4 6 8
print()

# ── enumerate — index + value ──────────────────────────────────────────
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# ── while + break / continue ──────────────────────────────────────────
n = 0
while n < 5:
    n += 1
    if n == 3:
        continue   # skip 3
    if n == 5:
        break      # stop at 4
    print(n, end=" ")
print()  # 1 2 4

# ── Loop else (runs if loop completes without break) ───────────────────
for i in range(2, 10):
    for j in range(2, i):
        if i % j == 0:
            print(f"{i} = {j} * {i//j}")
            break
    else:            # no break → i is prime
        print(f"{i} is prime")

# ── pass — placeholder ────────────────────────────────────────────────
def todo():
    pass   # syntactically required body

# ── match / case (Python 3.10+) ────────────────────────────────────────
def http_status(code):
    match code:
        case 200: return "OK"
        case 404: return "Not Found"
        case 500 | 503: return "Server Error"  # OR pattern
        case int(c) if c >= 400: return f"Client Error {c}"
        case _: return "Unknown"

print(http_status(200))   # OK
print(http_status(404))   # Not Found
print(http_status(418))   # Client Error 418""",
["'B'","even","0 2 4 6 8","1. apple","2. banana","3. cherry","1 2 4","2 is prime","3 is prime","5 is prime","7 is prime","4 = 2 * 2","6 = 2 * 3","8 = 2 * 4","9 = 3 * 3","OK","Not Found","Client Error 418"])
)

# ── Section 8: Functions ──────────────────────────────────────────────────────
s8 = section(8, "Functions",
  "Functions are first-class objects in Python. They support default parameters, *args/**kwargs, keyword-only and positional-only arguments, closures, and lambda expressions.",
  code_block("def / *args / **kwargs / lambda / builtins", "Python",
"""# ── Basic function ─────────────────────────────────────────────────────
def greet(name, greeting="Hello"):   # default parameter
    return f"{greeting}, {name}!"

print(greet("Ada"))                  # Hello, Ada!
print(greet("Turing", "Hi"))         # Hi, Turing!

# ── *args — variable positional arguments ─────────────────────────────
def total(*args):
    return sum(args)

print(total(1, 2, 3, 4, 5))   # 15

# ── **kwargs — variable keyword arguments ─────────────────────────────
def show_info(**kwargs):
    for k, v in kwargs.items():
        print(f"  {k}: {v}")

show_info(name="Ada", year=1815, country="UK")

# ── Keyword-only args (after bare *) ───────────────────────────────────
def make_tag(content, *, tag="p", cls=""):
    return f"&lt;{tag} class='{cls}'&gt;{content}&lt;/{tag}&gt;"

print(make_tag("Hello", tag="h1"))   # &lt;h1 class=''&gt;Hello&lt;/h1&gt;

# ── Positional-only args (before /, Python 3.8+) ───────────────────────
def rect(w, h, /):   # w and h CANNOT be passed as keyword args
    return w * h

print(rect(3, 4))    # 12
# rect(w=3, h=4)     # TypeError!

# ── Lambda — anonymous single-expression function ─────────────────────
double = lambda x: x * 2
add    = lambda a, b: a + b
print(double(5))     # 10
print(add(3, 4))     # 7

# Lambdas with builtins
nums = [3, -1, 4, -1, 5, -9]
print(sorted(nums, key=abs))          # [-1,-1,3,4,5,-9]
print(list(map(lambda x: x**2, [1,2,3,4])))  # [1,4,9,16]
print(list(filter(lambda x: x>0, nums)))      # [3,4,5]

# ── Built-in higher-order functions ───────────────────────────────────
from functools import reduce
print(reduce(lambda a,b: a*b, [1,2,3,4,5]))   # 120 (5!)

# zip — pair up iterables
names  = ["Alice", "Bob", "Carol"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# any / all
print(any([False, True, False]))   # True
print(all([True, True, False]))    # False
print(any(x > 90 for x in scores))  # True  (generator — lazy)

# enumerate / zip / min / max with key
pairs = list(zip(names, scores))
print(max(pairs, key=lambda p: p[1]))  # ('Alice', 95)""",
["Hello, Ada!","Hi, Turing!","15","name: Ada","year: 1815","country: UK",
 "12","10","7","[-1,-1,3,4,5,-9]","[1,4,9,16]","[3,4,5]","120",
 "Alice: 95","Bob: 87","Carol: 92","True","False","True","('Alice', 95)"])
)

# ── Section 9: File I/O ───────────────────────────────────────────────────────
s9 = section(9, "File I/O",
  "Python's open() function provides full file read/write/append capabilities. The 'with' statement ensures files are always closed even on exceptions.",
  code_block("open() / 'with' / all modes / pathlib", "Python",
"""import os, pathlib

# ── open() modes overview ─────────────────────────────────────────────
# 'r'   read text (default)  — FileNotFoundError if missing
# 'w'   write text           — creates or truncates
# 'a'   append text          — creates or appends
# 'x'   exclusive creation   — FileExistsError if exists
# 'r+'  read+write (no truncate)
# 'w+'  read+write (truncates)
# 'b'   binary mode suffix (rb, wb, ab)
# 't'   text mode (default, auto-encodes newlines)

# ── Writing a file ────────────────────────────────────────────────────
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("Line 1\\n")
    f.write("Line 2\\n")
    f.writelines(["Line 3\\n", "Line 4\\n"])  # write list of strings
    pos = f.tell()           # current byte position
    print("After write, pos:", pos)

# ── Reading a file ────────────────────────────────────────────────────
with open("demo.txt", "r", encoding="utf-8") as f:
    content  = f.read()          # entire file as string
    # f.seek(0)                  # reset to start
    # line   = f.readline()      # single line (includes \\n)
    # lines  = f.readlines()     # list of all lines (includes \\n)

# Iterate line by line (memory-efficient)
with open("demo.txt") as f:
    for i, line in enumerate(f, 1):
        print(f"  {i}: {line.rstrip()}")

# ── pathlib — modern OOP interface ────────────────────────────────────
p = pathlib.Path("demo.txt")
print(p.name)          # 'demo.txt'
print(p.stem)          # 'demo'
print(p.suffix)        # '.txt'
print(p.exists())      # True
print(p.is_file())     # True
print(p.stat().st_size)# file size in bytes

# One-liner read/write
text = p.read_text(encoding="utf-8")    # entire file as string
p.write_text("New content", encoding="utf-8")

# Path operations
cwd = pathlib.Path.cwd()
child = cwd / "subdir" / "file.txt"    # / operator builds paths
print(child.parent)    # the subdir directory

# Glob patterns
txt_files = list(cwd.glob("*.txt"))
all_py    = list(cwd.rglob("**/*.py")) # recursive

# Cleanup
os.remove("demo.txt")""",
["After write, pos: 28","  1: Line 1","  2: Line 2","  3: Line 3","  4: Line 4",
 "'demo.txt'","'demo'","'.txt'","True","True"])
)

# ── Section 10: Exception Handling ────────────────────────────────────────────
s10 = section(10, "Exception Handling",
  "Python uses structured exception handling with try/except/else/finally. All exceptions inherit from BaseException. Creating custom exceptions by subclassing Exception is best practice.",
  code_block("try/except/else/finally + Custom Exceptions + Built-ins", "Python",
"""import sys, traceback

# ── Basic try/except/else/finally ────────────────────────────────────
def safe_divide(a, b):
    try:
        result = a / b            # might raise ZeroDivisionError
    except ZeroDivisionError as e:
        print(f"Error: {e}")      # Error: division by zero
        return None
    except (TypeError, ValueError) as e:
        print(f"Type error: {e}")
        return None
    else:
        # runs ONLY if no exception occurred
        print("Success!")
        return result
    finally:
        # ALWAYS runs (even if return in try/except)
        print("cleanup")

print(safe_divide(10, 2))   # Success! cleanup 5.0
print(safe_divide(10, 0))   # Error: division by zero cleanup None

# ── except Exception as e — access the exception ──────────────────────
try:
    int("not_a_number")
except Exception as e:
    print(type(e).__name__)   # ValueError
    print(e)                  # invalid literal for int()...
    print(e.args)             # ("invalid literal for int()...",)

# ── raise — re-raise or raise new ────────────────────────────────────
try:
    raise ValueError("custom message")
except ValueError:
    raise   # re-raise same exception (preserves traceback)

# ── Custom Exception classes ──────────────────────────────────────────
class AppError(Exception):
    """Base class for application errors."""
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field   = field
        super().__init__(f"Validation failed on '{field}': {message}")

try:
    raise ValidationError("email", "must contain @")
except ValidationError as e:
    print(e)           # Validation failed on 'email': must contain @
    print(e.field)     # email

# ── Exception Hierarchy (key classes) ─────────────────────────────────
# BaseException
# ├─ SystemExit         (sys.exit())
# ├─ KeyboardInterrupt  (Ctrl+C)
# └─ Exception
#    ├─ ArithmeticError: ZeroDivisionError, OverflowError, FloatingPointError
#    ├─ LookupError:     IndexError, KeyError
#    ├─ ValueError, TypeError, AttributeError, RuntimeError
#    ├─ OSError:         FileNotFoundError, PermissionError, IsADirectoryError
#    └─ StopIteration   (end of iteration)

# ── traceback module ──────────────────────────────────────────────────
import traceback
try:
    1/0
except ZeroDivisionError:
    tb_str = traceback.format_exc()  # string with full traceback
    # traceback.print_exc()          # print to stderr""",
["Success!","cleanup","5.0","Error: division by zero","cleanup","None",
 "ValueError","Validation failed on 'email': must contain @","email"])
)

# ── Section 11: Comprehensions & Generators ───────────────────────────────────
s11 = section(11, "Comprehensions &amp; Generators",
  "Comprehensions are syntactic sugar for loops that produce collections. Generators produce values lazily — O(1) memory regardless of sequence size.",
  code_block("List/Dict/Set Comprehensions + Generator Expressions + Memory", "Python",
"""import sys

# ── List Comprehension ────────────────────────────────────────────────
squares = [x**2 for x in range(10)]         # [0,1,4,9,...,81]
filtered= [x for x in range(20) if x%3==0]  # [0,3,6,9,12,15,18]

# Nested comprehension (matrix transpose)
matrix  = [[1,2,3],[4,5,6],[7,8,9]]
transposed = [[row[i] for row in matrix] for i in range(3)]

# ── Dict Comprehension ────────────────────────────────────────────────
word_len = {word: len(word) for word in ["apple","bat","cherry"]}
inverted = {v: k for k, v in {"a":1,"b":2,"c":3}.items()}

# ── Set Comprehension ─────────────────────────────────────────────────
uniq_len = {len(w) for w in ["hi","hello","world","hey"]}  # {2,5}

# ── Generator Expression — lazy, one-time iteration ───────────────────
gen = (x**2 for x in range(1_000_000))   # NO list created in memory!
print(next(gen))      # 0  (computes on demand)
print(next(gen))      # 1
print(sum(x**2 for x in range(100)))      # 328350  (still lazy)

# Memory comparison
lst_size = sys.getsizeof([x**2 for x in range(1000)])
gen_size = sys.getsizeof((x**2 for x in range(1000)))
print(f"List: {lst_size} bytes, Generator: {gen_size} bytes")
# List: 8056 bytes, Generator: 208 bytes

# ── Generator Function ────────────────────────────────────────────────
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a          # pauses here, returns a to caller
        a, b = b, a + b  # resumes on next()

fibs = fibonacci(8)
print(list(fibs))      # [0,1,1,2,3,5,8,13]

# ── yield from — delegate to sub-generator ────────────────────────────
def chain(*iterables):
    for it in iterables:
        yield from it   # flattens one level

print(list(chain([1,2],[3,4],[5])))  # [1,2,3,4,5]

# ── Generator .send() — two-way communication ─────────────────────────
def accumulator():
    total = 0
    while True:
        val = yield total   # yields current total, receives new val
        total += val

acc = accumulator()
next(acc)           # prime the generator
print(acc.send(10)) # 10
print(acc.send(20)) # 30
print(acc.send(5))  # 35""",
["0","1","328350","List: 8056 bytes, Generator: 208 bytes","[0,1,1,2,3,5,8,13]","[1,2,3,4,5]","10","30","35"])
)

# ── Section 12: Classes & OOP ─────────────────────────────────────────────────
s12 = section(12, "Classes &amp; OOP",
  "Python OOP: classes, inheritance, MRO, all dunder (magic) methods, class/static methods, properties, ABCs, and dataclasses.",
  code_block("Class Fundamentals + Dunder Methods + Dataclass", "Python",
"""from __future__ import annotations
from functools import total_ordering
from dataclasses import dataclass, field

# ── Basic class ───────────────────────────────────────────────────────
class Animal:
    species = "unknown"   # class variable (shared)

    def __init__(self, name: str, age: int):
        self.name = name  # instance variable
        self.age  = age

    def speak(self) -> str:
        return f"..."

    @classmethod
    def from_string(cls, s: str) -> "Animal":
        name, age = s.split(",")
        return cls(name.strip(), int(age))

    @staticmethod
    def classify(age: int) -> str:
        return "young" if age < 3 else "adult"

    @property
    def info(self) -> str:
        return f"{self.name} ({self.age}y)"

    @info.setter
    def info(self, val: str):
        self.name, age = val.split(",")
        self.age = int(age)

# ── Inheritance + super() ─────────────────────────────────────────────
class Dog(Animal):
    species = "Canis lupus familiaris"

    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def speak(self) -> str:
        return f"Woof! I'm {self.name}"

    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, breed={self.breed!r})"

    def __str__(self) -> str:
        return f"{self.name} the {self.breed}"

d = Dog("Rex", 5, "Labrador")
print(repr(d))   # Dog(name='Rex', breed='Labrador')
print(str(d))    # Rex the Labrador
print(d.speak()) # Woof! I'm Rex
print(Dog.species)   # Canis lupus familiaris
print(Animal.classify(2))  # young

# ── All key dunder methods overview ───────────────────────────────────
# __init__    constructor
# __repr__    developer repr  (repr(obj))
# __str__     user-friendly string  (str(obj))
# __len__     len(obj)
# __getitem__ obj[key]
# __setitem__ obj[key] = val
# __contains__ key in obj
# __iter__    iter(obj)  — must return self
# __next__    next(obj)  — raises StopIteration when done
# __eq__      obj == other
# __lt__      obj < other
# __add__     obj + other
# __call__    obj()  — makes instance callable

@total_ordering   # from functools — auto-generates missing comparisons
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self): return f"Vector({self.x}, {self.y})"
    def __add__(self, o): return Vector(self.x+o.x, self.y+o.y)
    def __mul__(self, s): return Vector(self.x*s, self.y*s)
    def __len__(self): return 2
    def __iter__(self): return iter((self.x, self.y))
    def __eq__(self, o): return (self.x,self.y)==(o.x,o.y)
    def __lt__(self, o): return (self.x**2+self.y**2)<(o.x**2+o.y**2)
    def __abs__(self): return (self.x**2+self.y**2)**0.5

v = Vector(3, 4)
print(v + Vector(1,1))   # Vector(4, 5)
print(v * 2)             # Vector(6, 8)
print(abs(v))            # 5.0
print(list(v))           # [3, 4]

# ── @dataclass — auto-generates __init__, __repr__, __eq__ ───────────
@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"
    tags:  list = field(default_factory=list)  # mutable default!

p = Point(1.0, 2.0, label="A")
print(p)  # Point(x=1.0, y=2.0, label='A', tags=[])
print(p == Point(1.0, 2.0, "A"))   # True  (__eq__ auto-generated)""",
["Dog(name='Rex', breed='Labrador')","Rex the Labrador","Woof! I'm Rex",
 "Canis lupus familiaris","young","Vector(4, 5)","Vector(6, 8)","5.0","[3, 4]",
 "Point(x=1.0, y=2.0, label='A', tags=[])","True"])
)

# ── Section 13: Modules & Packages ────────────────────────────────────────────
s13 = section(13, "Modules &amp; Packages",
  "Python's module system: import mechanics, package structure, __init__.py, __all__, sys.path, and how Python finds modules.",
  code_block("import / from / as / __all__ / sys.path / __name__", "Python",
"""import sys
import os
import os.path as osp           # alias
from pathlib import Path        # specific import
from collections import (       # multi-import
    defaultdict, Counter, deque
)

# ── Introspection ─────────────────────────────────────────────────────
print(dir(os))          # list all names defined in os module
print(help(os.getcwd))  # show docstring
print(os.__file__)      # path to module source
print(os.__doc__[:60])  # first 60 chars of docstring

# ── sys.path — where Python looks for modules ─────────────────────────
# Order: current dir → PYTHONPATH → standard library → site-packages
print(sys.path[:3])     # first 3 locations

# ── __name__ — run code only when executed directly ───────────────────
# mymodule.py
# def helper(): ...
# if __name__ == "__main__":
#     helper()   # only runs when: python mymodule.py
#                # NOT when: import mymodule

# ── Package __init__.py ────────────────────────────────────────────────
# mypackage/
# ├── __init__.py       from .utils import helper  # public surface
# ├── utils.py
# └── core.py

# ── __all__ — controls "from module import *" ─────────────────────────
# In utils.py:
# __all__ = ["public_fn"]   # _private_fn will NOT be exported

# ── reload (development only) ─────────────────────────────────────────
import importlib
# importlib.reload(some_module)   # force re-import

# ── Relative imports (inside packages only) ───────────────────────────
# from . import sibling          # same package
# from .. import parent_module   # parent package
# from .utils import helper      # explicit relative

# ── Checking module availability ──────────────────────────────────────
import importlib.util
spec = importlib.util.find_spec("numpy")
if spec:
    print("numpy is installed")
else:
    print("numpy not found")""",
["numpy is installed"])
)

# ── Section 14: Iterators & Generators ───────────────────────────────────────
s14 = section(14, "Iterators &amp; Generators",
  "The iterator protocol: __iter__ returns self, __next__ returns the next value and raises StopIteration when exhausted. itertools provides industrial-strength lazy combinatorics.",
  code_block("Iterator Protocol + itertools", "Python",
"""import itertools

# ── Custom Iterator Class ─────────────────────────────────────────────
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):    # called by iter()
        return self        # iterator IS the iterable here

    def __next__(self):    # called by next()
        if self.current <= 0:
            raise StopIteration    # signal exhaustion
        val = self.current
        self.current -= 1
        return val

for n in CountDown(5):
    print(n, end=" ")     # 5 4 3 2 1
print()

# ── iter() with sentinel ──────────────────────────────────────────────
import io
stream = io.StringIO("hello\\nworld\\n\\nstop\\nmore")
for line in iter(stream.readline, "stop\\n"):  # stops at sentinel
    print(repr(line))

# ── itertools in depth ────────────────────────────────────────────────

# count(start, step) — infinite counter
c = itertools.count(1, 2)  # 1, 3, 5, 7, ...
print(list(itertools.islice(c, 5)))   # [1, 3, 5, 7, 9]

# cycle(iterable) — repeat forever
cy = itertools.cycle("ABC")
print([next(cy) for _ in range(6)])   # ['A','B','C','A','B','C']

# chain(*iterables) — link multiple sequences
print(list(itertools.chain([1,2],[3,4],[5])))  # [1,2,3,4,5]

# islice(iterable, stop) or (iterable, start, stop, step)
print(list(itertools.islice(range(100), 0, 20, 3)))  # [0,3,6,9,12,15,18]

# product — cartesian product
print(list(itertools.product("AB", repeat=2)))
# [('A','A'),('A','B'),('B','A'),('B','B')]

# combinations / permutations
print(list(itertools.combinations("ABCD", 2)))
# [('A','B'),('A','C'),('A','D'),('B','C'),('B','D'),('C','D')]
print(list(itertools.permutations("ABC", 2)))
# [('A','B'),('A','C'),('B','A'),('B','C'),('C','A'),('C','B')]

# accumulate
import operator
print(list(itertools.accumulate([1,2,3,4,5])))           # [1,3,6,10,15]
print(list(itertools.accumulate([1,2,3,4,5], operator.mul)))  # [1,2,6,24,120]

# groupby
data = sorted([("a",1),("b",2),("a",3),("b",4)], key=lambda x:x[0])
for key, group in itertools.groupby(data, key=lambda x:x[0]):
    print(key, list(group))

# zip_longest
print(list(itertools.zip_longest([1,2,3],[10,20], fillvalue=0)))
# [(1,10),(2,20),(3,0)]""",
["5 4 3 2 1","[1,3,5,7,9]","['A','B','C','A','B','C']","[1,2,3,4,5]",
 "[1,3,6,10,15]","[1,2,6,24,120]","a [('a',1),('a',3)]","b [('b',2),('b',4)]",
 "[(1,10),(2,20),(3,0)]"])
)

# ── Section 15: Decorators ────────────────────────────────────────────────────
s15 = section(15, "Decorators",
  "Decorators are higher-order functions that modify behaviour of functions/classes. They are sugar for: func = decorator(func). functools.wraps preserves the original docstring and name.",
  code_block("Decorators — Basic / Args / Chaining / Class-based / functools", "Python",
"""import functools, time

# ── Simple decorator ──────────────────────────────────────────────────
def timer(func):
    @functools.wraps(func)   # preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed*1e6:.2f} μs")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(1_000_000)   # slow_sum took ... μs

# ── Decorator with arguments ──────────────────────────────────────────
def repeat(n):
    """Repeat function n times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say(msg):
    print(msg)

say("Hi")   # prints: Hi / Hi / Hi

# ── Class-based decorator ─────────────────────────────────────────────
class Retry:
    def __init__(self, times=3, exceptions=(Exception,)):
        self.times = times
        self.exceptions = exceptions

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(self.times):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    if attempt == self.times - 1:
                        raise
                    print(f"Retry {attempt+1}: {e}")
        return wrapper

@Retry(times=2, exceptions=(ValueError,))
def flaky(x):
    if x < 0:
        raise ValueError("negative!")
    return x * 2

print(flaky(5))   # 10

# ── Chaining decorators (bottom applies first) ─────────────────────────
def bold(func):
    @functools.wraps(func)
    def wrapper(*args):
        return f"&lt;b&gt;{func(*args)}&lt;/b&gt;"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args):
        return f"&lt;i&gt;{func(*args)}&lt;/i&gt;"
    return wrapper

@bold
@italic
def greet(name):
    return f"Hello, {name}"

print(greet("World"))   # &lt;b&gt;&lt;i&gt;Hello, World&lt;/i&gt;&lt;/b&gt;

# ── functools.lru_cache / functools.cache ─────────────────────────────
@functools.lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

print(fib(30))                # 832040  (fast due to caching)
print(fib.cache_info())       # CacheInfo(hits=28, misses=31, maxsize=128, currsize=31)

# functools.cache — same as lru_cache(maxsize=None), Python 3.9+
@functools.cache
def factorial(n):
    return 1 if n == 0 else n * factorial(n-1)

print(factorial(10))          # 3628800""",
["Hi","Hi","Hi","10","<b><i>Hello, World</i></b>","832040",
 "CacheInfo(hits=28, misses=31, maxsize=128, currsize=31)","3628800"])
)

TOPICS = [
    "Variables & Data Types", "String Methods", "List Methods",
    "Dictionary Methods", "Set Methods", "Tuple Methods",
    "Control Flow", "Functions & Lambdas", "File I/O",
    "Exception Handling", "Comprehensions & Generators", "Classes & OOP",
    "Modules & Packages", "Iterators & Generators", "Decorators",
]

body = "\n".join([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15])

html = page_shell(
    "Python Basics",
    "Exhaustive reference for all built-in types, methods, control flow, OOP, and language features — every parameter, return value, and edge case documented with runnable examples.",
    15, TOPICS, body
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Written: {len(html):,} chars → {OUT}")
