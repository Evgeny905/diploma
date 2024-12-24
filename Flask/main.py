from flask import Flask

# Создаём наше маленькое приложение
app = Flask(__name__)
app.config.from_object(__name__)