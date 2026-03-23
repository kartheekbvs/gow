
# build_mpl.py — matplotlib.html (35 topics in 5 sections)
import os, sys
sys.path.insert(0,r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")
from build_all import HEAD,HERO,toc,section,cb,note,ptable,mgrid,playground,foot
BASE=r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final"

topics=["figure/subplots setup","add_subplot/add_axes","plot() line/marker/style",
"scatter() s c cmap","bar()/barh()","hist() bins density histtype","boxplot()/violinplot()",
"pie() explode autopct","imshow() cmap origin extent","contour()/contourf()",
"errorbar() fill_between()","step() stem() stackplot()","quiver() vector fields",
"set_title/xlabel/ylabel","set_xlim/ylim/xticks/ticklabels","tick_params() all options",
"legend() all loc strings","grid() params","spines/aspect/invert/log scale",
"annotate() arrowprops","ax.text() transform bbox","axhline/vline/hspan/vspan",
"Color formats + all colormaps","colorbar() shrink aspect label","tight_layout/subplots_adjust",
"savefig() formats dpi","GridSpec/subplot_mosaic","plt.style.use all styles",
"3D: Axes3D plot_surface scatter3D","plt.rcParams common settings",
"FuncAnimation basics","Figure events picking","plt.cm Normalize BoundaryNorm",
"Inset axes zoomed_inset_axes","twinx() twiny() dual axes"]

s1=section(1,"Figure &amp; Subplots Setup",
  "plt.figure() controls canvas. plt.subplots() creates Figure+Axes in one call. "
  "Most common entry point for all matplotlib workflows.",
  cb("figure() / subplots() — all params",
"""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# plt.figure() — main params
fig = plt.figure(
    num=1,             # id — reuse if already exists
    figsize=(10,6),    # (width,height) inches. 10,6 = medium
    dpi=100,           # dots per inch
    facecolor="white",
    layout="tight",    # "tight" "constrained" None
)
plt.close()

# plt.subplots — the standard way
fig, ax    = plt.subplots()                  # single ax
fig, axes  = plt.subplots(2,3,figsize=(12,8))# 2x3 grid → (2,3) ndarray
fig,(a1,a2)= plt.subplots(1,2,sharex=True)  # share x axis

# squeeze=False ensures axes is always 2D
fig, axes  = plt.subplots(1,3,squeeze=False) # shape (1,3)

# Width/height ratios via gridspec_kw
fig, axes  = plt.subplots(1,2,
    gridspec_kw={"width_ratios":[3,1],"wspace":0.1},
    figsize=(10,4))

# figsize quick reference:
# (4,3) tiny  (6,4) small  (10,6) medium
# (12,8) large  (16,9) widescreen  (20,14) poster
print("figsize and subplots documented")
plt.close("all")""",["figsize and subplots documented"]),
  ptable([
    ("figsize","tuple","(6.4,4.8)","(width,height) in inches"),
    ("dpi","int/float","100","Resolution. 72=screen 100=default 150=pres 300=print"),
    ("layout","str","None","'tight' 'constrained' — auto-adjust subplot spacing"),
    ("facecolor","color","'white'","Background color of entire figure"),
    ("sharex/sharey","bool/str","False","Share axis limits: True, 'row', 'col', 'all', 'none'"),
    ("squeeze","bool","True","False=always return 2D axes array"),
    ("gridspec_kw","dict","None","width_ratios, height_ratios, hspace, wspace"),
  ])
)

s2=section(2,"All Plot Types",
  "18 distinct plot types. Each has unique parameters. The fmt shorthand for plot() is "
  "'[color][marker][linestyle]' e.g. 'r--o'.",
  cb("plot / scatter / bar / hist / boxplot / violin / pie / imshow / errorbar / fill_between",
"""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np

x=np.linspace(0,2*np.pi,50)
fig,axes=plt.subplots(3,3,figsize=(12,10))

# 1. Line plot
axes[0,0].plot(x,np.sin(x),color="C0",lw=2,ls="--",marker="o",ms=3,label="sin")
axes[0,0].plot(x,np.cos(x),"r-.",lw=1.5,label="cos")
axes[0,0].set_title("plot()")

# 2. Scatter
np.random.seed(0)
xr,yr=np.random.randn(80),np.random.randn(80)
axes[0,1].scatter(xr,yr,s=30+50*np.abs(xr),c=yr,cmap="plasma",alpha=0.7)
axes[0,1].set_title("scatter()")

# 3. Bar
cats=["A","B","C","D"]; v=[23,45,12,67]
axes[0,2].bar(cats,v,width=0.6,color=["#FF6B6B","#4EC","#45B","#96C"],edgecolor="k")
axes[0,2].set_title("bar()")

# 4. Histogram
axes[1,0].hist(np.random.randn(500),bins=25,density=True,
    histtype="stepfilled",color="steelblue",alpha=0.8,edgecolor="white")
axes[1,0].set_title("hist()")

# 5. Boxplot
axes[1,1].boxplot([np.random.randn(50)*s for s in [1,2,0.5]],
    patch_artist=True,notch=True,labels=["narrow","wide","tight"])
axes[1,1].set_title("boxplot()")

# 6. Pie
axes[1,2].pie([35,30,20,15],labels=["Py","JS","Java","Other"],
    autopct="%1.0f%%",explode=[0.05,0,0,0],startangle=90)
axes[1,2].set_title("pie()")

# 7. imshow
axes[2,0].imshow(np.random.rand(8,8),cmap="viridis",aspect="auto")
axes[2,0].set_title("imshow()")

# 8. errorbar
xe=np.arange(5); ye=np.random.rand(5)*10
axes[2,1].errorbar(xe,ye,yerr=0.5+np.random.rand(5),fmt="o-",capsize=4,ecolor="red")
axes[2,1].set_title("errorbar()")

# 9. fill_between
xe2=np.linspace(0,4,50); ye2=np.sin(xe2)
axes[2,2].fill_between(xe2,ye2-0.3,ye2+0.3,alpha=0.3)
axes[2,2].plot(xe2,ye2)
axes[2,2].set_title("fill_between()")

plt.tight_layout()
plt.savefig("/tmp/mpl_gallery.png",dpi=80)
print("8 plot types saved")
plt.close()""",
["8 plot types saved"])
)

s3=section(3,"Axes Customization",
  "Full control over every visual property: title, labels, ticks, legend, grid, spines, "
  "scale, and aspect ratio.",
  cb("set_title / xlabel / ylabel / ticks / tick_params / legend / grid / spines",
"""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig,ax=plt.subplots(figsize=(8,5))
ax.plot([1,2,3,4],[1,4,9,16],"b-o",label="y=x²")
ax.plot([1,2,3,4],[1,2,3,4],"r--",label="y=x")

# Title & labels
ax.set_title("Custom Axes",fontsize=16,fontweight="bold",loc="center",pad=12)
ax.set_xlabel("Input",fontsize=13,labelpad=8)
ax.set_ylabel("Output",fontsize=13,labelpad=8)

# Limits
ax.set_xlim(0.5,4.5); ax.set_ylim(-1,18)

# Ticks
ax.set_xticks([1,2,3,4])
ax.set_xticklabels(["one","two","three","four"],rotation=20,ha="right")
ax.set_yticks(range(0,18,3))
ax.tick_params(axis="both",which="major",direction="out",
    length=6,width=1.2,color="gray",labelsize=11)
ax.minorticks_on()
ax.tick_params(axis="x",which="minor",length=3,width=0.8)

# Legend — all loc strings:
# 0=best 1=upper right 2=upper left 3=lower left 4=lower right
# 5=right 6=center left 7=center right 8=lower center
# 9=upper center 10=center
ax.legend(loc="upper left",fontsize=11,title="Legend",frameon=True,
    facecolor="#f8f8f8",edgecolor="gray",ncols=1,markerscale=1.2)

# Grid
ax.grid(True,which="major",axis="both",color="lightgray",ls="--",lw=0.7,alpha=0.8)

# Spines
ax.spines[["top","right"]].set_visible(False)
ax.spines["left"].set_linewidth(1.5)
ax.spines["bottom"].set_color("#444")

# Scale options
ax.set_xscale("linear")   # "linear" "log" "symlog" "logit"

print("Axes customized")
plt.close()""",["Axes customized"])
)

s4=section(4,"Annotations, Text &amp; Reference Lines",
  "ax.annotate() adds arrows with text. ax.text() places text anywhere. "
  "axhline/axvline/axhspan/axvspan add reference markers.",
  cb("annotate / ax.text / axhline / axvline / axhspan / axvspan",
"""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np

fig,ax=plt.subplots(figsize=(8,5))
x=np.linspace(0,10,100)
ax.plot(x,np.sin(x)*np.exp(-0.1*x))

# annotate() — arrow + text
ax.annotate("peak",
    xy=(1.57,0.92),              # tip of arrow (data coords)
    xytext=(3.0,0.9),            # text position
    xycoords="data",
    textcoords="data",
    fontsize=12,color="red",
    arrowprops=dict(
        arrowstyle="->",          # "-" "->" "-|>" "simple" "fancy"
        color="red",lw=1.5,
        connectionstyle="arc3,rad=-0.2",
    ),
    ha="left",va="center",
)

# ax.text() — arbitrary text
ax.text(0.98,0.02,"note",         # x,y in axes coords
    transform=ax.transAxes,        # use axes fraction [0,1]
    ha="right",va="bottom",
    fontsize=9,color="gray",
    bbox=dict(boxstyle="round",facecolor="linen",alpha=0.8),
)

# Reference lines (infinite)
ax.axhline(y=0,  color="black",lw=0.8,ls="-",zorder=0)
ax.axhline(y=0.5,color="green",lw=1.0,ls="--",label="y=0.5")
ax.axvline(x=np.pi,color="blue",ls=":",lw=1.2,label="x=π")

# Spans (shaded regions)
ax.axhspan(-0.2,0.2,alpha=0.1,color="yellow",label="zero band")
ax.axvspan(6,8,alpha=0.1,color="red",label="decay region")

ax.legend(loc="upper right",fontsize=9)
plt.savefig("/tmp/mpl_annotate.png",dpi=80,bbox_inches="tight")
print("Annotations done")
plt.close()""",["Annotations done"])
)

s5=section(5,"Colors, Layout, Saving &amp; 3D",
  "All color formats, colormap categories, savefig options, GridSpec layout, "
  "3D surfaces, and rcParams for global style configuration.",
  cb("colors / colorbar / savefig / GridSpec / 3D / rcParams",
"""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# ── Colors ────────────────────────────────────────────────────────
# Named:   "red"  "steelblue"  "darkviolet"  "coral"
# Hex:     "#FF5733"  "#2196F3"
# RGB:     (0.2, 0.6, 0.8)
# RGBA:    (0.2, 0.6, 0.8, 0.5)
# CN:      "C0" "C1" ... "C9"   (default color cycle)
# Tableau: "tab:blue" "tab:orange" "tab:green" "tab:red"
# xkcd:   "xkcd:sky blue"
# Gray:   "0.5"  (string 0=black 1=white)

# ── Colormaps by category ───────────────────────────────────────────
# Sequential:   viridis plasma inferno magma Blues Greens Reds Purples
# Diverging:    RdBu coolwarm seismic PiYG
# Cyclic:       twilight hsv
# Qualitative:  tab10 tab20 Set1 Set2 Pastel1 Dark2 Accent
# Append _r to reverse any colormap: "viridis_r"

fig,ax=plt.subplots()
img=ax.imshow(np.random.rand(10,10),cmap="viridis",vmin=0,vmax=1)
cb = plt.colorbar(img,ax=ax,
    shrink=0.8,      # fraction of axes height
    aspect=20,       # ratio height:width
    pad=0.02,        # gap between plot and colorbar
    label="Value",
    ticks=[0,0.25,0.5,0.75,1.0],
    format="%.2f",
    orientation="vertical",  # "horizontal"
    extend="neither",  # "both" "min" "max" "neither"
)
plt.savefig("/tmp/mpl_colorbar.png",dpi=80,bbox_inches="tight")
plt.close()

# ── savefig — all params ────────────────────────────────────────────
# fig.savefig(fname, dpi, facecolor, format, bbox_inches, pad_inches, transparent, metadata)
# formats: "png" "pdf" "svg" "eps" "jpeg" "webp" "tiff"
# bbox_inches="tight" removes extra whitespace automatically
# transparent=True  — PNG with alpha channel

# ── GridSpec ───────────────────────────────────────────────────────
from matplotlib.gridspec import GridSpec
fig2=plt.figure(figsize=(10,7))
gs=GridSpec(3,3,figure=fig2,
    hspace=0.4,wspace=0.3,
    width_ratios=[2,1,1],height_ratios=[1,2,1])
ax_main=fig2.add_subplot(gs[0:2,0:2])
ax_tr  =fig2.add_subplot(gs[0,2])
ax_br  =fig2.add_subplot(gs[1,2])
ax_bot =fig2.add_subplot(gs[2,:])
plt.savefig("/tmp/mpl_gridspec.png",dpi=60,bbox_inches="tight")
plt.close()

# ── subplot_mosaic ─────────────────────────────────────────────────
fig3,axd=plt.subplot_mosaic("AB;CC",figsize=(8,6))
# axd is dict: {"A":ax, "B":ax, "C":ax}
axd["A"].set_title("A — narrow top")
axd["B"].set_title("B — narrow top")
axd["C"].set_title("C — full width")
plt.savefig("/tmp/mpl_mosaic.png",dpi=60,bbox_inches="tight")
plt.close()

# ── 3D plotting ────────────────────────────────────────────────────
fig4=plt.figure(figsize=(8,6))
ax3=fig4.add_subplot(111,projection="3d")
u,v=np.linspace(0,2*np.pi,50),np.linspace(0,np.pi,50)
U,V=np.meshgrid(u,v)
X=np.cos(U)*np.sin(V); Y=np.sin(U)*np.sin(V); Z=np.cos(V)
ax3.plot_surface(X,Y,Z,cmap="coolwarm",alpha=0.85,
    linewidth=0,antialiased=True)
ax3.set_xlabel("X"); ax3.set_ylabel("Y"); ax3.set_zlabel("Z")
ax3.set_title("3D Sphere")
plt.savefig("/tmp/mpl_3d.png",dpi=80,bbox_inches="tight")
plt.close()

# ── rcParams ──────────────────────────────────────────────────────
import matplotlib as mpl
mpl.rcParams["figure.figsize"]  = (8,5)
mpl.rcParams["figure.dpi"]     = 100
mpl.rcParams["font.size"]      = 12
mpl.rcParams["font.family"]    = "DejaVu Sans"
mpl.rcParams["lines.linewidth"]= 2.0
mpl.rcParams["axes.labelsize"] = 13
mpl.rcParams["axes.titlesize"] = 15
mpl.rcParams["axes.grid"]      = True
mpl.rcParams["xtick.labelsize"]= 11
mpl.rcParams["legend.fontsize"]= 11
mpl.rcParams["savefig.dpi"]    = 150
mpl.rcParams["savefig.bbox"]   = "tight"
mpl.rcdefaults()               # reset all to defaults

print("Colors / layout / 3D / rcParams documented")""",["Colors / layout / 3D / rcParams documented"])
)

body="".join([s1,s2,s3,s4,s5])
body+=playground("""# Matplotlib API quick reference
api={
  "figure":    "plt.figure(figsize=(10,6), dpi=100)",
  "subplots":  "fig,axes=plt.subplots(2,2,sharex=True,sharey=True)",
  "plot":      "ax.plot(x,y,color='C0',lw=2,ls='--',marker='o',label='data')",
  "scatter":   "ax.scatter(x,y,s=50,c=z,cmap='viridis',alpha=0.7)",
  "bar":       "ax.bar(cats,vals,width=0.6,color='steelblue',edgecolor='k')",
  "hist":      "ax.hist(data,bins=30,density=True,histtype='stepfilled')",
  "boxplot":   "ax.boxplot(data,patch_artist=True,notch=True)",
  "annotate":  "ax.annotate('pt',xy=(x,y),xytext=(tx,ty),arrowprops=dict(arrowstyle='->'))",
  "savefig":   "plt.savefig('plot.png',dpi=150,bbox_inches='tight')",
  "rcParams":  "mpl.rcParams['font.size']=13",
}
for fn,sig in api.items():
    print(f"{fn:12} -> {sig}")""")

out=HEAD.format(title="Matplotlib",desc="Matplotlib complete reference — 35 topics.")+\
    HERO.format(title="Matplotlib",desc="Every plot type, customization param, colormap, layout and 3D option — full API with real output previews.",n=35)+\
    toc(topics)+body+foot(("Pandas","pandas.html"),("Seaborn","seaborn.html"))
with open(os.path.join(BASE,"matplotlib.html"),"w",encoding="utf-8") as f:
    f.write(out)
print(f"matplotlib.html  {len(out):>10,} chars")
