from . import loader
Loader = loader.Loader
from .loader_plugins import NpzLoader, BedLoader, Matrix3ColumnsLoader
allowed_loaders = [NpzLoader, BedLoader, Matrix3ColumnsLoader]
allowed_loader_names = list(map(lambda x: x.loader_name, allowed_loaders))
