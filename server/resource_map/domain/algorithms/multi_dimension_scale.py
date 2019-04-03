#!/usr/bin/env python
# coding: utf-8
__author__ = "Hongpeng Ma"
__copyright__ = "Copyright 2019, Michael Q Zhang Lab"
__credits__ = ['Juntao Gao', 'Yongge Li', 'Nahdir']

__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Hongpeng Ma"
__email__ = "mahongpengmars@163.com"
__status__ = "dev"
__date__ = "Fri Jan 11 19:56:11 CST 2019"
'''
Thanks:
Resources referenced during the implmentation
hiclib pastis: https://github.com/hiclib/pastis
'''

import numpy as np
from scipy import optimize
from scipy import sparse
from sklearn.utils import check_random_state
from sklearn.metrics import euclidean_distances
from sklearn.isotonic import IsotonicRegression


class Multi_Dimensional_Scaling_Base(object):
    """Documentation for Multi_Dimensional_Scaling_Base

    """

    def __init__(self):
        super(Multi_Dimensional_Scaling_Base, self).__init__()

    @classmethod
    def compute_wish_distances(cls,
                               counts_matrix,
                               alpha=-3.,
                               beta=1.,
                               bias=None):
        '''
        Compute wish distances matrix from a counts Matrix
        
        Parameters
        ----------
        counts_matrix: ndarray
        alpha: float, optional, default: -3
        beta: float, optional, default: 1
        
        Returns
        ----------
        wish_distance_matrix: ndarray
        '''
        if beta == 0:
            raise ValueError("Beta cannot be 0")
        c = counts_matrix.copy()
        if sparse.issparse(c):
            if not sparse.isspmatrix_coo(c):
                c = c.tocoo()
            if bias is not None:
                bias = bias.flatten()
                c /= bias[c.row] * bias[c.col]
            # w: wish distance matrix
            w = c / beta
            w.data[w.data != 0] **= 1. / alpha
            return w
        else:
            w = c / beta
            w[w != 0] **= 1. / alpha
            return w

    @classmethod
    def mds_objective_func(cls, guess_model, known_distance):
        '''
        Objective function for MDS Algorithm
    
        Parameters
        ----------
        guess_model: ndarray
            target 3d model
        known_distances:: ndarray
            known_distance from chromosome
        '''
        if sparse.issparse(known_distance):
            guess_model = guess_model.reshape(-1, 3)
            guess_distance = np.sqrt(((guess_model[known_distance.row] -
                                       guess_model[known_distance.col])
                                      **2).sum(axis=1))
            return ((guess_distance - known_distance.data)**2 /
                    known_distance.data**2).sum()
        else:
            guess_model = guess_model.reshape(-1, 3)
            guess_distance = euclidean_distances(guess_model)
            guess_model = guess_model.flatten()
            obj_mat = (1. / known_distance**2) * (
                (guess_distance - known_distance)**2)
            return obj_mat[np.invert(np.isnan(obj_mat)
                                     | np.isinf(obj_mat))].sum()

    @classmethod
    def mds_gradient_func(cls, guess_model, known_distance):
        if sparse.issparse(known_distance):
            guess_model = guess_model.reshape(-1, 3)
            guess_distance = np.sqrt(((guess_model[known_distance.row] -
                                       guess_model[known_distance.col])
                                      **2).sum(axis=1))
            gradient = 2 * (
                (guess_distance - known_distance.data) / guess_distance /
                known_distance.data**2)[:, np.newaxis] * (
                    guess_model[known_distance.row] -
                    guess_model[known_distance.col])
            gradient_ = np.zeros(guess_model.shape)

            for i in range(guess_model.shape[0]):
                gradient_[i] += gradient[known_distance.row == i].sum(axis=0)
                gradient_[i] -= gradient[known_distance.col == i].sum(axis=0)
            guess_model = guess_model.flatten()
            return gradient_.flatten()
        else:
            guess_model = guess_model.reshape(-1, 3)
            m, n = guess_model.shape
            tmp = guess_model.repeat(m, axis=0).reshape((m, m, n))
            dif = tmp - tmp.transpose(1, 0, 2)
            guess_distance = euclidean_distances(guess_model).repeat(
                3, axis=1).flatten()
            distances = known_distance.repeat(3, axis=1).flatten()
            gradient = 2 * dif.flatten() * (
                guess_distance - distances) / guess_distance / distances**2
            gradient[(distances == 0) | np.isnan(gradient)] = 0
            guess_model = guess_model.flatten()
            return gradient.reshape((m, m, n)).sum(axis=1).flatten()

    @classmethod
    def estimate_model(cls,
                       counts_matrix,
                       alpha=-3.,
                       beta=1.,
                       ini=None,
                       verbose=0,
                       use_zero_entries=False,
                       precompute_distances=False,
                       bias=None,
                       random_state=None,
                       type='MDS2',
                       factr=1e12,
                       maxiter=100000):
        if not sparse.isspmatrix_coo(counts_matrix):
            counts_matrix = sparse.coo_matrix(counts_matrix.copy())
        points_num = counts_matrix.shape[0]
        random_state = check_random_state(random_state)
        if ini is None or ini == 'random':
            ini = 1 - 2 * random_state.rand(points_num * 3)
        if not precompute_distances or precompute_distances == 'auto':
            known_distance = Multi_Dimensional_Scaling_Base.compute_wish_distances(
                counts_matrix, alpha=alpha, beta=beta, bias=bias)
        else:
            if bias is not None:
                counts_matrix /= bias
                counts_matrix /= bias.T
            known_distance = counts_matrix
        results, object_value, info = optimize.fmin_l_bfgs_b(
            Multi_Dimensional_Scaling_Base.mds_objective_func,
            ini.flatten(),
            Multi_Dimensional_Scaling_Base.mds_gradient_func,
            (known_distance, ),
            iprint=0,
            disp=0,
            factr=factr,
            maxiter=maxiter)
        print(object_value)
        print(info)
        return results.reshape(-1, 3)


