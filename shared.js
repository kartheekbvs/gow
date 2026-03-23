/**
 * Python Docs Final — Shared Layout & Interactive System
 * Handles: sidebar, search, code copy, playground, progress bar, dark-mode TOC
 */

// ─── Search Index ───────────────────────────────────────────────────────────
const SEARCH_INDEX = [
  // Python Basics
  { title:'Variables & Data Types', page:'python-basics.html', section:'s1', snippet:'int float str bool None, type() isinstance() id(), type coercion' },
  { title:'String Methods', page:'python-basics.html', section:'s2', snippet:'upper lower strip split join replace find index count startswith f-strings slicing' },
  { title:'List Methods', page:'python-basics.html', section:'s3', snippet:'append extend insert remove pop clear sort reverse copy sorted len min max sum comprehensions' },
  { title:'Dictionary Methods', page:'python-basics.html', section:'s4', snippet:'get setdefault update keys values items pop copy fromkeys comprehensions defaultdict Counter' },
  { title:'Set Methods', page:'python-basics.html', section:'s5', snippet:'add remove discard union intersection difference symmetric_difference issubset frozenset' },
  { title:'Tuple Methods', page:'python-basics.html', section:'s6', snippet:'count index named tuples unpacking tuple vs list' },
  { title:'Control Flow', page:'python-basics.html', section:'s7', snippet:'if elif else ternary for while break continue pass loop else match case' },
  { title:'Functions', page:'python-basics.html', section:'s8', snippet:'def return args kwargs lambda map filter zip enumerate sorted any all sum' },
  { title:'File I/O', page:'python-basics.html', section:'s9', snippet:'open read readline readlines write seek tell with open pathlib' },
  { title:'Exception Handling', page:'python-basics.html', section:'s10', snippet:'try except else finally raise custom exceptions built-in traceback' },
  { title:'Comprehensions & Generators', page:'python-basics.html', section:'s11', snippet:'list dict set comprehensions nested generator expressions memory' },
  { title:'Classes & OOP', page:'python-basics.html', section:'s12', snippet:'class __init__ self classmethod staticmethod property inheritance super dunder methods MRO ABC dataclass' },
  { title:'Modules & Packages', page:'python-basics.html', section:'s13', snippet:'import from import as __init__.py __all__ sys.path __name__' },
  { title:'Iterators & Generators', page:'python-basics.html', section:'s14', snippet:'iter next yield yield from send throw itertools count cycle islice chain product combinations' },
  { title:'Decorators', page:'python-basics.html', section:'s15', snippet:'@decorator functools.wraps decorator with args chaining class-based lru_cache cache' },
  // NumPy
  { title:'NumPy Array Creation', page:'numpy.html', section:'s1', snippet:'np.array zeros ones empty full eye arange linspace logspace random' },
  { title:'NumPy Shape & Indexing', page:'numpy.html', section:'s2', snippet:'reshape flatten ravel squeeze expand_dims transpose concatenate vstack hstack split' },
  { title:'NumPy Math & Ufuncs', page:'numpy.html', section:'s3', snippet:'add subtract multiply divide sqrt exp log sin cos arctan matmul dot linalg' },
  { title:'NumPy Aggregation', page:'numpy.html', section:'s4', snippet:'sum prod mean median std var min max argmin argmax percentile quantile nansum unique sort' },
  { title:'NumPy Boolean & Sets', page:'numpy.html', section:'s5', snippet:'all any isnan isinf isclose allclose in1d intersect1d union1d setdiff1d' },
  { title:'NumPy Advanced', page:'numpy.html', section:'s6', snippet:'broadcasting dtype view copy structured masked arrays save load einsum meshgrid pad vectorize' },
  // Pandas
  { title:'Pandas Creation & Reading', page:'pandas.html', section:'s1', snippet:'DataFrame Series read_csv read_excel read_json read_sql to_csv to_excel' },
  { title:'Pandas Inspection', page:'pandas.html', section:'s2', snippet:'head tail info describe shape dtypes columns index nunique value_counts sample' },
  { title:'Pandas Indexing', page:'pandas.html', section:'s3', snippet:'loc iloc at iat boolean indexing query where mask' },
  { title:'Pandas Cleaning', page:'pandas.html', section:'s4', snippet:'isna notna dropna fillna interpolate duplicated replace astype to_numeric to_datetime' },
  { title:'Pandas GroupBy', page:'pandas.html', section:'s5', snippet:'groupby agg aggregate transform apply filter cumsum ngroups groups' },
  { title:'Pandas Merge & Concat', page:'pandas.html', section:'s6', snippet:'merge join concat inner left right outer how on suffixes validate' },
  { title:'Pandas Reshape', page:'pandas.html', section:'s7', snippet:'pivot pivot_table melt stack unstack explode' },
  { title:'Pandas Window Functions', page:'pandas.html', section:'s8', snippet:'rolling ewm expanding mean sum std var min max' },
  { title:'Pandas Datetime', page:'pandas.html', section:'s9', snippet:'to_datetime dt accessor date_range Timedelta DateOffset year month day freq' },
  // Matplotlib
  { title:'Matplotlib Setup', page:'matplotlib.html', section:'s1', snippet:'figure subplots figsize dpi facecolor add_subplot layout' },
  { title:'Matplotlib Plot Types', page:'matplotlib.html', section:'s2', snippet:'plot scatter bar hist boxplot violinplot pie imshow contour quiver errorbar fill_between step stem stackplot' },
  { title:'Matplotlib Customization', page:'matplotlib.html', section:'s3', snippet:'title xlabel ylabel xlim ylim xticks legend grid spines aspect annotate text axhline colorbar' },
  { title:'Matplotlib Layout & 3D', page:'matplotlib.html', section:'s4', snippet:'tight_layout savefig GridSpec style rcParams 3D Axes3D plot_surface scatter3D' },
  // Seaborn
  { title:'Seaborn Distribution', page:'seaborn.html', section:'s1', snippet:'histplot kdeplot ecdfplot rugplot displot stat bins bw_adjust fill' },
  { title:'Seaborn Categorical', page:'seaborn.html', section:'s2', snippet:'boxplot violinplot boxenplot stripplot swarmplot barplot pointplot countplot catplot' },
  { title:'Seaborn Relational & Matrix', page:'seaborn.html', section:'s3', snippet:'scatterplot lineplot relplot regplot lmplot heatmap clustermap pairplot FacetGrid JointGrid' },
  // Sklearn
  { title:'Sklearn Core API', page:'sklearn.html', section:'s1', snippet:'fit predict score fit_transform get_params set_params clone check_array Universal Pattern' },
  { title:'Sklearn Preprocessing', page:'sklearn.html', section:'s2', snippet:'StandardScaler MinMaxScaler RobustScaler LabelEncoder OneHotEncoder SimpleImputer PolynomialFeatures Pipeline ColumnTransformer' },
  { title:'Sklearn Linear Models', page:'sklearn.html', section:'s3', snippet:'LinearRegression Ridge Lasso ElasticNet LogisticRegression SGDClassifier' },
  { title:'Sklearn Trees & Ensembles', page:'sklearn.html', section:'s4', snippet:'DecisionTreeClassifier RandomForestClassifier GradientBoostingClassifier HistGradientBoosting ExtraTreesClassifier' },
  { title:'Sklearn SVM & Neighbors', page:'sklearn.html', section:'s5', snippet:'SVC SVR LinearSVC KNeighborsClassifier KNeighborsRegressor NearestNeighbors' },
  { title:'Sklearn Clustering', page:'sklearn.html', section:'s6', snippet:'KMeans DBSCAN AgglomerativeClustering silhouette_score calinski_harabasz davies_bouldin' },
  { title:'Sklearn Model Selection & Metrics', page:'sklearn.html', section:'s7', snippet:'train_test_split cross_val_score GridSearchCV RandomizedSearchCV accuracy precision recall f1 confusion_matrix roc_auc' },
  // TensorFlow
  { title:'TensorFlow Tensors & Math', page:'tensorflow.html', section:'s1', snippet:'tf.constant tf.Variable zeros ones random cast reshape matmul reduce_sum nn.softmax' },
  { title:'TensorFlow Keras Layers', page:'tensorflow.html', section:'s2', snippet:'Dense Conv2D MaxPooling2D LSTM GRU Embedding Dropout BatchNormalization MultiHeadAttention Bidirectional' },
  { title:'TensorFlow Model Building', page:'tensorflow.html', section:'s3', snippet:'Sequential Functional API Subclassing Input Model summary compile fit evaluate predict' },
  { title:'TensorFlow Training & Callbacks', page:'tensorflow.html', section:'s4', snippet:'Adam SGD RMSprop losses BinaryCrossentropy ModelCheckpoint EarlyStopping ReduceLROnPlateau TensorBoard' },
  { title:'TensorFlow Transfer & Data', page:'tensorflow.html', section:'s5', snippet:'VGG16 ResNet50 EfficientNet MobileNet tf.data Dataset map batch shuffle prefetch cache' },
  // Stdlib
  { title:'os & pathlib', page:'stdlib.html', section:'s1', snippet:'os.getcwd listdir mkdir walk environ pathlib Path read_text write_text glob rglob' },
  { title:'json & re & datetime', page:'stdlib.html', section:'s2', snippet:'json.dumps loads dump load regex match search findall sub datetime strftime strptime timedelta' },
  { title:'collections & functools & itertools', page:'stdlib.html', section:'s3', snippet:'defaultdict Counter deque namedtuple lru_cache partial reduce wraps count cycle chain product combinations permutations' },
  { title:'typing & dataclasses & threading', page:'stdlib.html', section:'s4', snippet:'Optional Union List Dict Callable TypeVar Protocol dataclass field frozen Thread Lock Event Queue Pool subprocess' },
  { title:'logging & argparse & unittest', page:'stdlib.html', section:'s5', snippet:'basicConfig getLogger DEBUG INFO WARNING ERROR critical FileHandler ArgumentParser add_argument TestCase setUp assertRaises mock' },
];

