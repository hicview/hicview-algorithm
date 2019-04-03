import unittest
import sys
sys.path.append('..')
from server.resource_map import Resource_Map_Constructor
from server.resource_map import Resource_Map_Linker

class TestResourceMapLinker(unittest.TestCase):
    def test_infer_link_method(self):
        d1 = 'bed'
        d2 = 'model_3d'
        d = Resource_Map_Linker.infer_link_method(d1,d2,test=True)
        self.assertEqual(list(d), ['linker_bed_to_matrix', 'linker_matrix_to_model_3d'])
        d1= 'model_3d'
        d2 = 'bed'
        d = Resource_Map_Linker.infer_link_method(d1,d2,test=True)
        self.assertEqual(list(d), ['linker_model_3d_to_matrix', 'linker_matrix_to_bed'])
        d1= 'matrix'
        d2 = 'bed'
        d = Resource_Map_Linker.infer_link_method(d1,d2,test=True)
        self.assertEqual(list(d), ['linker_matrix_to_bed'])
        
