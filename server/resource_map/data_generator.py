from loader.loader_plugins import NpzLoader
from algorithms import MDS, NMDS, PM1, PM2
allowed_loaders = [NpzLoader]
allowed_algorithms = [MDS, NMDS, PM1, PM2]


###############################################################################
#             Todo: Generate new data given data & generate rules             #
###############################################################################
class Generator(object):
    """Documentation for Generator

    """
    '''
    Rules
    ----------
    {
      'algorithms':{
          'mds':MDS,
          ...
        }
      }
      ...
    }
    '''
    allowed_algorithms_name = list(
        map(lambda x: x.loader_name, allowed_algorithms))
    allowed_rules = {}
    for l in allowed_loaders:
        allowed_rules[l.loader_name] = {}
        allowed_rules[l.loader_name]['loader_plugins'] = l
        for alg in allowed_algorithms:
            allowed_rules[l.loader_name][alg.algorithm_name] = alg

    def __init__(self, args):
        super(Generator, self).__init__()
        self.args = args

    @classmethod
    def get_generate_rules(cls):
        return cls.allowed_rules

    '''
    get_generate_rules_info
        return required generate rules info 
    
    RETURN
    ----------
    loader_dtype: required data loader as the input data
    algorithms_identifier: required algorithm applyied on the input data
    '''

    @classmethod
    def get_generate_rules_info(cls, generate_rules):
        return (NpzLoader,
                Generator.allowed_rules['algorithms'][generate_rules])

    def generate_data(self, loader, alg):
        data = loader.data
        new_data = alg()