// ─── Sidebar Navigation Data ─────────────────────────────────────────────────
const NAV_SECTIONS = [
  { label:'🐍 Python Basics', links:[
    { text:'Variables & Data Types', href:'python-basics.html#s1' },
    { text:'String Methods', href:'python-basics.html#s2' },
    { text:'List Methods', href:'python-basics.html#s3' },
    { text:'Dictionary Methods', href:'python-basics.html#s4' },
    { text:'Set & Tuple Methods', href:'python-basics.html#s5' },
    { text:'Control Flow', href:'python-basics.html#s7' },
    { text:'Functions & Lambdas', href:'python-basics.html#s8' },
    { text:'File I/O', href:'python-basics.html#s9' },
    { text:'Exception Handling', href:'python-basics.html#s10' },
    { text:'Comprehensions & Generators', href:'python-basics.html#s11' },
    { text:'Classes & OOP', href:'python-basics.html#s12' },
    { text:'Decorators', href:'python-basics.html#s15' },
  ]},
  { label:'🔢 NumPy — 40 Topics', links:[
    { text:'Array Creation', href:'numpy.html#s1' },
    { text:'Shape & Indexing', href:'numpy.html#s2' },
    { text:'Math & Ufuncs', href:'numpy.html#s3' },
    { text:'Aggregation', href:'numpy.html#s4' },
    { text:'Boolean & Set Ops', href:'numpy.html#s5' },
    { text:'Advanced (Broadcasting, einsum…)', href:'numpy.html#s6' },
  ]},
  { label:'🐼 Pandas — 50 Topics', links:[
    { text:'DataFrame & Series Creation', href:'pandas.html#s1' },
    { text:'Inspection Methods', href:'pandas.html#s2' },
    { text:'Indexing (loc / iloc / query)', href:'pandas.html#s3' },
    { text:'Cleaning & Types', href:'pandas.html#s4' },
    { text:'GroupBy & Aggregation', href:'pandas.html#s5' },
    { text:'Merge, Join & Concat', href:'pandas.html#s6' },
    { text:'Reshape: pivot, melt, stack', href:'pandas.html#s7' },
    { text:'Window Functions', href:'pandas.html#s8' },
    { text:'Datetime & Timedelta', href:'pandas.html#s9' },
    { text:'MultiIndex & Performance', href:'pandas.html#s10' },
  ]},
  { label:'📊 Matplotlib — 35 Topics', links:[
    { text:'Figure & Subplots Setup', href:'matplotlib.html#s1' },
    { text:'All Plot Types (18 kinds)', href:'matplotlib.html#s2' },
    { text:'Axes Customization', href:'matplotlib.html#s3' },
    { text:'Text, Annotations & Colors', href:'matplotlib.html#s4' },
    { text:'Layout, 3D & rcParams', href:'matplotlib.html#s5' },
  ]},
  { label:'🎨 Seaborn — 30 Topics', links:[
    { text:'Theme & Palette Setup', href:'seaborn.html#s1' },
    { text:'Distribution Plots', href:'seaborn.html#s2' },
    { text:'Categorical Plots', href:'seaborn.html#s3' },
    { text:'Relational & Regression', href:'seaborn.html#s4' },
    { text:'Matrix: Heatmap & Clustermap', href:'seaborn.html#s5' },
    { text:'Multi-Plot Grids', href:'seaborn.html#s6' },
  ]},
  { label:'🤖 Scikit-Learn — 45 Topics', links:[
    { text:'Universal API Pattern', href:'sklearn.html#s1' },
    { text:'Preprocessing Pipeline', href:'sklearn.html#s2' },
    { text:'Linear Models', href:'sklearn.html#s3' },
    { text:'Trees & Ensembles', href:'sklearn.html#s4' },
    { text:'SVM & Neighbors', href:'sklearn.html#s5' },
    { text:'Clustering', href:'sklearn.html#s6' },
    { text:'Dimensionality Reduction', href:'sklearn.html#s7' },
    { text:'Model Selection & Metrics', href:'sklearn.html#s8' },
  ]},
  { label:'🧠 TensorFlow — 35 Topics', links:[
    { text:'Tensors, Variables & Math', href:'tensorflow.html#s1' },
    { text:'Keras Layers (13 types)', href:'tensorflow.html#s2' },
    { text:'Model Building APIs', href:'tensorflow.html#s3' },
    { text:'Compile, Fit & Evaluate', href:'tensorflow.html#s4' },
    { text:'Optimizers & Loss Functions', href:'tensorflow.html#s5' },
    { text:'Callbacks & Transfer Learning', href:'tensorflow.html#s6' },
    { text:'tf.data Pipeline', href:'tensorflow.html#s7' },
  ]},
  { label:'📦 Python Stdlib — 25 Topics', links:[
    { text:'os & pathlib', href:'stdlib.html#s1' },
    { text:'json & re', href:'stdlib.html#s2' },
    { text:'datetime & sys', href:'stdlib.html#s3' },
    { text:'collections & functools', href:'stdlib.html#s4' },
    { text:'itertools & string & math', href:'stdlib.html#s5' },
    { text:'random & copy & io', href:'stdlib.html#s6' },
    { text:'typing & dataclasses', href:'stdlib.html#s7' },
    { text:'threading & multiprocessing', href:'stdlib.html#s8' },
    { text:'subprocess & hashlib', href:'stdlib.html#s9' },
    { text:'logging & argparse & unittest', href:'stdlib.html#s10' },
  ]},
];

