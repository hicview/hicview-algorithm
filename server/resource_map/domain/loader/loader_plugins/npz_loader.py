import numpy as np
from scipy import sparse
from . import loader_prototype
from . import loader_plugins_exceptions


class NpzLoader(loader_prototype.LoaderPrototype):
    """Documentation for NpzLoader

    """
    loader_name = 'npz_loader'

    def __init__(self):
        super(NpzLoader, self).__init__()

    ###########################################################################
    #                              Class Methods                              #
    ###########################################################################
    @classmethod
    def get_loader_name(cls):
        return cls.loader_name

    ###########################################################################
    #                              Core Interface                             #
    ###########################################################################
    def check_header(self):
        if self.filepath[-4] != '.npz':
            raise loader_plugins_exceptions.HeaderNotInRulesFormatException
        try:
            with open(self.filepath) as f:
                pass
        except Exception:
            raise loader_plugins_exceptions.FileCannotOpenException

    def read_file(self):
        if 'compressed' in self.filepath:
            self.data = np.load(self.filepath)
        elif 'sparse' in self.filepath:
            self.data = sparse.load_npz(self.filepath)
        else:
            # Default load npz methods
            self.data = sparse.load_npz(self.filepath)
        self.size = str(self.data.size / (1024**2)) + ".MB"
        return True

    def load_data(self, filepath):
        self.filepath = filepath
        self.read_file()
        return self.data
        

    ###########################################################################
    #                         External Configurations                         #
    ###########################################################################
    def get_data_meta(self):
        raise NotImplementedError("Loader meta not implemented")
    
