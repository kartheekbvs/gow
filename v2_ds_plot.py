
# v2_ds_plot.py — generates visualization pages for v2.html
import sys, json

sys.path.insert(0, r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")
import v2_python

card = v2_python.card
section_header = v2_python.section_header
page_nav = v2_python.page_nav
pages = {}

# ─── PAGE: Matplotlib Plot Types ──────────────────────────────────────────────
def mpl_types_page():
    body = section_header("Matplotlib Plot Types","📊 Matplotlib","Intermediate","Python Data Science Handbook")
    body += "<p>Matplotlib provides a wide array of basic plotting functions on the <code>Axes</code> object.</p>"
    
    body += "<h2>Basic Plots</h2><div class='method-grid'>"
    body += card("ax.plot(x, y, fmt)", "Line plot", "Line2D list",
        "fmt is a shorthand format string like 'ro-' (Red, Circle, Solid Line).",
        [("x","array-like","—","X-axis data"),("y","array-like","—","Y-axis data"),("fmt","str","''","Format string")],
        examples=[("","ax.plot([1,2,3], [1,4,9], 'ro--')","")])
    body += card("ax.scatter(x, y, s, c)", "Scatter plot with varying marker size/color", "PathCollection",
        "s maps to area (size^2). c maps to color array.",
        examples=[("","ax.scatter(x, y, s=area, c=colors, alpha=0.5)","")])
    body += card("ax.bar(x, height, width, bottom)", "Vertical bar chart", "BarContainer",
        "For categorical comparison.",
        examples=[("","ax.bar(['A','B','C'], [10,20,15], color='blue')","")])
    body += "</div>"
    
    body += "<h2>Distributions &amp; Heatmaps</h2><div class='method-grid'>"
    body += card("ax.hist(x, bins)", "Compute and draw histogram", "tuple",
        "Returns (n, bins, patches).",
        examples=[("","ax.hist(data, bins=30, alpha=0.7)","")])
    body += card("ax.boxplot(x)", "Box and whisker plot", "dict",
        "Shows median, quartiles, and outliers.",
        examples=[("","ax.boxplot([data1, data2], labels=['A','B'])","")])
    body += card("ax.imshow(X, cmap)", "Display data as an image (heatmap)", "AxesImage",
        "Highly customizable with different colormaps.",
        examples=[("","img = ax.imshow(matrix, cmap='viridis')\\nfig.colorbar(img)","")])
    body += "</div>"
    body += page_nav("#mpl-setup","Figure &amp; Subplots","#mpl-axes","Axes Customization")
    return body

pages["mpl-types"] = mpl_types_page()

# ─── PAGE: Seaborn Categorical ──────────────────────────────────────────────
def sns_cat_page():
    body = section_header("Categorical Plots","🎨 Seaborn","Beginner","Python for Data Analysis")
    body += "<p>Seaborn provides high-level interfaces for drawing attractive and informative statistical graphics.</p>"
    
    body += "<h2>Categorical Distributions</h2><div class='method-grid'>"
    body += card("sns.boxplot(data, x, y, hue)", "Box plot with hue", "Axes",
        "Visualizes distributions across categories.",
        examples=[("","sns.boxplot(data=tips, x='day', y='total_bill', hue='smoker')","")])
    body += card("sns.violinplot(data, x, y)", "Violin plot", "Axes",
        "Combines boxplot with Kernel Density Estimation (KDE).",
        examples=[("","sns.violinplot(data=tips, x='day', y='total_bill')","")])
    body += card("sns.barplot(data, x, y, estimator)", "Summary bar plot", "Axes",
        "Shows point estimates and confidence intervals automatically computing mean (default) or other estimators.",
        examples=[("","sns.barplot(data=tips, x='day', y='total_bill', estimator=np.sum)","")])
    body += "</div>"
    body += page_nav("#sns-dist","Distribution Plots","#sns-matrix","Heatmap &amp; Clustermap")
    return body

pages["sns-cat"] = sns_cat_page()

try:
    with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\ds_pages.json", "r", encoding="utf-8") as f:
        existing = json.load(f)
except Exception:
    existing = {}

existing.update(pages)

with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\ds_pages.json", "w", encoding="utf-8") as f:
    json.dump(existing, f)

print(f"Added {len(pages)} Plotting pages.")
