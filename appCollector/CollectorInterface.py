class CollectorInterface(object):

    def get_response(self) -> dict:
        """Return a dictionary with the response"""
        raise NotImplementedError

    def __send_request(self) -> dict:
        """Return the request"""
        raise NotImplementedError
