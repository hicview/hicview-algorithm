import pandas as pd
from . import loader_prototype
from . import loader_plugins_exceptions


class BedLoader(loader_prototype.LoaderPrototype):
    """Documentation for BedLoader

    """
    loader_name = 'bed_loader'
    def __init__(self):
        super(BedLoader, self).__init__()

    
    @classmethod
    def get_loader_name(cls):
        return cls.loader_name

    def check_header(self):
        self.data = pd.read_csv(self.filepath, delimiter='\t')
        if self.data.shape[1] < 3:
            raise loader_plugins_exceptions.HeaderNotInRulesFormatException

    def read_file(self):
        self.data = pd.read_csv(self.filepath, header=None, delimiter='\t')
        col = [i+1 for i in range(self.data.shape[1])]
        col[:3] = ['chromosome', 'start', 'end']
        if len(self.data.columns):
            col[3] = 'bins'
        self.data.columns = col
        self.size = str(self.data.size / (1024**2)) + ".MB"

        
    def load_data(self, filepath):
        self.filepath = filepath
        self.read_file()
        return self.data


        

    ###########################################################################
    #                         External Configurations                         #
    ###########################################################################
    def get_data_meta(self):
        raise NotImplementedError("Loader meta not implemented")
