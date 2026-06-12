from collections import OrderedDict

SECTION_INFO = OrderedDict([
    ("ИСТОРИЯ СВЕТЛЫХ ВРЕМЕН", {
        "title": "История светлых времён",
        "slug": "istoriya-svetlyh-vremen",
        "desc": "Оглядываясь в прошлое, можно ощутить яркую вспышку в начале времен, которая озаряет особое измерение, живущее своей собственной жизнью. Вдруг консервный нож разрезает привычную реальность, и новая, всегда бывшая рядом действительность заполняет всё вокруг, заставляя нас забыть себя и безрассудно броситься ей навстречу.",
        "emoji": "🥫",
        "cover_class": "cover--1",
    }),
    ("ЦИКЛ", {
        "title": "Цикл «И пришёл Мессия»",
        "slug": "cikl",
        "desc": "Философская притча о непостижимости искупительной жертвы и быстроте человеческой памяти, написанная в стилистике, сочетающей библейский пафос с ироническим налётом современности.",
        "emoji": "🕯️",
        "cover_class": "cover--3",
    }),
    ("МОСКОВСКИЕ ЭТЮДЫ", {
        "title": "Московские этюды",
        "slug": "moskovskie-etyudy",
        "desc": "Магический реализм, знакомый каждому москвичу.",
        "emoji": "🌆",
        "cover_class": "cover--4",
    }),
    ("БАЛЛАДЫ", {
        "title": "Баллада о Плане",
        "slug": "ballady",
        "desc": "Исповедально-галлюцинаторная поэма про ссылку в место, забытое Богом, и прозябание среди кухонной грязи, блатного сленга и ЛАНГОЛЬЕРОВ, где действительность смешивается с безобразными видениями. Позор непальцу.",
        "emoji": "🌌",
        "cover_class": "cover--2",
    }),
])

