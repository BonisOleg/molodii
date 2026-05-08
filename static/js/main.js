/* main.js — mobile nav, scroll reveal, header state, anchor navigation */

(function () {
  "use strict";

  const body = document.body;

  /* ---------- Mobile navigation ---------- */

  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");

  function setNavOpen(open) {
    body.classList.toggle("is-nav-open", open);
    if (toggle) toggle.setAttribute("aria-expanded", String(open));
    if (nav) nav.setAttribute("aria-hidden", String(!open));
  }

  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = !body.classList.contains("is-nav-open");
      setNavOpen(open);
    });

    nav.addEventListener("click", (event) => {
      const link = event.target.closest("a");
      if (link) setNavOpen(false);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && body.classList.contains("is-nav-open")) {
        setNavOpen(false);
        toggle.focus();
      }
    });

    document.addEventListener("click", (event) => {
      if (!body.classList.contains("is-nav-open")) return;
      if (event.target.closest(".header") || event.target.closest("[data-nav]")) return;
      setNavOpen(false);
    });

    const desktopQuery = window.matchMedia("(min-width: 960px)");
    const handleQuery = (event) => {
      if (event.matches) setNavOpen(false);
    };
    if (desktopQuery.addEventListener) {
      desktopQuery.addEventListener("change", handleQuery);
    } else if (desktopQuery.addListener) {
      desktopQuery.addListener(handleQuery);
    }
  }

  /* ---------- Header scroll state ---------- */

  const header = document.querySelector(".header");
  if (header) {
    let ticking = false;
    const updateHeader = () => {
      const y = window.scrollY || window.pageYOffset || 0;
      header.classList.toggle("is-scrolled", y > 12);
      ticking = false;
    };

    window.addEventListener(
      "scroll",
      () => {
        if (!ticking) {
          window.requestAnimationFrame(updateHeader);
          ticking = true;
        }
      },
      { passive: true }
    );
    updateHeader();
  }

  /* ---------- Scroll reveal ---------- */

  const reveals = document.querySelectorAll("[data-reveal]");
  if (reveals.length) {
    if (
      "IntersectionObserver" in window &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-revealed");
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
      );

      reveals.forEach((el, idx) => {
        if (!el.style.getPropertyValue("--reveal-delay")) {
          const groupIdx = el.hasAttribute("data-reveal-group") ? idx % 6 : 0;
          el.style.setProperty("--reveal-delay", `${groupIdx * 80}ms`);
        }
        observer.observe(el);
      });
    } else {
      reveals.forEach((el) => el.classList.add("is-revealed"));
    }
  }

  /* ---------- Anchor navigation: active state on scroll ---------- */

  const anchorNavLinks = document.querySelectorAll("[data-anchor-nav]");
  if (anchorNavLinks.length) {
    const pairs = [];

    anchorNavLinks.forEach((link) => {
      const href = link.getAttribute("href");
      if (href && href.startsWith("#")) {
        const section = document.getElementById(href.slice(1));
        if (section) pairs.push({ section, link });
      }
    });

    if (pairs.length) {
      const headerHeight =
        parseInt(
          getComputedStyle(document.documentElement).getPropertyValue("--header-h"),
          10
        ) || 68;

      const updateActiveLink = () => {
        const scrollY = window.scrollY + headerHeight + 24;
        let activeLink = null;

        pairs.forEach(({ section, link }) => {
          if (section.offsetTop <= scrollY) {
            activeLink = link;
          }
        });

        pairs.forEach(({ link }) => {
          link.classList.toggle("is-active", link === activeLink);
        });
      };

      window.addEventListener("scroll", updateActiveLink, { passive: true });
      updateActiveLink();
    }
  }
})();
