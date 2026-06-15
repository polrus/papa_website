import html
import os
import re
import shutil
from collections import OrderedDict

from boroma_templates import SECTION_INFO, BOROMA_CSS, JS_BLOCK

# ---------- Конфигурация ----------
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_TXT = os.path.join(ROOT, "books", "denis_boroma_vsyakoe.txt")
BOOKS_DIR = os.path.join(ROOT, "books")
STORY_DIR = os.path.join(BOOKS_DIR, "story")
HOMEPAGE = os.path.join(ROOT, "boroma.html")

PICTURES_ROOT = os.path.join(ROOT, "pictures", "boroma")

def slugify(text):
    text = text.lower().strip()
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    result = []
    for ch in text:
        if ch in mapping:
            result.append(mapping[ch])
        elif ch.isalnum() or ch == '-':
            result.append(ch)
        else:
            result.append('-')
    slug = ''.join(result)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug

def get_image_path(identifier):
    """Вернуть URL картинки относительно корня сайта или None."""
    for ext in ('.jpg', '.jpeg', '.png'):
        img_path = os.path.join(PICTURES_ROOT, f"{identifier}{ext}")
        if os.path.exists(img_path):
            return f"pictures/boroma/{identifier}{ext}"
    return None

def parse_txt():
    with open(SRC_TXT, encoding='utf-8') as f:
        lines = f.read().splitlines()
    stories = []
    i = 0
    n = len(lines)
    current_section = None
    while i < n:
        line = lines[i].strip()
        if line.startswith('━') and len(line) > 10:
            if i+1 < n and lines[i+1].strip() in SECTION_INFO:
                current_section = lines[i+1].strip()
                i += 3
                continue
        if line.startswith('▶ ') and current_section:
            title = line[2:].strip()
            url = lines[i+1].strip() if i+1 < n else ''
            j = i+2
            while j < n and (lines[j].strip().startswith('─') or lines[j].strip() == ''):
                j += 1
            body_lines = []
            while j < n:
                s = lines[j].strip()
                if s.startswith('▶ ') or (s.startswith('━') and len(s) > 10):
                    break
                body_lines.append(lines[j])
                j += 1
            paragraphs = []
            buf = []
            for bl in body_lines:
                if bl.strip() == '':
                    if buf:
                        paragraphs.append(' '.join(x.strip() for x in buf).strip())
                        buf = []
                else:
                    buf.append(bl)
            if buf:
                paragraphs.append(' '.join(x.strip() for x in buf).strip())
            paragraphs = [p for p in paragraphs if p]
            date = ''
            m = re.search(r'proza\.ru/(\d{4})/(\d{2})/(\d{2})', url)
            if m:
                date = f"{m.group(3)}.{m.group(2)}.{m.group(1)}"
            stories.append({
                'section': current_section,
                'title': title,
                'url': url,
                'date': date,
                'paragraphs': paragraphs,
                'raw_text': '\n'.join(body_lines)
            })
            i = j
            continue
        i += 1
    return stories

def get_kind(section_key):
    kinds = {
        "ИСТОРИЯ СВЕТЛЫХ ВРЕМЕН": "рассказ",
        "БАЛЛАДЫ": "баллада",
        "ЦИКЛ": "цикл",
        "МОСКОВСКИЕ ЭТЮДЫ": "этюд"
    }
    return kinds.get(section_key, "произведение")

