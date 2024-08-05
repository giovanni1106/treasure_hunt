import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


command = BASE_DIR + "/.venv/bin/gunicorn"
pythonpath = BASE_DIR
bind = "0.0.0.0:8000"
workers = 3