# ---------- Единый тёмный стиль (как в boroma.html + улучшения) ----------
BOROMA_CSS = """
    #hero {
      scroll-margin-top: 70px;
    }
    body, body * { font-family: 'Cormorant Garamond', serif !important; }
    .card__emoji, .book__emoji, .float, .chip, .btn, .nav__burger span { font-family: inherit !important; }
    
    body {
      --ink: #000000;
      --ash: #CCCCCC;
      --ghost-white: #FFFFFF;
      background-color: var(--ink);
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.15'/%3E%3C/svg%3E");
      background-attachment: fixed;
      color: var(--ash);
      overflow-x: hidden;
    }

    .nav { 
      background: var(--ink); 
      border-bottom: 1px dashed #333;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .nav__inner {
      max-width: 1120px;
      margin: 0 auto;
      padding: 14px 22px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .nav__logo {
      color: var(--ash) !important;
      text-transform: uppercase;
      letter-spacing: 2px;
      text-decoration: none;
      line-height: 1;
      display: inline-block;
    }
    .nav__links {
      display: flex;
      gap: 48px;
      align-items: center;
    }
    .nav__links a {
      color: var(--ash) !important;
      text-transform: uppercase;
      letter-spacing: 2px;
      text-decoration: none;
      position: relative;
      padding-bottom: 4px;
      transition: color 0.3s ease;
      line-height: 1;
    }
    .nav__links a::after {
      content: "";
      position: absolute;
      left: 0;
      bottom: -2px;
      width: 0;
      height: 0.5px;
      background-color: var(--ghost-white);
      transition: width 0.25s ease;
    }
    .nav__links a.is-active::after {
      width: 100%;
    }
    .nav__links a:hover::after {
      width: 100%;
    }
    .nav__links a:hover {
      color: var(--ghost-white) !important;
      text-shadow: 0 0 8px rgba(255,255,255,0.7);
    }

    .switcher-btn {
      display: inline-grid;
      place-items: center;
      width: 36px;
      height: 36px;
      background: #f4f4f4;
      color: #111;
      border: 1px solid #aaa;
      border-radius: 50%;
      cursor: pointer;
      transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
      margin-right: 22px;
      box-shadow: 0 0 8px rgba(255, 255, 255, 0.7), 0 2px 6px rgba(0,0,0,0.2);
    }
    .switcher-btn:hover {
      background: #ffffff;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .switcher-btn:active { transform: translateY(0); }
    .switcher-btn__icon svg {
      stroke-width: 1.8;
    }

    .hero__title { 
      background: none;
      color: var(--ghost-white) !important;
      font-size: 4.5rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: -1px;
      text-shadow: 0 0 10px rgba(255,255,255,0.5), 2px 2px 0px #000;
    }
    .hero__eyebrow {
      color: #666 !important;
      text-transform: uppercase;
      letter-spacing: 4px;
    }
    .hero__tagline {
      font-style: italic;
      color: var(--ash);
      border-left: 3px double #444;
      padding-left: 15px;
    }

    .btn {
      display: inline-block;
      padding: 12px 28px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      border-radius: 0px;
      transition: all 0.25s ease;
      cursor: pointer;
      text-decoration: none;
      border: none;
      background: transparent;
    }
    .btn--primary {
      background: linear-gradient(135deg, #f0f0f0, #ffffff);
      color: #000 !important;
      box-shadow: 4px 4px 0 #222;
      border: 1px solid #aaa;
    }
    .btn--primary:hover {
      transform: translate(-2px, -2px);
      box-shadow: 6px 6px 0 #111;
      background: linear-gradient(135deg, #ffffff, #e0e0e0);
    }
    .btn--primary:active {
      transform: translate(2px, 2px);
      box-shadow: 2px 2px 0 #222;
    }
    .btn--ghost {
      background: transparent;
      color: var(--ghost-white) !important;
      border: 1px solid var(--ghost-white);
      box-shadow: none;
    }
    .btn--ghost:hover {
      background: rgba(255,255,255,0.12);
      transform: translateY(-2px);
      box-shadow: 0 6px 14px rgba(0,0,0,0.3);
    }
    .btn--ghost:active {
      transform: translateY(0);
    }

    .section__kicker { color: #555 !important; font-weight: bold; text-transform: uppercase; }
    .section__title { color: var(--ghost-white) !important; }
    
    .books-list { max-width: 880px; margin: 0 auto; }
    .book-item { 
      display: flex; gap: 32px; margin-bottom: 48px; align-items: center; 
      background: #080808 !important; 
      border: 1px solid #1a1a1a;
      border-radius: 0px !important; 
      padding: 24px; 
      box-shadow: 0 0 0 1px #000, 5px 5px 0px #111;
      justify-content: space-between;
      width: 60%; margin-left: auto; margin-right: auto;
    }
    .book-item:hover { border-color: #444; box-shadow: 0 0 15px rgba(255,255,255,0.1); }
    .book-item__info { flex: 1; }
    .book-item__title { font-size: 1.8rem; font-weight: 700; color: var(--ghost-white); margin-bottom: 8px; }
    .book-item__desc { color: #aeaeae !important; margin-bottom: 20px; }
    .book-item__cover { 
      flex: 0 0 160px; aspect-ratio: 3/4; border-radius: 0px !important; 
      filter: grayscale(100%) contrast(200%);
      background-color: #111 !important; 
      border: 2px solid #333;
      box-shadow: inset 0 0 20px #000;
      display: flex; align-items: center; justify-content: center;
      font-size: 3rem;
    }
    .book__emoji { 
      font-size: inherit;
      filter: none;
      opacity: 1;
    }

    .bookhero {
      max-width: 1120px; margin: 0 auto; padding: 40px 22px;
    }
    .bookhero__inner {
      display: grid; grid-template-columns: 230px 1fr; gap: 40px; align-items: center;
    }
    .bookhero__cover {
      aspect-ratio: 3/4; border-radius: 0px !important;
      background-color: #111; border: 2px solid #333;
      display: flex; align-items: center; justify-content: center;
      font-size: 3rem; filter: grayscale(100%) contrast(200%);
    }
    .bookhero__text .back-link {
      display: inline-block; color: #aeaeae; margin-bottom: 10px;
    }
    .bookhero__text .back-link:hover { color: var(--ghost-white); }
    .bookhero__desc { color: #aeaeae; max-width: 52ch; margin: 12px 0 22px; font-size: 1.05rem; }

    .grid {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 30px;
      max-width: 1120px; margin: 0 auto; padding: 0 22px;
    }
    .section .grid {
      margin-bottom: 48px;
    }
    .card {
      background: #080808; border: 1px solid #1a1a1a; border-radius: 0px;
      padding: 0; overflow: hidden; transition: all 0.2s;
    }
    .card:hover { border-color: #444; box-shadow: 0 0 12px rgba(255,255,255,0.08); transform: translateY(-2px); }
    .card__cover {
      aspect-ratio: 3/4; display: flex; align-items: center; justify-content: center;
      background-color: #111; border-bottom: 1px solid #222;
      font-size: 3rem; filter: grayscale(100%) contrast(200%);
    }
    .card__body { padding: 18px 20px 22px; }
    .card__title { font-size: 1.3rem; font-weight: 700; color: var(--ghost-white); margin-bottom: 6px; }
    .card__meta { color: #777; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 10px; }
    .card__link { color: #aaa; font-weight: bold; }
    .card__link:hover { color: var(--ghost-white); }

    .story {
      max-width: 760px; margin: 0 auto; padding: 40px 22px;
    }
    .story__head { text-align: center; margin-bottom: 36px; }
    .story__title { font-size: 2.2rem; font-weight: 700; color: var(--ghost-white); }
    .story__meta { color: #777; margin-top: 6px; }
    .back-link { color: #888; text-decoration: none; display: inline-block; margin-bottom: 20px; }
    .back-link:hover { color: var(--ghost-white); }
    .prose {
      background: #0a0a0a; border: 1px solid #222; padding: 32px 40px;
      box-shadow: 5px 5px 0px #111;
    }
    .prose p { font-size: 1.12rem; line-height: 1.6; margin-bottom: 1.2em; color: #ccc; }
    .prose p:first-child::first-letter {
      font-family: inherit; font-size: 3.4rem; float: left; padding: 6px 12px 0 0;
      color: #aaa; font-weight: bold;
    }
    .prose--poetry p {
      white-space: pre-wrap; font-family: 'Cormorant Garamond', serif;
      margin-bottom: 0.5em;
    }
    .prose--poetry p:first-child::first-letter {
      font: inherit; float: none; padding: 0; color: inherit; line-height: inherit;
    }
    .story__foot {
      margin-top: 40px; display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap;
    }

    .quote {
      text-align: center; max-width: 820px; margin: 0 auto; padding: 60px 30px;
    }
    .quote__mark { font-size: 6rem; line-height: 0.5; color: #222; }
    .quote blockquote { font-size: 1.6rem; color: #999; font-style: italic; margin: 10px 0 16px; }
    .quote__author { color: var(--ghost-white); text-transform: uppercase; letter-spacing: 2px; }

    .contact__card {
      max-width: 720px; margin: 40px auto; text-align: center;
      background: #000 !important; border: 3px double #222; padding: 40px;
    }
    .contact__lead { color: #888; margin: 12px 0 24px; }
    .contact__links { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
    .chip {
      background: #111 !important; color: #aaa !important; border: 1px solid #333 !important;
      border-radius: 0px !important; text-transform: uppercase; padding: 12px 24px;
      font-weight: bold; transition: all 0.25s ease;
      text-decoration: none;
    }
    .chip:hover {
      background: var(--ghost-white) !important; color: var(--ink) !important;
      transform: translateY(-2px);
      box-shadow: 0 6px 14px rgba(0,0,0,0.3);
    }

    .footer {
      text-align: center; padding: 50px 22px 40px;
      background: #000 !important; color: #444 !important;
      border-top: 1px solid #222 !important;
    }
    .footer__logo { font-size: 1.3rem; color: #919191 !important; text-transform: uppercase; letter-spacing: 3px; }
    .footer__copy { color: #777777 !important; opacity: 1; font-size: 0.9rem; }

    @media (max-width: 800px) {
      .bookhero__inner, .hero__inner { grid-template-columns: 1fr; text-align: center; }
      .book-item { flex-direction: column-reverse; text-align: center; }
      .book-item__cover { width: 140px; margin: 0 auto; }
      .story__foot { flex-direction: column; align-items: center; }
      .hero__title { font-size: 3rem; }
    }
    @media (max-width: 640px) {
      .prose { padding: 20px; }
      .hero__title { font-size: 2.6rem; }
    }
    .nav__burger {
      display: none; flex-direction: column; gap: 5px; background: none; border: none; cursor: pointer;
    }
    .nav__burger span { width: 26px; height: 3px; background: #ccc; transition: 0.2s; }
    @media (max-width: 820px) {
      .nav__burger { display: flex; }
      .nav__links {
        position: absolute; top: 100%; right: 0; left: 0;
        flex-direction: column; background: #000; padding: 20px; gap: 14px;
        transform: translateY(-12px); opacity: 0; pointer-events: none; transition: 0.25s;
        z-index: 100;
      }
      .nav__links.is-open { opacity: 1; transform: none; pointer-events: auto; }
    }
"""

