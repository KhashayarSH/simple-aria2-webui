from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from template_functions import size_adapter, time_adapter, sec_left, percent
from custom_queue import QueueHandler
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(Config)

queue_handler = QueueHandler()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

INTERVAL_TASK_ID = 'interval-task-id'

from download_manager_functions import queue_player

scheduler.add_job(id=INTERVAL_TASK_ID, func=queue_player, trigger='interval', seconds=30)
bootstap = Bootstrap(app)

app.jinja_env.filters['size_adapter'] = size_adapter
app.jinja_env.filters['time_adapter'] = time_adapter
app.jinja_env.filters['sec_left'] = sec_left
app.jinja_env.filters['percent'] = percent

from app import routes, errors
