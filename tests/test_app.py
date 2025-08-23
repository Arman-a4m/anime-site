#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тесты для приложения
"""

import json
import pytest
from app import app, catalog

@pytest.fixture
def client():
    """Фикстура для тестового клиента"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'anime' in response.data.lower()

def test_catalog_page(client):
    """Тест страницы каталога"""
    response = client.get('/catalog')
    assert response.status_code == 200
    assert b'catalog' in response.data.lower()

def test_api_anime(client):
    """Тест API для получения списка аниме"""
    response = client.get('/api/anime')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'success' in data
    assert data['success'] is True
    assert 'data' in data
    assert isinstance(data['data'], list)



def test_404_error(client):
    """Тест обработки ошибки 404"""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404

def test_anime_catalog_load():
    """Тест загрузки каталога аниме"""
    anime_list = catalog.get_all_anime()
    assert isinstance(anime_list, list)
    assert len(anime_list) > 0

def test_anime_search():
    """Тест поиска аниме"""
    # Тест поиска по названию
    results = catalog.search_anime(query="naruto")
    assert isinstance(results, list)
    
    # Тест фильтрации по жанру
    results = catalog.search_anime(genre="Action")
    assert isinstance(results, list)
    
    # Тест фильтрации по году
    results = catalog.search_anime(year="2002")
    assert isinstance(results, list)

def test_get_recommendations():
    """Тест получения рекомендаций"""
    anime_list = catalog.get_all_anime()
    if anime_list:
        first_anime = anime_list[0]
        recommendations = catalog.get_recommendations(first_anime)
        assert isinstance(recommendations, list)

if __name__ == '__main__':
    pytest.main([__file__]) 