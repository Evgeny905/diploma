from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3
import os
import random

# конфигурация
DATABASE = '/Fastapi.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# создаём наше маленькое приложение
app = Flask(__name__)
app.config.from_object(__name__)

# Загружаем конфиг по умолчанию и переопределяем в конфигурации часть значений через переменную окружения
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'Fastapi.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
def connect_db():
    """Соединяеет с указанной базой данных."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def get_db():
    """Если ещё нет соединения с базой данных, открыть новое - для
    текущего контекста приложения
    """
    if not hasattr(g, 'Fastapi.db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
@app.route('/')
def Main_Page():
    return render_template('Fastapi_Flask/main_page.html')
@app.route('/predictions')
def Predictions():
    return render_template('Fastapi_Flask/predictions.html')
@app.route('/viewing')
def Viewing():
    db = get_db()
    cur = db.execute("SELECT * FROM predictions")
    predictions = cur.fetchall()
    return render_template('Fastapi_Flask/viewing.html', Predictions = predictions)
@app.route('/prediction')
def Predictions_Random():
    db = get_db()
    cur = db.execute("SELECT * FROM predictions")
    predictions = cur.fetchall()
    return render_template('Fastapi_Flask/prediction.html', Prediction = predictions[random.randint(0,len(predictions)-1)])

if __name__ == '__main__':
    app.run()
