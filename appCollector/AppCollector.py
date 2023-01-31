from sys import argv, stdout
from time import sleep
from RequestCollector import RequestCollector
from loguru import logger as log

import pika


def setup_logger():
    log.remove()
    log.add(stdout, format="{time} {level} {message}", level="INFO")
    log.add(f"../logs/{argv[1]}Collector.log",
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            rotation="1 week",
            retention="1 month", level="DEBUG")


def main(name, collector, time=-1):
    log.info("create rabbitmq queue")
    isNotConnected = True
    while isNotConnected:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue=name, durable=True)
            isNotConnected = False
        except Exception as e:
            log.error(e)
            log.info("Waiting for rabbitmq to be ready")
            sleep(1)


    log.info(f"Starting appCollector : {name} with {time}s interval")
    while True:
        # Get Data API with request
        data = collector.get_response()
        log.debug("Data received")

        channel.basic_publish(exchange='', routing_key=name, body=str(data))
        log.debug("Data sent to rabbitMQ")

        if time == -1:
            break
        sleep(int(time))
    connection.close()


def verifArg(tab_argv):
    collectorType = ["REQUEST", "CURL"]
    if len(tab_argv) < 4 or len(tab_argv) > 5:
        log.error("Wrong number of arguments")
        log.info(
            "Usage : python3 AppCollector.py <name> <type> <url> <time> or python3 AppCollector.py <name> <url>")
        log.info(
            "Example : python3 AppCollector.py weather REQUEST https://api.openweathermap.org/data/2.5/weather?q=Paris&appid=1234567890 60")
        log.info("help : python3 AppCollector.py help")
        exit(1)
    elif len(tab_argv) == 5:
        if not tab_argv[4].isdigit():
            log.error("Time must be a digit")
            exit(1)
        elif tab_argv[2] not in collectorType:
            log.error("Collector type not found")
            exit(1)
    elif len(tab_argv) == 4:
        if tab_argv[2] not in collectorType:
            log.error("Collector type not found")
            exit(1)


def collector_choice(collector_type):
    if collector_type == "REQUEST":
        return RequestCollector(argv[3])
    elif collector_type == "CURL":
        raise NotImplementedError


def help():
    log.info(
        "Usage : python3 AppCollector.py <name> <type> <url> <time> or python3 AppCollector.py <name> <type> <url>")
    log.info("<name> : name of the collector")
    log.info("<type> : type of the collector")
    log.info("<url> : url of the API")
    log.info("<time> : time between each request in seconds")
    log.info(
        "Example : python3 AppCollector.py weather REQUEST https://api.openweathermap.org/data/2.5/weather?q=Paris&appid=1234567890 60")

    exit(0)


if __name__ == '__main__':
    if len(argv) == 1:
        print("No argument")
        print("Do the following command : python3 AppCollector.py help")
        exit(1)
    setup_logger()
    if argv[1] == "help":
        help()
    verifArg(argv)
    collector = collector_choice(argv[2])
    if len(argv) == 5:
        main(argv[1], collector, int(argv[4]))
    else:
        main(argv[1], collector)
