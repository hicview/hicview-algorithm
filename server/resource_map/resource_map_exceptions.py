
class ResourceMapException(Exception):
    pass

class LoadDataException(ResourceMapException):
    pass

class GenerateDataException(ResourceMapException):
    pass

class LinkDataException(ResourceMapException):
    pass
