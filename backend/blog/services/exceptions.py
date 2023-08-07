class ServiceException(Exception):
    """Appears when some suspicious error is happening in app logics"""
    def __init__(self, payload, **kwargs):
        self.kwargs = kwargs
        self.message = self.get_message(payload)
        # logger.error(self.message) IMPLEMENT LOGGING LATER!
        super(ServiceException, self).__init__(self.message)

    @staticmethod
    def get_message(payload):
        return f'Database operation error occurred. Payload: {payload}.'


class InvalidJWTException(ServiceException):
    """Appears when jwt user can not be decoded"""

    def get_message(self, payload):
        return f'Unable to get user data from jwt token. Detail: {payload}'
