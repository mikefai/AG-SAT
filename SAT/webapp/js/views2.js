/* SATPrep Studio — views: homework (Test), 1:1 sessions, progress. */
(function () {
  var esc = window.SATTools.esc;
  var store = function () { return window.SATStore; };
  var CATS = window.SATViews.CATS;

  /* ---------------- HOMEWORK ---------------- */
  var HW = { list: [], idx: 0, mode: "exam", title: "", secsLeft: 0, timerId: null, picks: {}, submitted: false, setId: "" };
  function setQuestions(setId, cat) {
    var Q = window.SAT_QUESTIONS;
    var n = store().state.attempts.length;
    function perCat(k) {
      var out = [];
      CATS.forEach(function (c) {
        var pool = Q.filter(function (q) { return q.category === c; });
        for (var i = 0; i < k; i++) out.push(pool[(n + i) % pool.length]);
      });
      return out;
    }
    if (setId === "cat") return { title: cat + " — Homework Test (10Q)", list: Q.filter(function (q) { return q.category === cat; }) };
    if (setId === "quick") return { title: "Quick Check Mock (8Q)", list: perCat(1) };
    if (setId === "standard") return { title: "Standard Mock (24Q)", list: perCat(3) };
    return { title: "Full Bank Challenge (280Q)", list: Q.slice() };
  }
  function HomeworkView(query) {
    if (query.set) return startHomework(query.set, query.cat || CATS[0], query.mode || "exam");
    var catOpts = CATS.map(function (c) { return '<option value="' + esc(c) + '">' + esc(c) + "</option>"; }).join("");
    var rows = store().state.attempts.slice().reverse().slice(0, 8).map(function (a) {
      var d = new Date(a.at);
      return "<tr><td>" + esc(a.title) + "</td><td>" + esc(a.mode) + "</td><td><strong>" + a.score + "/" + a.total + "</strong> (" + a.pct + "%)</td><td>" + d.toLocaleDateString() + "</td></tr>";
    }).join("");
    var html = '<div class="page-head"><div><h1>Homework</h1><p>Test layer — timed sets in exam mode, or instant-feedback practice. Attempts save to Progress.</p></div></div>' +
      '<div class="two-col"><div class="panel"><h2>New assignment</h2>' +
      '<div class="form-grid"><label class="field">Set<select id="hwSet">' +
      '<option value="cat">Single category (10Q)</option><option value="quick">Quick Check Mock (8Q)</option>' +
      '<option value="standard">Standard Mock (24Q)</option><option value="full">Full Bank (280Q)</option></select></label>' +
      '<label class="field">Category (for single set)<select id="hwCat">' + catOpts + "</select></label>" +
      '<label class="field">Mode<select id="hwMode"><option value="exam">Exam (locked until submit)</option><option value="practice">Practice (instant feedback)</option></select></label>' +
      '<label class="field">Minutes<select id="hwMins"><option value="auto">Auto (1.2 min / Q)</option><option value="10">10</option><option value="20">20</option><option value="35">35</option><option value="60">60</option></select></label></div>' +
      '<p><button class="btn btn-primary" id="hwStart">Start assignment →</button></p></div>' +
      '<div class="panel"><h2>Recent attempts</h2>' + (rows ? '<table class="clean"><tr><th>Set</th><th>Mode</th><th>Score</th><th>Date</th></tr>' + rows + "</table>" : "<p>No attempts yet — your results will appear here.</p>") + "</div></div>";
    return { html: html, mount: function () {
      document.getElementById("hwStart").addEventListener("click", function () {
        var set = document.getElementById("hwSet").value;
        var cat = document.getElementById("hwCat").value;
        var mode = document.getElementById("hwMode").value;
        var mins = document.getElementById("hwMins").value;
        location.hash = "#/homework?set=" + set + "&cat=" + encodeURIComponent(cat) + "&mode=" + mode + "&mins=" + mins;
      });
    } };
  }
  function startHomework(setId, cat, mode, mins) {
    var s = setQuestions(setId, cat);
    HW.list = s.list; HW.title = s.title; HW.idx = 0; HW.mode = mode || "exam";
    HW.setId = setId; HW.picks = {}; HW.submitted = false;
    var total = HW.list.length;
    var minutes = (mins && mins !== "auto") ? parseInt(mins, 10) : Math.max(5, Math.round(total * 1.2));
    HW.secsLeft = minutes * 60;
    return { html: '<div id="hwRunner"></div>', mount: mountRunner };
  }
  function fmtSecs(s) {
    s = Math.max(0, s);
    var m = Math.floor(s / 60), r = s % 60;
    return (m < 10 ? "0" : "") + m + ":" + (r < 10 ? "0" : "") + r;
  }
  function mountRunner() {
    renderRunner();
    clearInterval(HW.timerId);
    HW.timerId = setInterval(function () {
      HW.secsLeft -= 1;
      var el = document.getElementById("hwTimer");
      if (el) el.textContent = fmtSecs(HW.secsLeft);
      if (HW.secsLeft <= 0) { clearInterval(HW.timerId); submitHomework(true); }
    }, 1000);
  }
  function renderRunner() {
    var el = document.getElementById("hwRunner");
    if (!el) return;
    var q = HW.list[HW.idx];
    var letters = ["A", "B", "C", "D"];
    var nav = HW.list.map(function (item, i) {
      var cls = "q-pill" + (HW.picks[item.id] ? " done" : "") + (i === HW.idx ? " correct" : "");
      if (HW.submitted) {
        cls = "q-pill " + (HW.picks[item.id] === item.answer ? "correct" : "wrong");
      }
      return '<button class="' + cls + '" data-i="' + i + '">' + (i + 1) + "</button>";
    }).join("");
    var body = "";
    if (!HW.submitted) {
      var opts = q.options.map(function (o, i) {
        var sel = HW.picks[q.id] === letters[i] ? " picked-correct" : "";
        return '<button class="opt-btn' + sel + '" data-pick="' + letters[i] + '"><strong>' + letters[i] + ".</strong> " + esc(o) + "</button>";
      }).join("");
      var instant = "";
      if (HW.mode === "practice" && HW.picks[q.id]) {
        var ok = HW.picks[q.id] === q.answer;
        instant = '<div class="feedback ' + (ok ? "good" : "bad") + '">' + (ok ? "✓ Correct." : "✗ Correct answer: <strong>" + q.answer + "</strong>.") +
          '<details class="rationale"><summary>Why? Show rationale</summary><p>' + esc(q.rationale) + "</p></details></div>";
      }
      body = '<div class="practice-layout"><div class="panel stimulus-pane"><span class="badge badge-blue">' + esc(q.category) + '</span> ' +
        '<span class="diff diff-' + q.difficulty + '">' + esc(q.difficulty) + "</span>" +
        (q.passage ? "<h3>Passage</h3><p>" + esc(q.passage) + "</p>" : "") +
        (q.stimulus && !q.passage ? "<h3>Prompt</h3><p>" + esc(q.stimulus) + "</p>" : "") + "</div>" +
        '<div class="panel"><p><strong>Q' + (HW.idx + 1) + " of " + HW.list.length + ".</strong> " + esc(q.question || q.stimulus || "Choose the best answer.") + "</p>" +
        '<div id="hwOpts">' + opts + "</div>" + instant +
        '<p style="display:flex;gap:.5rem;flex-wrap:wrap"><button class="btn btn-ghost btn-sm" id="hwPrev">← Prev</button>' +
        '<button class="btn btn-ghost btn-sm" id="hwNext">Next →</button></p></div></div>';
    } else {
      var score = HW.list.filter(function (item) { return HW.picks[item.id] === item.answer; }).length;
      var rows = HW.list.map(function (item, i) {
        var ok = HW.picks[item.id] === item.answer;
        return '<tr><td>' + (i + 1) + "</td><td>" + esc(item.category) + "</td><td>" + (HW.picks[item.id] || "—") + "</td><td>" + item.answer + "</td>" +
          "<td>" + (ok ? "✓" : "✗") + "</td><td>" + esc(item.rationale) + "</td></tr>";
      }).join("");
      body = '<div class="panel"><h2>' + esc(HW.title) + " — Result: " + score + "/" + HW.list.length + "</h2>" +
        '<p>Saved to Progress. Review every miss below, then retry in Practice.</p>' +
        '<p><a class="btn btn-primary btn-sm" href="#/practice?review=1">Review misses in Practice →</a> ' +
        '<a class="btn btn-ghost btn-sm" href="#/homework">New assignment</a></p></div>' +
        '<div class="panel"><table class="clean"><tr><th>#</th><th>Category</th><th>You</th><th>Key</th><th>✓</th><th>Rationale</th></tr>' + rows + "</table></div>";
    }
    el.innerHTML = '<div class="page-head"><div><p><a href="#/homework">← Homework</a> · ' + esc(HW.mode) + ' mode</p><h1>' + esc(HW.title) + "</h1></div>" +
      (HW.submitted ? "" : '<div class="tabs-meta"><span>⏱ <strong id="hwTimer">' + fmtSecs(HW.secsLeft) + "</strong></span>" +
      '<button class="btn btn-ghost btn-sm" id="hwPause">Pause</button>' +
      '<button class="btn btn-primary btn-sm" id="hwSubmit">Submit</button></div>') + '</div><div class="q-nav">' + nav + "</div>" + body;
    el.querySelector(".q-nav").addEventListener("click", function (e) {
      var b = e.target.closest("[data-i]"); if (!b) return;
      HW.idx = parseInt(b.getAttribute("data-i"), 10); renderRunner();
    });
    if (!HW.submitted) {
      var box = document.getElementById("hwOpts");
      if (box) box.addEventListener("click", function (e) {
        var b = e.target.closest("[data-pick]"); if (!b) return;
        HW.picks[q.id] = b.getAttribute("data-pick");
        if (HW.mode === "practice") store().recordAnswer(q.id, HW.picks[q.id], HW.picks[q.id] === q.answer);
        renderRunner();
      });
      document.getElementById("hwPrev").addEventListener("click", function () { HW.idx = (HW.idx - 1 + HW.list.length) % HW.list.length; renderRunner(); });
      document.getElementById("hwNext").addEventListener("click", function () { HW.idx = (HW.idx + 1) % HW.list.length; renderRunner(); });
      document.getElementById("hwPause").addEventListener("click", function () {
        if (HW.timerId) { clearInterval(HW.timerId); HW.timerId = null; this.textContent = "Resume"; }
        else {
          this.textContent = "Pause";
          HW.timerId = setInterval(function () {
            HW.secsLeft -= 1;
            var t = document.getElementById("hwTimer");
            if (t) t.textContent = fmtSecs(HW.secsLeft);
            if (HW.secsLeft <= 0) { clearInterval(HW.timerId); submitHomework(true); }
          }, 1000);
        }
      });
      document.getElementById("hwSubmit").addEventListener("click", function () {
        var un = HW.list.filter(function (item) { return !HW.picks[item.id]; }).length;
        if (un > 0 && !window.confirm(un + " unanswered. Submit anyway?")) return;
        submitHomework(false);
      });
    }
  }
  function submitHomework(auto) {
    clearInterval(HW.timerId); HW.timerId = null;
    HW.submitted = true;
    var score = HW.list.filter(function (item) { return HW.picks[item.id] === item.answer; }).length;
    HW.list.forEach(function (item) {
      if (HW.picks[item.id]) store().recordAnswer(item.id, HW.picks[item.id], HW.picks[item.id] === item.answer);
    });
    store().addAttempt({ title: HW.title + (auto ? " (auto-submitted)" : ""), mode: HW.mode,
      score: score, total: HW.list.length, pct: Math.round((score / HW.list.length) * 100) });
    renderRunner();
    window.scrollTo(0, 0);
  }

  /* ---------------- SESSIONS ---------------- */
  function SessionsView() {
    var st = store();
    var topicOpts = '<option value="General SAT strategy">General SAT strategy</option>' +
      CATS.map(function (c) { return '<option value="' + esc(c) + '">' + esc(c) + "</option>"; }).join("");
    var upcoming = st.state.sessions.filter(function (s) { return !s.done; });
    var logged = st.state.sessions.filter(function (s) { return s.done; });
    function sesCard(s) {
      return '<div class="panel"><h3 style="margin-top:0">' + esc(s.student) + ' <span class="badge badge-blue">' + esc(s.topic) + "</span> " +
        (s.done ? '<span class="badge badge-green">done</span>' : '<span class="badge badge-amber">' + esc(s.date) + " · " + esc(s.time) + "</span>") + "</h3>" +
        "<p><strong>Goal:</strong> " + esc(s.goal || "—") + "</p>" +
        "<p><strong>Agenda:</strong><br>1. Review last homework attempt & misses (10 min)<br>2. Teach: " + esc(s.topic) +
        ' (<a href="#/lesson/' + lessonIdFor(s.topic) + '">open lesson</a>, 15 min)<br>3. Guided practice: <a href="#/practice?cat=' +
        encodeURIComponent(s.topic) + '">5 questions together</a> (15 min)<br>4. Assign homework: <a href="#/homework?set=cat&cat=' +
        encodeURIComponent(s.topic) + '">10Q test</a> (5 min)</p>' +
        '<label class="field">Session notes<textarea data-notes="' + s.id + '" placeholder="What was covered, strengths, next focus…">' + esc(s.notes || "") + "</textarea></label>" +
        '<p style="display:flex;gap:.5rem"><button class="btn btn-primary btn-sm" data-done="' + s.id + '">' + (s.done ? "Reopen" : "Mark done") + '</button>' +
        '<button class="btn btn-danger btn-sm" data-del="' + s.id + '">Delete</button></p></div>';
    }
    var html = '<div class="page-head"><div><h1>1:1 Sessions</h1><p>Book tutoring slots, follow the auto-built agenda, log notes. Everything saves on this device.</p></div></div>' +
      '<div class="two-col"><div class="panel"><h2>Book a session</h2><div class="form-grid">' +
      '<label class="field">Student<input id="sesName" placeholder="e.g. Elif K."></label>' +
      '<label class="field">Topic<select id="sesTopic">' + topicOpts + "</select></label>" +
      '<label class="field">Date<input id="sesDate" type="date"></label>' +
      '<label class="field">Time<input id="sesTime" type="time" value="17:00"></label></div>' +
      '<label class="field" style="margin-top:.6rem">Goal<textarea id="sesGoal" placeholder="e.g. Raise Algebra accuracy from 60% to 80%"></textarea></label>' +
      '<p><button class="btn btn-primary" id="sesBook">Book session →</button></p></div>' +
      '<div><h2>Upcoming (' + upcoming.length + ")</h2>" +
      (upcoming.map(sesCard).join("") || "<p>No upcoming sessions.</p>") +
      "<h2>Session log (" + logged.length + ")</h2>" +
      (logged.map(sesCard).join("") || "<p>No completed sessions yet.</p>") + "</div></div>";
    return { html: html, mount: function () {
      document.getElementById("sesBook").addEventListener("click", function () {
        var name = document.getElementById("sesName").value.trim();
        var date = document.getElementById("sesDate").value;
        if (!name || !date) { window.alert("Please enter student name and date."); return; }
        st.addSession({ student: name, topic: document.getElementById("sesTopic").value,
          date: date, time: document.getElementById("sesTime").value,
          goal: document.getElementById("sesGoal").value.trim(), notes: "" });
        location.hash = "#/sessions?r=" + Date.now();
      });
      document.querySelectorAll("[data-notes]").forEach(function (ta) {
        ta.addEventListener("change", function () {
          var id = ta.getAttribute("data-notes");
          st.state.sessions.forEach(function (x) { if (x.id === id) x.notes = ta.value; });
          st.save();
        });
      });
      document.querySelectorAll("[data-done]").forEach(function (b) {
        b.addEventListener("click", function () { st.toggleSession(b.getAttribute("data-done")); location.hash = "#/sessions?r=" + Date.now(); });
      });
      document.querySelectorAll("[data-del]").forEach(function (b) {
        b.addEventListener("click", function () {
          if (window.confirm("Delete this session?")) { st.deleteSession(b.getAttribute("data-del")); location.hash = "#/sessions?r=" + Date.now(); }
        });
      });
    } };
  }
  function lessonIdFor(topic) {
    var l = window.SAT_LESSONS.filter(function (x) { return x.title === topic; })[0];
    return l ? l.id : "algebra";
  }

  /* ---------------- PROGRESS ---------------- */
  function ProgressView() {
    var st = store();
    var s = st.stats(window.SAT_QUESTIONS);
    var bars = CATS.map(function (c) {
      var p = s.perCat[c];
      var pct = p.answered ? Math.round((p.correct / p.answered) * 100) : 0;
      return "<div><strong>" + esc(c) + "</strong> <span style='color:var(--text-muted)'>" + p.correct + "/" + p.answered + " (" + pct + "%)</span>" +
        '<div class="bar"><span style="width:' + pct + '%"></span></div></div>';
    }).join("");
    var atts = st.state.attempts.slice().reverse().map(function (a) {
      return "<tr><td>" + new Date(a.at).toLocaleString() + "</td><td>" + esc(a.title) + "</td><td>" + esc(a.mode) + "</td><td><strong>" + a.score + "/" + a.total + "</strong> (" + a.pct + "%)</td></tr>";
    }).join("");
    var html = '<div class="page-head"><div><h1>Progress</h1><p>Accuracy, attempts, lessons and sessions — all stored locally.</p></div>' +
      '<div class="tabs-meta"><button class="btn btn-danger btn-sm" id="resetAll">Reset all data</button></div></div>' +
      '<div class="stat-grid">' +
      '<div class="stat"><div class="num">' + s.answered + "/280</div><div class='lbl'>Questions answered</div></div>" +
      '<div class="stat"><div class="num">' + s.accuracy + '%</div><div class="lbl">Overall accuracy</div></div>' +
      '<div class="stat"><div class="num">' + st.state.lessonsDone.length + '/8</div><div class="lbl">Lessons completed</div></div>' +
      '<div class="stat"><div class="num">' + st.state.sessions.length + '</div><div class="lbl">1:1 sessions booked</div></div></div>' +
      '<div class="two-col" style="margin-top:1rem"><div class="panel"><h2>Accuracy by category</h2>' + bars + "</div>" +
      '<div class="panel"><h2>Homework attempts (' + st.state.attempts.length + ")</h2>" +
      (atts ? '<table class="clean"><tr><th>When</th><th>Set</th><th>Mode</th><th>Score</th></tr>' + atts + "</table>" : "<p>No attempts yet.</p>") + "</div></div>";
    return { html: html, mount: function () {
      document.getElementById("resetAll").addEventListener("click", function () {
        if (window.confirm("Erase all progress, attempts and sessions?")) { st.resetAll(); location.hash = "#/progress?r=" + Date.now(); }
      });
    } };
  }

  window.SATViews = Object.assign(window.SATViews || {}, {
    HomeworkView: HomeworkView, SessionsView: SessionsView, ProgressView: ProgressView,
    stopHomeworkTimer: function () { clearInterval(HW.timerId); HW.timerId = null; }
  });
})();
