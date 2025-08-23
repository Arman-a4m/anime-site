#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anime Catalog Web Application
Профессиональное веб-приложение для каталога аниме
"""

import json
import logging
import os
import random
from typing import List, Dict, Optional, Any
from flask import Flask, render_template, request, abort, jsonify
from flask_talisman import Talisman
from werkzeug.exceptions import HTTPException

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание приложения
app = Flask(__name__)

# Конфигурация
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'),
    JSON_AS_ASCII=False,
    JSONIFY_PRETTYPRINT_REGULAR=True
)

# 🛡️ Безопасные заголовки (защита от XSS, clickjacking и др.)
Talisman(
    app, 
    content_security_policy={
        'default-src': ["'self'"],
        'img-src': ["'self'", "data:", "https:", "http:"],
        'script-src': ["'self'", "'unsafe-inline'"],
        'style-src': ["'self'", "'unsafe-inline'"],
        'font-src': ["'self'", "https:", "data:"],
        'connect-src': ["'self'"],
        'media-src': ["'self'", "https:"],
        'frame-src': ["'self'", "https://www.youtube.com", "https://youtube.com"]
    },
    force_https=False  # Измените на True для продакшена
)

class AnimeCatalog:
    """Класс для работы с каталогом аниме"""
    
    def __init__(self, file_path: str = 'templates/anime.json'):
        self.file_path = file_path
        self._cache = None
        self._cache_timestamp = 0
    
    def load_anime(self) -> List[Dict[str, Any]]:
        """Загружает данные об аниме с кэшированием"""
        try:
            if self._cache is None:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self._cache = json.load(file)
                    logger.info(f"Загружено {len(self._cache)} аниме из файла")
            return self._cache
        except FileNotFoundError:
            logger.error(f"Файл {self.file_path} не найден")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Неожиданная ошибка при загрузке аниме: {e}")
            return []
    
    def get_random_anime(self, limit: int = 6) -> List[Dict[str, Any]]:
        """Возвращает случайные аниме"""
        anime_list = self.load_anime()
        return random.sample(anime_list, min(len(anime_list), limit))
    
    def search_anime(self, query: str = "", genre: str = "", year: str = "", 
                    status: str = "", studio: str = "") -> List[Dict[str, Any]]:
        """Поиск и фильтрация аниме"""
        anime_list = self.load_anime()
        result = []
        
        for anime in anime_list:
            # Поиск по названию
            title = anime.get("title", "").lower()
            original = anime.get("title_original", "").lower()
            english = anime.get("title_english", "").lower()
            
            if query and query not in title and query not in original and query not in english:
                continue
            
            # Фильтрация по жанру
            if genre and genre not in anime.get("genre", []):
                continue
            
            # Фильтрация по году
            if year and str(anime.get("year")) != year:
                continue
            
            # Фильтрация по статусу
            if status and anime.get("status") != status:
                continue
            
            # Фильтрация по студии
            if studio and anime.get("studio") != studio:
                continue
            
            result.append(anime)
        
        return result
    
    def get_anime_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        """Находит аниме по названию"""
        anime_list = self.load_anime()
        title_lower = title.lower()
        
        for anime in anime_list:
            if (anime.get("title", "").lower() == title_lower or
                anime.get("title_english", "").lower() == title_lower):
                return anime
        return None
    
    def get_recommendations(self, anime: Dict[str, Any], limit: int = 6) -> List[Dict[str, Any]]:
        """Получает рекомендации на основе жанров"""
        anime_list = self.load_anime()
        anime_genres = set(anime.get("genre", []))
        
        recommendations = []
        for a in anime_list:
            if a.get("title") != anime.get("title"):
                common_genres = set(a.get("genre", [])) & anime_genres
                if common_genres:
                    recommendations.append({
                        'anime': a,
                        'common_genres': len(common_genres),
                        'score': len(common_genres) / len(anime_genres) if anime_genres else 0
                    })
        
        # Сортировка по релевантности
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return [r['anime'] for r in recommendations[:limit]]
    
    def get_filter_options(self) -> Dict[str, List[str]]:
        """Получает опции для фильтров"""
        anime_list = self.load_anime()
        
        return {
            'genres': sorted({g for a in anime_list for g in a.get("genre", [])}),
            'years': sorted({str(a.get("year")) for a in anime_list if a.get("year")}),
            'statuses': sorted({a.get("status") for a in anime_list if a.get("status")}),
            'studios': sorted({a.get("studio") for a in anime_list if a.get("studio")})
        }

# Инициализация каталога
catalog = AnimeCatalog()

@app.route("/")
def index():
    """Главная страница"""
    try:
        featured_anime = catalog.get_random_anime(6)
        return render_template("index.html", anime_list=featured_anime)
    except Exception as e:
        logger.error(f"Ошибка на главной странице: {e}")
        return render_template("index.html", anime_list=[])

@app.route("/catalog")
def catalog_page():
    """Страница каталога с фильтрами"""
    try:
        # Получаем параметры фильтрации
        query = request.args.get("q", "").strip()
        genre = request.args.get("genre", "")
        year = request.args.get("year", "")
        status = request.args.get("status", "")
        studio = request.args.get("studio", "")
        
        # Поиск и фильтрация
        filtered_anime = catalog.search_anime(query, genre, year, status, studio)
        
        # Опции для фильтров
        filter_options = catalog.get_filter_options()
        
        return render_template(
            "catalog.html",
            anime=filtered_anime,
            genres=filter_options['genres'],
            years=filter_options['years'],
            statuses=filter_options['statuses'],
            studios=filter_options['studios'],
            current_filters={
                'query': query,
                'genre': genre,
                'year': year,
                'status': status,
                'studio': studio
            }
        )
    except Exception as e:
        logger.error(f"Ошибка в каталоге: {e}")
        return render_template("catalog.html", anime=[], error="Ошибка загрузки каталога")

@app.route("/anime/<title>")
def anime_page(title):
    """Страница отдельного аниме"""
    try:
        anime = catalog.get_anime_by_title(title)
        
        if not anime:
            abort(404, description="Аниме не найдено")
        
        # Получаем рекомендации
        recommendations = catalog.get_recommendations(anime, 6)
        
        return render_template("anime.html", anime=anime, recommendations=recommendations)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка на странице аниме {title}: {e}")
        abort(500, description="Внутренняя ошибка сервера")

@app.route("/api/anime")
def api_anime():
    """API endpoint для получения списка аниме"""
    try:
        anime_list = catalog.load_anime()
        return jsonify({
            'success': True,
            'count': len(anime_list),
            'data': anime_list
        })
    except Exception as e:
        logger.error(f"Ошибка API: {e}")
        return jsonify({
            'success': False,
            'error': 'Ошибка загрузки данных'
        }), 500

@app.route("/api/anime/<title>")
def api_anime_detail(title):
    """API endpoint для получения информации об аниме"""
    try:
        anime = catalog.get_anime_by_title(title)
        
        if not anime:
            return jsonify({
                'success': False,
                'error': 'Аниме не найдено'
            }), 404
        
        return jsonify({
            'success': True,
            'data': anime
        })
    except Exception as e:
        logger.error(f"Ошибка API для {title}: {e}")
        return jsonify({
            'success': False,
            'error': 'Внутренняя ошибка сервера'
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    """Обработчик ошибки 404"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Обработчик ошибки 500"""
    logger.error(f"Внутренняя ошибка сервера: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Общий обработчик исключений"""
    logger.error(f"Необработанное исключение: {e}")
    return render_template('errors/500.html'), 500

@app.context_processor
def inject_globals():
    """Внедряет глобальные переменные в шаблоны"""
    return {
        'app_name': 'Anime Catalog',
        'app_version': '1.0.0'
    }

if __name__ == "__main__":
    # Определяем порт для запуска
    port = int(os.environ.get('PORT', 5000))
    
    # Режим отладки только для разработки
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Запуск приложения на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

