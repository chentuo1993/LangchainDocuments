from distutils.log import log
from rocketry.conds import after_success, every
from fastapi import Request
from fastapi.responses import HTMLResponse
from pathlib import Path
import logging
import rutils

# setup logging in DEBUG mode
log_file = Path("./logs/rutils.log")
log_file.parent.mkdir(exist_ok=True, parents=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)

# create the scheduler
scheduler = rutils.Scheduler()

# Runs this task at startup and every 30 seconds
@scheduler.task(start_cond=every("30 seconds"))
def start():
    logging.info(f"Starting stage 1")

# Runs this task after the start task has been successfully executed and every 10 seconds.
@scheduler.task(start_cond=after_success(start) | every("10 seconds"))
def polling():
    logging.info("Polling")

# Serve a UI page at 0.0.0.0:8000/hello using FastAPI
@scheduler.hook(path="/hello")
def hello(request: Request):
    return HTMLResponse(f"<h1>Hello</h1>")

if __name__ == "__main__":
    # Gives the tasks.py script a command line interface
    scheduler.cli()