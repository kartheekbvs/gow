
# v2_core.py — generates the CSS/JS/sidebar/home for v2.html
# Run: python v2_core.py  (writes to v2_parts/core.html)

import os
os.makedirs(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts", exist_ok=True)

CSS = """
<style>
:root{
  --bg:#ffffff; --sidebar:#f8fafc; --card:#f4f6f9;
  --border:#e2e8f0; --accent:#2563eb; --accent-g:#16a34a;
  --accent-o:#d97706; --accent-r:#dc2626;
  --text:#1e293b; --text-muted:#64748b;
  --code-bg:#1e2030; --shadow:0 1px 4px rgba(0,0,0,.08);
}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);
     display:flex;line-height:1.65;font-size:15px;}

/* ── Sidebar ── */
.sidebar{width:280px;background:var(--sidebar);border-right:1px solid var(--border);
  position:fixed;height:100vh;display:flex;flex-direction:column;z-index:1000;
  box-shadow:2px 0 8px rgba(0,0,0,.05);}
.logo{padding:18px 20px;border-bottom:1px solid var(--border);display:flex;
  align-items:center;gap:10px;text-decoration:none;color:var(--accent);
  font-weight:800;font-size:18px;letter-spacing:-.5px;}
.logo span{color:var(--text);}
.search-box{padding:12px 14px;border-bottom:1px solid var(--border);}
.search-box input{width:100%;padding:8px 12px;background:#fff;
  border:1.5px solid var(--border);color:var(--text);border-radius:8px;font-size:13px;
  outline:none;transition:border-color .2s;}
.search-box input:focus{border-color:var(--accent);}
.nav-links{flex:1;overflow-y:auto;padding-bottom:90px;}
.nav-links::-webkit-scrollbar{width:4px;}
.nav-links::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}
.nav-section{border-bottom:1px solid var(--border);}
.nav-header{padding:11px 18px;font-size:13px;font-weight:700;cursor:pointer;
  display:flex;justify-content:space-between;align-items:center;
  user-select:none;color:var(--text);}
.nav-header:hover{background:rgba(37,99,235,.05);}
.nav-header .arrow{transition:transform .2s;font-size:10px;color:var(--text-muted);}
.nav-section.open .arrow{transform:rotate(90deg);}
.nav-items{display:none;background:#fff;}
.nav-section.open .nav-items{display:block;}
.nav-link{display:block;padding:7px 18px 7px 36px;text-decoration:none;
  color:var(--text-muted);font-size:13px;border-left:3px solid transparent;
  transition:all .15s;}
.nav-link:hover{color:var(--accent);background:rgba(37,99,235,.04);}
.nav-link.active{color:var(--accent);border-left-color:var(--accent);
  background:rgba(37,99,235,.07);font-weight:600;}
.nav-link.done::after{content:' ✓';color:var(--accent-g);font-size:11px;}
.progress-bar{position:absolute;bottom:0;width:100%;padding:12px 14px;
  background:var(--sidebar);border-top:1px solid var(--border);}
.progress-track{width:100%;height:5px;background:var(--border);border-radius:3px;}
.progress-fill{height:100%;background:var(--accent);width:0%;
  transition:width .4s;border-radius:3px;}
#top-progress{position:fixed;top:0;left:0;height:3px;background:var(--accent);
  z-index:2000;width:0%;transition:width .1s;}

/* ── Main ── */
.main{margin-left:280px;flex:1;display:flex;flex-direction:column;min-height:100vh;}
.topbar{position:sticky;top:0;background:rgba(255,255,255,.95);
  backdrop-filter:blur(8px);padding:13px 40px;border-bottom:1px solid var(--border);
  z-index:100;font-size:13px;color:var(--text-muted);
  box-shadow:0 1px 4px rgba(0,0,0,.06);}
.breadcrumb span{color:var(--accent);font-weight:600;}
.content{max-width:880px;margin:0 auto;padding:40px;width:100%;}
.page{display:none;}
.page.active{display:block;animation:fadeIn .25s;}
@keyframes fadeIn{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}

/* ── Typography ── */
h1{font-size:30px;color:var(--text);margin-bottom:18px;font-weight:800;
  letter-spacing:-.5px;line-height:1.25;}
h2{font-size:19px;color:var(--text);margin:36px 0 14px;
  border-bottom:2px solid var(--border);padding-bottom:8px;font-weight:700;}
h3{font-size:15px;color:var(--text-muted);margin:20px 0 10px;text-transform:uppercase;
  letter-spacing:.05em;font-weight:700;}
p{margin-bottom:14px;color:var(--text);line-height:1.7;}
code{background:#f1f5f9;color:#d63384;padding:2px 6px;border-radius:4px;
  font-family:'JetBrains Mono',monospace;font-size:13px;}

/* ── Badges ── */
.badge-row{display:flex;gap:12px;margin-bottom:22px;font-size:12px;
  align-items:center;flex-wrap:wrap;}
.badge{padding:3px 10px;border-radius:20px;font-weight:600;}
.badge-module{background:#eff6ff;color:var(--accent);}
.badge-beginner{background:#f0fdf4;color:var(--accent-g);}
.badge-intermediate{background:#fffbeb;color:var(--accent-o);}
.badge-advanced{background:#fef2f2;color:var(--accent-r);}
.source-note{color:var(--text-muted);font-style:italic;font-size:12px;}

/* ── Code Blocks ── */
.code-box{background:var(--code-bg);border-radius:10px;margin:16px 0;
  overflow:hidden;box-shadow:var(--shadow);border:1px solid #2d2d44;}
.code-header{background:#252540;padding:7px 14px;display:flex;
  justify-content:space-between;align-items:center;}
.lang{font-family:'JetBrains Mono',monospace;font-size:11px;
  text-transform:uppercase;color:#7c8db8;letter-spacing:.08em;}
.copy-btn{background:transparent;border:1px solid #3d3d60;color:#7c8db8;
  cursor:pointer;padding:3px 10px;border-radius:5px;font-size:11px;
  transition:all .15s;}
.copy-btn:hover{border-color:#6366f1;color:#a5b4fc;}
pre{padding:16px;overflow-x:auto;font-family:'JetBrains Mono',monospace;
  font-size:13px;color:#cdd6f4;line-height:1.6;}
.kw{color:#cba6f7;} .st{color:#a6e3a1;} .cm{color:#6c7086;font-style:italic;}
.fn{color:#89b4fa;} .nm{color:#fab387;} .op{color:#89dceb;}

/* ── Accordion Method Cards ── */
.method-grid{display:flex;flex-direction:column;gap:6px;margin:16px 0;}
.method-card{border:1.5px solid var(--border);border-radius:10px;
  background:#fff;overflow:hidden;transition:border-color .2s;}
.method-card:hover{border-color:#93c5fd;}
.method-card.open{border-color:var(--accent);}
.method-header{display:flex;align-items:center;gap:12px;padding:12px 16px;
  cursor:pointer;user-select:none;}
.method-header code{background:#eff6ff;color:var(--accent);font-size:14px;
  font-weight:700;padding:3px 10px;border-radius:6px;flex-shrink:0;}
.method-sig{color:var(--text-muted);font-size:13px;flex:1;}
.method-ret{color:var(--accent-g);font-size:12px;font-family:'JetBrains Mono',monospace;
  background:#f0fdf4;padding:2px 8px;border-radius:4px;flex-shrink:0;}
.method-chevron{font-size:11px;color:var(--text-muted);transition:transform .2s;
  margin-left:auto;flex-shrink:0;}
.method-card.open .method-chevron{transform:rotate(90deg);color:var(--accent);}
.method-body{display:none;padding:16px 20px 20px;border-top:1px solid var(--border);
  background:#fafcff;}
.method-card.open .method-body{display:block;}
.method-body p{font-size:14px;margin-bottom:12px;}
.method-body .param-table{width:100%;border-collapse:collapse;
  margin:12px 0;font-size:13px;}
.param-table th{background:#f8fafc;color:var(--text-muted);padding:8px 10px;
  border:1px solid var(--border);font-size:11px;text-transform:uppercase;
  letter-spacing:.06em;}
.param-table td{padding:8px 10px;border:1px solid var(--border);}
.param-table td:first-child{font-family:'JetBrains Mono',monospace;color:var(--accent);
  font-size:12px;font-weight:600;}

/* ── Comparison Tables ── */
table.comp{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px;}
table.comp th{background:#f8fafc;color:var(--text-muted);padding:10px 12px;
  border:1px solid var(--border);font-size:12px;text-transform:uppercase;
  letter-spacing:.05em;font-weight:700;}
table.comp td{padding:10px 12px;border:1px solid var(--border);}
table.comp tr:hover td{background:#f0f7ff;}

/* ── Mistake Boxes ── */
.mistakes{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:16px 0;}
.mistake{padding:14px;border-radius:8px;border:1.5px solid;}
.mistake h4{font-size:12px;margin-bottom:10px;text-transform:uppercase;
  letter-spacing:.06em;font-weight:700;}
.mistake.wrong{border-color:#fecaca;background:#fff5f5;}
.mistake.wrong h4{color:var(--accent-r);}
.mistake.right{border-color:#bbf7d0;background:#f0fdf4;}
.mistake.right h4{color:var(--accent-g);}
.mistake pre{font-size:12px;background:transparent;padding:0;color:var(--text);}

/* ── Cheat Sheet ── */
.cheat-sheet{background:#f0f7ff;border:1.5px solid #93c5fd;
  padding:18px 20px;border-radius:10px;margin:24px 0;}
.cheat-sheet h3{color:var(--accent);font-size:13px;text-transform:uppercase;
  letter-spacing:.08em;margin-bottom:12px;margin-top:0;}
.cheat-sheet ul{list-style:none;}
.cheat-sheet li{margin-bottom:7px;font-family:'JetBrains Mono',monospace;
  font-size:13px;color:var(--text);}

/* ── Notes / Tips / Warning ── */
.note,.tip,.warn{padding:14px 18px;border-radius:8px;margin:16px 0;
  font-size:14px;border-left:4px solid;}
.note{background:#f0f7ff;border-color:var(--accent);color:var(--text);}
.tip{background:#f0fdf4;border-color:var(--accent-g);color:var(--text);}
.warn{background:#fffbeb;border-color:var(--accent-o);color:var(--text);}
.note strong,.tip strong,.warn strong{display:block;font-size:12px;
  text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;}
.note strong{color:var(--accent);}
.tip strong{color:var(--accent-g);}
.warn strong{color:var(--accent-o);}

/* ── Homepage ── */
.hero{text-align:center;padding:50px 0 30px;}
.hero h1{font-size:40px;background:linear-gradient(135deg,var(--accent),#7c3aed);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:14px;}
.hero p{color:var(--text-muted);font-size:17px;max-width:540px;margin:0 auto 30px;}
.stats{display:flex;justify-content:center;gap:24px;margin:30px 0;flex-wrap:wrap;}
.stat{text-align:center;background:#f8fafc;padding:18px 36px;
  border-radius:12px;border:1.5px solid var(--border);}
.stat h2{font-size:28px;color:var(--accent);margin:0;border:none;padding:0;}
.stat small{font-size:11px;color:var(--text-muted);text-transform:uppercase;
  letter-spacing:.08em;}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:10px;}
.card{background:#fff;border:1.5px solid var(--border);padding:18px;
  border-radius:12px;text-decoration:none;color:inherit;display:flex;
  gap:14px;transition:all .2s;box-shadow:var(--shadow);}
.card:hover{border-color:var(--accent);transform:translateY(-2px);
  box-shadow:0 4px 16px rgba(37,99,235,.12);}
.card-icon{font-size:28px;flex-shrink:0;}
.card h3{font-size:15px;margin-bottom:4px;color:var(--text);}
.card p{font-size:13px;color:var(--text-muted);margin:0;}

/* ── Page Nav ── */
.page-nav{display:flex;justify-content:space-between;margin-top:50px;
  padding-top:24px;border-top:1.5px solid var(--border);}
.nav-btn{padding:10px 20px;border:1.5px solid var(--border);border-radius:8px;
  text-decoration:none;color:var(--text);background:#fff;
  display:flex;flex-direction:column;transition:all .2s;}
.nav-btn:hover{border-color:var(--accent);color:var(--accent);}
.nav-dir{font-size:11px;color:var(--text-muted);text-transform:uppercase;}
.nav-btn.right-nav{text-align:right;border-color:#93c5fd;}

/* ── Responsive ── */
@media(max-width:768px){
  .sidebar{transform:translateX(-100%);transition:transform .3s;}
  .sidebar.open{transform:translateX(0);}
  .main{margin-left:0;}
  .cards,.mistakes{grid-template-columns:1fr;}
}
</style>
"""

JS = """
<script>
// ── Progress ──────────────────────────────────────────────────────────────────
const TOPIC_COUNT = 150;

function initProgress(){
  const prog = JSON.parse(localStorage.getItem('pydocs_v2') || '{}');
  let done = 0;
  document.querySelectorAll('.nav-link').forEach(l=>{
    const id = l.getAttribute('href').substring(1);
    if(prog[id]){l.classList.add('done');done++;}
  });
  setPGBar((done/TOPIC_COUNT)*100);
  document.getElementById('pg-txt').innerText = Math.round((done/TOPIC_COUNT)*100)+'% Complete';
}

function setPGBar(pct){
  document.getElementById('main-pg').style.width = pct+'%';
}

// ── Router ────────────────────────────────────────────────────────────────────
function router(){
  const id = location.hash.substring(1) || 'home';
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));

  const page = document.getElementById('page-'+id);
  if(page) page.classList.add('active');
  else{location.hash='home';return;}

  window.scrollTo(0,0);
  const link = document.querySelector(`.nav-link[href="#${id}"]`);
  if(link){
    link.classList.add('active');
    link.closest('.nav-section').classList.add('open');
    const chap = link.closest('.nav-section').querySelector('.nav-header .nav-label').innerText;
    document.getElementById('bc').innerHTML = `<span>${chap}</span> → ${link.innerText}`;

    // Mark as visited after 2 seconds
    clearTimeout(window._markTimer);
    window._markTimer = setTimeout(()=>{
      const prog = JSON.parse(localStorage.getItem('pydocs_v2')||'{}');
      if(!prog[id]){
        prog[id]=true;
        localStorage.setItem('pydocs_v2',JSON.stringify(prog));
        link.classList.add('done');
        const doneCount = Object.keys(prog).length;
        setPGBar((doneCount/TOPIC_COUNT)*100);
        document.getElementById('pg-txt').innerText=Math.round((doneCount/TOPIC_COUNT)*100)+'% Complete';
      }
    },2000);
  } else {
    document.getElementById('bc').innerHTML='<a href="#home" style="color:var(--accent)">Home</a>';
  }
}

// ── Sidebar collapse ──────────────────────────────────────────────────────────
function initSidebar(){
  document.querySelectorAll('.nav-header').forEach(h=>{
    h.addEventListener('click',()=>h.parentElement.classList.toggle('open'));
  });
}

// ── Search ───────────────────────────────────────────────────────────────────
function initSearch(){
  document.getElementById('search').addEventListener('input',e=>{
    const q = e.target.value.toLowerCase().trim();
    document.querySelectorAll('.nav-link').forEach(l=>{
      const match = !q || l.innerText.toLowerCase().includes(q);
      l.style.display = match?'block':'none';
    });
    document.querySelectorAll('.nav-section').forEach(s=>{
      const any = Array.from(s.querySelectorAll('.nav-link')).some(l=>l.style.display!=='none');
      s.style.display = any?'block':'none';
      if(q && any) s.classList.add('open');
    });
  });
}

// ── Copy Buttons ─────────────────────────────────────────────────────────────
function initCopy(){
  document.querySelectorAll('.copy-btn').forEach(b=>{
    b.addEventListener('click',()=>{
      const code = b.closest('.code-box').querySelector('pre').innerText;
      navigator.clipboard.writeText(code).catch(()=>{
        const t=document.createElement('textarea');
        t.value=code;document.body.appendChild(t);t.select();
        document.execCommand('copy');document.body.removeChild(t);
      });
      b.innerText='✓ Copied';b.style.borderColor='#6366f1';
      setTimeout(()=>{b.innerText='Copy';b.style.borderColor='';},2000);
    });
  });
}

// ── Top progress bar while scrolling ─────────────────────────────────────────
function initScroll(){
  window.addEventListener('scroll',()=>{
    const h=document.documentElement;
    const pct=(h.scrollTop/(h.scrollHeight-h.clientHeight))*100;
    document.getElementById('top-progress').style.width=pct+'%';
  });
}

// ── Accordion method cards ─────────────────────────────────────────────────
function toggleMethod(header){
  const card = header.closest('.method-card');
  const wasOpen = card.classList.contains('open');
  // Optionally close siblings:
  // card.closest('.method-grid')?.querySelectorAll('.method-card.open')
  //   .forEach(c=>c.classList.remove('open'));
  card.classList.toggle('open',!wasOpen);
}

// ── Init ──────────────────────────────────────────────────────────────────────
window.addEventListener('hashchange',router);
window.onload = function(){
  initSidebar();
  initSearch();
  initCopy();
  initScroll();
  initProgress();
  router();
};
</script>
"""

SIDEBAR = """
<nav class="sidebar" id="sidebar">
  <a href="#home" class="logo">🐍 <span>PyDocs</span> <sup style="font-size:10px;background:var(--accent);color:#fff;padding:1px 5px;border-radius:4px;margin-left:2px;">v2</sup></a>
  <div class="search-box"><input type="text" id="search" placeholder="🔍 Search 150+ topics…"></div>
  <div class="nav-links">

    <div class="nav-section open">
      <div class="nav-header"><span class="nav-label">🐍 Python Basics</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#py-intro"    class="nav-link">Introduction &amp; Execution</a>
        <a href="#py-vars"     class="nav-link">Variables &amp; Data Types</a>
        <a href="#py-strings"  class="nav-link">String Methods (30+)</a>
        <a href="#py-lists"    class="nav-link">List Methods (14)</a>
        <a href="#py-dicts"    class="nav-link">Dictionary Methods</a>
        <a href="#py-sets"     class="nav-link">Set Methods</a>
        <a href="#py-tuples"   class="nav-link">Tuples &amp; Unpacking</a>
        <a href="#py-ops"      class="nav-link">Operators</a>
        <a href="#py-control"  class="nav-link">Control Flow</a>
        <a href="#py-loops"    class="nav-link">Loops &amp; Iteration</a>
        <a href="#py-funcs"    class="nav-link">Functions &amp; Lambdas</a>
        <a href="#py-comp"     class="nav-link">Comprehensions &amp; Generators</a>
        <a href="#py-io"       class="nav-link">File I/O</a>
        <a href="#py-exc"      class="nav-link">Exception Handling</a>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-header"><span class="nav-label">🏗️ OOP &amp; Advanced</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#py-oop"      class="nav-link">Classes &amp; Objects</a>
        <a href="#py-inherit"  class="nav-link">Inheritance &amp; MRO</a>
        <a href="#py-dunder"   class="nav-link">Dunder / Magic Methods</a>
        <a href="#py-decor"    class="nav-link">Decorators</a>
        <a href="#py-gen"      class="nav-link">Generators &amp; Iterators</a>
        <a href="#py-ctx"      class="nav-link">Context Managers</a>
        <a href="#py-async"    class="nav-link">Async / Await</a>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-header"><span class="nav-label">📦 Python Stdlib</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#std-os"       class="nav-link">os &amp; pathlib</a>
        <a href="#std-json"     class="nav-link">json &amp; csv</a>
        <a href="#std-re"       class="nav-link">re — Regular Expressions</a>
        <a href="#std-dt"       class="nav-link">datetime &amp; calendar</a>
        <a href="#std-coll"     class="nav-link">collections</a>
        <a href="#std-itools"   class="nav-link">itertools</a>
        <a href="#std-ftools"   class="nav-link">functools</a>
        <a href="#std-log"      class="nav-link">logging &amp; argparse</a>
        <a href="#std-thread"   class="nav-link">threading &amp; futures</a>
        <a href="#std-typing"   class="nav-link">typing</a>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-header"><span class="nav-label">🔢 NumPy</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#np-create"   class="nav-link">Array Creation</a>
        <a href="#np-attrs"    class="nav-link">Attributes &amp; dtypes</a>
        <a href="#np-index"    class="nav-link">Indexing &amp; Slicing</a>
        <a href="#np-reshape"  class="nav-link">Reshape &amp; Stack</a>
        <a href="#np-math"     class="nav-link">Math &amp; Ufuncs</a>
        <a href="#np-linalg"   class="nav-link">Linear Algebra</a>
        <a href="#np-agg"      class="nav-link">Aggregations</a>
        <a href="#np-broad"    class="nav-link">Broadcasting</a>
        <a href="#np-adv"      class="nav-link">Advanced (einsum, vectorize)</a>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-header"><span class="nav-label">🐼 Pandas</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#pd-create"   class="nav-link">DataFrame &amp; Series Creation</a>
        <a href="#pd-read"     class="nav-link">read_csv &amp; I/O functions</a>
        <a href="#pd-inspect"  class="nav-link">Inspection methods</a>
        <a href="#pd-index"    class="nav-link">loc / iloc / query</a>
        <a href="#pd-clean"    class="nav-link">Cleaning &amp; Missing Data</a>
        <a href="#pd-groupby"  class="nav-link">GroupBy &amp; Aggregation</a>
        <a href="#pd-merge"    class="nav-link">Merge / Join / Concat</a>
        <a href="#pd-reshape"  class="nav-link">pivot / melt / stack</a>
        <a href="#pd-window"   class="nav-link">Window Functions</a>
        <a href="#pd-dt"       class="nav-link">Datetime &amp; MultiIndex</a>
        <a href="#pd-str"      class="nav-link">.str accessor</a>
        <a href="#pd-apply"    class="nav-link">apply / map</a>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-header"><span class="nav-label">📊 Matplotlib</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#mpl-setup"   class="nav-link">figure &amp; subplots</a>
        <a href="#mpl-types"   class="nav-link">All Plot Types</a>
        <a href="#mpl-axes"    class="nav-link">Axes Customization</a>
        <a href="#mpl-annot"   class="nav-link">Annotations &amp; Text</a>
        <a href="#mpl-layout"  class="nav-link">Layout, 3D &amp; rcParams</a>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-header"><span class="nav-label">🎨 Seaborn</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#sns-theme"   class="nav-link">Theme &amp; Palettes</a>
        <a href="#sns-dist"    class="nav-link">Distribution Plots</a>
        <a href="#sns-cat"     class="nav-link">Categorical Plots</a>
        <a href="#sns-matrix"  class="nav-link">Heatmap &amp; Clustermap</a>
        <a href="#sns-grid"    class="nav-link">FacetGrid &amp; PairGrid</a>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-header"><span class="nav-label">🤖 Scikit-Learn</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#sk-api"      class="nav-link">Universal API</a>
        <a href="#sk-pre"      class="nav-link">Preprocessing</a>
        <a href="#sk-pipe"     class="nav-link">Pipeline &amp; ColumnTransformer</a>
        <a href="#sk-cv"       class="nav-link">Cross-Validation</a>
        <a href="#sk-models"   class="nav-link">Classification Models</a>
        <a href="#sk-reg"      class="nav-link">Regression Models</a>
        <a href="#sk-cluster"  class="nav-link">Clustering</a>
        <a href="#sk-metrics"  class="nav-link">Evaluation Metrics</a>
      </div>
    </div>

    <div class="nav-section">
      <div class="nav-header"><span class="nav-label">🧠 TensorFlow / Keras</span><span class="arrow">›</span></div>
      <div class="nav-items">
        <a href="#tf-tensors"  class="nav-link">Tensors &amp; Variables</a>
        <a href="#tf-layers"   class="nav-link">Keras Layers</a>
        <a href="#tf-model"    class="nav-link">Model Building APIs</a>
        <a href="#tf-train"    class="nav-link">Training &amp; Callbacks</a>
        <a href="#tf-data"     class="nav-link">tf.data Pipeline</a>
        <a href="#tf-transfer" class="nav-link">Transfer Learning</a>
      </div>
    </div>

  </div>
  <div class="progress-bar">
    <div class="progress-track"><div class="progress-fill" id="main-pg"></div></div>
    <div style="font-size:11px;color:var(--text-muted);text-align:right;margin-top:5px;" id="pg-txt">0% Complete</div>
  </div>
</nav>
"""

HOME = """
<div class="page active" id="page-home">
  <div class="hero">
    <div style="display:inline-block;background:#eff6ff;color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.08em;padding:5px 14px;border-radius:20px;margin-bottom:16px;text-transform:uppercase;">Complete Reference · Version 2</div>
    <h1>Python &amp; Data Science Hub</h1>
    <p>Textbook-quality reference with expandable concept cards, live examples, and comprehensive API coverage — sourced from leading data science books.</p>
    <div class="stats">
      <div class="stat"><h2>150+</h2><small>Topics</small></div>
      <div class="stat"><h2>600+</h2><small>Examples</small></div>
      <div class="stat"><h2>8</h2><small>Modules</small></div>
      <div class="stat"><h2>9</h2><small>Textbooks</small></div>
    </div>
  </div>
  <h2>Explore Modules</h2>
  <div class="cards">
    <a href="#py-strings" class="card"><div class="card-icon">🐍</div><div><h3>Python Basics</h3><p>Variables, all string/list/dict/set methods with expandable cards, OOP, generators, decorators.</p></div></a>
    <a href="#np-create"  class="card"><div class="card-icon">🔢</div><div><h3>NumPy</h3><p>ndarray architecture, indexing, broadcasting, ufuncs, linear algebra.</p></div></a>
    <a href="#pd-create"  class="card"><div class="card-icon">🐼</div><div><h3>Pandas</h3><p>DataFrame/Series, GroupBy, merge, pivot, datetime, .str accessor.</p></div></a>
    <a href="#mpl-setup"  class="card"><div class="card-icon">📊</div><div><h3>Matplotlib</h3><p>All 18 plot types, axes customization, GridSpec, 3D plots.</p></div></a>
    <a href="#sns-theme"  class="card"><div class="card-icon">🎨</div><div><h3>Seaborn</h3><p>Statistical visualization, palettes, FacetGrid, PairGrid.</p></div></a>
    <a href="#sk-api"     class="card"><div class="card-icon">🤖</div><div><h3>Scikit-Learn</h3><p>Pipeline, GridSearchCV, all classifiers, and every metric.</p></div></a>
    <a href="#tf-tensors" class="card"><div class="card-icon">🧠</div><div><h3>TensorFlow/Keras</h3><p>Tensors, GradientTape, Sequential/Functional/Subclass APIs, tf.data.</p></div></a>
    <a href="#std-os"     class="card"><div class="card-icon">📦</div><div><h3>Python Stdlib</h3><p>os, pathlib, json, re, datetime, collections, itertools, typing.</p></div></a>
  </div>
  <div class="note" style="margin-top:28px;">
    <strong>💡 How to use</strong>
    Click any topic in the sidebar → click a method card header to expand it → copy code examples. Your progress saves automatically.
  </div>
</div>
"""

# Helpers
def card(method, sig, ret, explanation, params_rows=None, examples=None, note_text=None, warn_text=None):
    """Create an expandable method card"""
    pid = method.replace('.','').replace('(','').replace(')','').replace(' ','_')
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
            html += f'    <p><strong>{title}</strong></p>\n'
            html += '    <div class="code-box"><div class="code-header"><span class="lang">python</span><button class="copy-btn">Copy</button></div><pre>'
            html += code
            html += '</pre></div>\n'
            if out:
                html += f'    <div class="note" style="margin-top:-8px;padding:8px 12px;"><strong>Output</strong><code style="background:transparent;color:var(--accent-g);font-size:12px;">{out}</code></div>\n'
    html += '  </div>\n</div>\n'
    return html

def section_header(title, badge_module, badge_level, source):
    return f'''<div class="badge-row">
  <span class="badge badge-module">{badge_module}</span>
  <span class="badge badge-{badge_level.lower()}">{badge_level}</span>
  <span class="source-note">📖 {source}</span>
</div>
<h1>{title}</h1>\n'''

def page_nav(prev_href, prev_label, next_href, next_label):
    return f'''<div class="page-nav">
  <a href="{prev_href}" class="nav-btn"><span class="nav-dir">← Previous</span><strong>{prev_label}</strong></a>
  <a href="{next_href}" class="nav-btn right-nav"><span class="nav-dir">Next →</span><strong>{next_label}</strong></a>
</div>\n'''

# Export for use by v2_python.py
import pickle
with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\helpers.pkl","wb") as f:
    pickle.dump({"card":card,"section_header":section_header,"page_nav":page_nav,"CSS":CSS,"JS":JS,"SIDEBAR":SIDEBAR,"HOME":HOME},f)

with open(r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final\v2_parts\core.html","w",encoding="utf-8") as f:
    f.write(CSS+SIDEBAR+HOME+JS)
print(f"core.html  {len(CSS)+len(SIDEBAR)+len(HOME)+len(JS):,} chars")
