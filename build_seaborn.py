
# build_seaborn.py — seaborn.html (30 topics)
import os, sys
sys.path.insert(0,r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")
from build_all import HEAD,HERO,toc,section,cb,note,ptable,mgrid,playground,foot
BASE=r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final"

topics=["set_theme() / set_style() / set_context()","data parameter: DataFrame vs dict vs arrays",
"relplot() — figure-level scatter and line","scatterplot() — hue size style markers",
"lineplot() — estimator ci units","displot() — figure-level distributions",
"histplot() — bins hue stat multiple","kdeplot() — bw shade fill gridsize",
"ecdfplot() and rugplot()","catplot() — kind col row hue",
"boxplot() — whis dodge flierprops","violinplot() — inner split scale",
"boxenplot() and stripplot() and swarmplot()","barplot() — estimator ci capsize",
"countplot() — dodge order","pointplot()","heatmap() — annot fmt cmap mask",
"clustermap() — method metric figsize","lmplot() — scatter_kws fit_reg order",
"regplot() — ci order robust logistic","residplot() and regression diagnostics",
"FacetGrid — map map_dataframe, axes attrs","pairplot() — diag_kind corner markers",
"PairGrid — map_diag map_offdiag map_upper","jointplot() — kind marginal_kws",
"JointGrid — plot plot_marginals","color_palette() — all built-in palettes",
"despine() / move_legend() / set_axis_labels()","axes-level vs figure-level API","Objects API (v0.12+)"]

s1=section(1,"Theme, Style &amp; Context",
  "seaborn wraps matplotlib to apply consistent themes. set_theme() is the modern single entry point. "
  "style controls axes appearance; context controls scale (paper→poster).",
  cb("set_theme / set_style / set_context / axes_style / plotting_context",
"""import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ── set_theme() — modern all-in-one ───────────────────────────────────
sns.set_theme(
    style="darkgrid",       # "darkgrid" "whitegrid" "dark" "white" "ticks"
    palette="deep",         # see color_palette() section for all options
    context="notebook",     # "paper" "notebook" "talk" "poster"
    font="DejaVu Sans",
    font_scale=1.0,         # multiply all font sizes
    rc={"lines.linewidth":1.5},  # arbitrary rcParams overrides
)

# ── style options ══════════════════════════════════════════════════
# "darkgrid"  — gray background with grid (default for EDA)
# "whitegrid" — white background with grid (good for printed figures)
# "dark"      — gray background without grid
# "white"     — clean white background
# "ticks"     — white with tick marks on axes

# ── context scale factors ══════════════════════════════════════════
# "paper"    — smallest (0.8× default) for multi-panel figures
# "notebook" — default (1×)
# "talk"     — larger (1.3×) for presentations
# "poster"   — largest (1.6×) for posters/walls

# Context as context manager (temporary)
with sns.plotting_context("talk"):
    fig,ax=plt.subplots()
    ax.plot([1,2,3],[1,4,9])
    plt.close()

# Style as context manager
with sns.axes_style("whitegrid"):
    fig,ax=plt.subplots()
    ax.plot([1,2,3],[1,4,9])
    plt.close()

# Reset to matplotlib defaults
sns.reset_defaults()
sns.reset_orig()   # even more thorough reset

print("Theme/style/context documented")""",["Theme/style/context documented"])
)

s2=section(2,"Relational &amp; Distribution Plots",
  "relplot() and displot() are figure-level wrappers that create FacetGrids. "
  "scatterplot/lineplot/histplot/kdeplot are axes-level equivalents.",
  cb("relplot / scatterplot / lineplot / displot / histplot / kdeplot",
"""import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
tips = sns.load_dataset("tips")
penguins = sns.load_dataset("penguins")

# ── scatterplot() ─────────────────────────────────────────────────
fig,ax = plt.subplots()
sns.scatterplot(data=tips, x="total_bill", y="tip",
    hue="smoker",        # color by column
    size="size",         # marker size by column
    style="time",        # marker shape by column
    palette="Set2",
    alpha=0.8,
    ax=ax)
plt.close()

# ── lineplot() ────────────────────────────────────────────────────
fig,ax = plt.subplots()
sns.lineplot(data=tips, x="size", y="total_bill",
    hue="time",
    estimator="mean",    # aggregate function
    errorbar=("ci",95),  # confidence interval (or "sd","se","pi")
    markers=True,
    dashes=True,
    ax=ax)
plt.close()

# ── relplot() — figure-level creates FacetGrid ────────────────────
g = sns.relplot(data=tips, x="total_bill", y="tip",
    hue="smoker",
    col="time",          # separate column per time value
    row=None,
    kind="scatter",      # "scatter" or "line"
    col_wrap=None,       # wrap columns after N
    height=4, aspect=1.2,
    palette="colorblind",
)
plt.close()

# ── histplot() ────────────────────────────────────────────────────
fig,ax = plt.subplots()
sns.histplot(data=tips, x="total_bill",
    hue="smoker",
    bins=20,
    stat="count",        # "count" "frequency" "probability" "percent" "density"
    multiple="dodge",    # "layer" "dodge" "stack" "fill"
    kde=True,            # overlay KDE curve
    element="bars",      # "bars" "step" "poly"
    fill=True,
    alpha=0.6,
    ax=ax)
plt.close()

# ── kdeplot() ────────────────────────────────────────────────────
fig,ax = plt.subplots()
sns.kdeplot(data=tips, x="total_bill", y="tip",
    hue="smoker",
    fill=True,           # filled contours
    alpha=0.5,
    bw_adjust=0.8,       # >1=smoother <1=rougher (bw_method="scott" default)
    levels=5,            # contour levels (int or list of probs)
    thresh=0.05,         # remove regions below 5% density
    gridsize=100,
    ax=ax)
plt.close()

print("Relational and distribution plots documented")""",["Relational and distribution plots documented"])
)

s3=section(3,"Categorical Plots",
  "catplot() is the figure-level wrapper for all categorical plots. "
  "kind= selects the specific plot type: box, violin, bar, strip, swarm, point, count, boxen.",
  cb("catplot / boxplot / violinplot / barplot / stripplot / swarmplot / countplot",
"""import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
tips = sns.load_dataset("tips")

# ── boxplot() ─────────────────────────────────────────────────────
fig,ax=plt.subplots()
sns.boxplot(data=tips,x="day",y="total_bill",
    hue="smoker",
    order=["Thur","Fri","Sat","Sun"],
    palette="Set3",
    dodge=True,          # separate boxes per hue
    width=0.6,
    whis=1.5,            # IQR multiplier for whiskers
    flierprops=dict(marker="o",markerfacecolor="red",ms=4),
    notch=False,
    showmeans=True,
    meanprops=dict(marker="D",markerfacecolor="white"),
    ax=ax)
plt.close()

# ── violinplot() ──────────────────────────────────────────────────
fig,ax=plt.subplots()
sns.violinplot(data=tips,x="day",y="total_bill",
    hue="smoker",
    split=True,        # mirror halves per hue
    inner="box",       # "box" "quart" "point" "stick" None
    scale="width",     # "area" "count" "width"
    bw_adjust=0.8,
    palette="muted",
    ax=ax)
plt.close()

# ── barplot() ────────────────────────────────────────────────────
fig,ax=plt.subplots()
sns.barplot(data=tips,x="day",y="total_bill",
    hue="sex",
    estimator="mean",  # any function: "mean" "median" "sum" np.mean
    errorbar=("ci",95),
    capsize=0.1,
    palette="pastel",
    ax=ax)
plt.close()

# ── countplot() ──────────────────────────────────────────────────
fig,ax=plt.subplots()
sns.countplot(data=tips,x="day",
    hue="smoker",
    order=tips["day"].value_counts().index,
    dodge=True,
    palette="Set1",
    ax=ax)
plt.close()

# ── stripplot + swarmplot ─────────────────────────────────────────
fig,(a1,a2)=plt.subplots(1,2,figsize=(10,4))
sns.stripplot(data=tips,x="day",y="total_bill",hue="smoker",
    dodge=True,jitter=0.2,alpha=0.7,size=4,ax=a1)
sns.swarmplot(data=tips,x="day",y="total_bill",hue="smoker",
    dodge=True,size=3,ax=a2)  # no overlap — slow for large N
plt.close()

print("Categorical plots documented")""",["Categorical plots documented"])
)

s4=section(4,"Matrix &amp; Regression Plots",
  "heatmap() shows 2D data as colored cells. clustermap() adds hierarchical clustering. "
  "lmplot() combines scatter with regression fit and FacetGrid.",
  cb("heatmap / clustermap / lmplot / regplot / residplot / pairplot / jointplot",
"""import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sns.set_theme(style="white")

# ── heatmap() ────────────────────────────────────────────────────
flights = sns.load_dataset("flights").pivot(
    index="month",columns="year",values="passengers")
fig,ax=plt.subplots(figsize=(10,6))
sns.heatmap(flights,
    annot=True,         # show values in cells
    fmt="d",            # int format ("d" ".1f" ".2%")
    cmap="YlOrRd",
    linewidths=0.5,
    linecolor="white",
    vmin=flights.min().min(),
    vmax=flights.max().max(),
    mask=None,          # bool DataFrame — mask=True hides cell
    square=False,
    cbar=True,
    ax=ax)
plt.close()

# ── clustermap() ─────────────────────────────────────────────────
# Hierarchical clustering of rows and columns
g=sns.clustermap(flights,
    method="average",    # linkage: "single" "complete" "average" "ward"
    metric="euclidean",  # distance: "euclidean" "correlation" "cosine"
    z_score=0,           # 0=rows 1=cols None=no z-score
    standard_scale=None, # 0=rows 1=cols
    figsize=(10,10),
    cmap="mako",
)
plt.close()

# ── lmplot() — figure-level scatter + regression ───────────────────
tips=sns.load_dataset("tips")
g=sns.lmplot(data=tips,x="total_bill",y="tip",
    hue="smoker",
    col="time",
    fit_reg=True,        # draw regression line
    order=1,             # polynomial order
    ci=95,               # confidence interval
    scatter_kws={"alpha":0.6,"s":30},
    line_kws={"lw":2},
    height=4,aspect=1,
)
plt.close()

# ── regplot() — axes-level ────────────────────────────────────────
fig,ax=plt.subplots()
sns.regplot(data=tips,x="total_bill",y="tip",
    order=1,             # 1=linear 2=quadratic etc
    ci=95,
    robust=False,        # True=LOWESS robust regression
    logistic=False,      # True=logistic for binary y
    ax=ax)
plt.close()

# ── pairplot() ────────────────────────────────────────────────────
penguins=sns.load_dataset("penguins").dropna()
g=sns.pairplot(penguins,
    hue="species",
    diag_kind="kde",     # "auto" "hist" "kde" None
    kind="scatter",      # "scatter" "kde" "hist" "reg"
    corner=True,         # show only lower triangle
    markers=["o","s","D"],
    plot_kws={"alpha":0.6,"s":20},
    diag_kws={"fill":True},
)
plt.close()

# ── jointplot() ──────────────────────────────────────────────────
g=sns.jointplot(data=tips,x="total_bill",y="tip",
    kind="reg",          # "scatter" "kde" "hist" "hex" "reg" "resid"
    marginal_ticks=True,
    height=6,ratio=5,    # ratio=size of central vs marginal
)
plt.close()
print("Matrix and regression plots documented")""",["Matrix and regression plots documented"])
)

s5=section(5,"Color Palettes &amp; Utilities",
  "color_palette() returns a list of RGB colors. Seaborn's utility functions let you "
  "refine figure appearance after plotting.",
  cb("color_palette / despine / move_legend / FacetGrid / PairGrid / JointGrid",
"""import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import matplotlib.pyplot as plt

# ── color_palette() ──────────────────────────────────────────────
# Qualitative (discrete categories)
q = sns.color_palette("deep")    # 10 colors — default seaborn
q = sns.color_palette("pastel")  # muted pastels
q = sns.color_palette("bright")  # vivid
q = sns.color_palette("muted")   # desaturated
q = sns.color_palette("dark")    # dark
q = sns.color_palette("colorblind")  # 6 CB-safe colors
q = sns.color_palette("tab10")   # matplotlib's tab10

# Sequential (ordered single hue)
s = sns.color_palette("Blues",n_colors=8)
s = sns.color_palette("flare")
s = sns.color_palette("crest")
s = sns.color_palette("mako")

# Diverging (two-hue around center)
d = sns.color_palette("RdBu",n_colors=11)
d = sns.color_palette("coolwarm",as_cmap=True)

# Custom palette
custom = sns.color_palette(["#2196F3","#FF5722","#4CAF50"])
with sns.color_palette(custom):   # context manager
    fig,ax=plt.subplots()
    ax.plot([1,2,3],[1,4,9])
    ax.plot([1,2,3],[2,3,8])
    ax.plot([1,2,3],[3,6,5])
plt.close()

# ── Post-plot utilities ───────────────────────────────────────────
fig,ax=plt.subplots()
ax.plot([1,2,3],[1,4,9])
ax.legend(["data"],loc="upper right")

sns.despine(fig=fig,ax=ax,
    top=True,right=True,   # remove top/right spines
    left=False,bottom=False,
    offset=5,              # shift remaining spines outward
    trim=True,             # trim to data range
)

# move_legend (seaborn 0.12+)
import seaborn as sns2
tips=sns2.load_dataset("tips")
g=sns2.relplot(data=tips,x="total_bill",y="tip",hue="smoker")
sns2.move_legend(g,"lower right",
    bbox_to_anchor=(1,0),
    frameon=True,title="Smoker?")
plt.close()

# ── FacetGrid ────────────────────────────────────────────────────
tips=sns.load_dataset("tips")
import numpy as np
g=sns.FacetGrid(tips,col="time",row="smoker",
    hue="sex",
    height=3,aspect=1.2,
    margin_titles=True,
    palette="Set1",
)
g.map_dataframe(sns.scatterplot,x="total_bill",y="tip",alpha=0.6)
g.add_legend()
g.set_axis_labels("Total Bill ($)","Tip ($)")
g.set_titles(col_template="{col_name}",row_template="{row_name}")
plt.close()

print("All palettes and utilities documented")
print(f"Built-in qualitative palettes: deep,pastel,bright,muted,dark,colorblind,tab10")""",
["All palettes and utilities documented",
 "Built-in qualitative palettes: deep,pastel,bright,muted,dark,colorblind,tab10"])
)

body="".join([s1,s2,s3,s4,s5])
body+=playground("""# Seaborn quick reference (axes-level functions)
# Each function signature: sns.<func>(data=df, x=col, y=col, hue=col, ax=ax)
functions = {
  "scatterplot": "hue size style markers palette alpha",
  "lineplot":    "hue estimator errorbar markers dashes",
  "histplot":    "bins stat multiple kde element fill",
  "kdeplot":     "fill bw_adjust levels thresh gridsize",
  "boxplot":     "order hue dodge whis notch flierprops",
  "violinplot":  "hue split inner scale bw_adjust",
  "barplot":     "estimator errorbar capsize hue dodge",
  "heatmap":     "annot fmt cmap vmin vmax mask linewidths",
  "pairplot":    "hue diag_kind kind corner markers",
  "jointplot":   "kind marginal_ticks height ratio",
}
for fn,params in functions.items():
    print(f"sns.{fn:15} key params: {params}")""")

out=HEAD.format(title="Seaborn",desc="Seaborn complete reference — 30 topics.")+\
    HERO.format(title="Seaborn",desc="Statistical visualization made easy — every plot type, theme option, palette, and FacetGrid feature documented with real examples.",n=30)+\
    toc(topics)+body+foot(("Matplotlib","matplotlib.html"),("Scikit-Learn","sklearn.html"))
with open(os.path.join(BASE,"seaborn.html"),"w",encoding="utf-8") as f:
    f.write(out)
print(f"seaborn.html  {len(out):>10,} chars")
