class ServiceError(Exception):
    """
    Generic Error for any handled errors
    """

    pass


class ModelError(ServiceError):
    """
    For any errors that occur in the model
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "{}".format(self.message)


class InputError(ServiceError):
    """
    For any errors with the input payload validation
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "{}".format(self.message)
