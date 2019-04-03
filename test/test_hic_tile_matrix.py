import unittest
import sys
sys.path.append('..')
from server.hic_matrix import HiCTiledMatrix

# class TestHiCTileMatrix(unittest.TestCase):

#    def test_matrix_reading(self):
#        test_mat = HiCTiledMatrix()
#        test_mat.from_text('./data/SRR400252_500000_iced.matrix')
#        print(test_mat.data.tocsr()[103910:103911,203910:203911])
#        try:
#            print(test_mat.data.shape)
#        except AttributeError:
#            pass

#    def test_add_level(self):
#        print('\nTest HiC Matrix Add Level\n')
#        test_mat = HiCTiledMatrix()
#        test_mat.from_text('./data/SRR400252_500000.matrix')
#        test_mat.add_level(10)
#        for i in test_mat.dataLevel:
#            print(i.shape)

