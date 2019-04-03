import numpy as np
import scipy as sp
from scipy import sparse
from . import loader_prototype
from . import loader_plugins_exceptions


class Matrix3ColumnsLoader(loader_prototype.LoaderPrototype):
    """Documentation for MatrixLoader
    Functions:
    load_hic_matrix: load hic matrix given path
    --------------------
    variables
    self.filepath: data file path
    self.data: converted sparse matrix data
    self.size: sparse matrix data size
    """

    loader_name = 'matrix_3_columns_loader'

    def __init__(self):
        super(Matrix3ColumnsLoader, self).__init__()
        pass

    ###########################################################################
    #                               Class Method                              #
    ###########################################################################
    @classmethod
    def get_loader_name(cls):
        return cls.loader_name

    ###########################################################################
    #                              Core Interface                             #
    ###########################################################################
    # Check .matrix File Header, if the data is in 3 columns
    def check_header(self):
        with open(self.filepath) as f:
            if (len(f.readline().split()) != 3):
                raise loader_plugins_exceptions.HeaderNotInRulesFormatException
            else:
                return True

    # Read .matrix file
    def read_file(self):
        try:
            self.check_header()
        except loader_plugins_exceptions.HeaderNotInRulesFormatException:
            return False
        with open(self.filepath) as f:
            line_num = 0
            for num, line in enumerate(f, 1):
                pass
        line_num = num
        coord_x = np.zeros(line_num, dtype=int)
        coord_y = np.zeros(line_num, dtype=int)
        value = np.zeros(line_num)
        with open(self.filepath) as f:
            for num, line in enumerate(f, 1):
                line_split = line.split()
                coord_x[num - 1], coord_y[num - 1], value[num - 1] = int(
                    line_split[0]), int(line_split[1]), np.float(line_split[2])

        self.data = sparse.coo_matrix((value, (coord_x,
                                                      coord_y))).tocsr()

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


def main():
    loader = Matrix3ColumnsLoader()
    loader.load_data("../../../data/SRR400252_500000.matrix")
    pass


if __name__ == '__main__':
    main()
