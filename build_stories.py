# -*- coding: utf-8 -*-
"""Parse books/vladimir_rusin_tonechka.txt and build on-site reader pages.

Generates:
  * books/story/<slug>.html        — one readable page per story
  * books/detstvo-tonechki.html     — listing, cards link to local readers
  * books/priklyucheniya-tonechki.html
  * books/scenarii.html
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "books", "vladimir_rusin_tonechka.txt")
STORY_DIR = os.path.join(ROOT, "books", "story")

# ---- per-story presentation (order matches the .txt) --------------------
META = [
    # slug, emoji, cover (1..9)
    ("skazka-pro-liliputov", "🧚", 1),
    ("homyachki", "🐹", 2),
    ("magazin-igrushek", "🧸", 3),
    ("drugoe", "🌈", 4),
    ("zoopark", "🦁", 5),
    ("dyadya-petya", "🎩", 6),
    ("krasnoe-pechenie", "🍪", 7),
    ("govoryashchiy-rulet", "🍰", 8),
    ("strashnaya-skazka", "👻", 9),
    ("tonechka-i-novyy-god", "🎄", 1),
    ("verhnie-kulichiki", "🏡", 2),
    ("kosmicheskie-praviteli", "🚀", 3),
    ("loshadinaya-noga", "🐴", 5),
    ("povelitel-blam-blanov", "👾", 6),
    ("priklyucheniya-buratino", "🐭", 7),
]

SECTION_PAGE = {
    "ДЕТСТВО ТОНЕЧКИ": "detstvo-tonechki.html",
    "ПРИКЛЮЧЕНИЯ ТОНЕЧКИ": "priklyucheniya-tonechki.html",
    "РАЗНОЕ": "scenarii.html",
}
SECTION_TITLE = {
    "ДЕТСТВО ТОНЕЧКИ": "Детство Тонечки",
    "ПРИКЛЮЧЕНИЯ ТОНЕЧКИ": "Приключения Тонечки",
    "РАЗНОЕ": "Сценарии",
}
KIND = {
    "ДЕТСТВО ТОНЕЧКИ": "сказка",
    "ПРИКЛЮЧЕНИЯ ТОНЕЧКИ": "сказка",
    "РАЗНОЕ": "сценарий",
}


def parse(text):
    """Return list of dicts: section, title, url, date, paragraphs."""
    lines = text.split("\n")
    stories = []
    section = None
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        # Section header: a ━ line, then a NAME line, then a ━ line
        if stripped.startswith("━") and i + 2 < n and lines[i + 2].strip().startswith("━"):
            section = lines[i + 1].strip()
            i += 3
            continue
        if stripped.startswith("▶ "):
            title = stripped[2:].strip()
            url = lines[i + 1].strip() if i + 1 < n else ""
            # skip the ──── divider line(s)
            j = i + 2
            while j < n and (lines[j].strip().startswith("─") or lines[j].strip() == ""):
                j += 1
            # collect body until next ▶ or section header or EOF
            body = []
            while j < n:
                s = lines[j].strip()
                if s.startswith("▶ "):
                    break
                if s.startswith("━") and j + 2 < n and lines[j + 2].strip().startswith("━"):
                    break
                body.append(lines[j])
                j += 1
            # split body into paragraphs on blank lines
            paras = []
            buf = []
            for bl in body:
                if bl.strip() == "":
                    if buf:
                        paras.append(" ".join(x.strip() for x in buf).strip())
                        buf = []
                else:
                    buf.append(bl)
            if buf:
                paras.append(" ".join(x.strip() for x in buf).strip())
            paras = [p for p in paras if p]
            date = ""
            m = re.search(r"proza\.ru/(\d{4})/(\d{2})/(\d{2})", url)
            if m:
                date = f"{m.group(3)}.{m.group(2)}.{m.group(1)}"
            stories.append({
                "section": section,
                "title": title,
                "url": url,
                "date": date,
                "paras": paras,
            })
            i = j
            continue
        i += 1
    return stories


READER_TMPL = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Владимир Русин</title>
  <meta name="description" content="{title} — {kind} Владимира Русина из сборника «{book}». Читать онлайн." />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Marck+Script&family=PT+Sans:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../css/styles.css" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>{emoji}</text></svg>" />
</head>
<body>

  <!-- ============ NAV ============ -->
  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="../../index.html#hero" class="nav__logo">🌙 Владимир&nbsp;Русин</a>
      <button class="nav__burger" id="burger" aria-label="Меню" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <nav class="nav__links" id="navLinks">
        <a href="../../index.html#hero">Об&nbsp;авторе</a>
        <a href="../../index.html#books">Книги</a>
        <a href="../../index.html#contact">Контакты</a>
      </nav>
    </div>
  </header>

  <!-- ============ STORY ============ -->
  <article class="story">
    <div class="story__head reveal">
      <a class="back-link" href="../{book_page}">← {book}</a>
      <span class="story__emoji cover--{cover}">{emoji}</span>
      <span class="section__kicker">~ {kind} ~</span>
      <h1 class="story__title">{title}</h1>
      <p class="story__meta">{kind} · {date}</p>
    </div>

    <div class="prose reveal">
{body}
    </div>

    <div class="story__foot reveal">
      <a class="btn btn--ghost" href="../{book_page}">← Все {kind_plural}</a>
      <a class="btn btn--ghost" href="{url}" target="_blank" rel="noopener">Оригинал на Проза.ру ↗</a>
    </div>
  </article>

  <!-- ============ FOOTER ============ -->
  <footer class="footer">
    <p class="footer__logo">🌙 Владимир Русин</p>
    <p class="footer__copy">© <span id="year"></span> Владимир Русин. Все права защищены.</p>
    <p class="footer__made">Сделано с ❤️ для маленьких и больших читателей</p>
  </footer>

  <script src="../../js/main.js"></script>
</body>
</html>
"""


