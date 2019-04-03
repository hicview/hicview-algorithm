from .domain_base import Domain_Base
from .loader import Loader


class Domain_Matrix(Domain_Base):
    """Documentation for Domain_Matrix

    """
    domain_class = 'domain_matrix'
    def __init__(self):
        super(Domain_Matrix, self).__init__()
            
    def set_domain_type(self, domain_type):
        self.domain_type = domain_type

    def load_data(self, file_locator, loader_type):
        self.loader = Loader()
        self.loader.load_data(file_locator, loader_type)
        self.data = self.loader.data

