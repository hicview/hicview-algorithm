class NotImplementedException(Exception):
    pass

class Domain_Base(object):
    """Documentation for Domain_Base

    """
    domain_class = 'domain_base'
    def __init__(self):
        super(Domain_Base, self).__init__()

    def set_domain_type(self):
        raise NotImplementedException
    
    def load_data(self, file_locator, loader):
        raise NotImplementedException

    def generate_data(self, file_locator, loader, algorithm):
        raise NotImplementedException
