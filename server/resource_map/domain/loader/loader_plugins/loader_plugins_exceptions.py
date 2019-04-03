class LoaderException(Exception):
    pass


class HeaderNotInRulesFormatException(LoaderException):
    pass

class FileCannotOpenException(LoaderException):
    pass
