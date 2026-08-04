// Ambient node mesh in the brand accent, and the mobile nav toggle.
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var cv = document.getElementById("mesh");
  if (!cv) return;
  var cx = cv.getContext("2d");
  var W, H, pts = [], N;

  function accent() {
    return getComputedStyle(document.documentElement)
      .getPropertyValue("--accent").trim();
  }
  function size() {
    W = cv.width = innerWidth * devicePixelRatio;
    H = cv.height = innerHeight * devicePixelRatio;
    cv.style.width = innerWidth + "px";
    cv.style.height = innerHeight + "px";
    N = Math.min(70, Math.floor(innerWidth / 22));
    pts = [];
    for (var i = 0; i < N; i++) {
      pts.push({
        x: Math.random() * W, y: Math.random() * H,
        vx: (Math.random() - .5) * .18 * devicePixelRatio,
        vy: (Math.random() - .5) * .18 * devicePixelRatio
      });
    }
  }
  addEventListener("resize", size);
  size();

  function frame() {
    cx.clearRect(0, 0, W, H);
    var col = accent(), link = 150 * devicePixelRatio;
    for (var i = 0; i < N; i++) {
      var p = pts[i];
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      cx.globalAlpha = .35;
      cx.fillStyle = col;
      cx.fillRect(p.x - 1, p.y - 1, 2.5, 2.5);
      for (var j = i + 1; j < N; j++) {
        var q = pts[j], dx = p.x - q.x, dy = p.y - q.y, d = dx * dx + dy * dy;
        if (d < link * link) {
          cx.globalAlpha = .07 * (1 - Math.sqrt(d) / link);
          cx.strokeStyle = col;
          cx.lineWidth = devicePixelRatio;
          cx.beginPath(); cx.moveTo(p.x, p.y); cx.lineTo(q.x, q.y); cx.stroke();
        }
      }
    }
    requestAnimationFrame(frame);
  }
  frame();
})();
