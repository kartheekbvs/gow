
# v2_compile.py — The master script to build v2.html

import json
import v2_python

# Load data science pages
try:
    with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\ds_pages.json", "r", encoding="utf-8") as f:
        ds_pages = json.load(f)
except FileNotFoundError:
    ds_pages = {}

# Merge python pages and ds pages
all_pages = {**v2_python.pages, **ds_pages}

# We add placeholders for the other 140 topics so the sidebar links work
# and don't just redirect to "home".
all_h1s = {
    # Basics
    "py-intro": "Introduction & Execution",
    "py-vars": "Variables & Data Types",
    "py-tuples": "Tuples & Unpacking",
    "py-ops": "Operators",
    "py-control": "Control Flow",
    "py-loops": "Loops & Iteration",
    "py-funcs": "Functions & Lambdas",
    "py-comp": "Comprehensions & Generators",
    "py-io": "File I/O",
    "py-exc": "Exception Handling",
    
    # OOP & Adv
    "py-oop": "Classes & Objects",
    "py-inherit": "Inheritance & MRO",
    "py-dunder": "Dunder / Magic Methods",
    "py-decor": "Decorators",
    "py-gen": "Generators & Iterators",
    "py-ctx": "Context Managers",
    "py-async": "Async / Await",

    # Stdlib
    "std-os": "os & pathlib",
    "std-json": "json & csv",
    "std-re": "re — Regular Expressions",
    "std-dt": "datetime & calendar",
    "std-coll": "collections",
    "std-itools": "itertools",
    "std-ftools": "functools",
    "std-log": "logging & argparse",
    "std-thread": "threading & futures",
    "std-typing": "typing",

    # Numpy
    "np-create": "Array Creation",
    "np-attrs": "Attributes & dtypes",
    "np-index": "Indexing & Slicing",
    "np-reshape": "Reshape & Stack",
    "np-math": "Math & Ufuncs",
    "np-linalg": "Linear Algebra",
    "np-agg": "Aggregations",
    "np-broad": "Broadcasting",
    "np-adv": "Advanced Operations",

    # Pandas (others)
    "pd-read": "read_csv & I/O",
    "pd-inspect": "Inspection Methods",
    "pd-index": "loc / iloc / query",
    "pd-groupby": "GroupBy & Aggregation",
    "pd-merge": "Merge / Join / Concat",
    "pd-reshape": "pivot / melt / stack",
    "pd-window": "Window Functions",
    "pd-dt": "Datetime & MultiIndex",
    "pd-str": ".str accessor",
    "pd-apply": "apply / map",

    # Matplotlib
    "mpl-setup": "figure & subplots",
    "mpl-types": "All Plot Types",
    "mpl-axes": "Axes Customization",
    "mpl-annot": "Annotations & Text",
    "mpl-layout": "Layout, 3D & rcParams",

    # Seaborn
    "sns-theme": "Theme & Palettes",
    "sns-dist": "Distribution Plots",
    "sns-cat": "Categorical Plots",
    "sns-matrix": "Heatmap & Clustermap",
    "sns-grid": "FacetGrid & PairGrid",

    # Scikit-Learn
    "sk-api": "Universal API",
    "sk-pre": "Preprocessing",
    "sk-pipe": "Pipeline & ColumnTransformer",
    "sk-cv": "Cross-Validation",
    "sk-models": "Classification Models",
    "sk-reg": "Regression Models",
    "sk-cluster": "Clustering",
    "sk-metrics": "Evaluation Metrics",

    # TensorFlow
    "tf-tensors": "Tensors & Variables",
    "tf-layers": "Keras Layers",
    "tf-model": "Model Building APIs",
    "tf-train": "Training & Callbacks",
    "tf-data": "tf.data Pipeline",
    "tf-transfer": "Transfer Learning",
}

for pid, title in all_h1s.items():
    if pid not in all_pages:
        all_pages[pid] = v2_python.section_header(title, "📚 Module", "Draft", "Building").replace('{id}',pid)
        all_pages[pid] += "<p><em>Content for this massive expansion is being actively written to the V2 build script. Please check back later!</em></p>\n</div>\n"

base = r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\\"
with open(base + "v2_parts\core.html", "r", encoding="utf-8") as f:
    core = f.read()

main = '<main class="main">\n<div class="topbar"><div class="breadcrumb" id="bc">Home</div></div>\n<div class="content">\n'
for pid, content in all_pages.items():
    main += content + "\n"
main += '</div>\n</main>\n'

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

print(f"Final v2.html created: {len(html)/1024:.1f} KB. Total Topics: {len(all_pages)}")
