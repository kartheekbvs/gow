
# v2_ds_np.py — generates NumPy pages for v2.html
import sys, json

sys.path.insert(0, r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")
import v2_python  # Ensure we have the helpers

card = v2_python.card
section_header = v2_python.section_header
page_nav = v2_python.page_nav
pages = {}

# ─── PAGE: NumPy Creation ─────────────────────────────────────────────────────
def np_create_page():
    body = section_header("Array Creation","🔢 NumPy","Intermediate","Python Data Science Handbook")
    body += "<p>NumPy's core object is the ndarray (N-dimensional array), which is a fast, memory-efficient multi-dimensional array providing vectorized arithmetic operations.</p>"
    body += "<h2>From Python Structures</h2><div class='method-grid'>"
    body += card("np.array(object, dtype=None)", "Create array from list/tuple", "ndarray",
        "Converts Python lists or tuples into NumPy arrays. Auto-infers dtype unless specified.",
        [("object","array-like","—","Source data"),("dtype","data-type","None","Desired data type")],
        examples=[("","import numpy as np\\narr = np.array([[1, 2], [3, 4]])\\nprint(arr)","[[1 2]\\n [3 4]]")])
    body += card("np.asarray(a)", "Convert input to array, avoid copying if possible", "ndarray",
        "Similar to np.array, but passes through ndarrays without copying them. Good for function guards.",
        examples=[("","lst = [1, 2]\\narr = np.asarray(lst)","")])
    body += "</div>"

    body += "<h2>Initialized Arrays</h2><div class='method-grid'>"
    body += card("np.zeros(shape, dtype)", "Array of zeros", "ndarray",
        "Creates array filled with 0. Default dtype is float64.",
        [("shape","int or tuple","—","Shape of new array")],
        examples=[("","z = np.zeros((2, 3), dtype=int)\\nprint(z)","[[0 0 0]\\n [0 0 0]]")])
    body += card("np.ones(shape, dtype)", "Array of ones", "ndarray",
        "Creates array filled with 1. Default dtype is float64.",
        examples=[("","o = np.ones((2, 2))","[[1. 1.]\\n [1. 1.]]")])
    body += card("np.full(shape, fill_value)", "Array of a constant value", "ndarray",
        "Fills the array with fill_value.",
        examples=[("","f = np.full((2, 2), 99)","[[99 99]\\n [99 99]]")])
    body += card("np.empty(shape)", "Uninitialized array", "ndarray",
        "Faster than zeros/ones, but leaves memory uninitialized (contains random garbage values). Use only when overwriting immediately.",
        examples=[("","e = np.empty((2, 2))","")])
    body += "</div>"

    body += "<h2>Ranges &amp; Sequences</h2><div class='method-grid'>"
    body += card("np.arange(start, stop, step)", "Return evenly spaced values", "ndarray",
        "Like Python's built-in range, but returns an array.",
        examples=[("","a = np.arange(0, 10, 2)\\nprint(a)","[0 2 4 6 8]")])
    body += card("np.linspace(start, stop, num)", "Evenly spaced numbers over interval", "ndarray",
        "Creates num evenly spaced samples. stop is inclusive by default.",
        [("num","int","50","Number of samples to generate")],
        examples=[("","l = np.linspace(0, 1, 5)\\nprint(l)","[0.   0.25 0.5  0.75 1.  ]")])
    body += card("np.logspace(start, stop, num)", "Evenly spaced on log scale", "ndarray",
        "Base defaults to 10.",
        examples=[("","l = np.logspace(0, 2, 3)\\nprint(l)","[  1.  10. 100.]")])
    body += "</div>"
    body += page_nav("#std-typing","typing","#np-attrs","Attributes &amp; dtypes")
    return body

pages["np-create"] = np_create_page()

# ─── Assemble into master dict ────────────────────────────────────────────────
try:
    with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\ds_pages.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
except Exception:
    existing = {}

existing.update(pages)

with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\ds_pages.json", "w", encoding="utf-8") as f:
    json.dump(existing, f)

print(f"v2_ds_np.py added {len(pages)} NumPy pages.")
