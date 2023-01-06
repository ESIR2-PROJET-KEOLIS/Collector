import os
import threading
import time
from sys import stdout
from loguru import logger as log

log.remove()
log.add(stdout, format="{time} {level} {message}", level="INFO")
log.add("../logs/appCollector.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="1 week",
        retention="1 month", level="DEBUG")



#connexion to rabbitMQ


def thread_function(name, type, url, time):
    print("Thread %s: starting", name)
    TheCommand = f'python3 appCollector/AppCollector.py {name} {type} {url} {time}'
    os.system(TheCommand)
    print("Thread %s: finishing", name)


def create_threads():
    threads = []
    time = [10]
    name = ['PositionAllBus']
    type = ['REQUEST']
    url = [
        "\"https://data.explore.star.fr/api/records/1.0/search/?dataset=tco-bus-vehicules-position-tr&q=&rows=1000\""]
    for key, i in enumerate(time):
        threads.append(threading.Thread(target=thread_function, args=(name[key], type[key], url[key], i,)))

    return threads


if __name__ == '__main__':
    log.info("Initial Sleep")
    time.sleep(30)
    log.info("Starting appCollector")
    threads = create_threads()
    for thread in threads:
        thread.start()

    threads[-1].join()
    log.info("Finished appCollector")
