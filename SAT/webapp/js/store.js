/* SATPrep Studio — persistent state (localStorage). No globals leaked except window.SATStore. */
(function () {
  var KEY = "satprep_studio_v1";
  function blank() {
    return { answers: {}, flagged: [], lessonsDone: [], attempts: [], sessions: [] };
  }
  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return blank();
      var s = JSON.parse(raw);
      if (!s.answers) s.answers = {};
      if (!Array.isArray(s.flagged)) s.flagged = [];
      if (!Array.isArray(s.lessonsDone)) s.lessonsDone = [];
      if (!Array.isArray(s.attempts)) s.attempts = [];
      if (!Array.isArray(s.sessions)) s.sessions = [];
      return s;
    } catch (e) { return blank(); }
  }
  var state = load();
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
  }
  function uid(prefix) {
    return (prefix || "id") + "_" + Date.now().toString(36) + Math.floor(Math.random() * 1e4).toString(36);
  }
  window.SATStore = {
    state: state,
    save: save,
    uid: uid,
    recordAnswer: function (qid, pick, correct) {
      state.answers[qid] = { pick: pick, correct: !!correct, at: Date.now() };
      save();
    },
    toggleFlag: function (qid) {
      var i = state.flagged.indexOf(qid);
      if (i >= 0) state.flagged.splice(i, 1); else state.flagged.push(qid);
      save();
      return state.flagged.indexOf(qid) >= 0;
    },
    isFlagged: function (qid) { return state.flagged.indexOf(qid) >= 0; },
    completeLesson: function (id) {
      if (state.lessonsDone.indexOf(id) < 0) { state.lessonsDone.push(id); save(); }
    },
    addAttempt: function (a) { a.id = uid("att"); a.at = Date.now(); state.attempts.push(a); save(); return a; },
    addSession: function (s) { s.id = uid("ses"); s.done = false; state.sessions.push(s); save(); return s; },
    toggleSession: function (id) {
      var s = null;
      state.sessions.forEach(function (x) { if (x.id === id) { x.done = !x.done; s = x; } });
      save(); return s;
    },
    deleteSession: function (id) {
      state.sessions = state.sessions.filter(function (x) { return x.id !== id; });
      save();
    },
    resetAll: function () { state = blank(); save(); },
    stats: function (questions) {
      var ids = Object.keys(state.answers);
      var correct = ids.filter(function (k) { return state.answers[k] && state.answers[k].correct; }).length;
      var perCat = {};
      questions.forEach(function (q) {
        if (!perCat[q.category]) perCat[q.category] = { total: 0, answered: 0, correct: 0 };
        perCat[q.category].total += 1;
        var a = state.answers[q.id];
        if (a) { perCat[q.category].answered += 1; if (a.correct) perCat[q.category].correct += 1; }
      });
      return { answered: ids.length, correct: correct,
        accuracy: ids.length ? Math.round((correct / ids.length) * 100) : 0, perCat: perCat };
    }
  };
})();
