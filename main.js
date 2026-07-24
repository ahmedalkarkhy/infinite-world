/* Infinite World - nav, mobile menu, scroll reveal, hero parallax */
(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const nav = document.getElementById("nav");
  const burger = document.getElementById("burger");
  const links = document.getElementById("navLinks");

  // nav shrink on scroll
  const onScroll = () => {
    if (nav) nav.classList.toggle("shrink", window.scrollY > 40);
    // hero watermark parallax
    if (!reduce) {
      const mark = document.querySelector(".hero-mark");
      if (mark)
        mark.style.transform = `translateY(calc(-50% + ${window.scrollY * 0.06}px))`;
    }
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // mobile menu
  if (burger && links) {
    const close = () => {
      links.classList.remove("open");
      burger.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    };
    burger.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      burger.classList.toggle("open", open);
      burger.setAttribute("aria-expanded", String(open));
    });
    links
      .querySelectorAll("a")
      .forEach((a) => a.addEventListener("click", close));
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
