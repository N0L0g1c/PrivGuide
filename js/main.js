(() => {
  "use strict";

  const STORAGE_KEY = "privguide-checklist-v1";
  const LANG_KEY = "privguide-lang";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isTouch =
    window.matchMedia("(pointer: coarse)").matches ||
    "ontouchstart" in window ||
    navigator.maxTouchPoints > 0;

  if (isTouch) document.body.classList.add("touch-device");

  // Year
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  // ---------- Page loader (Hubtown-style) ----------
  const loader = document.getElementById("pageLoader");
  const loaderFill = document.getElementById("loaderFill");
  const loaderPct = document.getElementById("loaderPct");

  function finishLoader() {
    if (!loader) return;
    if (loaderFill) loaderFill.style.width = "100%";
    if (loaderPct) loaderPct.textContent = "100%";
    setTimeout(() => {
      loader.classList.add("is-done");
      document.body.classList.add("is-ready");
    }, reduceMotion ? 0 : 280);
  }

  if (loader && !reduceMotion) {
    let p = 0;
    const tick = () => {
      p += Math.random() * 14 + 6;
      if (p >= 100) {
        p = 100;
        if (loaderFill) loaderFill.style.width = "100%";
        if (loaderPct) loaderPct.textContent = "100%";
        finishLoader();
        return;
      }
      if (loaderFill) loaderFill.style.width = `${p}%`;
      if (loaderPct) loaderPct.textContent = `${Math.floor(p)}%`;
      setTimeout(tick, 60 + Math.random() * 80);
    };
    tick();
    window.addEventListener("load", () => {
      setTimeout(finishLoader, 200);
    });
  } else {
    finishLoader();
  }

  // ---------- Custom cursor ----------
  const cursor = document.getElementById("cursor");
  const cursorDot = document.getElementById("cursorDot");
  let mx = window.innerWidth / 2;
  let my = window.innerHeight / 2;
  let cx = mx;
  let cy = my;

  if (cursor && cursorDot && !isTouch && !reduceMotion) {
    cursor.classList.add("is-on");
    cursorDot.classList.add("is-on");

    window.addEventListener("mousemove", (e) => {
      mx = e.clientX;
      my = e.clientY;
      cursorDot.style.transform = `translate3d(${mx}px, ${my}px, 0)`;
      document.documentElement.style.setProperty("--cursor-x", `${mx}px`);
      document.documentElement.style.setProperty("--cursor-y", `${my}px`);
    });

    const loopCursor = () => {
      cx += (mx - cx) * 0.18;
      cy += (my - cy) * 0.18;
      cursor.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      requestAnimationFrame(loopCursor);
    };
    loopCursor();

    const hoverSel =
      "a, button, .filter-btn, .platform-tab, .check-item, .app-card, .path-card, .lang-btn, summary, .section-nav a";
    document.querySelectorAll(hoverSel).forEach((el) => {
      el.addEventListener("mouseenter", () => cursor.classList.add("is-hover"));
      el.addEventListener("mouseleave", () => cursor.classList.remove("is-hover"));
    });
    window.addEventListener("mousedown", () => cursor.classList.add("is-click"));
    window.addEventListener("mouseup", () => cursor.classList.remove("is-click"));
  }

  // ---------- Scroll progress + header ----------
  const progress = document.getElementById("scrollProgress");
  const header = document.querySelector(".site-header");
  const navDots = document.querySelectorAll(".section-nav a");

  function onScroll() {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    const pct = h > 0 ? (window.scrollY / h) * 100 : 0;
    if (progress) progress.style.width = `${pct}%`;
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 40);

    // Active section for side nav
    if (navDots.length) {
      let current = "";
      document.querySelectorAll("section[id], .hero").forEach((sec) => {
        const id = sec.id || "top";
        const top = sec.offsetTop - 120;
        if (window.scrollY >= top) current = id === "" ? "top" : id;
      });
      navDots.forEach((a) => {
        const href = (a.getAttribute("href") || "").replace("#", "") || "top";
        a.classList.toggle("is-active", href === current || (current === "" && href === "top"));
      });
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ---------- Scroll reveal ----------
  if (!reduceMotion && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) {
            en.target.classList.add("is-in");
            io.unobserve(en.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    document.querySelectorAll("[data-reveal]").forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll("[data-reveal]").forEach((el) => el.classList.add("is-in"));
  }

  // ---------- 3D tilt on cards ----------
  if (!isTouch && !reduceMotion) {
    document.querySelectorAll(".app-card, .path-card, .terminal, .life-card, .desk-card").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        const rx = (0.5 - y) * 10;
        const ry = (x - 0.5) * 12;
        card.style.transform = `perspective(900px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-4px)`;
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
      });
    });
  }

  // ---------- Magnetic buttons ----------
  if (!isTouch && !reduceMotion) {
    document.querySelectorAll(".btn-primary, .nav-cta").forEach((btn) => {
      btn.addEventListener("mousemove", (e) => {
        const r = btn.getBoundingClientRect();
        const x = e.clientX - r.left - r.width / 2;
        const y = e.clientY - r.top - r.height / 2;
        btn.style.transform = `translate(${x * 0.22}px, ${y * 0.28}px)`;
      });
      btn.addEventListener("mouseleave", () => {
        btn.style.transform = "";
      });
    });
  }

  // ---------- Particle / cyber field canvas ----------
  const canvas = document.getElementById("fx-canvas");
  if (canvas && !reduceMotion) {
    const ctx = canvas.getContext("2d");
    let w = 0;
    let h = 0;
    let particles = [];
    const COUNT = Math.min(70, Math.floor((window.innerWidth * window.innerHeight) / 22000));

    function resize() {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener("resize", resize);

    function spawn() {
      particles = Array.from({ length: COUNT }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
        r: Math.random() * 1.6 + 0.4,
        c: Math.random() > 0.5 ? "0,245,255" : "255,45,149",
      }));
    }
    spawn();

    let px = w / 2;
    let py = h / 2;
    window.addEventListener(
      "mousemove",
      (e) => {
        px = e.clientX;
        py = e.clientY;
      },
      { passive: true }
    );

    function frame() {
      ctx.clearRect(0, 0, w, h);
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        const dx = px - p.x;
        const dy = py - p.y;
        const dist = Math.hypot(dx, dy) || 1;
        if (dist < 160) {
          p.vx -= (dx / dist) * 0.02;
          p.vy -= (dy / dist) * 0.02;
        }
        p.x += p.vx;
        p.y += p.vy;
        p.vx *= 0.99;
        p.vy *= 0.99;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h;
        if (p.y > h) p.y = 0;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.c},0.7)`;
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
          const q = particles[j];
          const d = Math.hypot(p.x - q.x, p.y - q.y);
          if (d < 110) {
            ctx.strokeStyle = `rgba(${p.c},${0.12 * (1 - d / 110)})`;
            ctx.lineWidth = 0.6;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(frame);
    }
    frame();
  }

  // ---------- Language ----------
  const ALLOWED_LANGS = new Set(["en", "no", "es", "de", "fr"]);
  function normalizeLangTag(value) {
    if (typeof value !== "string") return null;
    const normalized = value.trim().toLowerCase();
    return ALLOWED_LANGS.has(normalized) ? normalized : null;
  }

  document.querySelectorAll(".lang-option").forEach((link) => {
    link.addEventListener("click", () => {
      const lang = normalizeLangTag(link.getAttribute("data-lang"));
      if (lang) {
        try {
          localStorage.setItem(LANG_KEY, lang);
        } catch {
          /* ignore */
        }
      }
    });
  });

  (function maybeSuggestLang() {
    try {
      if (sessionStorage.getItem("privguide-lang-checked")) return;
      sessionStorage.setItem("privguide-lang-checked", "1");
      if (document.documentElement.lang !== "en") return;
      const saved = normalizeLangTag(localStorage.getItem(LANG_KEY));
      if (saved && saved !== "en") {
        window.location.replace(`${encodeURIComponent(saved)}/index.html`);
      }
    } catch {
      /* ignore */
    }
  })();

  const langBtn = document.getElementById("langBtn");
  const langMenu = document.getElementById("langMenu");
  const langSwitcher = document.querySelector(".lang-switcher");
  if (langBtn && langMenu && langSwitcher) {
    langBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = langMenu.hasAttribute("hidden");
      if (open) {
        langMenu.removeAttribute("hidden");
        langBtn.setAttribute("aria-expanded", "true");
        langSwitcher.classList.add("open");
      } else {
        langMenu.setAttribute("hidden", "");
        langBtn.setAttribute("aria-expanded", "false");
        langSwitcher.classList.remove("open");
      }
    });
    document.addEventListener("click", () => {
      langMenu.setAttribute("hidden", "");
      langBtn.setAttribute("aria-expanded", "false");
      langSwitcher.classList.remove("open");
    });
    langMenu.addEventListener("click", (e) => e.stopPropagation());
  }

  // ---------- Mobile nav ----------
  const navToggle = document.getElementById("navToggle");
  const navLinks = document.getElementById("navLinks");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      const open = navLinks.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    navLinks.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navLinks.classList.remove("open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // ---------- App filters ----------
  const filterBtns = document.querySelectorAll(".filter-btn");
  const appCards = document.querySelectorAll(".app-card");
  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const filter = btn.dataset.filter || "all";
      filterBtns.forEach((b) => {
        b.classList.remove("active");
        b.setAttribute("aria-selected", "false");
      });
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      appCards.forEach((card) => {
        const cat = card.dataset.cat;
        const isOurs = card.dataset.ours === "1";
        const show =
          filter === "all" ||
          cat === filter ||
          (filter === "ours" && isOurs);
        card.classList.toggle("is-hidden", !show);
        if (show && !reduceMotion) {
          card.style.animation = "none";
          // reflow
          void card.offsetWidth;
          card.style.animation = "";
        }
      });
    });
  });

  // ---------- Platform tabs ----------
  const platformTabs = document.querySelectorAll(".platform-tab");
  const panels = {
    android: document.getElementById("panel-android"),
    ios: document.getElementById("panel-ios"),
  };
  platformTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const platform = tab.dataset.platform;
      if (!platform || !panels[platform]) return;
      platformTabs.forEach((t) => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");
      Object.entries(panels).forEach(([key, panel]) => {
        if (!panel) return;
        const active = key === platform;
        panel.classList.toggle("active", active);
        panel.hidden = !active;
      });
    });
  });

  // ---------- Checklist ----------
  const checkboxes = document.querySelectorAll("#checklist input[type='checkbox']");
  const progressBar = document.getElementById("progressBar");
  const progressText = document.getElementById("progressText");
  const progressCount = document.getElementById("progressCount");
  const resetBtn = document.getElementById("resetChecklist");

  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch {
      return {};
    }
  }
  function saveState(state) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch {
      /* ignore */
    }
  }
  function updateProgress() {
    const total = checkboxes.length;
    let done = 0;
    checkboxes.forEach((cb) => {
      if (cb.checked) done += 1;
    });
    const pct = total ? Math.round((done / total) * 100) : 0;
    if (progressBar) progressBar.style.width = `${pct}%`;
    if (progressText) progressText.textContent = String(pct);
    if (progressCount) progressCount.textContent = `${done} / ${total}`;
  }

  const state = loadState();
  checkboxes.forEach((cb) => {
    const id = cb.dataset.id;
    if (id && state[id]) cb.checked = true;
    cb.addEventListener("change", () => {
      const next = loadState();
      if (id) next[id] = cb.checked;
      saveState(next);
      updateProgress();
    });
  });
  updateProgress();

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      const msg =
        resetBtn.getAttribute("data-confirm") ||
        "Reset all checklist progress on this device?";
      if (!confirm(msg)) return;
      checkboxes.forEach((cb) => {
        cb.checked = false;
      });
      saveState({});
      updateProgress();
    });
  }

  document.querySelectorAll(".path-link[data-level]").forEach((link) => {
    link.addEventListener("click", () => {
      const level = link.dataset.level;
      const group = document.querySelector(`.check-group[data-level="${level}"]`);
      if (!group) return;
      group.style.outline = "1px solid rgba(0, 245, 255, 0.5)";
      group.style.boxShadow = "0 0 0 4px rgba(255, 45, 149, 0.12)";
      setTimeout(() => {
        group.style.outline = "";
        group.style.boxShadow = "";
      }, 2200);
    });
  });

  const donateRoot = document.getElementById("donate");
  const copiedLabel =
    (donateRoot && donateRoot.dataset.copied) || "Copied";

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
  }

  document.querySelectorAll(".donate-copy[data-copy]").forEach((btn) => {
    const original = btn.textContent;
    btn.addEventListener("click", async () => {
      const value = btn.getAttribute("data-copy") || "";
      if (!value) return;
      try {
        await copyText(value);
        btn.textContent = copiedLabel;
        btn.classList.add("is-copied");
        window.setTimeout(() => {
          btn.textContent = original;
          btn.classList.remove("is-copied");
        }, 1600);
      } catch (_) {
        /* clipboard blocked — user can still select the address */
      }
    });
  });
})();
