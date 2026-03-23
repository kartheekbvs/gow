
# v2_ds.py — generates Data Science pages for v2.html
import sys
import v2_python  # We can re-use the helpers and the pages dict

card = v2_python.card
section_header = v2_python.section_header
page_nav = v2_python.page_nav
pages = {}

# ─── PAGE: Pandas Create & Read ───────────────────────────────────────────────
def pandas_page():
    body = section_header("Pandas Objects & I/O","🐼 Pandas","Intermediate","Python for Data Analysis")
    body += "<p>Pandas is the standard for tabular data in Python. Core objects are <code>Series</code> (1D) and <code>DataFrame</code> (2D).</p>"
    body += "<h2>Series &amp; DataFrame Creation</h2><div class='method-grid'>"
    body += card("pd.Series(data, index, dtype)", "Create 1D labeled array", "Series",
        "Data can be a dict, list, scalar, or ndarray. If data is a dict, keys become the index.",
        [("data","array-like/dict","—","Data values"),("index","array-like","RangeIndex","Labels for data")],
        examples=[("","import pandas as pd\\ns = pd.Series([10, 20], index=['a', 'b'])\\nprint(s['a'])   # 10", "10")])
    body += card("pd.DataFrame(data, index, columns)", "Create 2D tabular structure", "DataFrame",
        "Most common inputs: dict of lists, list of dicts, or 2D ndarray.",
        examples=[("","df = pd.DataFrame({'Name':['Ali','Bob'], 'Age':[25,30]})\\nprint(df.columns)   # Index(['Name', 'Age'], dtype='object')", "Index(['Name', 'Age'], dtype='object')")])
    body += "</div>"
    
    body += "<h2>Reading Data</h2><div class='method-grid'>"
    body += card("pd.read_csv(filepath)", "Load CSV to DataFrame", "DataFrame",
        "Supports huge number of parameters for parsing dates, handling missing values, and chunking.",
        [("filepath","str","—","Path or URL"),("parse_dates","list","False","Cols to parse as datetime"),("index_col","int/str","None","Column to use as row labels")],
        examples=[("","df = pd.read_csv('data.csv', index_col=0, parse_dates=['date'])", "")])
    body += card("pd.read_json(path)", "Load JSON to DataFrame", "DataFrame",
        "Orient depends on json format (records, columns, index).",
        examples=[("","df = pd.read_json('data.json', orient='records')", "")])
    body += card("pd.read_parquet(path)", "Read Parquet file", "DataFrame",
        "Parquet is highly compressed column-oriented storage. Faster and smaller than CSV.",
        examples=[("","df = pd.read_parquet('data.parquet')", "")])
    body += "</div>"

    body += "<h2>Basic Inspection</h2><div class='method-grid'>"
    body += card("df.head(n)", "Return first n rows", "DataFrame", "Default n=5.", examples=[("","print(df.head(2))","")])
    body += card("df.info()", "Print concise summary", "None", "Shows columns, non-null counts, and memory usage.", examples=[("","df.info()","")])
    body += card("df.describe()", "Generate descriptive statistics", "DataFrame", "Count, mean, std, min, percentiles, max for numeric columns.", examples=[("","print(df.describe())","")])
    body += card("df.value_counts()", "Return counts of unique rows/values", "Series", "Very common on Series to see categorical distributions.", examples=[("","print(df['category'].value_counts())","")])
    body += "</div>"
    body += page_nav("#np-create","NumPy","#pd-clean","Data Cleaning")
    return body

pages["pd-create"] = pandas_page()

# ─── PAGE: Pandas Clean & Merge ───────────────────────────────────────────────
def pandas_clean_page():
    body = section_header("Cleaning & Grouping","🐼 Pandas","Intermediate","Python for Data Analysis")
    
    body += "<h2>Missing Data</h2><div class='method-grid'>"
    body += card("df.isna() / df.isnull()", "Detect missing values", "DataFrame", "Returns boolean mask of same size.", examples=[("","print(df.isna().sum())   # Count missing per column","")])
    body += card("df.dropna(axis, how, thresh)", "Drop missing values", "DataFrame",
        "axis=0 drops rows, axis=1 drops columns.",
        [("how","str","'any'","'any' or 'all'"),("thresh","int","None","Require at least this many non-NA")],
        examples=[("","df_clean = df.dropna(subset=['Age', 'Income'])", "")])
    body += card("df.fillna(value, method)", "Fill NA/NaN values", "DataFrame",
        "Can fill with a scalar, dict of scalars per column, or ffill/bfill.",
        examples=[("","df['Age'] = df['Age'].fillna(df['Age'].mean())","")])
    body += "</div>"

    body += "<h2>Grouping &amp; Aggregation</h2><div class='method-grid'>"
    body += card("df.groupby(by)", "Group DataFrame by mapper or columns", "DataFrameGroupBy",
        "The core of split-apply-combine strategy.",
        examples=[("","grouped = df.groupby('Department')\\nprint(grouped['Salary'].mean())","")])
    body += card(".agg(func)", "Aggregate using one or more operations", "DataFrame",
        "Applies function(s) over the groups.",
        examples=[("","df.groupby('Dep').agg({'Salary': ['mean', 'max'], 'Age': 'mean'})","")])
    body += "</div>"

    body += "<h2>Merge &amp; Join</h2><div class='method-grid'>"
    body += card("pd.merge(left, right, how, on)", "Database-style join", "DataFrame",
        "how='inner'|'left'|'right'|'outer'.",
        [("how","str","'inner'","Type of merge"),("on","str/list","None","Column to join on")],
        examples=[("","merged = pd.merge(df_users, df_orders, how='left', on='user_id')","")])
    body += card("pd.concat(objs, axis)", "Concatenate pandas objects", "DataFrame",
        "axis=0 (stack vertically), axis=1 (side-by-side).",
        examples=[("","combined = pd.concat([df_2023, df_2024], axis=0)","")])
    body += "</div>"
    body += page_nav("#pd-create","Pandas I/O","#pd-index","Indexing")
    return body

pages["pd-clean"] = pandas_clean_page()

# ─── Merge new pages into existing python pages dictionary ──────────────────
# This script can write just its parts, or we can compile via a master script
import json
with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\ds_pages.json", "w", encoding="utf-8") as f:
    json.dump(pages, f)
print("v2_ds.py complete")
