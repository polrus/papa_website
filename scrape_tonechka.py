#!/usr/bin/env python3
"""
Scraper for Владимир Русин (rusin1) on proza.ru
Fetches all stories from «Детство Тонечки» and «Приключения Тонечки»

Requirements:
    pip install requests beautifulsoup4

Run:
    python scrape_tonechka.py
"""

import requests
from bs4 import BeautifulSoup
import time

# URLs taken directly from proza.ru/avtor/rusin1
# Sections decoded manually from page structure (order matches the page)
STORIES = [
    {"url": "https://proza.ru/2020/01/07/31",   "section": "Разное"},
    {"url": "https://proza.ru/2014/07/12/1909",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2014/07/12/1800",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2014/07/12/1900",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2014/07/12/1881",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2014/07/12/1858",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2014/07/12/1885",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2014/07/12/1779",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2014/07/19/1768",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2015/01/10/2190",  "section": "Детство Тонечки"},
    {"url": "https://proza.ru/2014/07/12/1906",  "section": "Приключения Тонечки"},
    {"url": "https://proza.ru/2014/07/13/11",    "section": "Приключения Тонечки"},
    {"url": "https://proza.ru/2014/07/13/22",    "section": "Приключения Тонечки"},
    {"url": "https://proza.ru/2014/07/19/1841",  "section": "Приключения Тонечки"},
    {"url": "https://proza.ru/2014/12/05/2160",  "section": "Приключения Тонечки"},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

OUTPUT_FILE = "vladimir_rusin_tonechka.txt"


def fetch_story(url):
    """Fetch a story page, return (title, body_text) decoded from windows-1251."""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.encoding = "windows-1251"
    soup = BeautifulSoup(response.text, "html.parser")

    # Title is in <h1>
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else url

    # Story text is in <div class="text">
    text_div = soup.find("div", class_="text")
    if text_div:
        body = text_div.get_text(separator="\n\n", strip=True)
    else:
        body = "(текст не найден)"

    return title, body


def main():
    print("=" * 60)
    print("Владимир Русин — загрузка рассказов")
    print("=" * 60)

    collected = []

    for i, story in enumerate(STORIES, 1):
        print(f"[{i}/{len(STORIES)}] {story['url']} ...", end=" ", flush=True)
        try:
            title, body = fetch_story(story["url"])
            collected.append({**story, "title": title, "body": body})
            print(f"✓  «{title}»  ({len(body)} симв.)")
        except Exception as e:
            collected.append({**story, "title": story["url"], "body": f"(ошибка: {e})"})
            print(f"✗ Ошибка: {e}")
        time.sleep(0.5)

    # Write output
    sections_order = ["Детство Тонечки", "Приключения Тонечки", "Разное"]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("ВЛАДИМИР РУСИН\n")
        f.write("Рассказы из сборников «Детство Тонечки» и «Приключения Тонечки»\n")
        f.write("Источник: https://proza.ru/avtor/rusin1\n")
        f.write("═" * 60 + "\n")

        for section in sections_order:
            items = [s for s in collected if s["section"] == section]
            if not items:
                continue
            f.write(f"\n\n{'━' * 60}\n{section.upper()}\n{'━' * 60}\n")
            for s in items:
                f.write(f"\n▶ {s['title']}\n")
                f.write(f"{s['url']}\n")
                f.write("─" * 40 + "\n\n")
                f.write(s["body"])
                f.write("\n\n")

    print(f"\n✓ Сохранено в: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
