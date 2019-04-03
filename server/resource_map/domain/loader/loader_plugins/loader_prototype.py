class LoaderPrototype(object):
    """Documentation for LoaderPrototype
    Interface for data loader
    """
    # Class
    loader_name = 'loader prototype'

    def __init__(self):
        super(LoaderPrototype, self).__init__()

    @classmethod
    def get_loader_name(cls):
        return cls.loader_name

    def check_header(self):
        raise NotImplementedError('check_header must be overwritten')

    def read_file(self):
        raise NotImplementedError('read_file must be overwritten')

    def load_data(self, path):
        raise NotImplementedError('load_data must be overwritten')