// ─── Inject Layout ────────────────────────────────────────────────────────────
function injectLayout() {
  const body = document.body;

  // Header
  const header = document.createElement('header');
  header.id = 'top-header';
  header.innerHTML = `
    <a href="index.html" id="logo">PyDocs</a>
    <div id="search-bar" style="position:relative;">
      <input type="text" id="search-input" placeholder="Search all topics… (Ctrl+K)" autocomplete="off">
      <div id="search-results"></div>
    </div>
    <div id="header-actions">
      <button class="header-btn" id="progress-label" title="Reading progress">📖 0%</button>
      <a href="index.html" class="header-btn">🏠 Home</a>
    </div>
  `;

  // Progress bar
  const progressBar = document.createElement('div');
  progressBar.id = 'progress-bar';

  // Sidebar toggle (mobile)
  const sidebarToggle = document.createElement('button');
  sidebarToggle.id = 'sidebar-toggle';
  sidebarToggle.title = 'Toggle sidebar';
  sidebarToggle.textContent = '☰';

  // Sidebar
  const sidebar = document.createElement('aside');
  sidebar.id = 'sidebar';
  let sidebarHTML = '<div style="padding:1rem 1.25rem 0.5rem;">' +
    '<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-muted);font-weight:700;margin-bottom:0.5rem;">Contents</div></div>';

  NAV_SECTIONS.forEach((sect, si) => {
    sidebarHTML += `<div class="sidebar-section">
      <div class="sidebar-group-label" data-idx="${si}">
        <span>${sect.label}</span>
        <i class="chevron">›</i>
      </div>
      <div class="sidebar-links" id="sg-${si}">
        ${sect.links.map(l => `<a class="sidebar-link" href="${l.href}">${l.text}</a>`).join('')}
      </div>
    </div>`;
  });
  sidebar.innerHTML = sidebarHTML;

  // Wrap existing body content
  const existingContent = body.innerHTML;
  body.innerHTML = '';
  body.appendChild(header);
  body.appendChild(progressBar);
  body.appendChild(sidebarToggle);

  const layout = document.createElement('div');
  layout.id = 'layout';

  layout.appendChild(sidebar);
  const main = document.createElement('main');
  main.id = 'main-content';
  main.innerHTML = existingContent;
  layout.appendChild(main);
  body.appendChild(layout);
}