JS_BLOCK = """
<script>
  (function() {
    // --- год в подвале ---
    var yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // --- мобильное меню ---
    var burger = document.getElementById('burger');
    var navLinks = document.getElementById('navLinks');
    if (burger && navLinks) {
      burger.addEventListener('click', function() {
        var open = navLinks.classList.toggle('is-open');
        burger.setAttribute('aria-expanded', String(open));
      });
      navLinks.querySelectorAll('a').forEach(function(a) {
        a.addEventListener('click', function() {
          navLinks.classList.remove('is-open');
          burger.setAttribute('aria-expanded', 'false');
        });
      });
    }

    // --- тень на навбаре ---
    var nav = document.getElementById('nav');
    function onScroll() {
      if (nav) nav.classList.toggle('is-scrolled', window.scrollY > 10);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // --- кнопка переключения автора (луна/солнце) ---
    var author = document.body.getAttribute('data-author') || 'boroma';
    var inBooks = window.location.pathname.replace(/\\\\/g, '/').indexOf('/books/') !== -1;
    var depth = inBooks ? (window.location.pathname.indexOf('/story/') !== -1 ? '../../' : '../') : './';
    var destUrl = author === 'boroma' ? depth + 'index.html' : depth + 'boroma.html';
    var destName = author === 'boroma' ? 'Владимир&nbsp;Русин' : 'Денис&nbsp;Борома';
    var moonIcon = '<svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/></svg>';
    var sunIcon = '<svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 1.8v2.4M12 19.8v2.4M4.2 4.2l1.7 1.7M18.1 18.1l1.7 1.7M1.8 12h2.4M19.8 12h2.4M4.2 19.8l1.7-1.7M18.1 5.9l1.7-1.7"/></svg>';
    var destIcon = author === 'boroma' ? sunIcon : moonIcon;

    var btn = document.createElement('button');
    btn.className = 'switcher-btn';
    btn.setAttribute('aria-label', 'Перейти к автору: ' + destName.replace(/&nbsp;/g, ' '));
    btn.innerHTML = '<span class="switcher-btn__icon">' + destIcon + '</span>';
    var navTarget = document.querySelector('.nav__links') || document.querySelector('.nav__inner') || document.body;
    navTarget.appendChild(btn);

    btn.addEventListener('click', function() {
      btn.style.pointerEvents = 'none';
      var iframe = document.createElement('iframe');
      iframe.setAttribute('src', destUrl);
      iframe.setAttribute('scrolling', 'no');
      iframe.style.cssText = 'position:fixed; inset:0; width:100%; height:100%; border:none; z-index:998; clip-path:circle(0% at calc(100% - 38px) calc(0% - 38px)); pointer-events:none;';
      document.body.appendChild(iframe);
      var revealed = false;
      function expandPortal() {
        if (revealed) return;
        revealed = true;
        requestAnimationFrame(function() {
          requestAnimationFrame(function() {
            iframe.style.transition = 'clip-path .68s cubic-bezier(.4,0,.2,1)';
            iframe.style.clipPath = 'circle(150% at calc(100% - 38px) calc(0% - 38px))';
            setTimeout(function() {
              sessionStorage.setItem('sw_portal', '1');
              window.location.href = destUrl;
            }, 720);
          });
        });
      }
      iframe.onload = expandPortal;
      setTimeout(expandPortal, 1400);
    });

    // --- плавное появление страницы (только если не из портала) ---
    var fromPortal = !!sessionStorage.getItem('sw_portal');
    if (!fromPortal && !window.location.search.includes('portal')) {
      document.body.style.opacity = '0';
      setTimeout(function() {
        document.body.style.transition = 'opacity .72s cubic-bezier(.4,0,.2,1)';
        document.body.style.opacity = '1';
        setTimeout(function() { document.body.style.transition = ''; document.body.style.opacity = ''; }, 800);
      }, 60);
    }
    sessionStorage.removeItem('sw_portal');

    // --- Подсветка активного пункта меню при прокрутке (только если есть секции с id) ---
    var sections = document.querySelectorAll('section[id]');
    var navLinksForActive = document.querySelectorAll('.nav__links a');
    if (sections.length && navLinksForActive.length) {
      function setActiveLink() {
        var scrollPos = window.scrollY + 100;
        var activeId = null;
        sections.forEach(function(section) {
          var top = section.offsetTop;
          var bottom = top + section.offsetHeight;
          if (scrollPos >= top && scrollPos < bottom) {
            activeId = section.getAttribute('id');
          }
        });
        navLinksForActive.forEach(function(link) {
          var href = link.getAttribute('href');
          if (href === '#' + activeId) {
            link.classList.add('is-active');
          } else {
            link.classList.remove('is-active');
          }
        });
      }
      window.addEventListener('scroll', setActiveLink);
      window.addEventListener('resize', setActiveLink);
      setActiveLink();
    }
  })();
</script>
"""
