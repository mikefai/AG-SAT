/* SATPrep Studio — views: home catalog, lessons, practice player. */
(function () {
  var esc = window.SATTools.esc;
  var store = function () { return window.SATStore; };

  var CATS = ["Craft & Structure", "Information & Ideas", "Expression of Ideas",
    "Standard English Conventions", "Algebra", "Advanced Math",
    "Problem Solving & Data Analysis", "Geometry & Trigonometry"];
  var RW = CATS.slice(0, 4), MATH = CATS.slice(4);
  var GUIDES = [
    { title: "2026 Digital Blueprint", meta: "Format · Adaptive · Desmos", href: "../Study_Notes/sat_2026_blueprint_notes.html", tags: ["2026", "bluebook", "desmos"] },
    { title: "Desmos Mastery Guide", meta: "Calculator hacks", href: "../Question_Banks/sat_desmos_calculator_mastery_guide_and_hacks.html", tags: ["desmos", "calculator", "math"] },
    { title: "Distractor Trap Radar", meta: "RW cheat sheet", href: "../Question_Banks/sat_digital_rw_distractor_trap_radar_and_cheat_sheet.html", tags: ["traps", "reading", "cheatsheet"] }
  ];

  function domainOf(cat) { return RW.indexOf(cat) >= 0 ? "Reading & Writing" : "Math"; }
  function iconFor(kind, domain) {
    if (kind === "mock") return ["icon-test", "🧪"];
    if (kind === "guide") return ["icon-guide", "📘"];
    if (domain === "Math") return ["icon-math", "∑"];
    return ["icon-rw", "✎"];
  }
  function catStats(cat) {
    var s = store().stats(window.SAT_QUESTIONS).perCat[cat] || { answered: 0, correct: 0, total: 10 };
    return s;
  }

  /* ---------------- HOME ---------------- */
  var HomeUI = { tab: "featured", pill: "all", q: "" };
  function cardHTML(c) {
    var ic = iconFor(c.kind, c.domain);
    var sub = "";
    if (c.kind === "lesson") {
      var done = store().state.lessonsDone.indexOf(c.id) >= 0;
      sub = '<span class="meta"><span>' + esc(c.meta) + '</span>' +
        (done ? '<span class="badge badge-green">✓ Studied</span>' : "") + "</span>";
    } else if (c.kind === "practice") {
      var st = catStats(c.cat);
      sub = '<span class="meta"><span>★★★★★ (' + st.answered + " answered)</span><span>" +
        st.correct + "/" + st.answered + " correct</span></span>";
    } else {
      sub = '<span class="meta"><span>' + esc(c.meta) + "</span></span>";
    }
    var tags = (c.tags || []).map(function (t) { return '<span class="tag">#' + esc(t) + "</span>"; }).join("");
    var btn = c.kind === "guide"
      ? '<a class="btn btn-ghost btn-sm" href="' + esc(c.href) + '">Open ↗</a>'
      : '<a class="btn btn-ghost btn-sm" href="' + esc(c.href) + '">Start →</a>';
    return '<article class="card" data-search="' + esc((c.title + " " + (c.tags || []).join(" ") + " " + (c.domain || "")).toLowerCase()) + '">' +
      '<div class="card-top"><span class="card-icon ' + ic[0] + '">' + ic[1] + '</span>' +
      "<div><h3>" + esc(c.title) + "</h3>" + sub + "</div></div>" +
      '<p class="desc">' + esc(c.desc) + "</p>" +
      '<div class="tags"><span class="kind-badge">' + esc(c.kind) + "</span>" + tags + "</div>" + btn + "</article>";
  }
  function buildCards() {
    var cards = [];
    window.SAT_LESSONS.forEach(function (l) {
      cards.push({ kind: "lesson", id: l.id, title: l.title, domain: l.domain,
        meta: "Lesson · " + l.time, desc: l.summary, tags: [l.domain === "Math" ? "math" : "reading", "teach"],
        href: "#/lesson/" + l.id, feat: true });
    });
    CATS.forEach(function (c) {
      cards.push({ kind: "practice", cat: c, title: c + " — Practice Set", domain: domainOf(c),
        meta: "10 questions · instant feedback", desc: "Show-style walkthrough set with why-right / why-wrong rationales.",
        tags: [domainOf(c) === "Math" ? "math" : "reading", "show"], href: "#/practice?cat=" + encodeURIComponent(c), feat: c === "Algebra" || c === "Craft & Structure" });
    });
    cards.push({ kind: "mock", title: "Quick Check Mock", domain: "Mixed",
      meta: "8 Qs · ~10 min · exam mode", desc: "One question per category, exam-mode scoring with full review.",
      tags: ["test", "mock", "timed"], href: "#/homework?set=quick", feat: true, isNew: true });
    cards.push({ kind: "mock", title: "Standard Mock (24Q)", domain: "Mixed",
      meta: "24 Qs · ~30 min · exam mode", desc: "Three per category across Reading, Writing and Math — a real homework test.",
      tags: ["test", "mock", "timed"], href: "#/homework?set=standard", feat: false, isNew: true });
    GUIDES.forEach(function (g) {
      cards.push({ kind: "guide", title: g.title, domain: "Guide", meta: g.meta, desc: "Compiled reference from the workspace.",
        tags: g.tags, href: g.href, feat: false });
    });
    return cards;
  }
  function HomeView() {
    var cards = buildCards();
    var pills = [["all", "All"], ["rw", "Reading & Writing"], ["math", "Math"],
      ["lesson", "Lessons"], ["practice", "Practice"], ["mock", "Mocks"], ["guide", "Guides"]];
    var html = '<section class="hero"><h1>Discover what SAT prep can do for you</h1>' +
      "<p>We've turned 280 workspace questions and 8 lessons into a studio: learn, practice, test, meet 1:1.</p>" +
      '<div class="searchbar"><input id="homeSearch" type="search" placeholder="Enter a topic or skill… (e.g. quadratics, transitions)" aria-label="Search topics">' +
      '<button class="btn btn-primary" id="homeSearchBtn">Search</button></div>' +
      '<div class="pills" id="homePills">' + pills.map(function (p) {
        return '<button class="pill' + (HomeUI.pill === p[0] ? " active" : "") + '" data-pill="' + p[0] + '">' + p[1] + "</button>";
      }).join("") + "</div></section>" +
      '<div class="tabs-row"><div class="tabs">' +
      [["featured", "✦ Featured"], ["popular", "★ Popular"], ["new", "✚ New"]].map(function (t) {
        return '<button class="tab' + (HomeUI.tab === t[0] ? " active" : "") + '" data-tab="' + t[0] + '">' + t[1] + "</button>";
      }).join("") + '</div><div class="tabs-meta"><span id="cardCount"></span></div></div>' +
      '<div class="grid" id="homeGrid"></div>';
    return { html: html, mount: mountHome };
    function mountHome() {
      var grid = document.getElementById("homeGrid");
      var input = document.getElementById("homeSearch");
      function render() {
        var list = cards.filter(function (c) {
          if (HomeUI.pill === "rw" && c.domain !== "Reading & Writing") return false;
          if (HomeUI.pill === "math" && c.domain !== "Math") return false;
          if (["lesson", "practice", "mock", "guide"].indexOf(HomeUI.pill) >= 0 && c.kind !== HomeUI.pill) return false;
          if (HomeUI.tab === "featured" && !c.feat) return false;
          if (HomeUI.tab === "new" && !c.isNew && c.kind !== "guide") return false;
          if (HomeUI.q && (c.title + " " + (c.tags || []).join(" ")).toLowerCase().indexOf(HomeUI.q) < 0) return false;
          return true;
        });
        if (HomeUI.tab === "popular") {
          list = list.slice().sort(function (a, b) {
            var sa = a.kind === "practice" ? catStats(a.cat).answered : 0;
            var sb = b.kind === "practice" ? catStats(b.cat).answered : 0;
            return sb - sa;
          });
        }
        grid.innerHTML = list.map(cardHTML).join("") || '<p style="color:var(--text-muted)">No matches — try another search.</p>';
        document.getElementById("cardCount").textContent = list.length + " resources";
      }
      input.addEventListener("input", function () { HomeUI.q = input.value.trim().toLowerCase(); render(); });
      document.getElementById("homeSearchBtn").addEventListener("click", render);
      document.getElementById("homePills").addEventListener("click", function (e) {
        var b = e.target.closest("[data-pill]"); if (!b) return;
        HomeUI.pill = b.getAttribute("data-pill");
        this.querySelectorAll(".pill").forEach(function (p) { p.classList.toggle("active", p === b); });
        render();
      });
      document.querySelector(".tabs").addEventListener("click", function (e) {
        var b = e.target.closest("[data-tab]"); if (!b) return;
        HomeUI.tab = b.getAttribute("data-tab");
        this.querySelectorAll(".tab").forEach(function (t) { t.classList.toggle("active", t === b); });
        render();
      });
      render();
    }
  }

  /* ---------------- LESSONS ---------------- */
  function LessonsView() {
    var cards = window.SAT_LESSONS.map(function (l) {
      var done = store().state.lessonsDone.indexOf(l.id) >= 0;
      return '<article class="card"><div class="card-top"><span class="card-icon ' +
        (l.domain === "Math" ? "icon-math\">∑" : "icon-rw\">✎") + "</span><div><h3>" + esc(l.title) + "</h3>" +
        '<span class="meta"><span>' + esc(l.domain) + " · " + esc(l.time) + "</span>" +
        (done ? '<span class="badge badge-green">✓ Studied</span>' : "") + "</span></div></div>" +
        '<p class="desc">' + esc(l.summary) + "</p>" +
        '<a class="btn btn-ghost btn-sm" href="#/lesson/' + l.id + '">Open lesson →</a></article>';
    }).join("");
    return { html: '<div class="page-head"><div><h1>Lessons</h1><p>Teach layer — strategy first, then practice. Use 🖍 Highlight and ✏ Pen while you read.</p></div></div><div class="grid">' + cards + "</div>" };
  }
  function LessonDetailView(id) {
    var l = window.SAT_LESSONS.filter(function (x) { return x.id === id; })[0];
    if (!l) return { html: '<div class="panel"><h2>Lesson not found</h2><a href="#/lessons">← All lessons</a></div>' };
    var secs = l.sections.map(function (s) {
      return "<h3>" + esc(s.h) + "</h3><p>" + esc(s.body) + "</p><ul>" +
        s.bullets.map(function (b) { return "<li>" + esc(b) + "</li>"; }).join("") + "</ul>";
    }).join("");
    var done = store().state.lessonsDone.indexOf(l.id) >= 0;
    var html = '<div class="page-head"><div><p><a href="#/lessons">← Lessons</a> · ' + esc(l.domain) + " · " + esc(l.time) + "</p><h1>" + esc(l.title) + "</h1><p>" + esc(l.summary) + "</p></div></div>" +
      '<div class="two-col"><div class="panel lesson-body">' + secs +
      '<h3>Common traps</h3><ul class="trap-list">' + l.traps.map(function (t) { return "<li>⚠ " + esc(t) + "</li>"; }).join("") + "</ul></div>" +
      '<div><div class="panel"><h2>Study checklist</h2><ul class="check-list">' +
      l.checklist.map(function (c) { return "<li>" + esc(c) + "</li>"; }).join("") + "</ul>" +
      '<p style="margin-top:1rem;display:flex;gap:.5rem;flex-wrap:wrap">' +
      '<button class="btn btn-primary btn-sm" id="lessonDone">' + (done ? "✓ Studied — review again" : "Mark as studied") + "</button>" +
      '<a class="btn btn-outline btn-sm" href="#/practice?cat=' + encodeURIComponent(titleToCat(l.title)) + '">Practice this topic →</a></p></div>' +
      '<div class="panel"><h2>Next steps</h2><p><a href="#/homework?set=cat&cat=' + encodeURIComponent(titleToCat(l.title)) + '">Assign as homework test →</a><br><a href="#/sessions">Book a 1:1 on this topic →</a></p></div></div></div>';
    return { html: html, mount: function () {
      document.getElementById("lessonDone").addEventListener("click", function () {
        store().completeLesson(l.id);
        this.textContent = "✓ Studied — review again";
      });
    } };
  }
  function titleToCat(title) {
    var map = { "Craft & Structure": "Craft & Structure", "Information & Ideas": "Information & Ideas",
      "Expression of Ideas": "Expression of Ideas", "Standard English Conventions": "Standard English Conventions",
      "Algebra": "Algebra", "Advanced Math": "Advanced Math",
      "Problem Solving & Data Analysis": "Problem Solving & Data Analysis",
      "Geometry & Trigonometry": "Geometry & Trigonometry" };
    return map[title] || "Algebra";
  }

  /* ---------------- PRACTICE (Show) ---------------- */
  var PracticeUI = { list: [], idx: 0, cat: "all", diff: "all", onlyReview: false, onlyFlagged: false };
  function PracticeView(query) {
    PracticeUI.cat = query.cat || "all";
    PracticeUI.diff = query.diff || "all";
    PracticeUI.onlyReview = query.review === "1";
    PracticeUI.onlyFlagged = query.flagged === "1";
    PracticeUI.idx = 0;
    applyPracticeFilter();
    return { html: practiceHTML(), mount: mountPractice };
  }
  function applyPracticeFilter() {
    PracticeUI.list = window.SAT_QUESTIONS.filter(function (q) {
      if (PracticeUI.cat !== "all" && q.category !== PracticeUI.cat) return false;
      if (PracticeUI.diff !== "all" && q.difficulty !== PracticeUI.diff) return false;
      var a = store().state.answers[q.id];
      if (PracticeUI.onlyReview && !( !a || (a && !a.correct))) return false;
      if (PracticeUI.onlyFlagged && !store().isFlagged(q.id)) return false;
      return true;
    });
    if (PracticeUI.idx >= PracticeUI.list.length) PracticeUI.idx = 0;
  }
  function practiceHTML() {
    var catOpts = ['<option value="all">All categories</option>'].concat(CATS.map(function (c) {
      return '<option value="' + esc(c) + '"' + (PracticeUI.cat === c ? " selected" : "") + ">" + esc(c) + "</option>";
    })).join("");
    return '<div class="page-head"><div><h1>Practice</h1><p>Show layer — instant feedback with why-right / why-wrong rationales. Keys: <kbd>1–4</kbd> answer, <kbd>←→</kbd> navigate.</p></div></div>' +
    '<div class="panel"><div class="form-grid"><label class="field">Category<select id="prCat">' + catOpts + "</select></label>" +
    '<label class="field">Difficulty<select id="prDiff">' + ["all", "easy", "medium", "hard"].map(function (d) {
      return '<option value="' + d + '"' + (PracticeUI.diff === d ? " selected" : "") + ">" + d[0].toUpperCase() + d.slice(1) + "</option>";
    }).join("") + "</select></label></div>" +
    '<p style="display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:0">' +
    '<button class="pill' + (PracticeUI.onlyReview ? " active" : "") + '" id="prReview">Needs review</button>' +
    '<button class="pill' + (PracticeUI.onlyFlagged ? " active" : "") + '" id="prFlagged">⚑ Flagged</button>' +
    '<span class="tabs-meta" id="prCount"></span></p></div>' +
    '<div id="prBody"></div>';
  }
  function mountPractice() {
    document.getElementById("prCat").addEventListener("change", function () { PracticeUI.cat = this.value; PracticeUI.idx = 0; applyPracticeFilter(); renderQ(); });
    document.getElementById("prDiff").addEventListener("change", function () { PracticeUI.diff = this.value; PracticeUI.idx = 0; applyPracticeFilter(); renderQ(); });
    document.getElementById("prReview").addEventListener("click", function () { PracticeUI.onlyReview = !PracticeUI.onlyReview; this.classList.toggle("active", PracticeUI.onlyReview); PracticeUI.idx = 0; applyPracticeFilter(); renderQ(); });
    document.getElementById("prFlagged").addEventListener("click", function () { PracticeUI.onlyFlagged = !PracticeUI.onlyFlagged; this.classList.toggle("active", PracticeUI.onlyFlagged); PracticeUI.idx = 0; applyPracticeFilter(); renderQ(); });
    document.addEventListener("keydown", practiceKeys);
    renderQ();
  }
  function practiceKeys(e) {
    if (!document.getElementById("prBody")) return;
    if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement && document.activeElement.tagName)) return;
    var map = { 1: 0, 2: 1, 3: 2, 4: 3, a: 0, b: 1, c: 2, d: 3, A: 0, B: 1, C: 2, D: 3 };
    var k = e.key;
    if (k in map) { var btns = document.querySelectorAll("#prOpts .opt-btn"); if (btns[map[k]]) btns[map[k]].click(); }
    if (k === "ArrowRight") practiceNav(1);
    if (k === "ArrowLeft") practiceNav(-1);
  }
  function practiceNav(d) {
    PracticeUI.idx = (PracticeUI.idx + d + PracticeUI.list.length) % Math.max(1, PracticeUI.list.length);
    renderQ();
  }
  function renderQ() {
    var body = document.getElementById("prBody");
    if (!body) return;
    document.getElementById("prCount").textContent = PracticeUI.list.length + " questions";
    if (!PracticeUI.list.length) { body.innerHTML = '<div class="panel"><p>No questions match these filters.</p></div>'; return; }
    var q = PracticeUI.list[PracticeUI.idx];
    var st = store();
    var saved = st.state.answers[q.id];
    var flagged = st.isFlagged(q.id);
    var nav = PracticeUI.list.map(function (item, i) {
      var a = st.state.answers[item.id];
      var cls = "q-pill" + (a ? (a.correct ? " correct" : " wrong") : "") + (i === PracticeUI.idx ? " done" : "") + (st.isFlagged(item.id) ? " flagged" : "");
      return '<button class="' + cls + '" data-i="' + i + '">' + (i + 1) + "</button>";
    }).join("");
    var letters = ["A", "B", "C", "D"];
    var opts = q.options.map(function (o, i) {
      var cls = "opt-btn";
      if (saved) {
        cls += " dim";
        if (letters[i] === q.answer) cls += " picked-correct";
        else if (letters[i] === saved.pick) cls += " picked-wrong";
      }
      return '<button class="' + cls + '" data-pick="' + letters[i] + '"' + (saved ? " disabled" : "") + "><strong>" + letters[i] + ".</strong> " + esc(o) + "</button>";
    }).join("");
    var fb = "";
    if (saved) {
      fb = '<div class="feedback ' + (saved.correct ? "good" : "bad") + '">' +
        (saved.correct ? "✓ Correct." : "✗ Not quite — correct answer: <strong>" + q.answer + "</strong>.") +
        '<details class="rationale"><summary>Why? Show rationale</summary><p>' + esc(q.rationale) + "</p></details></div>";
    }
    body.innerHTML = '<div class="q-nav">' + nav + '</div><div class="practice-layout">' +
      '<div class="panel stimulus-pane"><span class="badge badge-blue">' + esc(q.category) + '</span> ' +
      '<span class="diff diff-' + q.difficulty + '">' + esc(q.difficulty) + "</span>" +
      (q.passage ? "<h3>Passage</h3><p>" + esc(q.passage) + "</p>" : "") +
      (q.stimulus && !q.passage ? "<h3>Prompt</h3><p>" + esc(q.stimulus) + "</p>" : "") +
      '<p style="color:var(--text-muted);font-size:.82rem">Skill: ' + esc(q.skill) + " · " + esc(q.id) + "</p></div>" +
      '<div class="panel"><p><strong>Q' + (PracticeUI.idx + 1) + " of " + PracticeUI.list.length + ".</strong> " + esc(q.question || q.stimulus || "Choose the best answer.") + "</p>" +
      '<div id="prOpts">' + opts + "</div>" + fb +
      '<p style="display:flex;gap:.5rem;flex-wrap:wrap">' +
      '<button class="btn btn-ghost btn-sm" id="prPrev">← Prev</button>' +
      '<button class="btn btn-ghost btn-sm" id="prNext">Next →</button>' +
      '<button class="btn btn-outline btn-sm" id="prFlag">' + (flagged ? "⚑ Flagged" : "⚐ Flag") + "</button>" +
      (saved ? '<button class="btn btn-ghost btn-sm" id="prRetry">Retry</button>' : "") + "</p></div></div>";
    body.querySelector(".q-nav").addEventListener("click", function (e) {
      var b = e.target.closest("[data-i]"); if (!b) return;
      PracticeUI.idx = parseInt(b.getAttribute("data-i"), 10); renderQ();
    });
    if (!saved) {
      body.querySelector("#prOpts").addEventListener("click", function (e) {
        var b = e.target.closest("[data-pick]"); if (!b) return;
        var pick = b.getAttribute("data-pick");
        st.recordAnswer(q.id, pick, pick === q.answer);
        renderQ();
      });
    } else {
      var retry = document.getElementById("prRetry");
      if (retry) retry.addEventListener("click", function () {
        delete st.state.answers[q.id]; st.save(); renderQ();
      });
    }
    document.getElementById("prPrev").addEventListener("click", function () { practiceNav(-1); });
    document.getElementById("prNext").addEventListener("click", function () { practiceNav(1); });
    document.getElementById("prFlag").addEventListener("click", function () {
      var on = st.toggleFlag(q.id); this.textContent = on ? "⚑ Flagged" : "⚐ Flag";
    });
  }

  window.SATViews = Object.assign(window.SATViews || {}, {
    HomeView: HomeView, LessonsView: LessonsView, LessonDetailView: LessonDetailView,
    PracticeView: PracticeView, CATS: CATS, cleanupPracticeKeys: function () {
      document.removeEventListener("keydown", practiceKeys);
    }
  });
})();
