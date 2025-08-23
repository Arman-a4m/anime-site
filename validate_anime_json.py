#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anime JSON Validator
Проверяет валидность и качество данных в anime.json файле
"""

import json
import sys
from typing import Dict, List, Any

def validate_anime_json(file_path: str) -> bool:
    """
    Валидирует JSON файл с данными об аниме
    
    Args:
        file_path (str): Путь к JSON файлу
        
    Returns:
        bool: True если файл валиден, False в противном случае
    """
    try:
        # Загружаем JSON файл
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ JSON файл успешно загружен")
        print(f"📊 Количество записей: {len(data)}")
        
        # Проверяем структуру каждой записи
        required_fields = [
            'id', 'title', 'title_original', 'title_english', 
            'genre', 'year', 'status', 'studio', 'episodes', 
            'duration', 'age_rating', 'rating', 'description'
        ]
        
        optional_fields = [
            'season', 'characters', 'poster', 'trailers', 
            'source', 'aired', 'broadcast', 'licensors', 
            'producers', 'director', 'music'
        ]
        
        errors = []
        warnings = []
        
        for i, anime in enumerate(data):
            # Проверяем обязательные поля
            for field in required_fields:
                if field not in anime:
                    errors.append(f"Запись {i+1}: Отсутствует обязательное поле '{field}'")
                elif anime[field] is None:
                    errors.append(f"Запись {i+1}: Поле '{field}' не может быть null")
            
            # Проверяем типы данных
            if 'id' in anime and not isinstance(anime['id'], int):
                errors.append(f"Запись {i+1}: Поле 'id' должно быть числом")
            
            if 'title' in anime and not isinstance(anime['title'], str):
                errors.append(f"Запись {i+1}: Поле 'title' должно быть строкой")
            
            if 'genre' in anime and not isinstance(anime['genre'], list):
                errors.append(f"Запись {i+1}: Поле 'genre' должно быть массивом")
            
            if 'year' in anime and not isinstance(anime['year'], int):
                errors.append(f"Запись {i+1}: Поле 'year' должно быть числом")
            
            if 'episodes' in anime and not isinstance(anime['episodes'], int):
                errors.append(f"Запись {i+1}: Поле 'episodes' должно быть числом")
            
            if 'rating' in anime:
                if not isinstance(anime['rating'], (int, float)):
                    errors.append(f"Запись {i+1}: Поле 'rating' должно быть числом")
                elif anime['rating'] < 0 or anime['rating'] > 10:
                    warnings.append(f"Запись {i+1}: Рейтинг должен быть от 0 до 10")
            
            # Проверяем уникальность ID
            if 'id' in anime:
                id_count = sum(1 for a in data if a.get('id') == anime['id'])
                if id_count > 1:
                    errors.append(f"Запись {i+1}: Дублирующийся ID {anime['id']}")
        
        # Выводим результаты
        if errors:
            print(f"\n❌ Найдено ошибок: {len(errors)}")
            for error in errors:
                print(f"   {error}")
            return False
        
        if warnings:
            print(f"\n⚠️  Найдено предупреждений: {len(warnings)}")
            for warning in warnings:
                print(f"   {warning}")
        
        print(f"\n✅ Валидация завершена успешно!")
        print(f"📈 Статистика:")
        print(f"   - Всего записей: {len(data)}")
        print(f"   - Уникальных ID: {len(set(a.get('id') for a in data))}")
        print(f"   - Средний рейтинг: {sum(a.get('rating', 0) for a in data) / len(data):.2f}")
        
        # Анализ жанров
        all_genres = []
        for anime in data:
            if 'genre' in anime:
                all_genres.extend(anime['genre'])
        
        genre_counts = {}
        for genre in all_genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        print(f"   - Популярные жанры:")
        for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"     {genre}: {count}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Файл {file_path} не найден")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def main():
    """Основная функция"""
    file_path = "templates/anime.json"
    
    print("🔍 Валидация anime.json файла...")
    print("=" * 50)
    
    success = validate_anime_json(file_path)
    
    if success:
        print("\n🎉 Файл прошел все проверки!")
        sys.exit(0)
    else:
        print("\n💥 Файл содержит ошибки!")
        sys.exit(1)

if __name__ == "__main__":
    main() 