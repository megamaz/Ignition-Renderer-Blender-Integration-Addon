class BaseIgnitionException(Exception):
    pass


class NotAnIgnitionFile(BaseIgnitionException):
    '''Raised when the specified file is not a .ignition file'''