/* ============================================================
   Имя Автора — интерактив сайта
   ============================================================ */
(function () {
  "use strict";

  /* --- год в подвале --- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* --- мобильное меню --- */
  var burger = document.getElementById("burger");
  var navLinks = document.getElementById("navLinks");
  if (burger && navLinks) {
    burger.addEventListener("click", function () {
      var open = navLinks.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", String(open));
    });
    // закрывать меню после клика по ссылке
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

  /* --- появление блоков при прокрутке --- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
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
  var sections = document.querySelectorAll("section[id]");
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