// ─── Sidebar Collapse ─────────────────────────────────────────────────────────
function initSidebarCollapse() {
  document.querySelectorAll('.sidebar-group-label').forEach(label => {
    const idx = label.dataset.idx;
    const links = document.getElementById(`sg-${idx}`);
    label.addEventListener('click', () => {
      label.classList.toggle('collapsed');
      links.classList.toggle('collapsed');
    });
  });

  // Mobile toggle
  const toggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  toggle.addEventListener('click', () => sidebar.classList.toggle('open'));
}

// ─── Active Link ──────────────────────────────────────────────────────────────
function highlightActiveLink() {
  const path = window.location.pathname.split('/').pop() || 'index.html';
  const hash = window.location.hash;
  document.querySelectorAll('.sidebar-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === path + hash || href === path || href.startsWith(path + '#') && !hash) {
      link.classList.add('active');
      // Expand parent group
      const sg = link.closest('.sidebar-links');
      if (sg) sg.classList.remove('collapsed');
      const label = sg?.previousElementSibling;
      if (label) label.classList.remove('collapsed');
    }
  });
}

// ─── Reading Progress ─────────────────────────────────────────────────────────
function initReadingProgress() {
  const bar = document.getElementById('progress-bar');
  const label = document.getElementById('progress-label');
  document.addEventListener('scroll', () => {
    const total = document.documentElement.scrollHeight - window.innerHeight;
    const pct = total > 0 ? Math.round((window.scrollY / total) * 100) : 0;
    if (bar) bar.style.width = pct + '%';
    if (label) label.textContent = `📖 ${pct}%`;
  });
}

