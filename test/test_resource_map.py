import unittest
import sys
sys.path.append('..')
from server.resource_map import Resource_Map_Constructor
from server.resource_map import MDS
from server.resource_map.domain import Domain_Model3D, Domain_Matrix
from server.resource_map.domain import Loader
import numpy as np

class TestResourceMap(unittest.TestCase):
    def test_rm_create_domain_by_load(self):
        constructor = Resource_Map_Constructor()
        dm = constructor.create_domain_data_by_load('domain_sequence',
                                               'bed_file',
                                               "../data/SRR400252_500000_abs.bed",
                                               'bed_loader')
        self.assertEqual(dm.domain_class, 'domain_sequence')
        self.assertEqual(dm.domain_type, 'bed_file')
        self.assertEqual(dm.data.shape, (5322, 4))

    def test_rm_create_domain_by_generate(self):
        # Mock a domain data loaded constructor
        constructor = Resource_Map_Constructor()
        from_data = np.random.randint(100000, size=30).reshape(-1, 3)
        from_dm = Domain_Matrix()
        from_dm.loader = Loader()
        from_dm.loader.data = from_data
        from_dm.domain_type = 'matrix'
        constructor.domains.append(from_dm)
        
        dm = constructor.create_domain_data_by_generate('domain_model3d',
                                                        'model_3d',
                                                        'matrix',
                                                        'mds')
        self.assertEqual(dm.data.shape, (10,3))
        self.assertEqual(dm.from_data.all(), from_data.all())
        self.assertEqual(dm.domain_class,'domain_model3d')
        self.assertEqual(dm.domain_type, 'model_3d')

    def test_rm_queue_instructions(self):
        instructions = [['load','domain_sequence', 'bed_file',
                         "../data/SRR400252_500000_abs.bed", 'bed_loader'],
                        ['generate','domain_model3d','model_3d',
                         'matrix','mds']]
        constructor = Resource_Map_Constructor()
        constructor.queue_instructions(instructions)
        self.assertEqual(['domain_sequence', 'bed_file',
                         "../data/SRR400252_500000_abs.bed", 'bed_loader'],
                         constructor.load_instructions.get())
        self.assertEqual(['domain_model3d','model_3d',
                          'matrix','mds'],
                         constructor.generate_instructions.get())

    def test_rm_execute_instructions(self):
        # Mock matrix domain in Constructor
        constructor = Resource_Map_Constructor()
        from_data = np.random.randint(100000, size=30).reshape(-1, 3)
        from_dm = Domain_Matrix()
        from_dm.loader = Loader()
        from_dm.loader.data = from_data
        from_dm.domain_type = 'matrix'
        constructor.domains.append(from_dm)
        
        instructions = [['load','domain_sequence', 'bed_file',
                         "../data/SRR400252_500000_abs.bed", 'bed_loader'],
                        ['generate','domain_model3d','model_3d',
                         'matrix','mds']]
        constructor.queue_instructions(instructions)
        constructor.execute_instructions()
        self.assertEqual(len(constructor.domains), 3)
        dm = constructor.get_domain_by_type('bed_file')
        self.assertEqual(dm.domain_class, 'domain_sequence')
        self.assertEqual(dm.domain_type, 'bed_file')
        self.assertEqual(dm.data.shape, (5322, 4))
        dm1 = constructor.get_domain_by_type('model_3d')
        self.assertEqual(dm1.data.shape, (10,3))
        self.assertEqual(dm1.from_data.all(), from_data.all())
        self.assertEqual(dm1.domain_class,'domain_model3d')
        self.assertEqual(dm1.domain_type, 'model_3d')
        
