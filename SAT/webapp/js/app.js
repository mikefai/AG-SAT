/* SATPrep Studio — hash router + boot. */
(function () {
  var app = document.getElementById("app");

  function parseHash() {
    var h = location.hash || "#/home";
    var m = h.match(/^#\/([a-z]+)(?:\/([^?]+))?(?:\?(.*))?$/);
    if (!m) return { route: "home", param: null, query: {} };
    var query = {};
    if (m[3]) m[3].split("&").forEach(function (kv) {
      var p = kv.split("=");
      query[decodeURIComponent(p[0])] = decodeURIComponent((p[1] || "").replace(/\+/g, " "));
    });
    return { route: m[1], param: m[2] ? decodeURIComponent(m[2]) : null, query: query };
  }

  function render() {
    if (window.SATViews.cleanupPracticeKeys) window.SATViews.cleanupPracticeKeys();
    if (window.SATViews.stopHomeworkTimer) window.SATViews.stopHomeworkTimer();
    var r = parseHash();
    var V = window.SATViews;
    var view;
    if (r.route === "home") view = V.HomeView();
    else if (r.route === "lessons") view = V.LessonsView();
    else if (r.route === "lesson") view = V.LessonDetailView(r.param);
    else if (r.route === "practice") view = V.PracticeView(r.query);
    else if (r.route === "homework") view = V.HomeworkView(r.query);
    else if (r.route === "sessions") view = V.SessionsView();
    else if (r.route === "progress") view = V.ProgressView();
    else view = V.HomeView();
    app.innerHTML = view.html;
    document.querySelectorAll("[data-nav]").forEach(function (a) {
      var key = a.getAttribute("data-nav");
      a.classList.toggle("active", key === r.route || (key === "lessons" && r.route === "lesson"));
    });
    if (view.mount) view.mount();
    window.scrollTo(0, 0);
    var titles = { home: "SATPrep Studio", lessons: "Lessons", lesson: "Lesson",
      practice: "Practice", homework: "Homework", sessions: "1:1 Sessions", progress: "Progress" };
    document.title = (titles[r.route] || "SATPrep Studio") + " — SATPrep Studio";
  }

  window.addEventListener("hashchange", render);
  window.SATTools.init();
  window.SATTools.showToolbar(true);
  if (!window.SAT_QUESTIONS || !window.SAT_LESSONS) {
    app.innerHTML = '<div class="panel"><h2>Data failed to load</h2><p>Make sure <code>data/questions.js</code> and <code>data/lessons.js</code> sit next to this page.</p></div>';
    return;
  }
  render();
})();