// ─── Copy Code ────────────────────────────────────────────────────────────────
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const codeEl = btn.closest('.code-block').querySelector('.code-body code, .code-body pre');
      const text = codeEl ? codeEl.innerText : '';
      navigator.clipboard.writeText(text).then(() => {
        btn.textContent = '✓ Copied';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
      }).catch(() => {
        // Fallback
        const ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta); ta.select(); document.execCommand('copy');
        document.body.removeChild(ta);
        btn.textContent = '✓ Copied'; btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
      });
    });
  });
}

// ─── Interactive Python Playground (Skulpt) ───────────────────────────────────
function initPlayground() {
  // Load Skulpt for in-browser Python execution
  const skulptCore = document.createElement('script');
  skulptCore.src = 'https://skulpt.org/js/skulpt.min.js';
  skulptCore.onload = () => {
    const skulptStdlib = document.createElement('script');
    skulptStdlib.src = 'https://skulpt.org/js/skulpt-stdlib.js';
    skulptStdlib.onload = attachRepl;
    document.head.appendChild(skulptStdlib);
  };
  document.head.appendChild(skulptCore);
}

function attachRepl() {
  document.querySelectorAll('.playground').forEach(pg => {
    const editor = pg.querySelector('.playground-editor');
    const output = pg.querySelector('.playground-output');
    const btn = pg.querySelector('.run-btn');
    if (!btn || !editor || !output) return;

    btn.addEventListener('click', () => {
      output.textContent = '';
      output.className = 'playground-output';
      const code = editor.value;

      function outf(text) { output.textContent += text; }
      function builtinRead(x) {
        if (Sk.builtinFiles === undefined || Sk.builtinFiles.files[x] === undefined)
          throw "File not found: '" + x + "'";
        return Sk.builtinFiles.files[x];
      }
      Sk.configure({ output: outf, read: builtinRead, __future__: Sk.python3 });
      try {
        Sk.misceval.asyncToPromise(() => Sk.importMainWithBody('<stdin>', false, code, true))
          .catch(err => { output.textContent = err.toString(); output.classList.add('error'); });
      } catch(e) { output.textContent = e.toString(); output.classList.add('error'); }
    });

    // Ctrl+Enter to run
    editor.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); btn.click(); }
    });
    // Tab indentation
    editor.addEventListener('keydown', e => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const s = editor.selectionStart, en = editor.selectionEnd;
        editor.value = editor.value.substring(0, s) + '    ' + editor.value.substring(en);
        editor.selectionStart = editor.selectionEnd = s + 4;
      }
    });
  });
}

