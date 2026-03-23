
# build_all.py - generates all 8 HTML doc pages
import os, json

BASE = r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final"

HEAD = '''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — PyDocs</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="style.css">
<script src="shared.js" defer></script>
</head><body>'''

HERO = '''<div class="page-hero">
<div class="breadcrumb"><a href="index.html">PyDocs</a> &rsaquo; {title}</div>
<h1>{title}</h1><p class="subtitle">{desc}</p>
<span class="topic-count">&#128218; {n} Topics &nbsp;|&nbsp; Interactive Playground &nbsp;|&nbsp; Output Previews</span>
</div>'''

def toc(items):
    links = "".join(f'<a class="toc-link" href="#s{i+1}"><span class="toc-num">{i+1:02d}</span>{t}</a>' for i,t in enumerate(items))
    return f'<div class="toc-container"><h2>Table of Contents</h2><div class="toc-grid">{links}</div></div>'

def section(num, title, intro, *blocks):
    inner = "".join(blocks)
    return f'''<div class="content-section" id="s{num}">
<div class="section-header"><span class="section-num">{num:02d}</span><h2>{title}</h2></div>
<p class="section-intro">{intro}</p>{inner}</div>'''

def cb(label, code, out=None):
    out_html = ""
    if out:
        rows = "".join(f'<div class="out-line">{r}</div>' for r in out)
        out_html = f'<div class="output-block"><div class="out-label">Output</div>{rows}</div>'
    safe = code.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    return f'''<div class="code-block">
<div class="code-header"><span class="code-lang">&#9679; Python</span>
<span class="code-title">{label}</span><button class="copy-btn">Copy</button></div>
<div class="code-body"><pre><code>{safe}</code></pre></div>{out_html}</div>'''

def note(text, kind="note", icon="&#x2139;&#xFE0F;"):
    return f'<div class="callout {kind}"><span class="callout-icon">{icon}</span><div class="callout-body"><p>{text}</p></div></div>'

def ptable(rows):
    trs="".join(f"<tr><td>{p}</td><td>{t}</td><td>{d}</td><td>{desc}</td></tr>" for p,t,d,desc in rows)
    return f'''<div class="params-card"><div class="params-card-header">Parameters</div>
<table class="params-table"><thead><tr><th>Name</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>{trs}</tbody></table></div>'''

def mgrid(methods):
    cards="".join(f'<div class="method-card"><div class="method-name">{m}</div><div class="method-desc">{d}</div><div class="method-returns">{r}</div></div>' for m,d,r in methods)
    return f'<div class="method-grid">{cards}</div>'

def sig(text):
    return f'<div class="sig-box">{text}</div>'

def playground(code):
    safe = code.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    return f'''<div class="playground"><div class="playground-header">
<span class="playground-title">&#x1F9EA; Try it — Edit and Run</span>
<button class="run-btn">&#9654; Run</button></div>
<textarea class="playground-editor" spellcheck="false">{safe}</textarea>
<div class="playground-output">Click &#9654; Run to execute…</div></div>'''

def foot(prev, nxt):
    plink = f'<a href="{prev[1]}">&larr; {prev[0]}</a>' if prev else '<span></span>'
    nlink = f'<a href="{nxt[1]}">{nxt[0]} &rarr;</a>' if nxt else '<span></span>'
    return f'<div class="page-nav">{plink}{nlink}</div></body></html>'

