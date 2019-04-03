from . import loader_plugins
from . import loader_exceptions
import numpy as np
from scipy import sparse
from operator import is_not
from functools import partial
import pandas as pd
Matrix3ColumnsLoader = loader_plugins.Matrix3ColumnsLoader
NpzLoader = loader_plugins.NpzLoader
BedLoader = loader_plugins.BedLoader
allowed_loaders = [Matrix3ColumnsLoader, NpzLoader, BedLoader]


class Loader(object):
    """Documentation for Loader

    """
    ###########################################################################
    #                               Class Methods                             #
    ###########################################################################
    @classmethod
    def get_loader_module(
            cls, loader_name='matrix_3_columns_loader'
    ):  # Default Loader, change when new loaders are added
        allowed_loader_name = list(map(lambda x:x.loader_name, allowed_loaders))
        if loader_name in allowed_loader_name:
            loader = list(filter(
                partial(is_not, None),
                list(
                    map(
                        (lambda x:x if x.loader_name == loader_name else None),
                        allowed_loaders
                    )
                )
            ))[0]
            loader = loader()
        else:
            raise loader_exceptions.LoaderNotFoundException
        return loader

    @classmethod
    def get_allowed_loader_module(cls):
        return [i.loader_name for i in allowed_loaders]

    @classmethod
    def get_new_loader(cls):
        return Loader()

    ###########################################################################
    #                             Instance Methods                            #
    ###########################################################################

    def __init__(self):
        super(Loader, self).__init__()

    def _get_loader(self, dtype):
        return Loader.get_loader_module(dtype)

    def load_data(self, filepath, dtype):
        self.filepath = filepath
        self.dtype = dtype
        self.loader_modules = self._get_loader(self.dtype)
        self.data = self.loader_modules.load_data(filepath)
        self.data_size = self.loader_modules.size
        try:
            self.data_meta = self.loader_modules.get_data_meta()
        except NotImplementedError:
            self.data_meta = {}

    def get_loader_data_format(self):
        return self.dtype

    def get_data(self):
        return self.data

    def get_data_size(self):
        return self.data_size

    def get_data_meta(self):
        return self.data_meta

    def write_data(self, file_locator,suffix=True, method='npz'):
        if method == 'npz':
            if not sparse.issparse(self.data):
                if suffix:
                    file_locator += '_compressed.npz'
                np.savez_compressed(
                    file_locator,self.data)
            else:
                if suffix:
                    file_locator += '_sparse.npz'
                sparse.save_npz(file_locator, self.data)
                
        if method == 'bed':
            if suffix:
                file_locator +='.bed'
            self.data.to_csv(path_or_buf=file_locator,sep='\t', header=False, index=False)
            # np.savetxt(file_locator, self.data.values, delimiter='\t')

        self.filepath = file_locator
                

def main():
    a = Loader()
    a.load_data('../../../data/SRR400252_500000.matrix','matrix_3_columns_loader')
    print(a.loader_modules)
    a.write_data('/Users/k/PrivateHub/hic3dviewer-web/data/SRR400252_500000')


if __name__ == '__main__':
    main()
