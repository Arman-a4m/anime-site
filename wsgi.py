#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI entry point для продакшена
"""

import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == "__main__":
    app.run() 