class MDS(Multi_Dimensional_Scaling_Base):
    """Documentation for MDS
    Multi-Dimensional Scaling Algorithm
    for dimensional scaling
    
    Usage:
    ----------
    mds = MDS()
    mds.fit(x)
    """
    algorithm_name = "mds"

    def __init__(self,
                 alpha=-3.,
                 beta=1.,
                 max_iter=10000,
                 random_state=None,
                 n_init=1,
                 n_jobs=1,
                 precompute_distances=False,
                 bias=None,
                 init=None,
                 verbose=False,
                 factr=1e12):
        super(MDS, self).__init__()
        self.max_iter = max_iter
        self.alpha = alpha
        self.beta = beta
        self.max_iter = max_iter
        self.random_state = check_random_state(random_state)
        self.precompute_distances = precompute_distances
        self.n_init = n_init
        self.n_jobs = n_jobs
        self.init = init
        self.verbose = verbose
        self.bias = bias
        self.factr = factr

    def fit(self, counts_matrix, lengths=None):
        '''
        MDS fit Function, scale low dimension matrix to high dimension
        
        Parameters
        ----------
        counts_matrix: ndarray

        Returns
        ----------
        fit_matrix: ndarray
        '''
        if not sparse.isspmatrix_coo(counts_matrix):
            counts_matrix = sparse.coo_matrix(counts_matrix)
        fit_matrix = Multi_Dimensional_Scaling_Base.estimate_model(
            counts_matrix,
            alpha=self.alpha,
            beta=self.beta,
            ini=self.init,
            verbose=self.verbose,
            precompute_distances=self.precompute_distances,
            use_zero_entries=False,
            random_state=self.random_state,
            bias=self.bias,
            factr=self.factr,
            maxiter=self.max_iter)
        return fit_matrix


class NMDS(Multi_Dimensional_Scaling_Base):
    """Documentation for NMDS
    non-parametric Multi-Dimensional Scaling Algorithm
        for non-parametric dimensional scaling
    
    Usage:
    ----------
    nmds = NMDS()
    nmds.fit(x)
    """
    algorithm_name = "nmds"
    
    def __init__(self,
                 alpha=-3.,
                 beta=1.,
                 max_iter=10000,
                 random_state=None,
                 n_init=1,
                 n_jobs=1,
                 precompute_distances="auto",
                 bias=None,
                 init=None,
                 verbose=False,
                 max_iter_outer=5,
                 factr=1e12):
        super(NMDS, self).__init__()

        self.alpha = alpha
        self.beta = beta
        self.max_iter = max_iter
        self.random_state = check_random_state(random_state)
        self.precompute_distances = precompute_distances
        self.n_init = n_init
        self.n_jobs = n_jobs
        self.init = init
        self.verbose = verbose
        self.bias = bias
        self.factr = factr
        self.max_iter_outer = max_iter_outer

    def fit(self, counts_matrix, lengths=None):
        '''
          NMDS fit Function, scale low dimension matrix to high dimension
        
          Parameters
          ----------
          counts_matrix: ndarray
          
          Returns
          ----------
          fit_matrix: ndarray
          '''
        if not sparse.isspmatrix_coo(counts_matrix):
            counts_matrix = sparse.coo_matrix(counts_matrix)
            for i in range(self.max_iter_outer):
                if i == 0:
                    fit_matrix = Multi_Dimensional_Scaling_Base.estimate_model(
                        counts_matrix,
                        alpha=self.alpha,
                        beta=self.beta,
                        ini=self.init,
                        verbose=self.verbose,
                        precompute_distances=self.precompute_distances,
                        use_zero_entries=False,
                        random_state=self.random_state,
                        bias=self.bias,
                        factr=self.factr,
                        maxiter=self.max_iter)
                else:
                    ir = IsotonicRegression()
                    distances = np.sqrt(((fit_matrix[counts_matrix.row] -
                                          fit_matrix[counts_matrix.col])
                                         **2).sum(axis=1))
                    wish_distances = ir.fit_transform(1. / counts_matrix.data,
                                                      distances)
                    fit_matrix = Multi_Dimensional_Scaling_Base.estimate_model(
                        sparse.coo_matrix((wish_distances,
                                           (counts_matrix.row,
                                            counts_matrix.col))),
                        alpha=self.alpha,
                        beta=self.beta,
                        ini=fit_matrix,
                        verbose=self.verbose,
                        use_zero_entries=False,
                        precompute_distances='precomputed',
                        random_state=self.random_state,
                        factr=self.factr,
                        maxiter=self.max_iter,
                    )
            return fit_matrix


def main():
    a = np.random.randint(100000, size=30).reshape(-1, 3)
    #    a = sparse.coo_matrix(a)
    print(a)
    print(Multi_Dimensional_Scaling_Base.estimate_model(a))
    print('=' * 20)
    mds = MDS()
    print(a)
    print(mds.fit(a))
    nmds = NMDS()
    print('=' * 20)
    print(nmds.fit(a))


if __name__ == '__main__':
    main()
