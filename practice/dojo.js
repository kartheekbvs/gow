/* ============================================================================
   PyDocs Dojo — the practice notebook editor.
   ----------------------------------------------------------------------------
   Renders the tracks in practice/data/*.js (window.PRACTICE_TRACKS) as
   interactive notebooks: concept cells with runnable demos, and exercises
   graded by the shared harness (window.HARNESS_PY) executing in a Pyodide
   web worker (practice/dojo_worker.js).

   Views (hash-routed):
     #/                      home      — track catalog + global progress
     #t=<trackId>            track     — notebook list for one track
     #t=<trackId>&n=<nbId>   notebook  — the cells, top to bottom

   Progress, drafts and hint state live in localStorage under "dojo.v1".
   XP per difficulty matches scripts/verify_practice.py: 10 / 20 / 35.
   ========================================================================== */
'use strict';

(function () {

  // ── Constants ──────────────────────────────────────────────────────────────

  const DIFF_XP = { easy: 10, medium: 20, hard: 35 };
  const DIFF_LABEL = { easy: 'Easy', medium: 'Medium', hard: 'Hard' };
  const LEVEL_CLASS = { beginner: 'lv-beginner', intermediate: 'lv-intermediate', advanced: 'lv-advanced' };
  const ACCENT_VAR = {
    blue: 'var(--accent-blue)', orange: 'var(--accent-orange)', yellow: 'var(--accent-yellow)',
    green: 'var(--accent-green)', purple: 'var(--accent-purple)', red: 'var(--accent-red)', cyan: 'var(--accent-cyan)'
  };
  const STORE_KEY = 'dojo.v1';

  // ── Tiny DOM helpers ───────────────────────────────────────────────────────

  const $ = (sel, root) => (root || document).querySelector(sel);
  const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function el(tag, attrs, html) {
    const node = document.createElement(tag);
    if (attrs) for (const k in attrs) node.setAttribute(k, attrs[k]);
    if (html != null) node.innerHTML = html;
    return node;
  }

  function debounce(fn, ms) {
    let t = null;
    return function () {
      const args = arguments, self = this;
      clearTimeout(t);
      t = setTimeout(() => fn.apply(self, args), ms);
    };
  }

  // ── Persistent store ───────────────────────────────────────────────────────
  // solved:    { exId: { xp, firstTry, at } }
  // quizzes:   { quizId: { choice, correct, firstTry } }
  // drafts:    { exId: code }
  // hints:     { exId: revealedCount }
  // solutions: { exId: true }   (editorial was opened — honesty system)

  const Store = {
    data: { solved: {}, quizzes: {}, drafts: {}, hints: {}, solutions: {} },

    load() {
      try {
        const raw = localStorage.getItem(STORE_KEY);
        if (raw) {
          const parsed = JSON.parse(raw);
          for (const k of ['solved', 'quizzes', 'drafts', 'hints', 'solutions']) {
            if (parsed[k] && typeof parsed[k] === 'object') this.data[k] = parsed[k];
          }
        }
      } catch (e) { /* corrupted storage — start fresh, never crash the page */ }
    },

    save: debounce(function () {
      try { localStorage.setItem(STORE_KEY, JSON.stringify(Store.data)); }
      catch (e) { /* quota exceeded — drop drafts, keep progress */ 
        try {
          localStorage.setItem(STORE_KEY, JSON.stringify({
            solved: Store.data.solved, quizzes: Store.data.quizzes,
            hints: Store.data.hints, solutions: Store.data.solutions, drafts: {}
          }));
        } catch (e2) { /* give up silently */ }
      }
    }, 250),

    reset() {
      this.data = { solved: {}, quizzes: {}, drafts: {}, hints: {}, solutions: {} };
      try { localStorage.removeItem(STORE_KEY); } catch (e) { /* noop */ }
    },

    // ── exercises
    isSolved(exId) { return !!this.data.solved[exId]; },
    solve(exId, xp, firstTry) {
      if (this.isSolved(exId)) return false;
      this.data.solved[exId] = { xp: xp, firstTry: !!firstTry, at: Date.now() };
      this.save();
      return true;
    },
    totalXP() {
      let xp = 0;
      for (const k in this.data.solved) xp += this.data.solved[k].xp || 0;
      for (const k in this.data.quizzes) if (this.data.quizzes[k].correct) xp += this.data.quizzes[k].xp || 5;
      return xp;
    },

    // ── drafts
    draft(exId) { return this.data.drafts[exId]; },
    setDraft(exId, code) { this.data.drafts[exId] = code; this.save(); },
    clearDraft(exId) { delete this.data.drafts[exId]; this.save(); },

    // ── hints & solutions
    hintsShown(exId) { return this.data.hints[exId] || 0; },
    showHint(exId) {
      this.data.hints[exId] = this.hintsShown(exId) + 1;
      this.save();
    },
    solutionShown(exId) { return !!this.data.solutions[exId]; },
    markSolution(exId) { this.data.solutions[exId] = true; this.save(); },

    // ── predict-mode quizzes
    quizState(quizId) { return this.data.quizzes[quizId] || null; },
    answerQuiz(quizId, choice, nOptions) {
      const prev = this.data.quizzes[quizId];
      if (prev && prev.correct) return prev;          // already banked
      const firstTry = !prev;                          // no prior attempt at all
      const record = { choice: choice, correct: false, firstTry: firstTry };
      this.data.quizzes[quizId] = record;
      this.save();
      return record;
    },
    bankQuiz(quizId, xp) {
      const rec = this.data.quizzes[quizId];
      if (rec && !rec.correct) {
        rec.correct = true;
        rec.xp = xp || 5;
        rec.at = Date.now();
        this.save();
      }
      return rec;
    }
  };

  // ── Track model: merge data files that share a track id (py-core ships in
  //    two parts) and index everything for O(1) lookups. ────────────────────

  const Model = {
    tracks: [],           // merged + ordered
    byId: {},             // trackId -> track
    notebooks: {},        // nbId -> { nb, track }
    exercises: {},        // exId  -> { ex, nb, track }

    build() {
      const raw = (window.PRACTICE_TRACKS || []).slice();
      const merged = {};
      const order = [];
      for (const t of raw) {
        if (!t || !t.id || !Array.isArray(t.notebooks)) continue;
        if (!merged[t.id]) { merged[t.id] = Object.assign({}, t, { notebooks: [] }); order.push(t.id); }
        merged[t.id].notebooks = merged[t.id].notebooks.concat(t.notebooks);
      }
      for (const id of order) {
        const track = merged[id];
        // de-duplicate notebooks by id (defensive), order by "order"
        const seen = new Set();
        track.notebooks = track.notebooks
          .filter(nb => { if (!nb || !nb.id || seen.has(nb.id)) return false; seen.add(nb.id); return true; })
          .sort((a, b) => (a.order || 9999) - (b.order || 9999));
        for (const nb of track.notebooks) {
          this.notebooks[nb.id] = { nb: nb, track: track };
          for (const cell of nb.cells || []) {
            if (cell && cell.type === 'exercise' && cell.exercise && cell.exercise.id) {
              this.exercises[cell.exercise.id] = { ex: cell.exercise, nb: nb, track: track };
            }
          }
        }
        this.byId[id] = track;
        this.tracks.push(track);
      }
      // A stable, sensible display order: follow the curriculum story.
      const TRACK_ORDER = ['py-core', 'stdlib-power', 'numpy-reasoning', 'pandas-reasoning',
        'ml-viz-reasoning', 'leet-intuition'];
      this.tracks.sort((a, b) => {
        const ia = TRACK_ORDER.indexOf(a.id), ib = TRACK_ORDER.indexOf(b.id);
        return (ia < 0 ? 999 : ia) - (ib < 0 ? 999 : ib);
      });
    },

    trackStats(track) {
      let ex = 0, solved = 0;
      for (const nb of track.notebooks) {
        for (const cell of nb.cells || []) {
          if (cell.type === 'exercise' && cell.exercise) {
            ex++;
            const id = cell.exercise.id;
            if (cell.exercise.mode === 'predict'
              ? (Store.quizState(id) || {}).correct
              : Store.isSolved(id)) solved++;
          }
        }
      }
      const xpAvailable = this.xpAvailable(track);
      return { exercises: ex, solved: solved, notebooks: track.notebooks.length, xp: xpAvailable };
    },

    xpAvailable(track) {
      let xp = 0;
      for (const nb of track.notebooks) {
        for (const cell of nb.cells || []) {
          if (cell.type === 'exercise' && cell.exercise) {
            // Same table the verifier uses — predict exercises pay by difficulty too.
            xp += DIFF_XP[cell.exercise.difficulty] || 5;
          }
        }
      }
      return xp;
    },

    notebookStats(nb) {
      let ex = 0, solved = 0;
      for (const cell of nb.cells || []) {
        if (cell.type === 'exercise' && cell.exercise) {
          ex++;
          const id = cell.exercise.id;
          if (cell.exercise.mode === 'predict'
            ? (Store.quizState(id) || {}).correct
            : Store.isSolved(id)) solved++;
        }
      }
      return { exercises: ex, solved: solved };
    }
  };

  // ── Runner: the bridge to the Pyodide worker ───────────────────────────────

  const Runner = {
    worker: null,
    seq: 0,
    pending: new Map(),   // id -> { resolve, reject }
    status: 'idle',       // idle | booting | ready | error
    statusEl: null,
    onStatus: null,

    boot() {
      if (this.worker) return;
      try {
        this.worker = new Worker('practice/dojo_worker.js');
      } catch (e) {
        this._setStatus('error', 'worker blocked');
        return;
      }
      this.worker.onerror = () => this._setStatus('error', 'worker crashed');
      this.worker.onmessage = (ev) => {
        const msg = ev.data || {};
        const slot = this.pending.get(msg.id);
        if (slot) {
          this.pending.delete(msg.id);
          if (msg.kind === 'error') slot.reject(new Error(msg.error));
          else slot.resolve(msg.result);
        } else if (msg.kind === 'ready') {
          this._setStatus('ready');
        }
      };
    },

    _setStatus(status, detail) {
      this.status = status;
      if (this.onStatus) this.onStatus(status, detail);
    },

    _post(payload) {
      this.boot();
      if (!this.worker) return Promise.reject(new Error('Worker unavailable (blocked by browser or CSP).'));
      const id = 'r' + (++this.seq);
      return new Promise((resolve, reject) => {
        this.pending.set(id, { resolve: resolve, reject: reject });
        this.worker.postMessage(Object.assign({ id: id }, payload));
      });
    },

    ensureEngine() {
      // Boot Pyodide on first contact so the status pill can react.
      if (this.status === 'idle') {
        this._setStatus('booting');
        this._post({ kind: 'boot', harness: window.HARNESS_PY || '' }).then(
          () => this._setStatus('ready'),
          (err) => this._setStatus('error', err.message)
        );
      }
      return this.status !== 'error';
    },

    runCode(code, packages) {
      return this._post({ kind: 'code', code: code, packages: packages || [] })
        .then(r => JSON.parse(r));
    },

    runTests(code, func, tests, packages) {
      return this._post({ kind: 'tests', code: code, func: func, tests: JSON.stringify(tests), packages: packages || [] })
        .then(r => JSON.parse(r));
    }
  };

  // ── Router ─────────────────────────────────────────────────────────────────

  function parseHash() {
    const h = decodeURIComponent(window.location.hash || '');
    if (h.startsWith('#t=')) {
      const params = {};
      // strip only "#", then parse "t=…&n=…" pairs
      h.slice(1).split('&').forEach(pair => {
        const i = pair.indexOf('=');
        if (i > 0) params[pair.slice(0, i)] = pair.slice(i + 1);
      });
      return { view: params.n ? 'notebook' : 'track', trackId: params.t, nbId: params.n || null };
    }
    if (h.startsWith('#dojo-')) return { view: 'track', trackId: h.slice(6), nbId: null };
    return { view: 'home', trackId: null, nbId: null };
  }

  function go(hash) { window.location.hash = hash; }

  // ── Shared chrome ──────────────────────────────────────────────────────────

  function enginePill() {
    const map = {
      idle:    { cls: 'eng-idle',    ico: '⏻', txt: 'Python off' },
      booting: { cls: 'eng-booting', ico: '⏳', txt: 'Booting Python…' },
      ready:   { cls: 'eng-ready',   ico: '🐍', txt: 'Python ready' },
      error:   { cls: 'eng-error',   ico: '⚠️', txt: 'Python failed' }
    };
    const s = map[Runner.status] || map.idle;
    return '<span class="engine-pill ' + s.cls + '" id="engine-pill" title="The Dojo runs your code in a real Python (Pyodide) inside this tab. It boots on your first Run.">' +
      s.ico + ' <span class="eng-txt">' + s.txt + '</span></span>';
  }

  function renderChrome(root) {
    const bar = el('div', { class: 'dojo-bar' },
      '<div class="dojo-bar-left"><a class="dojo-crumb" href="#/">🥋 Dojo</a>' +
      '<span class="dojo-crumb-sep">/</span><span class="dojo-crumb-here" id="dojo-here">Home</span></div>' +
      '<div class="dojo-bar-right">' + enginePill() +
      '<span class="dojo-xp" id="dojo-xp" title="Experience points — earn them by passing all tests.">' +
      '⚡ <b id="dojo-xp-num">' + Store.totalXP() + '</b> XP</span></div>');
    root.appendChild(bar);
    Runner.onStatus = () => {
      const pill = $('#engine-pill');
      if (pill) pill.outerHTML = enginePill();
    };
  }

  function setCrumb(text) {
    const here = $('#dojo-here');
    if (here) here.textContent = text;
  }

  // ── Home view ──────────────────────────────────────────────────────────────

  function renderHome(root) {
    setCrumb('Home');
    let totalEx = 0, totalSolved = 0, totalXP = 0;
    Model.tracks.forEach(t => {
      const s = Model.trackStats(t);
      totalEx += s.exercises; totalSolved += s.solved; totalXP += s.xp;
    });
    const pct = totalEx ? Math.round(100 * totalSolved / totalEx) : 0;

    const hero = el('section', { class: 'page-hero dojo-hero' },
      '<div class="breadcrumb">🥋 PyDocs Dojo</div>' +
      '<h1>Practice like it&#39;s <span class="dojo-grad">real code review</span></h1>' +
      '<p class="subtitle">A reasoning-first gym for the whole PyDocs curriculum: every concept gets a crisp explanation, a demo you can run, and HackerRank-grade exercises with visible and hidden tests — including efficiency budgets that count how many elements your algorithm touches. No pattern memorization: each problem is a new story you solve with the concept itself.</p>' +
      '<div class="dojo-hero-stats">' +
        '<div class="dhs"><b>' + Model.tracks.length + '</b><span>tracks</span></div>' +
        '<div class="dhs"><b>' + Model.notebooksCount() + '</b><span>notebooks</span></div>' +
        '<div class="dhs"><b>' + totalEx + '</b><span>exercises</span></div>' +
        '<div class="dhs"><b>' + totalXP + '</b><span>XP on offer</span></div>' +
      '</div>' +
      '<div class="dojo-progress-wrap"><div class="dojo-progress"><div class="dojo-progress-fill" style="width:' + pct + '%"></div></div>' +
      '<div class="dojo-progress-label">' + totalSolved + ' / ' + totalEx + ' exercises solved · ' + pct + '%</div></div>' +
      '<div class="dojo-hero-actions"><button class="dojo-btn dojo-btn-ghost" id="dojo-reset">Reset my progress</button></div>');

    const grid = el('div', { class: 'home-grid dojo-grid' });
    Model.tracks.forEach(track => {
      const s = Model.trackStats(track);
      const tp = s.exercises ? Math.round(100 * s.solved / s.exercises) : 0;
      const accent = ACCENT_VAR[track.accent] || ACCENT_VAR.blue;
      const card = el('a', {
        class: 'home-card dojo-track-card', href: '#t=' + track.id,
        style: '--card-accent:' + accent + ';'
      },
        '<div class="card-icon">' + (track.icon || '🥋') + '</div>' +
        '<div class="card-title">' + esc(track.title) + '</div>' +
        '<div class="card-desc">' + esc(track.tagline || '') + '</div>' +
        '<div class="dojo-track-progress"><div class="dojo-progress slim"><div class="dojo-progress-fill" style="width:' + tp + '%;background:' + accent + '"></div></div>' +
        '<span class="dojo-track-pcount">' + s.solved + '/' + s.exercises + '</span></div>' +
        '<div class="card-meta"><span class="tag tag-blue">' + s.notebooks + ' notebooks</span>' +
        '<span class="tag tag-green">' + s.exercises + ' exercises</span>' +
        '<span class="tag tag-yellow">⚡' + s.xp + ' XP</span></div>');
      grid.appendChild(card);
    });

    const how = el('div', { class: 'callout tip dojo-how' },
      '<div class="callout-icon">🧠</div><div class="callout-body">' +
      '<strong>How the Dojo teaches</strong>' +
      '<p>Each notebook pairs <b>concept cells</b> (the mental model + a runnable demo) with <b>exercises</b>: first <i>predict-the-output</i> checks, then full coding problems graded by visible examples and hidden tests. Stuck? Reveal hints one at a time — each hint is a question-shaped nudge, and the last one is the answer. Solutions always come with the <i>reasoning</i> that generalizes, not just the code.</p></div>');

    root.appendChild(hero);
    root.appendChild(el('h2', { class: 'dojo-h2' }, 'Choose your track'));
    root.appendChild(grid);
    root.appendChild(how);

    $('#dojo-reset').addEventListener('click', () => {
      if (confirm('This wipes solved exercises, XP, drafts and hints from this browser. There is no undo. Continue?')) {
        Store.reset();
        route();
      }
    });
  }

  // ── Track view ─────────────────────────────────────────────────────────────

  function renderTrack(root, track) {
    if (!track) { renderHome(root); return; }
    setCrumb(track.title);
    const accent = ACCENT_VAR[track.accent] || ACCENT_VAR.blue;
    const s = Model.trackStats(track);

    const head = el('section', { class: 'page-hero dojo-hero dojo-hero-track', style: 'border-left:4px solid ' + accent + ';' },
      '<div class="breadcrumb"><a href="#/">🥋 Dojo</a> / ' + esc(track.title) + '</div>' +
      '<h1>' + (track.icon || '') + ' ' + esc(track.title) + '</h1>' +
      '<p class="subtitle">' + esc(track.tagline || '') + '</p>' +
      '<div class="dojo-progress-wrap"><div class="dojo-progress"><div class="dojo-progress-fill" style="width:' +
      (s.exercises ? Math.round(100 * s.solved / s.exercises) : 0) + '%;background:' + accent + '"></div></div>' +
      '<div class="dojo-progress-label">' + s.solved + ' / ' + s.exercises + ' solved</div></div>');

    const grid = el('div', { class: 'dojo-nb-grid' });
    track.notebooks.forEach((nb, i) => {
      const ns = Model.notebookStats(nb);
      const done = ns.exercises && ns.solved === ns.exercises;
      const card = el('a', {
        class: 'dojo-nb-card' + (done ? ' done' : ''), href: '#t=' + track.id + '&n=' + nb.id
      },
        '<div class="dojo-nb-num" style="background:' + accent + '">' + (i + 1) + '</div>' +
        '<div class="dojo-nb-main"><div class="dojo-nb-title">' + (nb.icon ? nb.icon + ' ' : '') + esc(nb.title) +
        (done ? ' <span class="dojo-done-badge">✓ done</span>' : '') + '</div>' +
        '<div class="dojo-nb-blurb">' + esc(nb.blurb || '') + '</div>' +
        '<div class="dojo-nb-meta"><span class="dojo-lv ' + (LEVEL_CLASS[nb.level] || '') + '">' + esc(nb.level || '') + '</span>' +
        '<span class="dojo-lv-ex">' + ns.solved + '/' + ns.exercises + ' exercises</span></div></div>' +
        '<div class="dojo-nb-go">→</div>');
      grid.appendChild(card);
    });

    root.appendChild(head);
    root.appendChild(el('h2', { class: 'dojo-h2' }, 'Notebooks in this track'));
    root.appendChild(grid);
  }

  // ── Notebook view ──────────────────────────────────────────────────────────

  function renderNotebook(root, track, nb) {
    if (!nb) {
      const entry = Model.byId[track ? track.id : ''];
      if (entry) { renderTrack(root, entry); return; }
      renderHome(root); return;
    }
    setCrumb(nb.title);
    const accent = ACCENT_VAR[track.accent] || ACCENT_VAR.blue;
    const idx = track.notebooks.indexOf(nb);
    const prev = track.notebooks[idx - 1], next = track.notebooks[idx + 1];
    const stats = Model.notebookStats(nb);

    const head = el('section', { class: 'dojo-nb-head', style: '--nb-accent:' + accent + ';' },
      '<div class="breadcrumb"><a href="#/">🥋 Dojo</a> / <a href="#t=' + track.id + '">' + esc(track.title) + '</a> / Notebook ' + (idx + 1) + ' of ' + track.notebooks.length + '</div>' +
      '<h1>' + (nb.icon ? nb.icon + ' ' : '') + esc(nb.title) + '</h1>' +
      '<p class="subtitle">' + esc(nb.blurb || '') + '</p>' +
      '<div class="dojo-nb-head-meta">' +
      '<span class="dojo-lv ' + (LEVEL_CLASS[nb.level] || '') + '">' + esc(nb.level || '') + '</span>' +
      '<span class="dojo-lv-ex" id="nb-solved-count">' + stats.solved + '/' + stats.exercises + ' exercises solved</span>' +
      (nb.conceptRef ? '<a class="dojo-ref-link" href="' + esc(nb.conceptRef) + '">📖 Full reference chapter</a>' : '') +
      '</div>');

    const cells = el('div', { class: 'dojo-cells' });
    let conceptNo = 0, exNo = 0;
    (nb.cells || []).forEach(cell => {
      if (cell.type === 'concept') {
        conceptNo++;
        cells.appendChild(conceptCell(cell, conceptNo, track, nb));
      } else if (cell.type === 'exercise' && cell.exercise) {
        exNo++;
        cells.appendChild(exerciseCell(cell.exercise, exNo, track, nb));
      }
    });

    const nav = el('div', { class: 'dojo-nb-nav' },
      (prev ? '<a class="dojo-btn dojo-btn-ghost" href="#t=' + track.id + '&n=' + prev.id + '">← ' + esc(prev.title) + '</a>' : '<span></span>') +
      (next ? '<a class="dojo-btn dojo-btn-primary" style="background:' + accent + '" href="#t=' + track.id + '&n=' + next.id + '">' + esc(next.title) + ' →</a>'
            : '<a class="dojo-btn dojo-btn-primary" style="background:' + accent + '" href="#t=' + track.id + '">Finish track ✓</a>'));

    root.appendChild(head);
    root.appendChild(cells);
    root.appendChild(nav);
  }

  // ── Concept cell ───────────────────────────────────────────────────────────

  function conceptCell(cell, no, track, nb) {
    const wrap = el('div', { class: 'dojo-cell dojo-concept' });
    wrap.innerHTML =
      '<div class="dojo-cell-head"><span class="dojo-cell-kind concept">CONCEPT ' + no + '</span>' +
      '<span class="dojo-cell-title">' + esc(cell.title || '') + '</span></div>' +
      '<div class="dojo-concept-body">' + (cell.body || '') + '</div>';

    if (cell.demo && cell.demo.code) {
      const demo = el('div', { class: 'dojo-demo' });
      demo.innerHTML =
        '<div class="dojo-demo-bar"><span class="dojo-demo-lang">python · demo</span>' +
        '<button class="dojo-run-btn" type="button">▶ Run</button></div>' +
        '<pre class="dojo-demo-code"><code>' + esc(cell.demo.code) + '</code></pre>' +
        '<div class="dojo-demo-out" hidden></div>';
      wrap.appendChild(demo);

      const out = $('.dojo-demo-out', demo);
      const btn = $('.dojo-run-btn', demo);
      btn.addEventListener('click', () => {
        btn.disabled = true;
        btn.textContent = '⏳ running…';
        out.hidden = false;
        out.className = 'dojo-demo-out running';
        out.textContent = 'Booting a real Python (Pyodide) in this tab — the first run takes a few seconds…';
        Runner.ensureEngine();
        Runner.runCode(cell.demo.code, track.packages).then(res => {
          btn.disabled = false;
          btn.textContent = '▶ Run';
          const text = (res.ok
            ? (res.stdout && res.stdout.length ? res.stdout.trimEnd() : '(no output — the demo defines or mutates silently)')
            : (res.stdout ? res.stdout.trimEnd() + '\n' : '') + String(res.error || 'error'));
          out.className = 'dojo-demo-out ' + (res.ok ? 'ok' : 'err');
          out.textContent = text;
        }).catch(err => {
          btn.disabled = false;
          btn.textContent = '▶ Run';
          out.className = 'dojo-demo-out err';
          out.textContent = 'Could not start Python: ' + err.message;
        });
      });
    }
    return wrap;
  }

  // ── Exercise cell ──────────────────────────────────────────────────────────

  function exerciseCell(ex, no, track, nb) {
    if (ex.mode === 'predict') return predictCell(ex, no, track, nb);
    return codeCell(ex, no, track, nb);
  }

  // ── Predict-mode exercise ──────────────────────────────────────────────────

  function predictCell(ex, no, track, nb) {
    const wrap = el('div', { class: 'dojo-cell dojo-exercise', id: 'ex-' + ex.id });
    const xp = DIFF_XP[ex.difficulty] || 5;
    const state = Store.quizState(ex.id);
    const solved = !!(state && state.correct);

    wrap.innerHTML =
      '<div class="dojo-cell-head"><span class="dojo-cell-kind exercise">EXERCISE ' + no + '</span>' +
      '<span class="dojo-cell-kind predict">PREDICT</span>' +
      '<span class="dojo-cell-title">' + esc(ex.title || '') + '</span>' +
      '<span class="dojo-diff d-' + ex.difficulty + '">' + (DIFF_LABEL[ex.difficulty] || ex.difficulty) + '</span>' +
      '<span class="dojo-xp-chip' + (solved ? ' earned' : '') + '" title="' + xp + ' XP for a first-try prediction">' + (solved ? '✓ ' : '') + xp + ' XP</span></div>' +
      '<div class="dojo-ex-body">' + (ex.statement || '') + '</div>' +
      '<pre class="dojo-predict-code"><code>' + esc(ex.code || '') + '</code></pre>' +
      '<div class="dojo-options" role="group" aria-label="Answer options"></div>' +
      '<div class="dojo-predict-feedback" hidden></div>';

    const optionsEl = $('.dojo-options', wrap);
    const feedback = $('.dojo-predict-feedback', wrap);
    const answer = ex.answer | 0;

    function paint(selectedIdx, locked) {
      optionsEl.innerHTML = '';
      (ex.options || []).forEach((opt, i) => {
        const cls = ['dojo-option'];
        if (locked) {
          if (i === answer) cls.push('correct');
          else if (i === selectedIdx) cls.push('wrong');
        } else if (i === selectedIdx) cls.push('picked');
        const b = el('button', { class: cls.join(' '), type: 'button', 'data-idx': i },
          '<span class="dojo-opt-letter">' + String.fromCharCode(65 + i) + '</span><span class="dojo-opt-text">' + esc(opt) + '</span>');
        if (locked) b.disabled = true;
        optionsEl.appendChild(b);
      });
    }

    function showFeedback(correct, firstTry) {
      feedback.hidden = false;
      feedback.className = 'dojo-predict-feedback ' + (correct ? 'ok' : 'bad');
      feedback.innerHTML =
        (correct
          ? '<b>' + (firstTry ? '✓ First try — +' + xp + ' XP banked.' : '✓ Correct.') + '</b> '
          : '<b>✗ Not this one.</b> The printed result would be the other highlighted option. ') +
        '<div class="dojo-predict-explain">' + (ex.explain || '') + '</div>';
    }

    if (solved) {
      paint(state.choice, true);
      showFeedback(true, state.firstTry);
    } else {
      paint(-1, false);
      optionsEl.addEventListener('click', (ev) => {
        const btn = ev.target.closest('.dojo-option');
        if (!btn || btn.disabled) return;
        const choice = +btn.dataset.idx;
        const rec = Store.answerQuiz(ex.id, choice, (ex.options || []).length);
        const correct = choice === answer;
        rec.firstTry = rec.firstTry && correct;
        if (correct) {
          Store.bankQuiz(ex.id, xp);   // marks correct + banks the XP
          awardXPPill(wrap, xp);
        }
        paint(choice, true);
        showFeedback(correct, rec.firstTry);
        refreshCounters();
      });
    }
    return wrap;
  }

  // ── Code-mode exercise ─────────────────────────────────────────────────────

  function codeCell(ex, no, track, nb) {
    const wrap = el('div', { class: 'dojo-cell dojo-exercise', id: 'ex-' + ex.id });
    const xp = DIFF_XP[ex.difficulty] || 0;
    const solved = Store.isSolved(ex.id);
    const hintsShown = Store.hintsShown(ex.id);
    const solutionOpen = Store.solutionShown(ex.id) && solved;
    const tests = (ex.tests || []);
    const visible = tests.filter(t => !t.hidden);
    const hidden = tests.filter(t => t.hidden);
    const draft = Store.draft(ex.id);

    wrap.innerHTML =
      '<div class="dojo-cell-head"><span class="dojo-cell-kind exercise">EXERCISE ' + no + '</span>' +
      '<span class="dojo-cell-title">' + esc(ex.title || '') + '</span>' +
      '<span class="dojo-diff d-' + ex.difficulty + '">' + (DIFF_LABEL[ex.difficulty] || ex.difficulty) + '</span>' +
      '<span class="dojo-xp-chip' + (solved ? ' earned' : '') + '" title="Pass every test to bank ' + xp + ' XP.">' + (solved ? '✓ ' : '') + xp + ' XP</span></div>' +
      '<div class="dojo-ex-body">' + (ex.statement || '') + '</div>' +
      ((ex.constraints || []).length
        ? '<ul class="dojo-constraints">' + ex.constraints.map(c => '<li><code>' + esc(c) + '</code></li>').join('') + '</ul>' : '') +
      ((ex.examples || []).length
        ? '<div class="dojo-examples"><div class="dojo-examples-title">Examples</div>' +
          ex.examples.map(x =>
            '<div class="dojo-example"><code class="dojo-example-call">' + esc(x.call) + '</code>' +
            '<span class="dojo-example-arrow">→</span><code class="dojo-example-ret">' + esc(x.returns) + '</code>' +
            (x.why ? '<span class="dojo-example-why">' + esc(x.why) + '</span>' : '') + '</div>').join('') + '</div>' : '') +
      ((ex.tags || []).length
        ? '<div class="dojo-tags">' + ex.tags.map(t => '<span class="tag tag-purple">' + esc(t) + '</span>').join('') + '</div>' : '') +
      '<div class="dojo-editor-zone">' +
        '<div class="dojo-editor-bar"><span class="dojo-demo-lang">python · your solution</span>' +
        '<span class="dojo-draft-state" id="draft-' + ex.id + '"></span></div>' +
        '<textarea class="dojo-editor" id="ed-' + ex.id + '" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" wrap="off" aria-label="Code editor for ' + esc(ex.title) + '"></textarea>' +
      '</div>' +
      '<div class="dojo-actions">' +
        '<button class="dojo-btn dojo-btn-primary dojo-run-tests" type="button">▶ Run tests <kbd>Ctrl↵</kbd></button>' +
        '<button class="dojo-btn dojo-btn-ghost dojo-hint-btn" type="button">💡 Hint (' + hintsShown + '/' + (ex.hints || []).length + ')</button>' +
        '<button class="dojo-btn dojo-btn-ghost dojo-solution-btn" type="button">🔓 Solution</button>' +
        '<button class="dojo-btn dojo-btn-ghost dojo-reset-btn" type="button" title="Restore the starter code">↺ Reset</button>' +
      '</div>' +
      '<div class="dojo-hints" hidden></div>' +
      '<div class="dojo-results" hidden></div>' +
      '<div class="dojo-solution" hidden>' +
        '<div class="dojo-solution-bar">editorial — the reasoning, then the code</div>' +
        (ex.reasoning ? '<div class="dojo-solution-reason">' + ex.reasoning + '</div>' : '') +
        '<pre class="dojo-solution-code"><code>' + esc(ex.solution || '') + '</code></pre>' +
      '</div>';

    const editor = $('.dojo-editor', wrap);
    editor.value = draft != null ? draft : (ex.starter || '');
    autoGrow(editor);

    // ── editor behaviors
    bindEditorKeys(editor, wrap, ex, track);
    editor.addEventListener('input', () => {
      autoGrow(editor);
      const ds = $('#draft-' + ex.id, wrap);
      if (ds) { ds.textContent = 'saving…'; }
      saveDraft(ex.id, editor.value);
    });
    setTimeout(() => { const ds = $('#draft-' + ex.id, wrap); if (ds) ds.textContent = 'draft saved ✓'; }, 400);

    $('.dojo-reset-btn', wrap).addEventListener('click', () => {
      if (editor.value !== (ex.starter || '') && !confirm('Discard your current code and restore the starter?')) return;
      editor.value = ex.starter || '';
      Store.clearDraft(ex.id);
      autoGrow(editor);
      hideResults(wrap);
    });

    // ── hints (progressive disclosure, last hint is the answer)
    const hintsEl = $('.dojo-hints', wrap);
    if (hintsShown > 0) {
      hintsEl.hidden = false;
      hintsEl.innerHTML = (ex.hints || []).slice(0, hintsShown)
        .map((h, i) => '<div class="dojo-hint"><span class="dojo-hint-n">Hint ' + (i + 1) + '</span>' + esc(h) + '</div>').join('');
    }
    const hintBtn = $('.dojo-hint-btn', wrap);
    if (hintsShown >= (ex.hints || []).length) hintBtn.disabled = true;
    hintBtn.addEventListener('click', () => {
      const n = Store.hintsShown(ex.id);
      if (n >= (ex.hints || []).length) return;
      Store.showHint(ex.id);
      hintsEl.hidden = false;
      hintsEl.insertAdjacentHTML('beforeend',
        '<div class="dojo-hint"><span class="dojo-hint-n">Hint ' + (n + 1) + '</span>' + esc(ex.hints[n]) + '</div>');
      hintBtn.innerHTML = '💡 Hint (' + (n + 1) + '/' + ex.hints.length + ')';
      if (n + 1 >= ex.hints.length) hintBtn.disabled = true;
    });

    // ── solution (always visible after solving; confirm before)
    const solutionEl = $('.dojo-solution', wrap);
    if (solutionOpen) solutionEl.hidden = false;
    $('.dojo-solution-btn', wrap).addEventListener('click', () => {
      if (!Store.isSolved(ex.id)
        && !Store.solutionShown(ex.id)
        && !confirm('Peeking is allowed — the XP is yours once your own code passes every test.\n\nOpen the editorial?')) return;
      Store.markSolution(ex.id);
      solutionEl.hidden = false;
      solutionEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });

    // ── run tests
    const runBtn = $('.dojo-run-tests', wrap);
    runBtn.addEventListener('click', () => runExercise(wrap, ex, track, runBtn));

    return wrap;
  }

  function runExercise(wrap, ex, track, runBtn) {
    const editor = $('.dojo-editor', wrap);
    const results = $('.dojo-results', wrap);
    const code = editor.value;
    runBtn.disabled = true;
    runBtn.innerHTML = '⏳ Running…';
    results.hidden = false;
    results.className = 'dojo-results running';
    results.innerHTML = '<div class="dojo-results-summary running">Running your code against ' +
      (ex.tests || []).length + ' tests' + ((track.packages || []).length ? ' (loading ' + esc(track.packages.join(', ')) + ' first)' : '') +
      ' — first run boots Python, please hold…</div>';
    Runner.ensureEngine();
    Runner.runTests(code, ex.func, ex.tests, track.packages).then(res => {
      runBtn.disabled = false;
      runBtn.innerHTML = '▶ Run tests <kbd>Ctrl↵</kbd>';
      renderResults(wrap, ex, res);
    }).catch(err => {
      runBtn.disabled = false;
      runBtn.innerHTML = '▶ Run tests <kbd>Ctrl↵</kbd>';
      results.className = 'dojo-results';
      results.innerHTML = '<div class="dojo-results-summary fail">⚠ Could not run: ' + esc(err.message) +
        ' — check your connection (Pyodide loads from a CDN) and try again.</div>';
    });
  }

  function renderResults(wrap, ex, res) {
    const results = $('.dojo-results', wrap);
    results.className = 'dojo-results';

    if (res.stage === 'compile') {
      results.innerHTML =
        '<div class="dojo-results-summary fail">✗ Your code raised before any test ran</div>' +
        '<pre class="dojo-stderr">' + esc((res.error || '').trim()) + '</pre>' +
        (res.stdout ? '<pre class="dojo-stdout">' + esc(res.stdout) + '</pre>' : '');
      return;
    }

    const rows = (res.results || []).map((r, i) => {
      const pass = !!r.passed;
      let detail = '';
      if (!pass) {
        const bits = [];
        if (r.call) bits.push('<div class="dojo-t-row"><span>call</span><code>' + esc(r.call) + '</code></div>');
        if (r.expected !== undefined && r.expected !== '') bits.push('<div class="dojo-t-row"><span>expected</span><code class="t-exp">' + esc(r.expected) + '</code></div>');
        if (r.got !== undefined && r.got !== '') bits.push('<div class="dojo-t-row"><span>got</span><code class="t-got">' + esc(r.got) + '</code></div>');
        if (r.error) bits.push('<pre class="dojo-t-err">' + esc(r.error) + '</pre>');
        if (r.stdout) bits.push('<pre class="dojo-t-out">' + esc(r.stdout) + '</pre>');
        detail = '<div class="dojo-t-detail">' + bits.join('') + '</div>';
      }
      const ops = (r.ops !== undefined)
        ? '<span class="dojo-t-ops' + (r.passed ? '' : ' over') + '" title="Elements your algorithm inspected vs the efficiency budget">⚙ ' + r.ops + (r.budget ? ' / ' + r.budget : '') + '</span>' : '';
      return '<div class="dojo-t ' + (pass ? 'pass' : 'fail') + '">' +
        '<span class="dojo-t-ico">' + (pass ? '✓' : '✗') + '</span>' +
        '<span class="dojo-t-label">' + esc(r.label || ('test ' + (i + 1))) + '</span>' +
        (r.hidden ? '<span class="dojo-t-hidden" title="Inputs hidden — same shape as the visible ones, tougher corners">hidden</span>' : '') +
        ops + detail + '</div>';
    }).join('');

    const nPass = (res.results || []).filter(r => r.passed).length;
    const nAll = (res.results || []).length;
    const allPass = res.ok && nAll > 0 && nPass === nAll;
    const firstTry = !runFailures[ex.id];
    runFailures[ex.id] = runFailures[ex.id] || !allPass;

    const already = Store.isSolved(ex.id);
    let summary;
    if (allPass) {
      const newly = Store.solve(ex.id, DIFF_XP[ex.difficulty] || 0, firstTry);
      summary = '<div class="dojo-results-summary pass">✓ All ' + nAll + ' tests passed' +
        (newly ? ' — <b>+' + (DIFF_XP[ex.difficulty] || 0) + ' XP' + (firstTry ? ' first try</b> 🎉' : '</b>') : ' (already solved)') + '</div>';
    } else {
      summary = '<div class="dojo-results-summary fail">✗ ' + nPass + ' / ' + nAll + ' tests passed — ' +
        (nPass === 0 ? 'start from the first failure, it usually explains the rest' : 'fix the red ones, the hidden tests probe the same edges harder') + '</div>';
    }

    results.innerHTML = summary + rows +
      ((res.stdout && !allPass) ? '<pre class="dojo-stdout">' + esc(res.stdout) + '</pre>' : '');

    if (allPass) {
      const chip = $('.dojo-xp-chip', wrap);
      if (chip) { chip.classList.add('earned'); chip.textContent = '✓ ' + (DIFF_XP[ex.difficulty] || 0) + ' XP'; }
      if (!already) {
        burstConfetti(results);
        refreshCounters();
        const sol = $('.dojo-solution', wrap);
        if (sol) sol.hidden = false;   // earned the editorial
      }
    }
  }

  const runFailures = {};   // exId -> true once a run has failed (first-try tracking)

  // ── Editor helpers ─────────────────────────────────────────────────────────

  function autoGrow(ta) {
    const min = 6 * 21 + 24;
    ta.style.height = 'auto';
    const h = Math.max(min, ta.scrollHeight + 12);
    ta.style.height = h + 'px';
  }

  function saveDraft(exId, code) {
    Store.setDraft(exId, code);
    const ds = document.getElementById('draft-' + exId);
    if (ds) {
      ds.textContent = 'draft saved ✓';
      setTimeout(() => { if (ds.textContent === 'draft saved ✓') ds.textContent = ''; }, 1600);
    }
  }

  function bindEditorKeys(editor, wrap, ex, track) {
    editor.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + Enter runs tests
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        runExercise(wrap, ex, track, $('.dojo-run-tests', wrap));
        return;
      }
      if (e.key === 'Tab') {
        e.preventDefault();
        const s = editor.selectionStart, en = editor.selectionEnd, v = editor.value;
        if (s === en || !v.slice(s, en).includes('\n')) {
          if (e.shiftKey) {
            const ls = v.lastIndexOf('\n', s - 1) + 1;
            const lead = v.slice(ls, s);
            const cut = lead.match(/^ {1,4}/);
            if (cut) {
              editor.value = v.slice(0, ls) + lead.slice(cut[0].length) + v.slice(s);
              editor.selectionStart = editor.selectionEnd = s - cut[0].length;
            }
          } else {
            editor.value = v.slice(0, s) + '    ' + v.slice(en);
            editor.selectionStart = editor.selectionEnd = s + 4;
          }
        } else {
          // indent / outdent whole lines
          const ls = v.lastIndexOf('\n', s - 1) + 1;
          const block = v.slice(ls, en);
          const re = e.shiftKey ? /^ {1,4}/gm : /^/gm;
          const delta = e.shiftKey ? -1 : 1;
          const next = e.shiftKey ? block.replace(re, m => m.slice(0, Math.max(0, m.length - 4))) : block.replace(re, '    ');
          const grown = next.length - block.length;
          editor.value = v.slice(0, ls) + next + v.slice(en);
          editor.selectionStart = ls;
          editor.selectionEnd = en + grown;
          void delta;
        }
        autoGrow(editor);
        return;
      }
      if (e.key === 'Enter') {
        // auto-indent: copy leading whitespace; +4 after a colon
        e.preventDefault();
        const s = editor.selectionStart, v = editor.value;
        const ls = v.lastIndexOf('\n', s - 1) + 1;
        const line = v.slice(ls, s);
        const lead = (line.match(/^\s*/) || [''])[0];
        const extra = /:\s*$/.test(line) ? '    ' : '';
        const ins = '\n' + lead + extra;
        editor.value = v.slice(0, s) + ins + v.slice(editor.selectionEnd);
        editor.selectionStart = editor.selectionEnd = s + ins.length;
        autoGrow(editor);
        return;
      }
      if (e.key === 'Backspace' && editor.selectionStart === editor.selectionEnd) {
        // dedent: swallowing 4 spaces at once feels like an editor
        const s = editor.selectionStart, v = editor.value;
        const ls = v.lastIndexOf('\n', s - 1) + 1;
        const before = v.slice(ls, s);
        if (before.length >= 4 && /^ +$/.test(before) && before.length % 4 === 0) {
          e.preventDefault();
          editor.value = v.slice(0, s - 4) + v.slice(s);
          editor.selectionStart = editor.selectionEnd = s - 4;
          autoGrow(editor);
        }
      }
    });
  }

  function hideResults(wrap) {
    const r = $('.dojo-results', wrap);
    if (r) { r.hidden = true; r.innerHTML = ''; }
  }

  // ── Celebration & counters ─────────────────────────────────────────────────

  function awardXPPill(wrap, xp) {
    const chip = $('.dojo-xp-chip', wrap);
    if (chip) { chip.classList.add('earned'); chip.textContent = '✓ ' + (xp || 5) + ' XP'; }
    burstConfetti(chip || wrap);
  }

  function refreshCounters() {
    const xpEl = $('#dojo-xp-num');
    if (xpEl) xpEl.textContent = String(Store.totalXP());
    const nbCount = $('#nb-solved-count');
    if (nbCount && window.__dojoCurrentNb) {
      const s = Model.notebookStats(window.__dojoCurrentNb);
      nbCount.textContent = s.solved + '/' + s.exercises + ' exercises solved';
    }
  }

  function burstConfetti(anchor) {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const host = anchor.closest('.dojo-cell') || anchor.parentElement;
    if (!host) return;
    const rect = host.getBoundingClientRect();
    const colors = ['#58a6ff', '#3fb950', '#f0883e', '#bc8cff', '#e3b341'];
    for (let i = 0; i < 22; i++) {
      const p = el('span', { class: 'dojo-confetti' });
      p.style.left = (8 + Math.random() * 84) + '%';
      p.style.background = colors[i % colors.length];
      p.style.animationDelay = (Math.random() * 0.25) + 's';
      p.style.setProperty('--dx', (Math.random() * 160 - 80) + 'px');
      p.style.setProperty('--dr', (Math.random() * 540 - 270) + 'deg');
      host.appendChild(p);
      setTimeout(() => p.remove(), 1600);
    }
    void rect;
  }

  // ── Routing & init ─────────────────────────────────────────────────────────

  function route() {
    const root = $('#dojo-root');
    if (!root) return;
    const r = parseHash();
    root.innerHTML = '';
    renderChrome(root);
    window.__dojoCurrentNb = null;

    if (r.view === 'notebook') {
      const entry = Model.notebooks[r.nbId];
      if (entry) {
        window.__dojoCurrentNb = entry.nb;
        renderNotebook(root, entry.track, entry.nb);
      } else {
        renderHome(root);
      }
    } else if (r.view === 'track') {
      renderTrack(root, Model.byId[r.trackId]);
    } else {
      renderHome(root);
    }

    const main = $('#main-content') || root;
    if (main && main.scrollIntoView) window.scrollTo(0, 0);
  }

  function boot() {
    Store.load();
    Model.build();
    // Merge py-core note counts etc. — expose small helper used by renderHome.
    Model.notebooksCount = function () { return Object.keys(this.notebooks).length; };
    if (!window.PRACTICE_TRACKS || !window.PRACTICE_TRACKS.length) {
      const root = $('#dojo-root');
      root.innerHTML = '<div class="callout warning" style="margin-top:2rem;">' +
        '<div class="callout-icon">⚠️</div><div class="callout-body"><strong>Track data did not load</strong>' +
        '<p>The notebook data files under <code>practice/data/</code> could not be read. If you are serving this site from a file, use a local web server (e.g. <code>python3 -m http.server</code>) instead of opening the HTML directly.</p></div></div>';
      return;
    }
    window.addEventListener('hashchange', route);
    route();
  }

  // ── Start after shared.js has injected the site layout.
  // injectLayout() re-creates the body via innerHTML inside its own
  // DOMContentLoaded handler; rendering before it would clone our nodes and
  // drop every event listener. A macrotask after DOMContentLoaded guarantees
  // the layout pass has finished. Fallback covers late/dynamic loading.
  function start() { setTimeout(boot, 0); }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else if (document.getElementById('top-header')) {
    start();                       // layout already injected
  } else {
    document.addEventListener('DOMContentLoaded', start);
  }

})();


