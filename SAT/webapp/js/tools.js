/* SATPrep Studio — study tools: theme, highlighter, pen, clear. */
(function () {
  var penOn = false, ctx = null, drawing = false;

  function initTheme() {
    try {
      if (localStorage.getItem("satprep_theme") === "dark") {
        document.documentElement.setAttribute("data-theme", "dark");
      }
    } catch (e) {}
    var btn = document.getElementById("themeToggle");
    if (btn) btn.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme");
      var next = cur === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("satprep_theme", next); } catch (e) {}
    });
  }

  function showToolbar(show) {
    var tb = document.getElementById("toolbar");
    if (tb) tb.hidden = !show;
  }

  function currentRange() {
    var sel = window.getSelection();
    if (!sel || sel.rangeCount === 0 || sel.isCollapsed) return null;
    var range = sel.getRangeAt(0);
    var app = document.getElementById("app");
    if (!app.contains(range.commonAncestorContainer)) return null;
    return range;
  }

  function applyHighlight() {
    var range = currentRange();
    if (!range) return;
    try {
      var mark = document.createElement("mark");
      mark.className = "sat-hl";
      mark.title = "Click to remove highlight";
      mark.addEventListener("click", function () {
        var parent = mark.parentNode;
        while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
        parent.removeChild(mark);
      });
      range.surroundContents(mark);
      window.getSelection().removeAllRanges();
    } catch (e) {
      // Fallback: wrap each text node in the range
      try {
        var frag = range.extractContents();
        var mark2 = document.createElement("mark");
        mark2.className = "sat-hl";
        mark2.appendChild(frag);
        range.insertNode(mark2);
        window.getSelection().removeAllRanges();
      } catch (e2) {}
    }
    hideTip();
  }

  function hideTip() { var t = document.getElementById("hlTip"); if (t) t.hidden = true; }

  function initHighlight() {
    document.addEventListener("mouseup", function () {
      var tip = document.getElementById("hlTip");
      if (!tip) return;
      var hlBtn = document.getElementById("toolHighlight");
      if (!hlBtn || !hlBtn.classList.contains("on")) { hideTip(); return; }
      var range = currentRange();
      if (!range) { hideTip(); return; }
      var rect = range.getBoundingClientRect();
      tip.style.left = Math.min(window.innerWidth - 200, rect.left + window.scrollX) + "px";
      tip.style.top = (rect.bottom + window.scrollY + 6) + "px";
      tip.hidden = false;
    });
    var apply = document.getElementById("hlApply");
    if (apply) apply.addEventListener("click", applyHighlight);
    document.addEventListener("keyup", function (e) { if (e.key === "Escape") hideTip(); });
  }

  function sizeCanvas(canvas) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  function initPen() {
    var canvas = document.getElementById("penCanvas");
    if (!canvas) return;
    ctx = canvas.getContext("2d");
    ctx.strokeStyle = "#e11d48";
    ctx.lineWidth = 2.5;
    ctx.lineCap = "round";
    function pos(e) {
      if (e.touches && e.touches[0]) return { x: e.touches[0].clientX, y: e.touches[0].clientY };
      return { x: e.clientX, y: e.clientY };
    }
    canvas.addEventListener("pointerdown", function (e) {
      if (!penOn) return;
      drawing = true; ctx.beginPath();
      var p = pos(e); ctx.moveTo(p.x, p.y);
      e.preventDefault();
    });
    canvas.addEventListener("pointermove", function (e) {
      if (!penOn || !drawing) return;
      var p = pos(e); ctx.lineTo(p.x, p.y); ctx.stroke();
    });
    ["pointerup", "pointerleave"].forEach(function (ev) {
      canvas.addEventListener(ev, function () { drawing = false; });
    });
    window.addEventListener("resize", function () {
      if (!canvas.hidden) {
        var img = ctx.getImageData(0, 0, canvas.width, canvas.height);
        sizeCanvas(canvas);
        try { ctx.putImageData(img, 0, 0); } catch (e) {}
      }
    });
  }

  function initToolbar() {
    var hl = document.getElementById("toolHighlight");
    var pen = document.getElementById("toolPen");
    var clear = document.getElementById("toolClear");
    var canvas = document.getElementById("penCanvas");
    if (hl) hl.addEventListener("click", function () {
      hl.classList.toggle("on");
      if (!hl.classList.contains("on")) hideTip();
    });
    if (pen) pen.addEventListener("click", function () {
      penOn = !penOn;
      pen.classList.toggle("on", penOn);
      if (penOn) { sizeCanvas(canvas); canvas.hidden = false; }
      else { canvas.hidden = true; drawing = false; }
    });
    if (clear) clear.addEventListener("click", function () {
      document.querySelectorAll("mark.sat-hl").forEach(function (m) {
        var p = m.parentNode;
        while (m.firstChild) p.insertBefore(m.firstChild, m);
        p.removeChild(m);
      });
      if (ctx && canvas) { ctx.clearRect(0, 0, canvas.width, canvas.height); }
      if (pen) { pen.classList.remove("on"); penOn = false; }
      if (canvas) canvas.hidden = true;
      hideTip();
    });
  }

  window.SATTools = {
    init: function () { initTheme(); initToolbar(); initHighlight(); initPen(); },
    showToolbar: showToolbar,
    esc: function (s) {
      return String(s == null ? "" : s)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
  };
})();
