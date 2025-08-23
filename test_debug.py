#!/usr/bin/env python3
import json
import urllib.parse

# Загружаем данные
with open('templates/anime.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Загружено аниме: {len(data)}")
print("\nПервые 5 аниме:")
for i, anime in enumerate(data[:5]):
    print(f"{i+1}. {anime['title']}")

print("\nТестируем поиск:")
test_titles = ["Naruto", "Attack on Titan", "Death Note"]

for title in test_titles:
    print(f"\nПоиск: '{title}'")
    found = None
    for anime in data:
        if (anime.get('title', '').lower() == title.lower() or
            anime.get('title_english', '').lower() == title.lower() or
            anime.get('title_original', '').lower() == title.lower()):
            found = anime
            break
    
    if found:
        print(f"✓ Найдено: {found['title']}")
    else:
        print(f"✗ Не найдено")

print("\nТестируем URL-кодирование:")
test_url = "Rurouni%20Kenshin"
decoded = urllib.parse.unquote(test_url)
print(f"URL: {test_url}")
print(f"Декодировано: {decoded}")

# Тестируем поиск с декодированным названием
print(f"\nПоиск: '{decoded}'")
found = None
for anime in data:
    if (anime.get('title', '').lower() == decoded.lower() or
        anime.get('title_english', '').lower() == decoded.lower() or
        anime.get('title_original', '').lower() == decoded.lower()):
        found = anime
        break

if found:
    print(f"✓ Найдено: {found['title']}")
else:
    print(f"✗ Не найдено")



