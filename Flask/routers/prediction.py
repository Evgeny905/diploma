from flask import Flask, render_template
import random
import os
from Flask.backend.db import get_db
from Flask.main import app

# Загружаем конфигурацию по умолчанию и переопределяем в конфигурации часть значений через переменную окружения
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'Predictions_base.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
@app.route('/')
def Main_Page():
    return render_template('main_page.html')
@app.route('/predictions')
def Predictions():
    return render_template('predictions.html')
@app.route('/viewing')
def Viewing():
    db = get_db()
    cur = db.execute("SELECT * FROM predictions")
    predictions = cur.fetchall()
    return render_template('viewing.html', Predictions = predictions)
@app.route('/prediction')
def Predictions_Random():
    db = get_db()
    cur = db.execute("SELECT * FROM predictions")
    predictions = cur.fetchall()
    return render_template('prediction.html',
                           Prediction = predictions[random.randint(0,len(predictions)-1)])
if __name__ == '__main__':
    app.run()