def render_reader(story, meta):
    slug, emoji, cover = meta
    book_section = story["section"]
    book = SECTION_TITLE[book_section]
    kind = KIND[book_section]
    kind_plural = "сценарии" if kind == "сценарий" else "сказки"
    body = "\n".join(
        f"      <p>{html.escape(p)}</p>" for p in story["paras"]
    )
    return READER_TMPL.format(
        title=html.escape(story["title"]),
        kind=kind,
        kind_plural=kind_plural,
        book=html.escape(book),
        book_page=SECTION_PAGE[book_section],
        emoji=emoji,
        cover=cover,
        date=story["date"],
        body=body,
        url=story["url"],
    )


CARD_TMPL = """      <article class="card reveal">
        <a class="card__cover cover--{cover}" href="story/{slug}.html">
          <span class="card__emoji">{emoji}</span>
        </a>
        <div class="card__body">
          <h3 class="card__title">{title}</h3>
          <p class="card__meta">{kind} · {date}</p>
          <a class="card__link" href="story/{slug}.html">Читать →</a>
        </div>
      </article>"""


def build_cards(stories, metas):
    out = []
    for story, meta in zip(stories, metas):
        slug, emoji, cover = meta
        out.append(CARD_TMPL.format(
            cover=cover,
            slug=slug,
            emoji=emoji,
            title=html.escape(story["title"]),
            kind=KIND[story["section"]],
            date=story["date"],
        ))
    return "\n\n".join(out)


def replace_grid(page_path, grid_html):
    """Replace the inner content of the first <div class="grid">...</div>."""
    with open(page_path, encoding="utf-8") as f:
        page = f.read()
    new_grid = '<div class="grid">\n' + grid_html + "\n    </div>"
    # Match grid (handles both the cards-grid and empty-state cases by anchoring
    # on the STORIES section, replacing from <div class="grid"> to its </div>).
    pat = re.compile(r'<div class="grid">.*?</div>\s*</section>', re.S)
    if pat.search(page):
        page = pat.sub(new_grid + "\n  </section>", page, count=1)
    else:
        # empty-state page (priklyucheniya): replace from the editor comment that
        # precedes the empty block up to the closing </section>.
        pat2 = re.compile(
            r'<!-- ✏️ Когда пришлёте.*?-->\s*<div class="empty">.*?</div>\s*</section>',
            re.S,
        )
        page = pat2.sub(new_grid + "\n  </section>", page, count=1)
        # also refresh the section heading/lead for the now-populated book
        page = page.replace(
            '<h2 class="section__title">Сказки книги</h2>\n'
            '      <p class="section__lead">Список сказок этого сборника добавим, '
            'как только вы его пришлёте.</p>',
            '<h2 class="section__title">Сказки книги</h2>\n'
            '      <p class="section__lead">Нажмите на сказку, чтобы прочитать её целиком.</p>',
        )
    with open(page_path, "w", encoding="utf-8") as f:
        f.write(page)


def main():
    with open(SRC, encoding="utf-8") as f:
        stories = parse(f.read())
    assert len(stories) == len(META), f"{len(stories)} stories vs {len(META)} meta"

    os.makedirs(STORY_DIR, exist_ok=True)

    # reader pages
    for story, meta in zip(stories, META):
        out = render_reader(story, meta)
        with open(os.path.join(STORY_DIR, meta[0] + ".html"), "w", encoding="utf-8") as f:
            f.write(out)

    # group by section, preserving order
    groups = {}
    for story, meta in zip(stories, META):
        groups.setdefault(story["section"], []).append((story, meta))

    for section, page in SECTION_PAGE.items():
        items = groups.get(section, [])
        st = [x[0] for x in items]
        mt = [x[1] for x in items]
        grid = build_cards(st, mt)
        replace_grid(os.path.join(ROOT, "books", page), grid)

    print(f"Built {len(stories)} reader pages.")
    for story, meta in zip(stories, META):
        print(f"  {meta[0]:28s} {len(story['paras']):3d} ¶  {story['title']}")


if __name__ == "__main__":
    main()
