from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from template_functions import size_adapter, time_adapter, sec_left, percent

app = Flask(__name__)
app.config.from_object(Config)

bootstap = Bootstrap(app)

app.jinja_env.filters['size_adapter'] = size_adapter
app.jinja_env.filters['time_adapter'] = time_adapter
app.jinja_env.filters['sec_left'] = sec_left
app.jinja_env.filters['percent'] = percent

from app import routes, errors
