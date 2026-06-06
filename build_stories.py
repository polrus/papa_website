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
      <a href="../../index.html#hero" class="nav__logo">Владимир&nbsp;Русин</a>
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
  <article class="story{story_extra}">
{banner}    <div class="story__head reveal">
      <a class="back-link" href="../{book_page}">← {book}</a>
      <span class="story__emoji cover--{cover}">{emoji}</span>
      <span class="section__kicker">~ {kind} ~</span>
      <h1 class="story__title">{title}</h1>
      <p class="story__meta">{kind} · {date}</p>
    </div>

    <div class="prose{prose_extra}">
{body}
    </div>
{video_figure}
    <div class="story__foot reveal">
      <a class="btn btn--ghost" href="../{book_page}">← Все {kind_plural}</a>
      <a class="btn btn--ghost" href="{url}" target="_blank" rel="noopener">Оригинал на Проза.ру ↗</a>
    </div>
  </article>

  <!-- ============ FOOTER ============ -->
  <footer class="footer">
    <p class="footer__logo">Владимир Русин</p>
    <p class="footer__copy">© <span id="year"></span> Владимир Русин. Все права защищены.</p>
    <p class="footer__made">Сделано с ❤️ для маленьких и больших читателей</p>
  </footer>

  <script src="../../js/main.js"></script>
</body>
</html>
"""


def has_video(slug):
    """A cover video exists for the story card / book covers."""
    return os.path.exists(os.path.join(ROOT, "pictures", f"story-{slug}.mp4"))


def text_video(slug):
    """Filename stem for the in-text illustration.

    Prefers a dedicated `text-<slug>` clip (some stories have a separate
    cover vs. in-text version); otherwise falls back to the cover clip.
    Returns the stem (e.g. "text-strashnaya-skazka") or None.
    """
    pics = os.path.join(ROOT, "pictures")
    if os.path.exists(os.path.join(pics, f"text-{slug}.mp4")):
        return f"text-{slug}"
    if os.path.exists(os.path.join(pics, f"story-{slug}.mp4")):
        return f"story-{slug}"
    return None


VIDEO_FIGURE_TMPL = """
    <figure class="story-figure reveal">
      <video class="story-figure__video" src="../../pictures/{stem}.mp4" poster="../../pictures/{stem}.jpg" autoplay loop muted playsinline preload="metadata"></video>
      <figcaption class="story-figure__cap">{title}</figcaption>
    </figure>
"""


# Stories whose body is a play script kept verbatim in a side file
# (preserves line breaks, scene headings, songs).
SCRIPT_FILES = {
    "priklyucheniya-buratino": os.path.join(ROOT, "books", "buratino-script.txt"),
}
SCENE_RE = re.compile(
    r"^(Предисловие|Использованная литература:|Действующие лица.*:|"
    r"[А-Яа-я]+\s+картина\..*|Счастливый конец\.?)$"
)


def render_script_body(raw):
    """Render a play script: blank-line blocks → <p> (lines joined with <br>),
    scene/section markers → <h2>."""
    lines = raw.split("\n")
    # drop a leading title + "Владимир Русин" byline if present
    while lines and lines[0].strip() == "":
        lines.pop(0)
    if lines and lines[0].strip():
        lines.pop(0)  # title line
    if lines and lines[0].strip() == "Владимир Русин":
        lines.pop(0)
    blocks, buf = [], []
    for ln in lines:
        if ln.strip() == "":
            if buf:
                blocks.append(buf)
                buf = []
        else:
            buf.append(ln.rstrip())
    if buf:
        blocks.append(buf)
    out = []
    for block in blocks:
        if len(block) == 1 and SCENE_RE.match(block[0].strip()):
            out.append(f'      <h2 class="scene-title">{html.escape(block[0].strip())}</h2>')
        else:
            inner = "<br>\n      ".join(html.escape(l) for l in block)
            out.append(f"      <p>{inner}</p>")
    return "\n".join(out)


def render_reader(story, meta):
    slug, emoji, cover = meta
    book_section = story["section"]
    book = SECTION_TITLE[book_section]
    kind = KIND[book_section]
    kind_plural = "сценарии" if kind == "сценарий" else "сказки"
    prose_extra = ""
    if slug in SCRIPT_FILES and os.path.exists(SCRIPT_FILES[slug]):
        with open(SCRIPT_FILES[slug], encoding="utf-8") as f:
            body = render_script_body(f.read())
        prose_extra = " prose--script"
    else:
        lines = []
        for i, p in enumerate(story["paras"]):
            s = p.strip()
            # a leading parenthetical note (e.g. co-authorship) — italic, muted,
            # and no drop-cap; the drop-cap moves to the next paragraph.
            if i == 0 and s.startswith("(") and s.endswith(")"):
                lines.append(f'      <p class="story-note">{html.escape(p)}</p>')
            else:
                lines.append(f"      <p>{html.escape(p)}</p>")
        body = "\n".join(lines)
    video_figure = ""
    stem = text_video(slug)
    if stem:
        video_figure = VIDEO_FIGURE_TMPL.format(
            stem=stem, title=html.escape(story["title"]),
        )
    # optional wide banner image at the top of the story (pictures/banner-<slug>.jpg)
    banner = ""
    story_extra = ""
    if os.path.exists(os.path.join(ROOT, "pictures", f"banner-{slug}.jpg")):
        banner = (f'    <img class="story-banner reveal" '
                  f'src="../../pictures/banner-{slug}.jpg" '
                  f'alt="{html.escape(story["title"])}" />\n')
        story_extra = " story--banner"
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
        banner=banner,
        story_extra=story_extra,
        prose_extra=prose_extra,
        video_figure=video_figure,
        url=story["url"],
    )


CARD_TMPL = """      <article class="card reveal">
        <a class="card__cover cover--{cover}{has_video_cls}" href="story/{slug}.html">
{cover_inner}
        </a>
        <div class="card__body">
          <h3 class="card__title">{title}</h3>
          <p class="card__meta">{kind} · {date}</p>
          <a class="card__link" href="story/{slug}.html">Читать →</a>
        </div>
      </article>"""

CARD_VIDEO = ('          <video class="cover-video" src="../pictures/story-{slug}.mp4" '
              'poster="../pictures/story-{slug}.jpg" muted loop playsinline preload="metadata"></video>\n'
              '          <span class="card__emoji">{emoji}</span>')


def build_cards(stories, metas):
    out = []
    for story, meta in zip(stories, metas):
        slug, emoji, cover = meta
        if has_video(slug):
            cover_inner = CARD_VIDEO.format(slug=slug, emoji=emoji)
            has_video_cls = " has-video"
        else:
            cover_inner = f'          <span class="card__emoji">{emoji}</span>'
            has_video_cls = ""
        out.append(CARD_TMPL.format(
            cover=cover,
            has_video_cls=has_video_cls,
            cover_inner=cover_inner,
            slug=slug,
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

    # manual card-order tweaks: swap the on-page position of two stories
    # (each pair is (slug_a, slug_b); reader pages are unaffected).
    CARD_SWAPS = [("govoryashchiy-rulet", "strashnaya-skazka")]
    for items in groups.values():
        slugs = [m[0] for (_s, m) in items]
        for a, b in CARD_SWAPS:
            if a in slugs and b in slugs:
                ia, ib = slugs.index(a), slugs.index(b)
                items[ia], items[ib] = items[ib], items[ia]
                slugs[ia], slugs[ib] = slugs[ib], slugs[ia]

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
