from requests import request
from CollectorInterface import CollectorInterface
from loguru import logger as log


class RequestCollector(CollectorInterface):

    def __init__(self, url):
        super().__init__()
        self.__url = url

    def __send_request(self):
        log.info(f"GET request to {self.__url}")
        try:
            response = request("GET", self.__url)
            response.raise_for_status()
            log.debug(response.text)
        except Exception as e:
            log.error(e)
            return {}
        else:
            log.info(f"Response status code: {response.status_code}")
            log.debug(f"Response content: {response.content}")
            return response.json()

    def get_response(self):
        return self.__send_request()
