from flask import Flask
from .views.routes import routes


app = Flask(__name__)

app.register_blueprint(routes)
