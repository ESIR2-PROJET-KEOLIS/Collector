import json
import os
import threading
from sys import stdout
from loguru import logger as log

log.remove()
log.add(stdout, format="{time} {level} {message}", level="INFO")
log.add("../logs/appCollector.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="1 week",
        retention="1 month", level="DEBUG")


# connexion to rabbitMQ


def thread_function(name, type, url, time):
    log.info("Thread %s: starting", name)
    PROD = os.environ.get('PROD')
    if PROD == "True":
        log.info("PROD")
        TheCommand = f'python3 appCollector/AppCollector.py {name} {type} {url} {time}'
        log.info(os.system(TheCommand))
        log.info(TheCommand)
    else:
        log.info("DEV")
        TheCommand = f'python3 ../appCollector/AppCollector.py {name} {type} {url} {time}'
        log.info(os.system(TheCommand))
        log.info(TheCommand)

    os.system(TheCommand)
    log.info("Thread %s: finishing", name)


def create_threads():
    PROD = os.environ.get('PROD')
    if PROD == "True":
        path = "./launcher/"
    else:
        path = ""

    threads = []
    with open(path + "config.json", "r") as f:
        data = json.load(f)
        for collector in data["collectors"]:
            log.info(collector["name"], collector["type"], collector["url"], collector["time"])
            threads.append(threading.Thread(target=thread_function, args=(
                collector["name"],
                collector["type"],
                collector["url"],
                collector["time"],)))
    return threads


if __name__ == '__main__':
    log.info("Starting appCollector")
    threads = create_threads()
    for thread in threads:
        thread.start()

    threads[-1].join()
    log.info("Finished appCollector")
