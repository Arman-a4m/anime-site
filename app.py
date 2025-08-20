import json
import random
from flask import Flask, render_template, request
from flask_talisman import Talisman

app = Flask(__name__)

# 🛡️ Безопасные заголовки (защита от XSS, clickjacking и др.)
Talisman(app, content_security_policy=None)

def load_anime():
    with open('templates/anime.json', "r", encoding="utf-8") as file:
        return json.load(file)


@app.route("/")
def index():
    anime_list = load_anime()
    anime_list = random.sample(anime_list, min(len(anime_list), 6))
    return render_template("index.html", anime_list=anime_list)



@app.route("/catalog")
def catalog():
    query = request.args.get("q", "").strip().lower()
    genre = request.args.get("genre") or ""
    year = request.args.get("year") or ""
    status = request.args.get("status") or ""
    studio = request.args.get("studio") or ""

    anime_list = load_anime()

    # списки для фильтров
    genres = sorted({g for a in anime_list for g in a.get("genre", [])})
    years = sorted({str(a.get("year")) for a in anime_list if a.get("year")})
    statuses = sorted({a.get("status") for a in anime_list if a.get("status")})
    studios = sorted({a.get("studio") for a in anime_list if a.get("studio")})

    # фильтрация
    result = []
    for a in anime_list:
        title = a.get("title", "").lower()
        original = a.get("title_original", "").lower()

        if query and query not in title and query not in original:
            continue
        if genre and genre not in a.get("genre", []):
            continue
        if year and str(a.get("year")) != year:
            continue
        if status and a.get("status") != status:
            continue
        if studio and a.get("studio") != studio:
            continue

        result.append(a)

    return render_template(
        "catalog.html",
        anime=result,
        genres=genres,
        years=years,
        statuses=statuses,
        studios=studios
    )


@app.route("/anime/<title>")
def anime_page(title):
    anime_list = load_anime()
    anime = next((a for a in anime_list if a["title"].lower() == title.lower()), None)

    if anime:
        # ищем похожие по жанрам
        recommendations = [
            a for a in anime_list
            if a["title"].lower() != anime["title"].lower()
            and set(a.get("genre", [])) & set(anime.get("genre", []))
        ]

        # сортировка по количеству совпадений жанров
        recommendations = sorted(
            recommendations,
            key=lambda x: len(set(x.get("genre", [])) & set(anime.get("genre", []))),
            reverse=True
        )

        return render_template("anime.html", anime=anime, recommendations=recommendations)

    return "Anime not found", 404



if __name__ == "__main__":
    app.run(debug=True)

