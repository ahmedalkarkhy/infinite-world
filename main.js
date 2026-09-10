/* Infinite World - nav, mobile menu, scroll reveal, hero parallax */
(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const nav = document.getElementById("nav");
  const burger = document.getElementById("burger");
  const links = document.getElementById("navLinks");

  // nav shrink on scroll
  const onScroll = () => {
    if (nav) nav.classList.toggle("shrink", window.scrollY > 40);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // hero mark: small tilt towards the pointer, so the plate feels physical
  const mark = document.getElementById("heroMark");
  const art = mark && mark.querySelector(".mark-art");
  if (mark && art && !reduce) {
    mark.addEventListener("pointermove", (e) => {
      const r = mark.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      art.style.transform = `rotateY(${x * 11}deg) rotateX(${-y * 9}deg)`;
    });
    mark.addEventListener("pointerleave", () => {
      art.style.transform = "";
    });
  }

  /* Mega menu by business area, plus the mobile drawer that contains it.
     On a pointer device the panels also open on hover; on touch and by
     keyboard the trigger is a plain toggle button. */
  const triggers = [...document.querySelectorAll(".mega-trigger")];
  const panelOf = (t) => document.getElementById(t.getAttribute("aria-controls"));

  const closeMega = (except) => {
    triggers.forEach((t) => {
      if (t === except) return;
      t.setAttribute("aria-expanded", "false");
      const panel = panelOf(t);
      if (panel) panel.hidden = true;
    });
  };

  const openMega = (t) => {
    closeMega(t);
    t.setAttribute("aria-expanded", "true");
    const panel = panelOf(t);
    if (panel) panel.hidden = false;
  };

  const isOpen = (t) => t.getAttribute("aria-expanded") === "true";

  if (burger && links) {
    const closeDrawer = () => {
      links.classList.remove("open");
      burger.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
      closeMega();
    };
    burger.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      burger.classList.toggle("open", open);
      burger.setAttribute("aria-expanded", String(open));
      if (!open) closeMega();
    });
    links.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => {
        closeDrawer();
      }),
    );
  }

  triggers.forEach((t) => {
    t.addEventListener("click", () => {
      if (isOpen(t)) closeMega();
      else openMega(t);
    });
  });

  const hoverable = window.matchMedia("(hover: hover) and (min-width: 641px)");
  if (nav) {
    let timer;
    triggers.forEach((t) => {
      const item = t.closest(".nav-item");
      if (!item) return;
      item.addEventListener("pointerenter", () => {
        if (!hoverable.matches) return;
        clearTimeout(timer);
        timer = setTimeout(() => openMega(t), 90);
      });
    });
    nav.addEventListener("pointerleave", () => {
      if (!hoverable.matches) return;
      clearTimeout(timer);
      timer = setTimeout(() => closeMega(), 180);
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape") return;
    const open = triggers.find(isOpen);
    if (!open) return;
    closeMega();
    open.focus();
  });

  document.addEventListener("click", (e) => {
    if (nav && !nav.contains(e.target)) closeMega();
  });

  // A panel pinned over content the reader has already scrolled past is noise
  window.addEventListener(
    "scroll",
    () => {
      if (hoverable.matches) closeMega();
    },
    { passive: true },
  );

  // stagger: every card in a group carries its own position in the queue
  document
    .querySelectorAll(".card, .cap, .kpi, .screen, .pillar, .figure, .child")
    .forEach((el) => {
      el.classList.add("reveal-item");
      const siblings = [...el.parentElement.children].filter((n) =>
        n.classList.contains("reveal-item"),
      );
      el.style.setProperty("--i", siblings.indexOf(el));
    });

  /* Numbers roll up from zero when they arrive. Years and ordinals are left
     alone: counting to 2040 reads as a bug, not as motion. */
  const COUNTABLE = /^([+]?)(\d+)(%?)$/;

  const countUp = (el) => {
    const m = el.textContent.trim().match(COUNTABLE);
    if (!m) return;
    const target = Number(m[2]);
    if (target > 200) return;
    const [, sign, , suffix] = m;
    const started = performance.now();
    const run = (now) => {
      const p = Math.min((now - started) / 900, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = sign + Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(run);
    };
    requestAnimationFrame(run);
  };

  /* An arc is drawn only where the number really is a percentage, so the
     graphic always encodes something true. */
  const addMeter = (el) => {
    const m = el.textContent.trim().match(COUNTABLE);
    if (!m || m[3] !== "%") return null;
    const pct = Math.min(Number(m[2]), 100);
    const NS = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "meter");
    svg.setAttribute("viewBox", "0 0 46 46");
    svg.setAttribute("aria-hidden", "true");
    const ring = (cls) => {
      const c = document.createElementNS(NS, "circle");
      c.setAttribute("class", cls);
      c.setAttribute("cx", "23");
      c.setAttribute("cy", "23");
      c.setAttribute("r", "19");
      svg.appendChild(c);
      return c;
    };
    ring("bg");
    const fg = ring("fg");
    el.parentElement.insertBefore(svg, el);
    const circumference = 2 * Math.PI * 19;
    return () => {
      fg.style.strokeDasharray = `${(circumference * pct) / 100} ${circumference}`;
    };
  };

  const numbers = [...document.querySelectorAll(".kpi .n, .figure .fn")];
  const draws = new Map();
  // Meters only outside the product panel: a ring in there would push one card
  // taller than the rest and break the mock interface.
  document.querySelectorAll(".figure .fn").forEach((el) => {
    const draw = addMeter(el);
    if (draw) draws.set(el, draw);
  });

  if (reduce || !("IntersectionObserver" in window)) {
    draws.forEach((draw) => draw());
  } else {
    const numObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          countUp(e.target);
          const draw = draws.get(e.target);
          if (draw) draw();
          numObserver.unobserve(e.target);
        });
      },
      { threshold: 0.6 },
    );
    numbers.forEach((el) => numObserver.observe(el));
  }

  // scroll reveal
  const sections = document.querySelectorAll(".section");
  if (reduce || !("IntersectionObserver" in window)) {
    sections.forEach((s) => s.classList.add("in"));
  } else {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("in");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" },
    );
    sections.forEach((s) => io.observe(s));
  }
})();
