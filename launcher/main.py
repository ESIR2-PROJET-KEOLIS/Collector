from loguru import logger as log

log.add("../logs/appCollector.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="1 week",
        retention="1 month", level="DEBUG")

if __name__ == '__main__':
    log.info("Starting appCollector")
    log.info("Finished appCollector")
