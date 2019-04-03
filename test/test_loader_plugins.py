import unittest
import sys
sys.path.append('..')
from server.resource_map import Matrix3ColumnsLoader
from server.resource_map import NpzLoader
from server.resource_map import BedLoader

class TestLoaderPlugins(unittest.TestCase):


    def test_matrix_3_cols_loader_loading(self):
        loader = Matrix3ColumnsLoader()
        loader.load_data("../data/SRR400252_500000.matrix")
        self.assertEqual(loader.data.shape,(5297,5297),'should return the same size')

    def test_npz_loader_loading(self):
        loader = NpzLoader()
        loader.load_data('../data/SRR400252_500000_sparse.npz')
        self.assertEqual(loader.data.shape, (5297,5297))

    def test_bed_loader_loading(self):
        loader = BedLoader()
        loader.filepath = '../data/SRR400252_500000_abs.bed'
        loader.read_file()
        
if __name__ == '__main__':
    unittest.main()
