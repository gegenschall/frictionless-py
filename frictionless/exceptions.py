class FrictionlessException(Exception):
    """Main Frictionless exception

    # Arguments
        error

    """

    def __init__(self, error):
        self.__error = error
        super().__init__(self.__error.message)

    @property
    def error(self):
        return self.__error
