import unittest
import sys
sys.path.append('..')
from server.resource_map.domain import Domain_Sequence, Domain_Matrix, Domain_Model3D
from server.resource_map import MDS
import numpy as np

class TestDomain(unittest.TestCase):

    def test_domain_sequence_load(self):
        ds = Domain_Sequence()
        ds.load_data("../data/SRR400252_500000_abs.bed",'bed_loader')
        self.assertEqual(ds.data.shape, (5322,4))

    def test_domain_matrix_load(self):
        dm = Domain_Matrix()
        dm.load_data('../data/SRR400252_500000.matrix','matrix_3_columns_loader')
        self.assertEqual(dm.data.shape, (5297, 5297))

    def test_domain_model3d_load(self):
        # TODO
        pass

    def test_domain_model3d_generate(self):
        from_data = np.random.randint(100000, size=30).reshape(-1, 3)
        dm3 = Domain_Model3D()
        dm3.generate_data_from_ndarray(from_data, MDS)
        self.assertEqual(dm3.data.shape, (10,3))
        # assertEqual(dm3.data.shape)