def render_story_page(story, slug, kind, emoji, is_single):
    is_ballad = (kind == 'баллада')
    if is_ballad:
        lines = [html.escape(line) for line in story['raw_text'].splitlines()]
        body = '<div class="prose prose--poetry">\n      <p>' + '<br>\n      '.join(lines) + '</p>\n    </div>'
    else:
        paras = ''.join(f'      <p>{html.escape(p)}</p>\n' for p in story['paragraphs'])
        body = f'<div class="prose">\n{paras}    </div>'
    
    book_slug = SECTION_INFO[story['section']]['slug']
    if is_single:
        back_link = '<a class="back-link" href="../../boroma.html">← Все книги</a>'
        foot_link = '<a class="btn btn--ghost" href="../../boroma.html">← На главную</a>'
    else:
        back_link = f'<a class="back-link" href="../../books/{book_slug}.html">← {html.escape(SECTION_INFO[story["section"]]["title"])}</a>'
        foot_link = f'<a class="btn btn--ghost" href="../../books/{book_slug}.html">← Ко всем {kind}ам</a>'
    
    lamp_off_url = "/pictures/boroma/lamp-off.png"
    lamp_on_url  = "/pictures/boroma/lamp-on.png"

    bg_url = "../../pictures/boroma/background.png"
    custom_css = BOROMA_CSS.replace("{{BACKGROUND_URL}}", bg_url)

    content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(story['title'])} — Денис Борома</title>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet" />
  <style>{custom_css}</style>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90' fill='#aaa'>📖</text></svg>" />
</head>
<body data-author="boroma">
  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="../../boroma.html" class="nav__logo">Денис&nbsp;Борома</a>
      <button class="nav__burger" id="burger" aria-label="Меню" aria-expanded="false"><span></span><span></span><span></span></button>
      <nav class="nav__links" id="navLinks">
        <a href="../../boroma.html#hero">Об авторе</a>
        <a href="../../boroma.html#books">Книги</a>
        <a href="../../boroma.html#contact">Контакты</a>
      </nav>
    </div>
  </header>

  <article class="story">
    <div class="story__head">
      {back_link}
      <span class="section__kicker">~ {kind} ~</span>
      <h1 class="story__title">{html.escape(story['title'])}</h1>
      <p class="story__meta">{kind} · {story['date']}</p>
    </div>

    <div class="story-text-holder">
      <button class="lamp-toggle" data-off="../../{lamp_off_url}" data-on="../../{lamp_on_url}">
        <img src="../../{lamp_off_url}" alt="Переключить тему текста">
      </button>
      {body}
    </div>

    <div class="story__foot">
      {foot_link}
      <a class="btn btn--ghost" href="{story['url']}" target="_blank" rel="noopener">Оригинал на Проза.ру ↗</a>
    </div>
  </article>

  <footer class="footer">
    <p class="footer__logo">Денис Борома</p>
    <p class="footer__copy">© <span id="year"></span> Денис Борома. Все права защищены.</p>
  </footer>
  {JS_BLOCK}
