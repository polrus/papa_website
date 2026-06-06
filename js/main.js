/* ============================================================
   Имя Автора — интерактив сайта
   ============================================================ */

/* Read & clear the portal flag ONCE, before any IIFE runs.
   fromPortal === true  when we just navigated here via the
   iframe-portal switcher (should skip all intro animations).
   inPortalFrame === true  when this script runs inside the
   hidden iframe (page must look fully rendered right away).   */
var fromPortal    = !!sessionStorage.getItem("sw_portal");
var inPortalFrame = (window.self !== window.top);
sessionStorage.removeItem("sw_portal");

/* Convenience: skip ALL enter-animations in both cases */
var skipAnims = fromPortal || inPortalFrame;

(function () {
  "use strict";

  /* --- год в подвале --- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* --- мобильное меню --- */
  var burger   = document.getElementById("burger");
  var navLinks = document.getElementById("navLinks");
  if (burger && navLinks) {
    burger.addEventListener("click", function () {
      var open = navLinks.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", String(open));
    });
    navLinks.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        navLinks.classList.remove("is-open");
        burger.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* --- тень на навбаре при прокрутке --- */
  var nav = document.getElementById("nav");
  function onScroll() {
    if (!nav) return;
    nav.classList.toggle("is-scrolled", window.scrollY > 10);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* --- появление блоков при прокрутке ---
   Portal arrivals / iframe: make everything visible instantly,
   no IntersectionObserver, no CSS transitions needed.         */
  var reveals = document.querySelectorAll(".reveal");
  if (skipAnims) {
    // Гарантированно отключаем любые анимации появления
    document.body.classList.add('skip-reveal');
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  } else if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* --- видео-обложки: статичны, оживают при наведении --- */
  var coverVideos = document.querySelectorAll(".cover-video");
  coverVideos.forEach(function (video) {
    // зона наведения — карточка книги или сама обложка
    var hot = video.closest(".book") ||
              video.closest(".card") ||
              video.closest(".bookhero__cover") ||
              video.parentElement;
    if (!hot) return;

    function play() {
      var p = video.play();
      if (p && typeof p.catch === "function") p.catch(function () {});
    }
    function stop() {
      video.pause();
      video.currentTime = 0;
    }

    hot.addEventListener("mouseenter", play);
    hot.addEventListener("mouseleave", stop);
    // на сенсорных экранах нет наведения — короткий показ по касанию
    hot.addEventListener("touchstart", play, { passive: true });
  });

  /* --- почта автора: собираем адрес в рантайме, чтобы он не светился
         в разметке/во всплывающей подсказке у кнопки «Написать автору» --- */
  var mailEls = document.querySelectorAll("[data-mail]");
  mailEls.forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      var user = "vrusin1", domain = "rambler.ru";
      window.location.href = "mailto:" + user + "@" + domain;
    });
  });

  /* --- подсветка активного пункта меню --- */
  var sections   = document.querySelectorAll("section[id]");
  var navAnchors = navLinks ? navLinks.querySelectorAll("a") : [];
  if (sections.length && navAnchors.length && "IntersectionObserver" in window) {
    var spy = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var id = entry.target.getAttribute("id");
          navAnchors.forEach(function (a) {
            a.classList.toggle("is-active", a.getAttribute("href") === "#" + id);
          });
        });
      },
      { threshold: 0.5 }
    );
    sections.forEach(function (s) { spy.observe(s); });
  }
})();

/* ============================================================
   AUTHOR SWITCHER + PAGE TRANSITION  (iframe portal reveal)

   LEAVE  — destination page loads in a hidden <iframe>;
            clip-path circle expands from the button corner,
            revealing the real destination site underneath.
            Once the circle covers the viewport we navigate.

   ENTER  — body fades in from opacity:0  UNLESS skipAnims
            is true (portal navigation or inside iframe),
            in which case page appears instantly — it was
            already fully visible inside the expanding circle.
   ============================================================ */
(function () {
  var author  = document.body.getAttribute("data-author") || "rusin";
  var inBooks = window.location.pathname.replace(/\\/g, "/").indexOf("/books/") !== -1;
  var depth   = inBooks ? "../" : "./";

  var destUrl  = author === "rusin" ? depth + "boroma.html" : depth + "index.html";
  var destIcon = author === "rusin" ? "🌙" : "☀️";
  var destName = author === "rusin" ? "Денис&nbsp;Борома" : "Владимир&nbsp;Русин";

  /* ---- inject switcher button ---- */
  var btn = document.createElement("button");
  btn.className = "switcher-btn";
  btn.setAttribute("aria-label", "Перейти к другому автору");
  btn.innerHTML =
    '<span class="switcher-btn__icon">' + destIcon + '</span>' +
    '<span class="switcher-btn__text">' + destName + '</span>' +
    '<span class="switcher-btn__arrow">→</span>';
  document.body.appendChild(btn);

  /* ---- PAGE ENTER: body fade-in (normal visits only) ---- */
  if (!skipAnims) {
    document.body.style.opacity = "0";
    setTimeout(function () {
      document.body.style.transition = "opacity .72s cubic-bezier(.4,0,.2,1)";
      document.body.style.opacity    = "1";
      setTimeout(function () {
        document.body.style.transition = "";
        document.body.style.opacity    = "";
      }, 800);
    }, 60);
  }

  /* ---- PAGE LEAVE: iframe portal ---- */
  btn.addEventListener("click", function () {
    btn.style.pointerEvents = "none";

    var iframe = document.createElement("iframe");
    iframe.setAttribute("src", destUrl);
    iframe.setAttribute("scrolling", "no");
    iframe.style.cssText = [
      "position:fixed", "inset:0",
      "width:100%", "height:100%",
      "border:none", "z-index:998",
      "clip-path:circle(0% at calc(100% - 38px) calc(100% - 38px))",
      "pointer-events:none"
    ].join(";");
    document.body.appendChild(iframe);

    var revealed = false;
    function expandPortal() {
      if (revealed) return;
      revealed = true;
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          iframe.style.transition =
            "clip-path .68s cubic-bezier(.4,0,.2,1)";
          iframe.style.clipPath =
            "circle(150% at calc(100% - 38px) calc(100% - 38px))";

          setTimeout(function () {
            sessionStorage.setItem("sw_portal", "1");
            window.location.href = destUrl;
          }, 720);
        });
      });
    }

    iframe.onload = expandPortal;
    setTimeout(expandPortal, 1400);  /* safety fallback */
  });
})();
