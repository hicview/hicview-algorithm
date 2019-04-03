import unittest
import sys
sys.path.append('..')
from server.resource_map import Loader
from server.resource_map import NpzLoader, BedLoader

class TestLoader(unittest.TestCase):
    def test_loader_read_file(self):
        a = Loader()
        a.load_data('../data/SRR400252_500000.matrix','matrix_3_columns_loader')
        self.assertEqual(a.data.shape, (5297, 5297))

    def test_loader_write_npz_file(self):
        loader = Loader()
        loader.load_data("../data/SRR400252_500000.matrix",'matrix_3_columns_loader')
        from tempfile import NamedTemporaryFile
        outfile = NamedTemporaryFile(mode='w',suffix='.npz')
        print(outfile.name)
        loader.write_data(outfile.name, suffix=False)
        outfile.seek(0)
        loader_y = NpzLoader()
        loader_y.load_data(outfile.name)
        outfile.close()
        self.assertEqual(loader.data.shape, loader_y.data.shape)

    def test_loader_write_bed_file(self):
        loader = Loader()
        loader.load_data("../data/SRR400252_500000_abs.bed",'bed_loader')
        from tempfile import NamedTemporaryFile
        outfile = NamedTemporaryFile(mode='w',suffix='.bed')
        print(outfile.name)
        loader.write_data(outfile.name, suffix=False, method='bed')
        outfile.seek(0)
        loader_z = BedLoader()
        loader_z.load_data(outfile.name)
        outfile.close()
        self.assertEqual(loader.data.shape, loader_z.data.shape)

if __name__ == '__main__':
    unittest.main()