</body>
</html>'''
    return content

def render_book_page(section_key, stories):
    info = SECTION_INFO[section_key]
    title = info['title']
    slug = info['slug']
    desc = info['desc']
    emoji = info['emoji']
    kind = get_kind(section_key)
    kind_plural = "рассказы" if kind == "рассказ" else "этюды"
    
    cards = []
    for story in stories:
        story_slug = slugify(story['title'])
        date = story['date'] if story['date'] else 'без даты'
        
        # Изображение для карточки рассказа
        img_url = get_image_path(story_slug)
        if img_url:
            cover_html = f'<img src="../{img_url}" alt="{html.escape(story["title"])}">'
        else:
            cover_html = f'<span class="card__emoji">{emoji}</span>'
        
        card = f'''      <article class="card">
        <a class="card__cover" href="story/{story_slug}.html">
          {cover_html}
        </a>
        <div class="card__body">
          <h3 class="card__title">{html.escape(story['title'])}</h3>
          <p class="card__meta">{kind} · {date}</p>
          <a class="card__link" href="story/{story_slug}.html">Читать →</a>
        </div>
      </article>'''
        cards.append(card)
    cards_html = '\n\n'.join(cards)
    
    # Изображение для обложки сборника
    book_img = get_image_path(slug)
    if book_img:
        hero_cover_html = f'<img src="../{book_img}" alt="{html.escape(title)}">'
    else:
        hero_cover_html = f'<span class="book__emoji">{emoji}</span>'
    
    bg_url = "../pictures/boroma/background.png"
    custom_css = BOROMA_CSS.replace("{{BACKGROUND_URL}}", bg_url)

    content = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} — Денис Борома</title>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet" />
  <style>{custom_css}</style>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90' fill='#aaa'>📖</text></svg>" />
</head>
<body data-author="boroma">
  <header class="nav" id="nav">
    <div class="nav__inner">
      <a href="../boroma.html" class="nav__logo">Денис&nbsp;Борома</a>
      <button class="nav__burger" id="burger" aria-label="Меню" aria-expanded="false"><span></span><span></span><span></span></button>
      <nav class="nav__links" id="navLinks">
        <a href="../boroma.html#hero">Об авторе</a>
        <a href="../boroma.html#books">Книги</a>
        <a href="../boroma.html#contact">Контакты</a>
      </nav>
    </div>
  </header>

  <section class="bookhero">
    <div class="bookhero__inner">
      <div class="bookhero__cover {info['cover_class']}">
        {hero_cover_html}
      </div>
      <div class="bookhero__text">
        <a class="back-link" href="../boroma.html">← Все книги</a>
        <span class="section__kicker">~ сборник ~</span>
        <h1 class="section__title">{html.escape(title)}</h1>
        <p class="bookhero__desc">{html.escape(desc)}</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section__head" style="text-align:center; margin-bottom:48px;">
      <span class="section__kicker">~ {kind_plural} ~</span>
      <h2 class="section__title">{len(stories)} {("произведение" if len(stories)==1 else "произведения" if len(stories)<5 else "произведений")}</h2>
      <p class="section__lead" style="color:#777; max-width:560px; margin:12px auto 0;">Нажмите на произведение, чтобы прочитать его.</p>
    </div>
    <div class="grid">
{cards_html}
    </div>
  </section>

  <footer class="footer">
    <p class="footer__logo">Денис Борома</p>
    <p class="footer__copy">© <span id="year"></span> Денис Борома. Все права защищены.</p>
  </footer>
  {JS_BLOCK}
</body>
</html>'''
    return content

def render_books_list(grouped_items):
    """Генерирует HTML для блока <div class="books-list">...</div>"""
    book_items = []
    for section_key, stories in grouped_items:
        info = SECTION_INFO[section_key]
        title = info['title']
        desc = info['desc']
        emoji = info['emoji']
        cover_class = info['cover_class']
        slug = info['slug']
        if len(stories) == 1:
            story_slug = slugify(stories[0]['title'])
            link = f"books/story/{story_slug}.html"
        else:
            link = f"books/{slug}.html"
        
        # Изображение для книги на главной
        img_url = get_image_path(slug)
        link = f"books/story/{story_slug}.html" if len(stories) == 1 else f"books/{slug}.html"

        if img_url:
            cover_content = f'<img src="{img_url}" alt="{html.escape(title)}">'
        else:
            cover_content = f'<span class="book__emoji">{emoji}</span>'

        cover_html = f'<a href="{link}" class="book-item__cover-link">{cover_content}</a>'
        
        book_items.append(f'''
    <div class="book-item">
      <div class="book-item__info">
        <h2 class="book-item__title">{html.escape(title)}</h2>
        <p class="book-item__desc">{html.escape(desc)}</p>
        <a href="{link}" class="btn btn--primary">Читать →</a>
      </div>
      <div class="book-item__cover {cover_class}">
        {cover_html}
      </div>
    </div>''')
    return '\n'.join(book_items)

def render_quote():
    return '''  <section class="quote">
    <p class="quote__mark">“</p>
    <blockquote>Дети идут рядом и держат за руку.<br>Ты думаешь: вот пройдём этот квартал — и всё наладится.<br>Но кварталы тянутся бесконечно, а сумерки сгущаются.</blockquote>
    <p class="quote__author">— «Прогулка с детьми»</p>
  </section>'''

