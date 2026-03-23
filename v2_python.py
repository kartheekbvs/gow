
# v2_python.py — generates Python Basics pages for v2.html
import sys
sys.path.insert(0, r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")

# ─── Inline Helpers to avoid pickle issues ──────────────────────────────────
def card(method, sig, ret, explanation, params_rows=None, examples=None, note_text=None, warn_text=None):
    pid = method.replace('.','').replace('(','').replace(')','').replace(' ','_').replace(',','')
    html = f'<div class="method-card" id="mc-{pid}">\n'
    html += f'  <div class="method-header" onclick="toggleMethod(this)">\n'
    html += f'    <code>{method}</code>\n'
    html += f'    <span class="method-sig">{sig}</span>\n'
    if ret:
        html += f'    <span class="method-ret">→ {ret}</span>\n'
    html += '    <span class="method-chevron">›</span>\n'
    html += '  </div>\n'
    html += '  <div class="method-body">\n'
    html += f'    <p>{explanation}</p>\n'
    if params_rows:
        html += '    <table class="param-table"><thead><tr><th>Param</th><th>Type</th><th>Default</th><th>Description</th></tr></thead><tbody>\n'
        for r in params_rows:
            html += f'      <tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>\n'
        html += '    </tbody></table>\n'
    if note_text:
        html += f'    <div class="note"><strong>📝 Note</strong>{note_text}</div>\n'
    if warn_text:
        html += f'    <div class="warn"><strong>⚠️ Warning</strong>{warn_text}</div>\n'
    if examples:
        for title, code, out in examples:
            if title:
                html += f'    <p><strong>{title}</strong></p>\n'
            html += '    <div class="code-box"><div class="code-header"><span class="lang">python</span><button class="copy-btn">Copy</button></div><pre>'
            html += code
            html += '</pre></div>\n'
            if out:
                html += f'    <div class="note" style="margin-top:-8px;padding:8px 12px;"><strong>Output</strong><code style="background:transparent;color:var(--accent-g);font-size:12px;">{out}</code></div>\n'
    html += '  </div>\n</div>\n'
    return html

def section_header(title, badge_module, badge_level, source):
    return f'''<div class="page active" id="page-{{id}}">
<div class="badge-row">
  <span class="badge badge-module">{badge_module}</span>
  <span class="badge badge-{badge_level.lower()}">{badge_level}</span>
  <span class="source-note">📖 {source}</span>
</div>
<h1>{title}</h1>
'''

def page_nav(prev_href, prev_label, next_href, next_label):
    return f'''<div class="page-nav">
  <a href="{prev_href}" class="nav-btn"><span class="nav-dir">← Previous</span><strong>{prev_label}</strong></a>
  <a href="{next_href}" class="nav-btn right-nav"><span class="nav-dir">Next →</span><strong>{next_label}</strong></a>
</div>\n</div>\n'''

pages = {}

# ─── PAGE: String Methods ─────────────────────────────────────────────────────
def strings_page():
    body = section_header("String Methods","🐍 Python Basics","Beginner","Python Data Science Handbook").replace('{id}','py-strings')
    body += """<p>Strings are <strong>immutable</strong> sequences of Unicode characters. Python provides 40+ built-in string methods — none modify the original string, all return a new value. Below every method is expandable with full signature, parameters, and real examples.</p>"""

    body += "<h2>Case &amp; Alignment</h2><div class='method-grid'>"
    body += card(".upper()", "Return uppercase copy", "str",
        "Converts all cased characters to uppercase. Only ASCII-mapped letters transform; accented characters follow locale rules.",
        examples=[("Basic",
            's = "hello world"\\nprint(s.upper())       # HELLO WORLD\\nprint("café".upper())  # CAFÉ', "HELLO WORLD")])
    body += card(".lower()", "Return lowercase copy", "str",
        "Converts all cased characters to lowercase. Use <code>.casefold()</code> for aggressive Unicode-aware lowercasing.",
        examples=[("",
            's = "Hello WORLD"\\nprint(s.lower())        # hello world\\nprint("ß".lower())      # ß (unchanged — casefold gives "ss")', "hello world")])
    body += card(".casefold()", "Aggressive lowercase for Unicode comparison", "str",
        "Stronger than .lower() — designed for case-insensitive comparisons. Converts ß → ss, ﬁ → fi, etc. Use when comparing strings from different locales.",
        examples=[("Unicode-safe comparison",
            's1 = "Straße"\\ns2 = "strasse"\\nprint(s1.casefold() == s2.casefold())   # True\\nprint(s1.lower()    == s2.lower())      # False (lower keeps ß)', "True")])
    body += card(".title()", "Title-case each word", "str",
        "First letter of each word uppercased, rest lowercased. Splits on any non-letter.",
        examples=[("",
            'print("the quick brown fox".title())   # The Quick Brown Fox', "The Quick Brown Fox")])
    body += card(".capitalize()", "Uppercase first character only", "str",
        "Uppercases the very first character and lowercases all the rest. Different from .title() which does every word.",
        examples=[("","print('hello world'.capitalize())   # Hello world", "Hello world")])
    body += card(".swapcase()", "Swap case of each character", "str",
        "Uppercase → lowercase and lowercase → uppercase for every character.",
        examples=[("","print('Hello World'.swapcase())   # hELLO wORLD", "hELLO wORLD")])
    body += card(".center(width, fillchar)", "Center in a field of width", "str",
        "Returns the string centered in width characters. fillchar fills the padding (default is space).",
        [("width","int","—","Total field width"),("fillchar","str","' '","Single char to pad with")],
        examples=[("","print('hi'.center(10))       # '    hi    '\\nprint('hi'.center(10,'*'))  # ****hi****", "    hi    ")])
    body += card(".ljust(width, fillchar)", "Left-justify in a field", "str",
        "Pads the right side to reach width. fillchar is the padding character (default space).",
        examples=[("","print('hi'.ljust(8,'.'))", "hi......")])
    body += card(".rjust(width, fillchar)", "Right-justify in a field", "str",
        "Pads the left side to reach width.",
        examples=[("","print('42'.rjust(6,'0'))", "000042")])
    body += card(".zfill(width)", "Zero-pad a numeric string", "str",
        "Inserts '0' on the left until the string reaches width. Preserves +/- sign prefix.",
        examples=[("","print('42'.zfill(6))    # 000042\\nprint('-7'.zfill(6))   # -00007", "000042")])
    body += "</div>"

    body += "<h2>Search &amp; Test</h2><div class='method-grid'>"
    body += card(".find(sub, start, end)", "Return lowest index of sub (-1 if not found)", "int",
        "Returns the lowest index where sub is found. Returns -1 if not found.",
        [("sub","str","—","Substring to search"),("start","int","0","Start searching from"),("end","int","len(s)","Stop before this index")],
        examples=[("","s='hello world'\\nprint(s.find('world'))     # 6\\nprint(s.find('xyz'))       # -1", "6")])
    body += card(".index(sub, start, end)", "Like .find() but raises ValueError if not found", "int",
        "Same as .find() but raises ValueError when sub is missing — safer for required substrings.",
        examples=[("","try:\\n    'hello'.index('xyz')\\nexcept ValueError as e:\\n    print(e)  # substring not found", "substring not found")])
    body += card(".rfind(sub, start, end)", "Return highest index of sub", "int",
        "Like .find() but searches right-to-left, returning the last occurrence.",
        examples=[("","print('abcabc'.rfind('b'))   # 4", "4")])
    body += card(".count(sub, start, end)", "Count non-overlapping occurrences", "int",
        "Returns how many times sub appears. Useful for frequency analysis.",
        examples=[("","print('banana'.count('a'))    # 3\\nprint('aaa'.count('aa'))     # 1  (non-overlapping!)", "3")])
    body += card(".startswith(prefix, start, end)", "True if string starts with prefix", "bool",
        "prefix can be a string or a tuple of strings to test against any of them.",
        [("prefix","str or tuple","—","Prefix(es) to match"),("start","int","0","Slice start"),("end","int","len(s)","Slice end")],
        examples=[("","url = 'https://example.com'\\nprint(url.startswith('http'))             # True", "True")])
    body += card(".endswith(suffix, start, end)", "True if string ends with suffix", "bool",
        "suffix can be a string or a tuple of strings.",
        examples=[("","f = 'report.pdf'\\nprint(f.endswith(('.pdf','.docx')))  # True", "True")])
    body += card(".isdigit()", "True if all chars are digits", "bool",
        "Returns True only if all characters are decimal digits [0-9].",
        examples=[("","print('2024'.isdigit())    # True", "True")])
    body += card(".isalpha()", "True if all chars are letters", "bool",
        "Every character must be alphabetic. Spaces, digits, or punctuation → False.",
        examples=[("","print('hello'.isalpha())   # True", "True")])
    body += card(".isalnum()", "True if all chars are letters or digits", "bool",
        "Alphanumeric — no spaces or punctuation.",
        examples=[("","print('abc123'.isalnum())   # True", "True")])
    body += card(".isspace()", "True if all chars are whitespace", "bool",
        "Whitespace includes spaces, tabs, newlines, vertical tabs. Empty string → False.",
        examples=[("","print('   \\t\\n'.isspace())   # True", "True")])
    body += card(".isupper()", "True if all cased chars are uppercase", "bool",
        "At least one cased character must exist and all must be uppercase.",
        examples=[("","print('HELLO'.isupper())   # True", "True")])
    body += card(".islower()", "True if all cased chars are lowercase", "bool",
        "Mirror of .isupper().",
        examples=[("","print('hello123'.islower())   # True", "True")])
    body += card(".istitle()", "True if string is title-cased", "bool",
        "Each word starts with an uppercase character followed by lowercase characters.",
        examples=[("","print('The Quick Fox'.istitle())   # True", "True")])
    body += card(".isprintable()", "True if all chars are printable", "bool",
        "Printable means not a control character.",
        examples=[("","print('hello\\n'.isprintable())  # False", "False")])
    body += "</div>"

    body += "<h2>Modification &amp; Transformation</h2><div class='method-grid'>"
    body += card(".strip(chars)", "Remove leading and trailing chars", "str",
        "Removes any combination of the specified chars from both ends. Default chars=None removes whitespace. Not a literal string — each char in chars is stripped individually.",
        [("chars","str","None","Characters to strip (each char independently)")],
        examples=[
            ("Default — strip whitespace","print('  hello  '.strip())       # 'hello'", "'hello'"),
            ("Custom chars","print('***hello***'.strip('*'))   # 'hello'", "'hello'"),
        ])
    body += card(".lstrip(chars)", "Strip from the left only", "str",
        "Same as .strip() but only removes from the leading (left) side.",
        examples=[("","print('   hello   '.lstrip())   # 'hello   '", "'hello   '")])
    body += card(".rstrip(chars)", "Strip from the right only", "str",
        "Same as .strip() but only removes from the trailing (right) side.",
        examples=[("","print('path/'.rstrip('/'))    # 'path'", "'path'")])
    body += card(".replace(old, new, count)", "Replace occurrences of old with new", "str",
        "Replaces all non-overlapping occurrences unless count is given.",
        [("old","str","—","Substring to search for"),("new","str","—","Replacement string"),("count","int","all","Max replacements")],
        examples=[
            ("Replace all","print('aabbcc'.replace('b','X'))        # 'aaXXcc'", "'aaXXcc'")
        ])
    body += card(".removeprefix(prefix)", "Remove prefix if present (Python 3.9+)", "str",
        "Removes prefix only if the string starts with it.",
        examples=[("","url = 'https://example.com'\\nprint(url.removeprefix('https://'))  # 'example.com'", "'example.com'")])
    body += card(".removesuffix(suffix)", "Remove suffix if present (Python 3.9+)", "str",
        "Mirror of .removeprefix().",
        examples=[("","f = 'report.html'\\nprint(f.removesuffix('.html'))   # 'report'", "'report'")])
    body += card(".expandtabs(tabsize)", "Replace tab characters with spaces", "str",
        "Replaces \\t with spaces to align to the next tab stop.",
        [("tabsize","int","8","Number of spaces per tab stop")],
        examples=[("","print('a\\tb\\tc'.expandtabs(4))   # 'a   b   c'", "'a   b   c'")])
    body += "</div>"

    body += "<h2>Split &amp; Join</h2><div class='method-grid'>"
    body += card(".split(sep, maxsplit)", "Split into list on sep", "list",
        "Splits at sep delimiter. Default sep=None splits on any whitespace.",
        [("sep","str","None","Delimiter. None=any whitespace"),("maxsplit","int","-1","Max splits. -1=unlimited")],
        examples=[
            ("Default whitespace","print('a  b  c'.split())          # ['a','b','c']", "['a', 'b', 'c']"),
        ])
    body += card(".rsplit(sep, maxsplit)", "Split from the right", "list",
        "Like .split() but starts counting splits from the right.",
        examples=[("","print('a:b:c:d'.rsplit(':',1))   # ['a:b:c', 'd']", "['a:b:c', 'd']")])
    body += card(".splitlines(keepends)", "Split on line boundaries", "list",
        "Splits on universal newlines. If keepends=True, line endings are preserved.",
        [("keepends","bool","False","Keep line-ending character in each line")],
        examples=[("","text = 'line1\\nline2\\nline3'\\nprint(text.splitlines())         # ['line1','line2','line3']", "['line1', 'line2', 'line3']")])
    body += card(".join(iterable)", "Join iterable elements with this string as separator", "str",
        "The string acts as the separator between each element.",
        examples=[
            ("Simple join","print(', '.join(['a','b','c']))        # 'a, b, c'", "'a, b, c'"),
        ])
    body += card(".partition(sep)", "Split into 3-tuple: (before, sep, after)", "tuple",
        "Splits at the <em>first</em> occurrence of sep, always returning a 3-tuple.",
        [("sep","str","—","Separator to split on (required)")],
        examples=[("","h='Content-Type: text/html'\\nbefore, sep, after = h.partition(': ')\\nprint(before)  # 'Content-Type'", "Content-Type")])
    body += card(".rpartition(sep)", "Partition from the right", "tuple",
        "Like .partition() but splits at the <em>last</em> occurrence of sep.",
        examples=[("","print('a/b/c'.rpartition('/'))   # ('a/b', '/', 'c')", "('a/b', '/', 'c')")])
    body += "</div>"

    body += "<h2>Formatting</h2><div class='method-grid'>"
    body += card(".format(*args, **kwargs)", "Format string with substitution", "str",
        "The classic format method. Placeholders are {0}, {1} or {name}.",
        examples=[
            ("Positional","print('{0} has {1} topics'.format('PyDocs',150))", "PyDocs has 150 topics"),
        ])
    body += card(".format_map(mapping)", "Format with a dict-like mapping", "str",
        "Like .format(**mapping) but the mapping is used directly.",
        examples=[("","from collections import defaultdict\\nd = defaultdict(lambda:'N/A')\\nd['name']='Alice'\\nprint('{name} from {city}'.format_map(d))   # 'Alice from N/A'", "Alice from N/A")])
    body += "</div>"

    body += "<h2>Encoding &amp; Translation</h2><div class='method-grid'>"
    body += card(".encode(encoding, errors)", "Encode string to bytes", "bytes",
        "Returns a <code>bytes</code> object representing the string encoded.",
        [("encoding","str","'utf-8'","Codec name"),("errors","str","'strict'","'strict'|'ignore'|'replace'")],
        examples=[
            ("UTF-8","print('hello'.encode('utf-8'))                 # b'hello'", "b'hello'"),
        ])
    body += card(".decode(encoding, errors)", "Decode bytes to string [bytes method]", "str",
        "This is a <em>bytes</em> method, not str.",
        examples=[("","b = 'café'.encode('utf-8')\\nprint(b.decode('utf-8'))     # 'café'", "'café'")])
    body += card(".maketrans(x, y, z)", "Build a translation table", "dict",
        "Static method. x → y maps each char in x to y. z is chars to map to None (deletion).",
        [("x","str or dict","—","Chars to replace (or dict mapping)"),("y","str","—","Replacement chars"),("z","str","None","Chars to delete")],
        examples=[
            ("Char substitution","table = str.maketrans('aeiou','*****')\\nprint('hello world'.translate(table))   # 'h*ll* w*rld'", "'h*ll* w*rld'"),
        ])
    body += card(".translate(table)", "Apply character mapping", "str",
        "Uses the translation table built by str.maketrans().",
        examples=[("","table = str.maketrans({'a':'@','e':'3'})\\nprint('hello world'.translate(table))   # 'h3llo world'", "'h3llo world'")])
    body += "</div>"

    body += """<h2>Slicing Quick Reference</h2>
<div class="code-box"><div class="code-header"><span class="lang">python</span><button class="copy-btn">Copy</button></div><pre>
s = "Hello, World!"
#    0123456789...
#   -13-12-11...  (negative indices from end)

s[0]       # 'H'        first char
s[-1]      # '!'        last char
s[0:5]     # 'Hello'    chars 0,1,2,3,4
s[7:]      # 'World!'   from 7 to end
s[:5]      # 'Hello'    start to 5
s[::2]     # 'Hlo ol!'  every 2nd char
s[::-1]    # '!dlroW ,olleH'  reversed
s[7:12]    # 'World'    slice [7,12)
</pre></div>"""
    body += page_nav("#py-vars","Variables &amp; Types","#py-lists","List Methods")
    return body

pages["py-strings"] = strings_page()

# ─── PAGE: List Methods ───────────────────────────────────────────────────────
def lists_page():
    body = section_header("List Methods","🐍 Python Basics","Beginner","Python for Data Analysis").replace('{id}','py-lists')
    body += "<p>Lists are <strong>mutable</strong>, ordered, heterogeneous sequences. They support in-place modification.</p>"

    body += "<h2>Mutation Methods</h2><div class='method-grid'>"
    body += card(".append(x)", "Add single element to end", "None",
        "Adds x as a single element to the end of the list in O(1) time.",
        examples=[
            ("","lst = [1,2,3]\\nlst.append(4)\\nprint(lst)             # [1, 2, 3, 4]","[1, 2, 3, 4]"),
        ])
    body += card(".extend(iterable)", "Add all elements from iterable", "None",
        "Extends the list by appending all items from iterable.",
        examples=[
            ("","lst = [1,2,3]\\nlst.extend([4,5,6])\\nprint(lst)            # [1, 2, 3, 4, 5, 6]", "[1, 2, 3, 4, 5, 6]"),
        ])
    body += card(".insert(i, x)", "Insert element before index i", "None",
        "Inserts x before position i. i=0 inserts at the start; i=len(lst) is equivalent to append().",
        [("i","int","—","Index to insert before"),("x","any","—","Element to insert")],
        examples=[("","lst=[1,2,3]\\nlst.insert(1,'X')\\nprint(lst)    # [1, 'X', 2, 3]", "[1, 'X', 2, 3]")])
    body += card(".remove(x)", "Remove first occurrence of x", "None",
        "Removes the first item equal to x. Raises ValueError if not found.",
        examples=[("","lst=[1,2,3,2]\\nlst.remove(2)\\nprint(lst)    # [1, 3, 2]", "[1, 3, 2]")])
    body += card(".pop(i=-1)", "Remove and return element at index i", "element",
        "Pops the element at index i (default last element).",
        [("i","int","-1","Index to pop. Negative indices work.")],
        examples=[
            ("Pop last","lst=[1,2,3]\\nv=lst.pop()\\nprint(v, lst)    # 3 [1, 2]", "3 [1, 2]"),
        ])
    body += card(".clear()", "Remove all elements", "None",
        "Empties the list in-place.",
        examples=[("","lst=[1,2,3]\\nlst.clear()\\nprint(lst)    # []", "[]")])
    body += card(".sort(*, key, reverse)", "Sort in-place", "None",
        "Sorts the list in-place using Timsort. key is a function applied to each element for comparison.",
        [("key","callable","None","Function applied to each element for ordering"),("reverse","bool","False","True=descending order")],
        examples=[
            ("Command","lst=[3,1,4,1,5]\\nlst.sort()\\nprint(lst)    # [1, 1, 3, 4, 5]", "[1, 1, 3, 4, 5]"),
        ])
    body += card(".reverse()", "Reverse in-place", "None",
        "Reverses the list in-place in O(n).",
        examples=[("","lst=[1,2,3]\\nlst.reverse()\\nprint(lst)    # [3, 2, 1]", "[3, 2, 1]")])
    body += "</div>"
    body += "<h2>Query &amp; Copy Methods</h2><div class='method-grid'>"
    body += card(".index(x, start, end)", "Return index of first occurrence of x", "int",
        "Raises ValueError if x is not present.",
        [("x","any","—","Value to find"),("start","int","0","Start of search range"),("end","int","len","End of search range")],
        examples=[("","lst=[10,20,30,20]\\nprint(lst.index(20))        # 1","1")])
    body += card(".count(x)", "Count occurrences of x", "int",
        "Returns how many times x appears in the list.",
        examples=[("","lst=[1,2,2,3,2,4]\\nprint(lst.count(2))   # 3","3")])
    body += card(".copy()", "Return a shallow copy", "list",
        "Returns a new list with the same elements. Equivalent to lst[:].",
        examples=[("","orig=[[1,2],[3,4]]\\ncopy=orig.copy()\\ncopy[0].append(99)\\nprint(orig)           # [[1, 2, 99], [3, 4]]","[[1, 2, 99], [3, 4]]")])
    body += "</div>"
    body += page_nav("#py-strings","String Methods","#py-dicts","Dictionary Methods")
    return body

pages["py-lists"] = lists_page()

# ─── PAGE: Dictionary Methods ─────────────────────────────────────────────────
def dicts_page():
    body = section_header("Dictionary Methods","🐍 Python Basics","Beginner","Python Data Science Handbook").replace('{id}','py-dicts')
    body += "<p>Dictionaries are <strong>mutable, ordered</strong> (Python 3.7+) key→value hash maps.</p>"
    body += "<div class='method-grid'>"
    body += card(".get(key, default)", "Get value for key without raising", "value",
        "Returns default (None if not specified) when key is missing. Never raises KeyError.",
        [("key","hashable","—","Key to look up"),("default","any","None","Returned if key missing")],
        examples=[("","d={'a':1,'b':2}\\nprint(d.get('a'))       # 1\\nprint(d.get('z',999))   # 999","1")])
    body += card(".setdefault(key, default)", "Get or set default for missing key", "value",
        "If key is in the dict, returns its value. If not, inserts key with default and returns default.",
        examples=[
            ("Grouping pattern","groups={}\\nfor word in ['cat','cow', 'dog']:\\n    groups.setdefault(word[0],[]).append(word)\\nprint(groups)   # {'c':['cat','cow'], 'd':['dog']}","{'c': ['cat', 'cow'], 'd': ['dog']}")
        ])
    body += card(".update(other)", "Merge another dict or iterable of pairs", "None",
        "Updates in-place. If key exists, its value is overwritten.",
        examples=[("","d={'a':1}\\nd.update({'b':2})\\nprint(d)   # {'a':1,'b':2}","{'a': 1, 'b': 2}")])
    body += card(".pop(key, default)", "Remove and return value", "value",
        "Removes key and returns its value. Raises KeyError if key not found and no default is given.",
        examples=[("","d={'a':1,'b':2}\\nprint(d.pop('a'))          # 1","1")])
    body += card(".popitem()", "Remove and return last inserted (key, value) pair", "tuple",
        "LIFO order since Python 3.7. Raises KeyError on empty dict.",
        examples=[("","d={'x':1,'y':2}\\nprint(d.popitem())   # ('y', 2)","('y', 2)")])
    body += card(".clear()", "Remove all items", "None",
        "Empties the dict in-place.", examples=[("","d={'a':1}; d.clear(); print(d)   # {}","{}")])
    body += card(".copy()", "Shallow copy", "dict",
        "Returns a new dict with the same key-value pairs.",
        examples=[("","d={'a':1}; e=d.copy(); e['b']=2; print(d)   # {'a': 1}","{'a': 1}")])
    body += card(".fromkeys(iterable, value)", "Create dict from iterable of keys", "dict",
        "Class method. Creates a new dict with each key from iterable mapped to value.",
        [("iterable","iterable","—","Source of keys"),("value","any","None","Default value for all keys")],
        examples=[("","d=dict.fromkeys(['a','b'],0)\\nprint(d)    # {'a':0,'b':0}","{'a': 0, 'b': 0}")])
    body += card(".keys()", "View of all keys", "dict_keys",
        "Returns a view object — it dynamically reflects dict changes.",
        examples=[("","d={'a':1,'b':2}\\nprint(list(d.keys()))   # ['a','b']","['a', 'b']")])
    body += card(".values()", "View of all values", "dict_values",
        "View of all values. Supports iteration and len().",
        examples=[("","print(list({'a':1,'b':2}.values()))   # [1, 2]","[1, 2]")])
    body += card(".items()", "View of all (key, value) pairs", "dict_items",
        "Most commonly used for iteration.",
        examples=[("","d={'a':1,'b':2}\\nfor k,v in d.items():\\n    print(f'{k} → {v}')","a → 1")])
    body += "</div>"
    body += page_nav("#py-lists","List Methods","#py-sets","Set Methods")
    return body

pages["py-dicts"] = dicts_page()

# ─── Assemble and Write ───────────────────────────────────────────────────────
base = r"C:\\Users\\DELL\\.gemini\\antigravity\\scratch\\python-docs-final\\"
with open(base + "v2_parts\\core.html", "r", encoding="utf-8") as f:
    core = f.read()

# Insert pages into the main container
main = '<main class="main">\n<div class="topbar"><div class="breadcrumb" id="bc">Home</div></div>\n<div class="content">\n'

for pid, content in pages.items():
    # Because section_header already opens <div class="page" id="...
    main += content + "\n"

main += '</div>\n</main>\n'

# Core is currently: CSS + SIDEBAR + HOME + JS, but they are flat.
# Let's rebuild the structure cleanly.
# The core.html contains raw strings.
# We'll split the JS from the rest.
js_part = core[core.find('<script>'):]
css_part = core[core.find('<style>'):core.find('</style>')+8]
sidebar_home = core[core.find('<nav class="sidebar"'):core.find('<script>')]

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PyDocs V2 — Complete Reference</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
{css_part}
</head>
<body>
<div id="top-progress"></div>
{sidebar_home}
{main}
{js_part}
</body>
</html>"""

with open(base + "v2.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"v2.html created: {len(html)/1024:.1f} KB")