// ─── Search ───────────────────────────────────────────────────────────────────
function initSearch() {
  const input = document.getElementById('search-input');
  const resultsEl = document.getElementById('search-results');
  if (!input || !resultsEl) return;

  function doSearch(query) {
    if (!query || query.length < 2) { resultsEl.classList.remove('visible'); return; }
    const q = query.toLowerCase();
    const matches = SEARCH_INDEX.filter(item =>
      item.title.toLowerCase().includes(q) ||
      item.snippet.toLowerCase().includes(q)
    ).slice(0, 10);

    if (matches.length === 0) {
      resultsEl.innerHTML = '<div style="padding:1rem;color:var(--text-muted);font-size:0.88rem;">No results found</div>';
    } else {
      resultsEl.innerHTML = matches.map(m => `
        <a class="sr-item" href="${m.page}#${m.section}">
          <span class="sr-item-title">${highlight(m.title, q)}</span>
          <span class="sr-item-page">${m.page.replace('.html','').replace('-',' → ').toUpperCase()}</span>
          <span class="sr-item-snippet">${highlight(m.snippet.substring(0, 80), q)}…</span>
        </a>
      `).join('');
    }
    resultsEl.classList.add('visible');
  }

  function highlight(text, q) {
    return text.replace(new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})`, 'gi'),
      '<mark class="search-highlight">$1</mark>');
  }

  input.addEventListener('input', () => doSearch(input.value.trim()));
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); input.focus(); input.select(); }
    if (e.key === 'Escape') { resultsEl.classList.remove('visible'); input.blur(); }
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('#search-bar')) resultsEl.classList.remove('visible');
  });
}

// ─── Smooth TOC scroll ────────────────────────────────────────────────────────
function initTOCLinks() {
  document.querySelectorAll('.toc-link').forEach(link => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');
      if (href.startsWith('#')) {
        e.preventDefault();
        document.querySelector(href)?.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

// ─── Intersection Observer for sidebar active ─────────────────────────────────
function initScrollSpy() {
  const sections = document.querySelectorAll('.content-section[id]');
  const obs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        document.querySelectorAll('.sidebar-link').forEach(l => {
          if (l.getAttribute('href').includes(id)) l.classList.add('active');
          else l.classList.remove('active');
        });
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  sections.forEach(s => obs.observe(s));
}

// ─── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  injectLayout();
  initSidebarCollapse();
  highlightActiveLink();
  initReadingProgress();
  initCopyButtons();
  initPlayground();
  initSearch();
  initTOCLinks();
  initScrollSpy();
});
