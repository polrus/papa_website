#!/usr/bin/env python3
"""
Scraper for Денис Борома (rusin1) on proza.ru
Fetches all stories

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
    {"url": "https://proza.ru/2022/04/25/1893",   "section": "История светлых времен"},
    {"url": "https://proza.ru/2022/04/25/1900",  "section": "История светлых времен"},
    {"url": "https://proza.ru/2022/04/28/12",  "section": "История светлых времен"},
    {"url": "https://proza.ru/2022/05/09/51",  "section": "История светлых времен"},
    {"url": "https://proza.ru/2018/11/12/2033",  "section": "Баллады"},
    {"url": "https://proza.ru/2022/04/25/1917",  "section": "Цикл"},
    {"url": "https://proza.ru/2023/12/23/1768",  "section": "Московские этюды"},
    {"url": "https://proza.ru/2023/08/13/1572",  "section": "Московские этюды"}
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

OUTPUT_FILE = "denis_boroma_vsyakoe.txt"


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
    print("Денис Борома — загрузка рассказов")
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
    sections_order = ["История светлых времен", "Баллады", "Цикл", "Московские этюды"]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("ДЕНИС БОРОМА\n")
        f.write("Рассказы, баллады, этюды\n")
        f.write("Источник: https://proza.ru/avtor/boroma\n")
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
