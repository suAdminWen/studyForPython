import time
from . import app


@app.task
def add(x, y):
    time.sleep(2)
    return x + y
