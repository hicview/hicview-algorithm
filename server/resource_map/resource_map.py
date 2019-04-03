# -*- coding: utf-8 -*-
__author__ = "Hongpeng Ma"
__copyright__ = "Copyright 2019, Michael Q Zhang Lab"
__credits__ = ['Juntao Gao', 'Yongge Li', 'Nadhir']

__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Hongpeng Ma"
__email__ = "mahongpengmars@163.com"
__status__ = "dev"
__date__ = "Mon Jan 14 20:51:09 CST 2019"

from .domain import MDS, NMDS, PM1, PM2
from .domain import Loader
from .domain import Domain_Matrix, Domain_Model3D, Domain_Sequence
from .domain.loader import allowed_loaders, allowed_loader_names
from .resource_map_exceptions import *
import uuid
import queue
from operator import is_not
from functools import partial
from .linker import Resource_Map_Linker
import copy

allowed_algorithms = [MDS, NMDS, PM1, PM2]
get_algorithm = {i.algorithm_name: i for i in allowed_algorithms}

allowed_domain_class = [Domain_Matrix, Domain_Sequence, Domain_Model3D]
get_domain_class = {d.domain_class: d for d in allowed_domain_class}


class Resource_Map_Factory(object):
    '''
    CLASS Resource_Map_Factory
    acts as resource_map factory & manager

    FUNCTIONS
    ----------
    create_resource_map() @classmethod 
    get_resource_map() @classmethod
    get_resource_map_reporsitory() @classmethod
    '''

    def __init__(self):
        super(Resource_Map_Factory).__init__()


class Resource_Map(object):
    '''
    '''

    def __init__(self):
        super(Resource_Map, self).__init__()
        self._generate_uuid()
        self.loaders = {}
        self.link_methods = {}

    def _generate_uuid(self):
        self.uuid = uuid.uuid4().hex

    def construct_resource_map(self, instruction_list):
        constructor = Resource_Map_Constructor()
        constructor.queue_instructions(instruction_list)
        constructor.execute_instructions()
        self.domains = constructor.get_domains().deepcopy()

    def convert_index(self, data, d1_type, d2_type):
        return Resource_Map_Linker.convert_index(data, d1_type, d2_type)
        
    
        #######################################################################
        #                       Resource Map Constructor
        #######################################################################
class Resource_Map_Constructor(object):
    """Documentation for Resource_Map_Constructor

    """

    def __init__(self):
        super(Resource_Map_Constructor, self).__init__()
        self.domains = []
        self.load_instructions = queue.Queue()
        self.generate_instructions = queue.Queue()

    def create_domain_data_by_load(self, domain_class, domain_type,
                                   file_locator, loader_type):
        dm = get_domain_class[domain_class]()
        if domain_type not in list(map(lambda x: x.domain_type, self.domains)):
            dm.set_domain_type(domain_type)
        dm.load_data(file_locator, loader_type)
        return dm

    def create_domain_data_by_generate(self, domain_class, domain_type,
                                       from_domain_type, algorithm):
        dm = get_domain_class[domain_class]()
        if domain_type not in list(map(lambda x: x.domain_type, self.domains)):
            dm.set_domain_type(domain_type)
        existed_dm = {d.domain_type: d for d in self.domains}
        try:
            from_dm = existed_dm[from_domain_type]
        except Exception:
            raise Exception('Required domain not loaded')
        _alg = get_algorithm[algorithm]
        dm.generate_data(from_dm.loader.data, _alg)
        return dm

    def queue_instructions(self, instruction_list):
        for ins in instruction_list:
            if ins[0] == 'load' and len(ins) == 5:
                self.load_instructions.put(ins[1:])
            elif ins[0] == 'generate' and len(ins) == 5:
                self.generate_instructions.put(ins[1:])
            else:
                raise Warning('Cannot parse instructions')

    def execute_instructions(self):
        while not self.load_instructions.empty():
            domain_class, domain_type, file_locator, loader_type = self.load_instructions.get(
            )
            self.domains.append(
                self.create_domain_data_by_load(domain_class, domain_type,
                                                file_locator, loader_type))
        while not self.generate_instructions.empty():
            domain_class, domain_type, from_domain_type, algorithm = self.generate_instructions.get(
            )
            self.domains.append(
                self.create_domain_data_by_generate(
                    domain_class, domain_type, from_domain_type, algorithm))
    
    def get_domain_by_type(self, domain_type):
        return {d.domain_type: d for d in self.domains}[domain_type]

    def get_domains(self):
        return self.domains
