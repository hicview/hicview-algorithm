import numpy as np
from scipy import sparse
from server.resource_map.domain.loader import Matrix3ColumnsLoader, BedLoader
import h5py as h5


class HiCTiledMatrix(object):
    """Documentation for HiCTiledMatrix

    """

    def __init__(self):
        super(HiCTiledMatrix, self).__init__()
        self.zoomLevel = []
        self.dataLevel = []

    def _check_header(self, path):
        with open(path) as f:
            if (len(f.readline().split()) != 3):
                raise Exception('Header Not Allowed')
            else:
                return True

    def _read_file(self, path):
        try:
            self._check_header(path)
        except Exception:
            return False
        with open(path) as f:
            line_num = 0
            for num, line in enumerate(f, 1):
                pass
        line_num = num
        coord_x = np.zeros(line_num, dtype=int)
        coord_y = np.zeros(line_num, dtype=int)
        value = np.zeros(line_num)
        with open(path) as f:
            for num, line in enumerate(f, 1):
                line_split = line.split()
                coord_x[num - 1], coord_y[num - 1], value[num - 1] = int(
                    line_split[0]), int(line_split[1]), np.float(line_split[2])

        max_idx = max(coord_x.max(), coord_y.max())
        print('Matrix Max index is', max_idx)
        print('Coordinate Shape', coord_x.shape, coord_y.shape)

        # Normalize the matrix to a square format
        coord_x = np.concatenate((coord_x, np.array([max_idx], dtype=int)),
                                 axis=0)
        coord_y = np.concatenate((coord_y, np.array([max_idx], dtype=int)),
                                 axis=0)
        value = np.concatenate((value, np.array([0], dtype=int)), axis=0)

        self.data = sparse.coo_matrix((value, (coord_x, coord_y)))  # .tocsr()
        print('Normalized data shape', self.data.shape)
        self.size = str(self.data.size / (1024**2)) + ".MB"
        return True

    def from_text(self, path):
        self._read_file(path)
        return self.data

    def set_base_name(self, name):
        self.base_name = name

    def load_bed(self, path):
        loader = BedLoader()
        loader.filepath = path
        loader.read_file()
        self.bed_file = loader.data.values
        self.resolution = loader.data.values[0][2] - loader.data.values[0][1]

    def _write_file(self, path):
        f = h5.File(path, 'w')
        # TODO
        # if isinstance(self.bed_file, np.ndarray):
        #     f['bed_file'] = self.bed_file

        for i in range(len(self.zoomLevel)):
            resolution = self.resolution * self.zoomLevel[i]
            f['zoom' + '_' + str(resolution) + '_' +
              'data'] = self.dataLevel[i].data
            f['zoom' + '_' + str(resolution) + '_' +
              'row'] = self.dataLevel[i].row
            f['zoom' + '_' + str(resolution) + '_' +
              'col'] = self.dataLevel[i].col
            f['zoom' + '_' + str(resolution) + '_' +
              'shape'] = self.dataLevel[i].shape
        f['zoomLevel'] = np.array(self.zoomLevel)

        f.close()

    def write_file(self,path=None):
        if not path:
            self._write_file(self.base_name + '.h5')
        else:
            self._write_file(path)

    def add_zoom_series(self, zoomlist):
        for i in zoomlist:
            self.add_level(i)

    def add_level(self, zoomFactor):
        if len(self.zoomLevel) == 0:
            self.zoomLevel.append(1)
            self.dataLevel.append(self.data)
            self.add_level(zoomFactor)
        elif zoomFactor == 1:
            return
        else:
            x = self.dataLevel[-1].shape[0]
            _next_mat = self.generate_next_level_mat(self.dataLevel[-1],
                                                     zoomFactor)
            self.zoomLevel.append(zoomFactor)
            self.dataLevel.append(_next_mat)
            print('Next level matrix shape', _next_mat.shape)
            return

    def print_summary(self):
        print('Base name', self.base_name)
        print('Data', self.data.shape)
        try:
            print(self.data[0:10])
        except TypeError:
            print(self.data.tocsr()[0:10])
        print('Bed file', self.bed_file.shape)
        print(self.bed_file[0:10])
        print('Zoom Level', self.zoomLevel)
        print('Data Level')
        for i in range(len(self.dataLevel)):
            d = self.dataLevel[i]
            print(d.shape)
            try:
                print(d[0:10])
            except TypeError:
                print(d.tocsr()[0:10])

    def generate_next_level_mat(self, data, zoomFactor):
        '''
         n - n % z  | n % z               
        ------------|--|---            
        |           |--| n            
        |           |--| |           
        |           |--| n           
        |           |--| %           
        |           |--| z           
        ------------|--|--           
        |||||||||||||--| n % z        
        ------------|--|--      
        '''
        _n_ = data.shape[0]
        _n_reg = _n_ - _n_ % zoomFactor
        _n_comp = _n_ % zoomFactor
        print("Regular part len", _n_reg, "Compensate part len", _n_comp)
        _zoomed_set = set()
        _zoomed_row = []
        _zoomed_col = []
        _zoomed_value = []
        _data_csr = data.tocsr()

        # Regular region ######################################################
        _data_regular = _data_csr[0:_n_reg, 0:_n_reg]
        _data_reg_col = _data_csr.tocoo().col
        _data_reg_row = _data_csr.tocoo().row
        for i in range(_data_reg_row.shape[0]):
            if i % max((_data_reg_row.shape[0] //
                        (_data_reg_row.shape[0] / 100)), 10000) == 0:
                print('Regular', i, _data_reg_row.shape[0],
                      i / _data_reg_row.shape[0] * 100, '% Complete')
            # after zoom position
            _new_idx_row = np.int(np.floor(_data_reg_row[i] / zoomFactor))
            _new_idx_col = np.int(np.floor(_data_reg_col[i] / zoomFactor))
            if not (_new_idx_row, _new_idx_col) in _zoomed_set:
                _zoomed_set.add((_new_idx_row, _new_idx_col))
                _new_value = np.sum(
                    _data_regular[_new_idx_row:_new_idx_row +
                                  zoomFactor, _new_idx_col:_new_idx_col +
                                  zoomFactor])
                _zoomed_row.append(_new_idx_row)
                _zoomed_col.append(_new_idx_col)
                _zoomed_value.append(_new_value)

        # Compensate Region ###################################################
        _compensate_row = _data_csr[0:_n_reg, _n_reg:_n_reg + _n_comp]
        _compensate_col = _data_csr[_n_reg:_n_reg + _n_comp, 0:_n_reg +
                                    _n_comp]
        _data_comp_row_row = _compensate_row.tocoo().row
        _data_comp_row_col = _compensate_row.tocoo().col
        _data_comp_col_row = _compensate_col.tocoo().row
        _data_comp_col_col = _compensate_col.tocoo().col

        for i in range(_data_comp_row_row.shape[0]):
            # after zoom position
            _new_idx_row = np.int(np.floor(_data_comp_row_row[i] / zoomFactor))
            _new_idx_col = np.int(np.floor(_data_comp_row_col[i] / zoomFactor))
            if not (_new_idx_row, _new_idx_col) in _zoomed_set:
                _zoomed_set.add((_new_idx_row, _new_idx_col))
                _new_value = np.sum(
                    _compensate_row[_new_idx_row:_new_idx_row +
                                    zoomFactor, _new_idx_col:_new_idx_col +
                                    _n_comp])
                _zoomed_row.append(_new_idx_row)
                _zoomed_col.append(_new_idx_col)
                _zoomed_value.append(_new_value)

        for i in range(_data_comp_col_row.shape[0]):
            # after zoom position
            _new_idx_row = np.int(np.floor(_data_comp_col_row[i] / zoomFactor))
            _new_idx_col = np.int(np.floor(_data_comp_col_col[i] / zoomFactor))
            if not (_new_idx_row, _new_idx_col) in _zoomed_set:
                _zoomed_set.add((_new_idx_row, _new_idx_col))
                try:
                    _new_value = np.sum(
                        _compensate_col[_new_idx_row:_new_idx_row +
                                        _n_comp, _new_idx_col:_new_idx_col +
                                        zoomFactor])
                except Error:
                    _new_value = np.sum(
                        _compensate_col[_new_idx_row:_new_idx_row +
                                        _n_comp, _new_idx_col:_new_idx_col +
                                        _n_comp])
                _zoomed_row.append(_new_idx_row)
                _zoomed_col.append(_new_idx_col)
                _zoomed_value.append(_new_value)

        # New Sparse Matrix ###################################################
        _zoomed_mat = sparse.coo_matrix((_zoomed_value, (_zoomed_row,
                                                         _zoomed_col)))
        return _zoomed_mat
