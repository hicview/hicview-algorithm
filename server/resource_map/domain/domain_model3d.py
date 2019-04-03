from .domain_base import Domain_Base
from .loader import Loader


class Domain_Model3D(Domain_Base):
    """Documentation for Domain_Model3D

    """
    domain_class = 'domain_model3d'

    def __init__(self):
        super(Domain_Model3D, self).__init__()

    def set_domain_type(self, domain_type):
        self.domain_type = domain_type

    def create_npz_loader(self):
        self.loader = Loader()
        self.loader.dtype = 'npz_loader'
        self.loader.loader_modules = self.loader._get_loader(self.loader.dtype)
        self.loader.data = self.data

    def load_data(self, file_locator, loader_type):
        self.loader = Loader()
        self.loader.load_data(file_locator, loader_type)
        self.data = self.loader.data

    def generate_data(self, *args, **kwargs):
        if len(args) + len(kwargs.keys()) == 3:
            self.generate_data_from_loader(*args, **kwargs)
        elif len(args) + len(kwargs.keys()) == 2:
            self.generate_data_from_ndarray(*args, **kwargs)
        else:
            raise Exception(
                'The number of Arguments is not in range, you got ',
                len(args) + len(kwargs.keys()), 'args')

    def generate_data_from_loader(self, file_locator, loader_type, algorithm):
        self.from_loader = Loader()
        self.from_loader.load_data(file_locator, loader_type)
        self.from_data = self.from_loader.data
        self.alg = algorithm()
        self.data = self.alg.fit(self.from_data)
        self.create_npz_loader()

    def generate_data_from_ndarray(self, arr, algorithm):
        self.from_data = arr
        self.alg = algorithm()
        self.data = self.alg.fit(self.from_data)
        self.create_npz_loader()