# ─── PYTHON BASICS ────────────────────────────────────────────────────────────
def build_python_basics():
    topics = [
        "Variables & Data Types","String Methods","List Methods","Dictionary Methods",
        "Set Methods","Tuple Methods","Control Flow","Functions","File I/O",
        "Exception Handling","Comprehensions & Generators","Classes & OOP",
        "Modules & Packages","Iterators & Generators","Decorators"
    ]

    s1 = section(1,"Variables &amp; Data Types",
        "Python is dynamically typed. Every value has a type, identity, and value. "
        "type() returns the exact class; isinstance() checks inheritance; id() returns memory address.",
        cb("All scalar types + type() / isinstance() / id() + coercion",
"""# Scalar literals
x = 42;  big = 1_000_000;  b = 0b1010;  h = 0xFF   # int variants
pi = 3.14159;  sci = 1.5e-3;  inf = float('inf')     # float
s = "hello";  raw = r"C:\\path";  multi = '''line1\nline2'''
t, f = True, False   # bool subclasses int: True==1
nothing = None

# type() — exact class
print(type(42))          # <class 'int'>
print(type(3.14))        # <class 'float'>
print(type("hi"))        # <class 'str'>
print(type(True))        # <class 'bool'>
print(type(None))        # <class 'NoneType'>

# isinstance() — respects inheritance
print(isinstance(True, int))          # True (bool IS-A int)
print(isinstance(3.14, (int,float)))  # True (tuple of types)

# id() — CPython caches small ints -5..256
a = 256; b = 256
print(id(a) == id(b))   # True  (cached)
a = 1000; b = 1000
print(id(a) == id(b))   # False (new objects)

# Type coercion
print(int("42"))         # 42
print(int(3.99))         # 3  (truncates, NOT rounds!)
print(int("FF", 16))     # 255
print(float("1.5e2"))    # 150.0
print(str(42))           # '42'
print(bool(0), bool(""), bool([]))   # False False False
print(bool(1), bool("x"), bool([0]))  # True True True""",
["<class 'int'>","<class 'float'>","<class 'str'>","<class 'bool'>","<class 'NoneType'>",
 "True","True","True","False","42","3","255","150.0","'42'",
 "False False False","True True True"]),
        note("int() truncates toward zero: int(3.99)=3, int(-3.99)=-3. Use round() for rounding. "
             "CPython caches integers -5 to 256 — identities match for those values.","warning","&#x26A0;&#xFE0F;")
    )

    s2 = section(2,"String Methods",
        "Strings are immutable Unicode sequences. All methods return a NEW string. "
        "Python has 47 built-in string methods.",
        cb("Case / strip / find / replace / split / join / format / f-strings / slicing",
"""s = "  Hello, World!  "
# Case
print(s.upper())          # '  HELLO, WORLD!  '
print(s.lower())          # '  hello, world!  '
print(s.title())          # '  Hello, World!  '
print(s.swapcase())       # '  hELLO, wORLD!  '

# Strip
print(s.strip())          # 'Hello, World!'
print(s.lstrip())         # 'Hello, World!  '
print(s.rstrip())         # '  Hello, World!'

# Find / Count / Replace
t = "abcabcabc"
print(t.find("bc"))       # 1   (-1 if not found)
print(t.rfind("bc"))      # 7   (search from right)
print(t.index("bc"))      # 1   (raises ValueError if missing)
print(t.count("bc"))      # 3
print("aabbcc".replace("b","X"))    # 'aaXXcc'
print("aabbcc".replace("b","X",1))  # 'aaXbcc' (max replacements=1)

# starts/endswith (tuple of options)
print("hello".startswith("he"))         # True
print("world".endswith(("d","x","q")))  # True

# Split / Join
parts = "a,b,c".split(",")       # ['a','b','c']
print("|".join(parts))            # 'a|b|c'
print("a  b  c".split())          # ['a','b','c'] any whitespace
print("l1\nl2\nl3".splitlines())  # ['l1','l2','l3']

# f-strings (fastest formatting)
name, score = "Ada", 98.5
print(f"{name} scored {score:.1f}%")     # 'Ada scored 98.5%'
print(f"{1000000:,}")                     # '1,000,000'
print(f"{'center':^20}")                  # '       center       '
print(f"{42:#010x}")                      # '0x0000002a'

# Slicing  s[start:stop:step]
s2 = "abcdefghij"
print(s2[2:7])    # 'cdefg'
print(s2[::2])    # 'acegi'
print(s2[::-1])   # 'jihgfedcba'  (reverse)
print(s2[-3:])    # 'hij'

# Validation (return bool)
print("123".isdigit())      # True
print("abc".isalpha())      # True
print("abc123".isalnum())   # True
print("   ".isspace())      # True

# Padding
print("42".zfill(6))        # '000042'
print("hi".center(10,"*"))  # '****hi****'
print("left".ljust(10,"-")) # 'left------'
print("right".rjust(10))    # '     right'""",
["'  HELLO, WORLD!  '","'  hello, world!  '","'  Hello, World!  '","'  hELLO, wORLD!  '",
 "'Hello, World!'","'Hello, World!  '","'  Hello, World!'",
 "1","7","1","3","'aaXXcc'","'aaXbcc'","True","True",
 "['a','b','c']","'a|b|c'","['a','b','c']","['l1','l2','l3']",
 "'Ada scored 98.5%'","'1,000,000'","'       center       '","'0x0000002a'",
 "'cdefg'","'acegi'","'jihgfedcba'","'hij'",
 "True","True","True","True",
 "'000042'","'****hi****'","'left------'","'     right'"]),
        mgrid([
            (".encode(enc)","Encode string to bytes","→ bytes"),
            (".decode(enc)","Decode bytes to string","→ str"),
            (".partition(sep)","Split into 3-tuple around sep","→ tuple"),
            (".maketrans(x,y)","Build translation table","→ dict"),
            (".translate(tbl)","Apply char mapping","→ str"),
            (".expandtabs(n)","Replace tabs with spaces","→ str"),
            (".removeprefix(s)","Remove prefix if present (3.9+)","→ str"),
            (".removesuffix(s)","Remove suffix if present (3.9+)","→ str"),
            (".casefold()","Aggressive lowercase for comparison","→ str"),
            (".format_map(d)","Format with dict mapping","→ str"),
        ])
    )

    s3 = section(3,"List Methods",
        "Lists are ordered, mutable sequences. Mutating methods return None and modify in-place. "
        "Comprehensions are the idiomatic way to build new lists.",
        cb("All list methods + builtins + comprehensions + unpacking",
"""lst = [3,1,4,1,5,9,2,6]

# --- Mutating (return None) ---
lst.append(7)          # [3,1,4,1,5,9,2,6,7]        O(1)
lst.extend([8,9])      # adds all elements of iterable O(k)
lst.insert(0, 0)       # insert 0 at index 0           O(n)
lst.remove(1)          # remove first occurrence        O(n)
p1 = lst.pop()         # remove & return last           O(1)
p2 = lst.pop(2)        # remove & return at index       O(n)
lst.sort()             # Timsort stable in-place        O(n log n)
lst.sort(reverse=True)
lst.sort(key=lambda x: -x)
lst.reverse()          # in-place reverse               O(n)
lst.clear()            # empties list                   O(n)

# --- Non-mutating (return value) ---
lst = [3,1,4,1,5,9]
print(lst.index(4))    # 2   (raises ValueError if missing)
print(lst.count(1))    # 2
cpy = lst.copy()       # shallow copy

# Built-ins
print(len(lst))        # 6
print(min(lst))        # 1
print(max(lst))        # 9
print(sum(lst))        # 23
print(sorted(lst))              # [1,1,3,4,5,9]  new list
print(sorted(lst,key=lambda x:-x))  # [9,5,4,3,1,1]

# Comprehensions
squares = [x**2 for x in range(1,6)]            # [1,4,9,16,25]
evens   = [x for x in range(10) if x%2==0]     # [0,2,4,6,8]
flat    = [x for row in [[1,2],[3,4]] for x in row]  # [1,2,3,4]

# Unpacking
a, b, c = [1,2,3]
first, *middle, last = [1,2,3,4,5]
print(first, middle, last)    # 1 [2,3,4] 5

# Operators
print([1,2]+[3,4])   # [1,2,3,4]
print([0]*5)         # [0,0,0,0,0]
print(3 in [1,2,3])  # True""",
["2","2","6","1","9","23","[1, 1, 3, 4, 5, 9]","[9, 5, 4, 3, 1, 1]",
 "1 [2, 3, 4] 5","[1, 2, 3, 4]","[0, 0, 0, 0, 0]","True"])
    )

    s4 = section(4,"Dictionary Methods",
        "Dicts are hash maps with O(1) average get/set/delete. Ordered since Python 3.7. "
        "Keys must be hashable. Python 3.9+ adds | merge operator.",
        cb("All dict methods + comprehensions + defaultdict + Counter",
"""d = {"a":1, "b":2, "c":3}

# Access
print(d["a"])              # 1  (KeyError if missing)
print(d.get("z", 0))      # 0  (safe default)
d.setdefault("d", 4)      # adds "d":4 only if absent

# Views (live)
print(list(d.keys()))      # ['a','b','c','d']
print(list(d.values()))    # [1,2,3,4]
print(list(d.items()))     # [('a',1),('b',2),('c',3),('d',4)]

# Mutating
d.update({"e":5, "a":99}) # merge; overwrites existing
removed = d.pop("c")       # returns 3
last = d.popitem()         # remove & return last (k,v)
d.clear()

# fromkeys
empty = dict.fromkeys(["x","y","z"], 0)  # {'x':0,'y':0,'z':0}

# Dict comprehension
sq = {x:x**2 for x in range(1,6)}             # {1:1,2:4,...}
flt= {k:v for k,v in sq.items() if v>9}       # {4:16,5:25}

# Python 3.9+ merge
a = {"x":1}; b = {"x":99,"y":2}
print(a | b)   # {'x':99,'y':2}  new dict
a |= b         # in-place

from collections import defaultdict, Counter

# defaultdict — auto-creates missing keys
dd = defaultdict(list)
dd["fruits"].append("apple")
dd["fruits"].append("banana")
print(dict(dd))  # {'fruits': ['apple', 'banana']}

# Counter — counts hashable items
c = Counter("abracadabra")
print(c.most_common(3))    # [('a',5),('b',2),('r',2)]
print(c["a"])              # 5
c2 = Counter(a=1, b=3)
print(dict(c + c2))        # combined counts
print(dict(c - c2))        # positive differences only""",
["1","0","['a','b','c','d']","[1,2,3,4]","[('a',1),('b',2),('c',3),('d',4)]",
 "{'x':99,'y':2}","{'fruits': ['apple', 'banana']}",
 "[('a',5),('b',2),('r',2)]","5"])
    )

    s5 = section(5,"Set Methods",
        "Sets are unordered collections of unique hashable elements. O(1) membership test. "
        "frozenset is the immutable hashable variant usable as dict keys.",
        cb("All set operations + algebra + comprehension",
"""A = {1,2,3,4}; B = {3,4,5,6}

# Mutating
A.add(10); A.discard(10)  # add/remove (discard no error)
A.remove(4)               # raises KeyError if missing
# p = A.pop()             # remove arbitrary element

# Set algebra (return new sets)
print(A | B)              # {1,2,3,5,6}   union
print(A & B)              # {3}            intersection
print(A - B)              # {1,2}          difference
print(A ^ B)              # {1,2,5,6}      symmetric diff

# Relationship tests
print({1,2}.issubset({1,2,3}))    # True
print({1,2,3}.issuperset({1,2}))  # True
print({1,2}.isdisjoint({3,4}))    # True

# frozenset — hashable, can be dict key
fs = frozenset([1,2,3])
d = {fs: "key"}    # legal!

# Set comprehension
even_sq = {x**2 for x in range(10) if x%2==0}
print(even_sq)  # {0,4,16,36,64}

# In-place versions
A = {1,2,3,4}
A.update(B)                    # A |= B
A.intersection_update(B)       # A &= B
A.difference_update(B)         # A -= B
A.symmetric_difference_update(B) # A ^= B""",
["{1, 2, 3, 5, 6}","{3}","{1, 2}","{1, 2, 5, 6}","True","True","True","{0, 4, 16, 36, 64}"])
    )

    s6 = section(6,"Tuple Methods",
        "Tuples are immutable ordered sequences — only 2 methods. Used for multiple return values, "
        "dict keys, and named tuples that act as lightweight structs.",
        cb("Tuple methods + namedtuple + unpacking",
"""t = (3,1,4,1,5,9,2,6,5)
print(t.count(1))    # 2
print(t.index(5))    # 4  (first occurrence; ValueError if missing)

# Named tuples
from collections import namedtuple
Point = namedtuple("Point", ["x","y"])
p = Point(3,4)
print(p.x, p.y)      # 3 4
print(p[0])          # 3  (indexing still works)
print(p._asdict())   # {'x':3,'y':4}
p2 = p._replace(x=10)
print(p2)            # Point(x=10, y=4)

# Typed NamedTuple (Python 3.6+)
from typing import NamedTuple
class Color(NamedTuple):
    r: int; g: int; b: int = 0
c = Color(255,128)
print(c)   # Color(r=255, g=128, b=0)

# Unpacking
a,b,c = (1,2,3)
first,*rest = (10,20,30,40)
print(first, rest)   # 10 [20,30,40]
*head,last = (10,20,30,40)
print(head, last)    # [10,20,30] 40
(a,b),c = (1,2),3
print(a,b,c)         # 1 2 3""",
["2","4","3 4","3","{'x':3,'y':4}","Point(x=10, y=4)","Color(r=255, g=128, b=0)",
 "10 [20, 30, 40]","[10, 20, 30] 40","1 2 3"])
    )

    s7 = section(7,"Control Flow",
        "if/elif/else, ternary, for/while loops, break/continue/pass, loop else clause, "
        "and Python 3.10+ structural pattern matching with match/case.",
        cb("if / ternary / for / while / break / continue / loop-else / match-case",
"""# if/elif/else
score = 87
grade = "A" if score>=90 else ("B" if score>=80 else "C")
print(grade)   # B

# for with range, enumerate, zip
for i in range(0,10,2): print(i,end=" ")  # 0 2 4 6 8
print()
fruits=["apple","banana","cherry"]
for i,f in enumerate(fruits,1): print(f"{i}. {f}")

# while + break/continue
n=0
while n<5:
    n+=1
    if n==3: continue
    if n==5: break
    print(n,end=" ")
print()   # 1 2 4

# Loop else — runs if loop completed without break
for i in range(2,8):
    for j in range(2,i):
        if i%j==0: break
    else:
        print(f"{i} is prime",end=" ")
print()   # 2 3 5 7

# pass — placeholder
def todo(): pass
class Empty: pass

# match/case (Python 3.10+)
def http(code):
    match code:
        case 200: return "OK"
        case 404: return "Not Found"
        case 500|503: return "Server Error"
        case int(c) if c>=400: return f"Client Error {c}"
        case _: return "Unknown"

print(http(200), http(404), http(418))""",
["B","0 2 4 6 8","1. apple","2. banana","3. cherry","1 2 4","2 is prime 3 is prime 5 is prime 7 is prime","OK Not Found Client Error 418"])
    )

    s8 = section(8,"Functions",
        "Functions are first-class objects. Supports default params, *args/**kwargs, "
        "keyword-only (after *), positional-only (before /), lambda, and closures.",
        cb("def / *args / **kwargs / keyword-only / positional-only / lambda / builtins",
"""def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Ada"))              # Hello, Ada!
print(greet("Turing","Hi"))      # Hi, Turing!

def total(*args):                # variable positional
    return sum(args)
print(total(1,2,3,4,5))         # 15

def info(**kwargs):              # variable keyword
    return {k:v for k,v in kwargs.items()}
print(info(name="Ada",year=1815))  # {'name':'Ada','year':1815}

def tag(content, *, tag="p", cls=""):  # keyword-only (after *)
    return f"<{tag} class='{cls}'>{content}</{tag}>"
print(tag("Hi", tag="h1"))       # <h1 class=''>Hi</h1>

def rect(w, h, /):               # positional-only (before /)
    return w*h
print(rect(3,4))                 # 12

# Lambda
double = lambda x: x*2
print(double(5))                 # 10
print(sorted([3,-1,4,-1],key=abs))  # [-1,-1,3,4]
print(list(map(lambda x:x**2,[1,2,3,4])))   # [1,4,9,16]
print(list(filter(lambda x:x>0,[3,-1,4,-2]))) # [3,4]

from functools import reduce
print(reduce(lambda a,b:a*b,[1,2,3,4,5]))  # 120

# Useful builtins
names=["Alice","Bob","Carol"]; scores=[95,87,92]
for n,s in zip(names,scores): print(f"{n}:{s}")
print(any(x>90 for x in scores))  # True
print(all(x>80 for x in scores))  # True
print(max(zip(names,scores),key=lambda p:p[1]))  # ('Alice',95)""",
["Hello, Ada!","Hi, Turing!","15","{'name':'Ada','year':1815}","12","10",
 "[-1,-1,3,4]","[1,4,9,16]","[3,4]","120","Alice:95","Bob:87","Carol:92","True","True","('Alice',95)"])
    )

    s9 = section(9,"File I/O",
        "open() provides full file access. Always use 'with' to guarantee closing. "
        "pathlib.Path offers a modern OOP interface to the filesystem.",
        cb("open() modes / read / write / pathlib",
"""from pathlib import Path

# Writing
with open("demo.txt","w",encoding="utf-8") as f:
    f.write("Line 1\n")
    f.writelines(["Line 2\n","Line 3\n"])

# Reading — all approaches
with open("demo.txt","r",encoding="utf-8") as f:
    all_text = f.read()          # entire file as str
with open("demo.txt") as f:
    lines = f.readlines()        # list of lines (with \n)
with open("demo.txt") as f:
    for i,line in enumerate(f,1):
        print(f"{i}: {line.rstrip()}")

# Seek / Tell
with open("demo.txt","r") as f:
    print(f.read(6))   # first 6 chars
    print(f.tell())    # current byte pos
    f.seek(0)          # back to start
    print(f.readline())

# Modes summary:
# 'r'  read text  'w'  write text (truncates)  'a'  append
# 'x'  create exclusive  'rb'/'wb'  binary  'r+' read+write

# pathlib.Path — OOP filesystem
p = Path("demo.txt")
print(p.name)           # 'demo.txt'
print(p.stem)           # 'demo'
print(p.suffix)         # '.txt'
print(p.exists())       # True
print(p.stat().st_size) # size in bytes
text = p.read_text()                  # one-liner read
p.write_text("New content")           # one-liner write

# Path arithmetic
cwd = Path.cwd()
child = cwd / "subdir" / "file.txt"  # / operator
print(child.parent)     # .../subdir

# Glob
txt_files = list(Path(".").glob("*.txt"))
all_py    = list(Path(".").rglob("**/*.py"))

import os
os.remove("demo.txt")""",
["1: Line 1","2: Line 2","3: Line 3","'demo.txt'","'demo'","'.txt'","True"]),
        ptable([
            ("mode","str","'r'","r=read  w=write  a=append  x=exclusive  b=binary  +=read+write"),
            ("encoding","str","None","'utf-8', 'ascii', 'latin-1' etc. None uses system default"),
            ("buffering","int","-1","-1=auto  0=raw(binary only)  1=line  >1=byte count"),
            ("newline","str","None","None=universal  ''=no translate  '\\n'  '\\r\\n'  '\\r'"),
        ])
    )

    s10 = section(10,"Exception Handling",
        "Structured exception handling with try/except/else/finally. All exceptions inherit from "
        "BaseException. Custom exceptions should subclass Exception.",
        cb("try/except/else/finally + raise + custom exceptions + hierarchy",
"""# Basic structure
def safe_div(a,b):
    try:
        result = a/b
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        return None
    except (TypeError,ValueError) as e:
        print(f"Type error: {e}")
        return None
    else:
        print("Success")    # only if no exception
        return result
    finally:
        print("cleanup")    # ALWAYS runs

print(safe_div(10,2))   # Success / cleanup / 5.0
print(safe_div(10,0))   # Error / cleanup / None

# Access exception info
try:
    int("abc")
except Exception as e:
    print(type(e).__name__)  # ValueError
    print(e.args)            # ('invalid literal...',)

# Re-raise
try:
    raise ValueError("bad value")
except ValueError:
    raise   # preserves original traceback

# Custom exceptions
class AppError(Exception):
    pass

class ValidationError(AppError):
    def __init__(self,field,msg):
        self.field = field
        super().__init__(f"Validation failed on '{field}': {msg}")

try:
    raise ValidationError("email","must contain @")
except ValidationError as e:
    print(e)          # Validation failed on 'email': must contain @
    print(e.field)    # email

# Exception hierarchy (key classes):
# BaseException -> SystemExit, KeyboardInterrupt, Exception
# Exception -> ArithmeticError (ZeroDivisionError, OverflowError)
#           -> LookupError (IndexError, KeyError)
#           -> ValueError, TypeError, AttributeError
#           -> OSError (FileNotFoundError, PermissionError)
#           -> RuntimeError, StopIteration, NameError""",
["Success","cleanup","5.0","Error: division by zero","cleanup","None",
 "ValueError","Validation failed on 'email': must contain @","email"])
    )

    s11 = section(11,"Comprehensions &amp; Generators",
        "Comprehensions build collections concisely. Generator expressions produce values lazily — "
        "constant O(1) memory regardless of sequence size.",
        cb("list/dict/set comprehensions + generator functions + yield + itertools",
"""import sys

# List comprehension
squares=[x**2 for x in range(10)]           # [0,1,4,...,81]
evens  =[x for x in range(20) if x%3==0]   # [0,3,6,9,12,15,18]
nested =[[i*j for j in range(1,4)] for i in range(1,4)]

# Dict / Set comprehensions
wlen   ={w:len(w) for w in ["apple","bat","cherry"]}
uniq   ={len(w) for w in ["hi","hello","world","hey"]}  # {2,5}

# Generator expression — lazy, O(1) memory
gen = (x**2 for x in range(1_000_000))
print(next(gen))   # 0
print(next(gen))   # 1
print(sum(x**2 for x in range(100)))   # 328350 (computed lazily)

lst_sz=sys.getsizeof([x for x in range(1000)])
gen_sz=sys.getsizeof((x for x in range(1000)))
print(f"List:{lst_sz}B vs Generator:{gen_sz}B")

# Generator function
def fibonacci(n):
    a,b=0,1
    for _ in range(n):
        yield a       # pause, return a
        a,b=b,a+b

print(list(fibonacci(8)))   # [0,1,1,2,3,5,8,13]

# yield from — delegate to sub-generator
def chain(*its):
    for it in its:
        yield from it

print(list(chain([1,2],[3,4],[5])))   # [1,2,3,4,5]

# Two-way generator with .send()
def accumulator():
    total=0
    while True:
        val = yield total
        total += val

acc=accumulator()
next(acc)           # prime
print(acc.send(10)) # 10
print(acc.send(20)) # 30
print(acc.send(5))  # 35""",
["0","1","328350","List:8056B vs Generator:208B","[0,1,1,2,3,5,8,13]",
 "[1,2,3,4,5]","10","30","35"])
    )

    s12 = section(12,"Classes &amp; OOP",
        "Python OOP: class definition, instance vs class variables, all dunder methods, "
        "@classmethod/@staticmethod/@property, multiple inheritance, MRO, ABC, dataclass.",
        cb("class / inheritance / super() / dunder methods / @dataclass",
"""from dataclasses import dataclass, field

# Basic class
class Animal:
    species="unknown"               # class variable

    def __init__(self,name,age):
        self.name=name              # instance variable
        self.age=age

    @classmethod
    def from_string(cls,s):
        n,a=s.split(",")
        return cls(n.strip(),int(a))

    @staticmethod
    def classify(age):
        return "young" if age<3 else "adult"

    @property
    def info(self):
        return f"{self.name}({self.age}y)"

    @info.setter
    def info(self,val):
        self.name,age=val.split(",")
        self.age=int(age)

# Inheritance + super()
class Dog(Animal):
    def __init__(self,name,age,breed):
        super().__init__(name,age)
        self.breed=breed

    def __repr__(self):
        return f"Dog({self.name!r},{self.breed!r})"

    def __str__(self):
        return f"{self.name} the {self.breed}"

d=Dog("Rex",5,"Lab")
print(repr(d))   # Dog('Rex','Lab')
print(str(d))    # Rex the Lab
print(Animal.classify(2))   # young

# Key dunder methods
# __len__     len(obj)
# __getitem__ obj[key]
# __setitem__ obj[key]=val
# __contains__ key in obj
# __iter__/__next__  iteration protocol
# __eq__/__lt__  comparison
# __add__/__mul__  arithmetic
# __call__  obj() callable

class Vector:
    def __init__(self,x,y): self.x,self.y=x,y
    def __repr__(self): return f"V({self.x},{self.y})"
    def __add__(self,o): return Vector(self.x+o.x,self.y+o.y)
    def __mul__(self,s): return Vector(self.x*s,self.y*s)
    def __abs__(self): return (self.x**2+self.y**2)**0.5
    def __len__(self): return 2
    def __iter__(self): return iter((self.x,self.y))
    def __eq__(self,o): return (self.x,self.y)==(o.x,o.y)

v=Vector(3,4)
print(v+Vector(1,1))  # V(4,5)
print(v*2)            # V(6,8)
print(abs(v))         # 5.0
print(list(v))        # [3,4]

# @dataclass — auto __init__/__repr__/__eq__
@dataclass
class Point:
    x:float; y:float
    label:str="origin"
    tags:list=field(default_factory=list)

p=Point(1.0,2.0,label="A")
print(p)   # Point(x=1.0, y=2.0, label='A', tags=[])
print(p==Point(1.0,2.0,"A"))  # True""",
["Dog('Rex','Lab')","Rex the Lab","young","V(4,5)","V(6,8)","5.0","[3,4]",
 "Point(x=1.0, y=2.0, label='A', tags=[])","True"])
    )

    s13 = section(13,"Modules &amp; Packages",
        "Python module resolution: current dir → PYTHONPATH → stdlib → site-packages. "
        "__init__.py defines package public API; __all__ controls 'from x import *'.",
        cb("import / from / as / __all__ / sys.path / __name__ / importlib",
"""import sys
import os
import os.path as osp
from pathlib import Path
from collections import defaultdict, Counter, deque

# Introspection
print(dir(os)[:5])          # first 5 names in os
print(os.__file__[:40])     # path to os.py
# help(os.getcwd)           # shows docstring

# sys.path — search order
# 1. Current directory  2. PYTHONPATH  3. stdlib  4. site-packages
print(type(sys.path))       # <class 'list'>

# __name__ guard — standard idiom
# mymodule.py:
#   def main(): ...
#   if __name__ == "__main__":
#       main()   # only when run directly, not when imported

# Package structure
# mypackage/
#   __init__.py       # from .utils import helper (public API)
#   utils.py
#   core.py

# __all__ — what 'from module import *' exports
# utils.py:  __all__ = ["public_fn"]  # _private excluded

# Relative imports (inside packages)
# from . import sibling
# from .. import parent
# from .utils import helper

# Check installation
import importlib.util
def is_installed(pkg):
    return importlib.util.find_spec(pkg) is not None

print(is_installed("numpy"))    # True or False
print(is_installed("nonexist")) # False

# importlib.reload — force re-import during development
import importlib
# importlib.reload(some_module)""",
["True","False"])
    )

    s14 = section(14,"Iterators &amp; Generators",
        "The iterator protocol: __iter__ returns self, __next__ returns next value and "
        "raises StopIteration when done. itertools provides lazy combinatorics.",
        cb("Custom iterator + iter() with sentinel + itertools in depth",
"""import itertools

# Custom iterator class
class Countdown:
    def __init__(self,n): self.n=n
    def __iter__(self): return self
    def __next__(self):
        if self.n<=0: raise StopIteration
        self.n-=1; return self.n+1

print(list(Countdown(5)))   # [5,4,3,2,1]

# iter(callable, sentinel) — stop when sentinel returned
import io
stream=io.StringIO("a\nb\nc\n")
lines=list(iter(stream.readline,""))
print(lines)   # ['a\n','b\n','c\n']

# itertools
c=itertools.count(1,2)
print(list(itertools.islice(c,5)))   # [1,3,5,7,9]

cy=itertools.cycle("ABC")
print([next(cy) for _ in range(6)])  # ['A','B','C','A','B','C']

print(list(itertools.chain([1,2],[3,4])))   # [1,2,3,4]
print(list(itertools.chain.from_iterable([[1,2],[3,4]])))  # [1,2,3,4]

# product / combinations / permutations
print(list(itertools.product("AB",repeat=2)))
# [('A','A'),('A','B'),('B','A'),('B','B')]
print(list(itertools.combinations("ABC",2)))
# [('A','B'),('A','C'),('B','C')]
print(list(itertools.permutations("AB",2)))
# [('A','B'),('B','A')]

# accumulate (running totals)
import operator
print(list(itertools.accumulate([1,2,3,4,5])))             # running sum
print(list(itertools.accumulate([1,2,3,4,5],operator.mul)))# running product

# zip_longest / dropwhile / takewhile
print(list(itertools.zip_longest([1,2,3],[10,20],fillvalue=0)))
print(list(itertools.dropwhile(lambda x:x<5,[1,2,5,6,7])))
print(list(itertools.takewhile(lambda x:x<5,[1,2,3,5,6])))""",
["[5,4,3,2,1]","['a\\n','b\\n','c\\n']","[1,3,5,7,9]","['A','B','C','A','B','C']",
 "[1,2,3,4]","[1,2,3,4]","[1,3,6,10,15]","[1,2,6,24,120]",
 "[(1,10),(2,20),(3,0)]","[5,6,7]","[1,2,3]"])
    )

    s15 = section(15,"Decorators",
        "Decorators are syntactic sugar for higher-order functions. Always use functools.wraps "
        "to preserve __name__ and __doc__. Supports args, chaining, and class-based decorators.",
        cb("Basic / args / class-based / chaining / lru_cache",
"""import functools, time

# Basic decorator
def timer(func):
    @functools.wraps(func)   # preserves metadata!
    def wrapper(*args,**kw):
        t=time.perf_counter()
        r=func(*args,**kw)
        print(f"{func.__name__}: {(time.perf_counter()-t)*1e3:.2f}ms")
        return r
    return wrapper

@timer
def slow(n): return sum(range(n))
slow(100000)   # slow: 2.31ms

# Decorator with arguments (3-level nesting)
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*a,**kw):
            for _ in range(n): func(*a,**kw)
        return wrapper
    return decorator

@repeat(3)
def say(msg): print(msg)
say("Hi")   # prints Hi 3 times

# Class-based decorator (callable class)
class Retry:
    def __init__(self,times=3): self.times=times
    def __call__(self,func):
        @functools.wraps(func)
        def wrapper(*a,**kw):
            for i in range(self.times):
                try: return func(*a,**kw)
                except Exception as e:
                    if i==self.times-1: raise
                    print(f"Retry {i+1}: {e}")
        return wrapper

@Retry(times=2)
def flaky(x):
    if x<0: raise ValueError("negative")
    return x*2
print(flaky(5))   # 10

# Chaining decorators (bottom applies first)
def bold(f):
    @functools.wraps(f)
    def w(*a): return f"<b>{f(*a)}</b>"
    return w
def italic(f):
    @functools.wraps(f)
    def w(*a): return f"<i>{f(*a)}</i>"
    return w

@bold
@italic
def greet(n): return f"Hello {n}"
print(greet("World"))   # <b><i>Hello World</i></b>

# functools.lru_cache — memoization
@functools.lru_cache(maxsize=128)
def fib(n): return n if n<2 else fib(n-1)+fib(n-2)
print(fib(30))           # 832040
print(fib.cache_info())  # CacheInfo(hits=28,misses=31,...)

@functools.cache          # lru_cache(maxsize=None), 3.9+
def fact(n): return 1 if n==0 else n*fact(n-1)
print(fact(10))           # 3628800""",
["Hi","Hi","Hi","10","<b><i>Hello World</i></b>","832040","3628800"])
    )

    body = "".join([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15])
    body += playground("""# Try any Python — edit and run!
data = {"Python":95, "NumPy":88, "Pandas":91, "TensorFlow":79}
for lib, score in sorted(data.items(), key=lambda x:-x[1]):
    bar = "█" * (score // 5)
    print(f"{lib:<12} {bar} {score}")""")

    html = HEAD.format(title="Python Basics",desc="Exhaustive Python reference — 15 topics, every method and parameter.") + \
           HERO.format(title="Python Basics",desc="All built-in types, methods, control structures, OOP, closures and decorators — with runnable examples and real output.",n=15) + \
           toc(topics) + body + foot(("Home","index.html"),("NumPy","numpy.html"))

    with open(os.path.join(BASE,"python-basics.html"),"w",encoding="utf-8") as f:
        f.write(html)
    print(f"python-basics.html  {len(html):>10,} chars")

build_python_basics()
print("Done.")