def render_contact():
    return '''  <section class="section contact" id="contact">
    <div class="contact__card">
      <h2 class="section__title">Связаться с автором</h2>
      <p class="contact__lead">невозможно...</p>
    </div>
  </section>'''

def update_homepage_blocks(grouped_items):
    """Обновляет boroma.html, заменяя блоки между маркерами"""
    if not os.path.exists(HOMEPAGE):
        print("Ошибка: boroma.html не найден.")
        return False
    
    shutil.copy2(HOMEPAGE, HOMEPAGE + ".bak")
    with open(HOMEPAGE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Убедимся, что маркеры существуют
    if '<!-- BOOKS_LIST_START -->' not in content:
        print("Маркеры не найдены. Добавляю автоматически...")
        books_section_pattern = r'(<section class="section" id="books">.*?)(<div class="books-list">.*?</div>)(.*?</section>)'
        def replacer(m):
            before = m.group(1)
            books_div = m.group(2)
            after = m.group(3)
            new_books_div = '<!-- BOOKS_LIST_START -->\n' + books_div + '\n    <!-- BOOKS_LIST_END -->'
            return before + new_books_div + after
        content = re.sub(books_section_pattern, replacer, content, flags=re.DOTALL)
        with open(HOMEPAGE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Маркеры добавлены. Перезапустите скрипт для обновления содержимого.")
        return False
    
    new_books_html = render_books_list(grouped_items)
    new_quote_html = render_quote()
    new_contact_html = render_contact()
    
    def replace_block(start_marker, end_marker, new_content):
        pattern = re.escape(start_marker) + r'(.*?)' + re.escape(end_marker)
        replacement = start_marker + '\n' + new_content + '\n    ' + end_marker
        return re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    content = replace_block('<!-- BOOKS_LIST_START -->', '<!-- BOOKS_LIST_END -->', new_books_html)
    content = replace_block('<!-- QUOTE_START -->', '<!-- QUOTE_END -->', new_quote_html)
    content = replace_block('<!-- CONTACT_START -->', '<!-- CONTACT_END -->', new_contact_html)
    
    with open(HOMEPAGE, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    stories = parse_txt()
    print(f"Найдено произведений: {len(stories)}")
    grouped = OrderedDict()
    for story in stories:
        sec = story['section']
        if sec not in SECTION_INFO:
            continue
        grouped.setdefault(sec, []).append(story)
    
    os.makedirs(STORY_DIR, exist_ok=True)
    
    counts = {sec: len(sec_stories) for sec, sec_stories in grouped.items()}
    
    for story in stories:
        sec = story['section']
        if sec not in SECTION_INFO:
            continue
        kind = get_kind(sec)
        emoji = SECTION_INFO[sec]['emoji']
        slug = slugify(story['title'])
        is_single = (counts.get(sec, 0) == 1)
        out_path = os.path.join(STORY_DIR, f"{slug}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(render_story_page(story, slug, kind, emoji, is_single))
        print(f"  Страница произведения: {slug}.html")
    
    for sec, sec_stories in grouped.items():
        if len(sec_stories) <= 1:
            continue
        book_path = os.path.join(BOOKS_DIR, f"{SECTION_INFO[sec]['slug']}.html")
        with open(book_path, 'w', encoding='utf-8') as f:
            f.write(render_book_page(sec, sec_stories))
        print(f"  Страница сборника: {SECTION_INFO[sec]['slug']}.html")
    
    ordered_grouped_items = [(sec, grouped[sec]) for sec in SECTION_INFO.keys() if sec in grouped]
    success = update_homepage_blocks(ordered_grouped_items)
    if success:
        print("boroma.html успешно обновлён (блоки книг, цитаты, контактов).")
    else:
        print("Не удалось обновить boroma.html (возможно, добавлены маркеры, запустите скрипт ещё раз).")

if __name__ == "__main__":
    main()
