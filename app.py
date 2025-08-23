#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anime Catalog Web Application
Профессиональное веб-приложение для каталога аниме
"""

import json
import random
import logging
from flask import Flask, render_template, request, jsonify, abort
from flask_talisman import Talisman
from config import get_config

# Настройка логирования
logger = logging.getLogger(__name__)

# Загрузка конфигурации
config = get_config()

app = Flask(__name__)
app.config.from_object(config)

# Инициализация Talisman для безопасности
Talisman(app, content_security_policy=None)

class AnimeCatalog:
    def __init__(self, data_file):
        self.data_file = data_file
        self._anime_data = None
        self._load_data()
    
    def _load_data(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                self._anime_data = json.load(file)

            # фикс трейлеров
            for anime in self._anime_data:
                if "trailers" in anime:
                    fixed_trailers = []
                    for url in anime["trailers"]:
                        if "watch?v=" in url:
                            video_id = url.split("watch?v=")[-1].split("&")[0]
                            fixed_trailers.append(f"https://www.youtube.com/embed/{video_id}")
                        else:
                            fixed_trailers.append(url)
                    anime["trailers"] = fixed_trailers

            logger.info(f"Загружено {len(self._anime_data)} аниме из файла")
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
            self._anime_data = []

    
    def get_all_anime(self):
        """Получить все аниме"""
        return self._anime_data
    
    def get_random_anime(self, count=6):
        """Получить случайные аниме для рекомендаций"""
        return random.sample(self._anime_data, min(count, len(self._anime_data)))
    
    def search_anime(self, query=None, genre=None, year=None, status=None, studio=None):
        """Поиск аниме по различным критериям"""
        results = self._anime_data.copy()
        
        if query:
            query = query.lower()
            results = [
                anime for anime in results
                if (query in anime.get('title', '').lower() or
                    query in anime.get('title_english', '').lower() or
                    query in anime.get('title_original', '').lower() or
                    query in anime.get('description', '').lower())
            ]
        
        if genre:
            results = [
                anime for anime in results
                if genre in anime.get('genre', [])
            ]
        
        if year:
            results = [
                anime for anime in results
                if str(anime.get('year', '')) == str(year)
            ]
        
        if status:
            results = [
                anime for anime in results
                if anime.get('status', '').lower() == status.lower()
            ]
        
        if studio:
            results = [
                anime for anime in results
                if studio.lower() in anime.get('studio', '').lower()
            ]
        
        return results
    
    def get_anime_by_title(self, title):
        """Получить аниме по названию"""
        # Декодируем URL-encoded строку
        import urllib.parse
        try:
            title = urllib.parse.unquote(title)
        except:
            pass
        
        # Также заменяем %20 на пробелы для совместимости
        title = title.replace('%20', ' ')
        
        for anime in self._anime_data:
            if (anime.get('title', '').lower() == title.lower() or
                anime.get('title_english', '').lower() == title.lower() or
                anime.get('title_original', '').lower() == title.lower()):
                return anime
        return None
    
    def get_recommendations(self, anime, count=4):
        """Получить рекомендации на основе жанров"""
        if not anime or not anime.get('genre'):
            return self.get_random_anime(count)
        
        anime_genres = set(anime['genre'])
        recommendations = []
        
        for item in self._anime_data:
            if item['id'] != anime['id']:
                item_genres = set(item.get('genre', []))
                if anime_genres & item_genres:  # Есть общие жанры
                    recommendations.append(item)
        
        # Если рекомендаций мало, добавляем случайные
        if len(recommendations) < count:
            random_anime = self.get_random_anime(count - len(recommendations))
            recommendations.extend(random_anime)
        
        return recommendations[:count]
    
    def get_unique_values(self, field):
        """Получить уникальные значения для поля"""
        values = set()
        for anime in self._anime_data:
            value = anime.get(field)
            if isinstance(value, list):
                values.update(value)
            elif value:
                values.add(value)
        return sorted(list(values))

# Инициализация каталога
catalog = AnimeCatalog(config.ANIME_DATA_FILE)

@app.context_processor
def inject_config():
    """Внедрение конфигурации в шаблоны"""
    return {
        'app_name': 'Anime Catalog',
        'app_version': '2.0.0',
        'config': config
    }

@app.route('/')
def index():
    """Главная страница с рекомендациями"""
    try:
        anime_list = catalog.get_random_anime(6)
        return render_template('index.html', anime_list=anime_list)
    except Exception as e:
        logger.error(f"Ошибка на главной странице: {e}")
        return render_template('index.html', anime_list=[])

@app.route('/catalog')
def catalog_page():
    """Страница каталога с фильтрами"""
    try:
        # Получение параметров фильтрации
        query = request.args.get('q', '').strip()
        genre = request.args.get('genre', '').strip()
        year = request.args.get('year', '').strip()
        status = request.args.get('status', '').strip()
        studio = request.args.get('studio', '').strip()
        
        # Поиск аниме
        anime = catalog.search_anime(query, genre, year, status, studio)
        
        # Получение уникальных значений для фильтров
        genres = catalog.get_unique_values('genre')
        years = catalog.get_unique_values('year')
        statuses = catalog.get_unique_values('status')
        studios = catalog.get_unique_values('studio')
        
        # Текущие фильтры для отображения
        current_filters = {
            'query': query,
            'genre': genre,
            'year': year,
            'status': status,
            'studio': studio
        }
        
        return render_template('catalog.html', 
                             anime=anime,
        genres=genres,
        years=years,
        statuses=statuses,
                             studios=studios,
                             current_filters=current_filters)
    except Exception as e:
        logger.error(f"Ошибка в каталоге: {e}")
        return render_template('catalog.html', anime=[], error="Ошибка загрузки каталога")

@app.route('/anime/<title>')
def anime_page(title):
    """Страница отдельного аниме"""
    try:
        anime = catalog.get_anime_by_title(title)
        if not anime:
            abort(404)
        
        recommendations = catalog.get_recommendations(anime, 4)
        return render_template('anime.html', anime=anime, recommendations=recommendations)
    except Exception as e:
        logger.error(f"Ошибка на странице аниме {title}: {e}")
        abort(404)

# API endpoints
@app.route('/api/anime')
def api_anime():
    """API для получения всех аниме"""
    try:
        anime_list = catalog.get_all_anime()
        return jsonify({
            'success': True,
            'data': anime_list,
            'count': len(anime_list)
        })
    except Exception as e:
        logger.error(f"Ошибка API /api/anime: {e}")
        return jsonify({
            'success': False,
            'error': 'Ошибка загрузки данных'
        }), 500

@app.route('/api/search')
def api_search():
    """API для поиска аниме"""
    try:
        query = request.args.get('q', '').strip()
        genre = request.args.get('genre', '').strip()
        year = request.args.get('year', '').strip()
        status = request.args.get('status', '').strip()
        studio = request.args.get('studio', '').strip()
        
        results = catalog.search_anime(query, genre, year, status, studio)
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'filters': {
                'query': query,
                'genre': genre,
                'year': year,
                'status': status,
                'studio': studio
            }
        })
    except Exception as e:
        logger.error(f"Ошибка API /api/search: {e}")
        return jsonify({
            'success': False,
            'error': 'Ошибка поиска'
        }), 500

# Обработчики ошибок
@app.errorhandler(404)
def not_found_error(error):
    """Обработка ошибки 404"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Обработка ошибки 500"""
    logger.error(f"Внутренняя ошибка сервера: {error}")
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)

