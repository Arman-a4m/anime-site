# Anime Data JSON File

## Описание
Файл `templates/anime.json` содержит качественные данные о популярных аниме сериалах. Все данные являются официальными и не нарушают авторские права.

## Структура данных

Каждая запись аниме содержит следующие поля:

### Обязательные поля:
- `id` (number) - Уникальный идентификатор
- `title` (string) - Название на английском языке
- `title_original` (string) - Оригинальное название на японском
- `title_english` (string) - Английское название
- `genre` (array) - Массив жанров
- `year` (number) - Год выпуска
- `season` (string) - Сезон выпуска (Spring, Summer, Fall, Winter)
- `status` (string) - Статус (Finished, Ongoing, etc.)
- `studio` (string) - Студия анимации
- `episodes` (number) - Количество эпизодов
- `duration` (string) - Продолжительность эпизода
- `age_rating` (string) - Возрастной рейтинг
- `rating` (number) - Рейтинг (0-10)
- `description` (string) - Краткое описание
- `characters` (array) - Основные персонажи
- `poster` (string) - URL постера
- `trailers` (array) - Массив URL трейлеров

### Дополнительные поля:
- `source` (string) - Источник (Manga, Light Novel, Original, etc.)
- `aired` (string) - Период трансляции
- `broadcast` (string) - Время трансляции
- `licensors` (array) - Лицензиары
- `producers` (array) - Продюсеры
- `director` (string) - Режиссер
- `music` (array) - Композиторы

## Пример использования

```python
import json

# Загрузка данных
with open('templates/anime.json', 'r', encoding='utf-8') as f:
    anime_data = json.load(f)

# Поиск аниме по названию
def find_anime_by_title(title):
    for anime in anime_data:
        if title.lower() in anime['title'].lower():
            return anime
    return None

# Фильтрация по жанру
def filter_by_genre(genre):
    return [anime for anime in anime_data if genre in anime['genre']]

# Сортировка по рейтингу
def get_top_rated(limit=10):
    return sorted(anime_data, key=lambda x: x['rating'], reverse=True)[:limit]
```

## Жанры

Доступные жанры:
- Action
- Adventure
- Comedy
- Drama
- Fantasy
- Horror
- Mecha
- Mystery
- Psychological
- Romance
- Sci-Fi
- Shounen
- Shoujo
- Slice of Life
- Sports
- Supernatural
- Thriller

## Источники данных

Все данные взяты из официальных источников:
- AniList API
- MyAnimeList
- Официальные сайты студий
- Лицензированные трейлеры на YouTube

## Обновления

Файл регулярно обновляется с новыми данными и исправлениями. Все изменения проходят проверку на валидность JSON.

## Лицензия

Данные используются в соответствии с условиями использования соответствующих API и сервисов. 