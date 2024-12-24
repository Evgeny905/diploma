import sqlite3
from flask import g
from Flask.main import app
def connect_db():
    """Соединяет с указанной базой данных."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    """Если ещё нет соединения с базой данных, открыть новое - для текущего контекста приложения"""
    if not hasattr(g, 'Predictions_base.db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db