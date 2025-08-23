#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Конфигурация приложения
"""

import os
from typing import Dict, Any

class Config:
    """Базовая конфигурация"""
    
    # Основные настройки
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Настройки безопасности
    SESSION_COOKIE_SECURE = False  # True для HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Настройки логирования
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Пути к файлам
    ANIME_DATA_FILE = os.environ.get('ANIME_DATA_FILE', 'templates/anime.json')
    
    # Настройки кэширования
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Настройки API
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '100 per minute')
    
    @staticmethod
    def init_app(app):
        """Инициализация приложения"""
        pass

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    
    DEBUG = True
    TESTING = False
    
    # Настройки безопасности для разработки
    SESSION_COOKIE_SECURE = False
    
    # Дополнительные настройки для разработки
    TEMPLATES_AUTO_RELOAD = True

class TestingConfig(Config):
    """Конфигурация для тестирования"""
    
    TESTING = True
    DEBUG = False
    
    # Используем тестовую базу данных
    ANIME_DATA_FILE = 'tests/test_anime.json'
    
    # Отключаем CSRF для тестов
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    
    DEBUG = False
    TESTING = False
    
    # Настройки безопасности для продакшена
    SESSION_COOKIE_SECURE = True
    
    # Настройки логирования
    LOG_LEVEL = 'WARNING'
    
    # Настройки кэширования
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')

class StagingConfig(Config):
    """Конфигурация для staging"""
    
    DEBUG = False
    TESTING = False
    
    # Настройки безопасности
    SESSION_COOKIE_SECURE = True
    
    # Настройки логирования
    LOG_LEVEL = 'INFO'

# Словарь конфигураций
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'staging': StagingConfig,
    'default': DevelopmentConfig
}

def get_config() -> Config:
    """Получает конфигурацию на основе переменной окружения"""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default']) 