#!/usr/bin/env python
# coding: utf-8
__author__ = "Hongpeng Ma"
__copyright__ = "Copyright 2018, Michael Q Zhang Lab"
__credits__ = ['Juntao Gao', 'Yongge Li', 'Nahdir']

__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Hongpeng Ma"
__email__ = "mahongpengmars@163.com"
__status__ = "dev"
__date__ = "Mon Jan 14 09:50:08 CST 2019"

import numpy as np
from scipy import sparse
from scipy import optimize
from sklearn.utils import check_random_state
from . import poisson_model
from . import multi_dimension_scale


class Poisson_Model_Base(object):
    '''
    Posisson Algorithm Base Class
    '''
    @classmethod
    def poisson_obj(cls,
                    X,
                    counts,
                    alpha=-3.,
                    beta=1.,
                    bias=None,
                    use_zero_counts=False,
                    cst=0):
        if bias is None:
            bias = np.ones((counts.shape[0], 1))

        if sparse.issparse(counts):
            return Poisson_Model_Base._poisson_obj_sparse(
                X,
                counts,
                beta=beta,
                bias=bias,
                alpha=alpha,
                use_zero_counts=use_zero_counts,
                cst=cst)
        else:
            raise NotImplementedError(
                "Poisson model is not implemented for dense")

    @classmethod
    def _poisson_obj_sparse(cls,
                            X,
                            counts,
                            alpha=-3.,
                            beta=1.,
                            bias=None,
                            use_zero_counts=False,
                            cst=0):

        if bias is None:
            bias = np.ones((X.shape[0], ))
        bias = bias.flatten()
        dis = np.sqrt(((X[counts.row] - X[counts.col])**2).sum(axis=1))
        fdis = bias[counts.row] * bias[counts.col] * beta * dis**alpha

        obj = fdis.sum() - (counts.data * np.log(fdis)).sum()
        if np.isnan(obj):
            raise ValueError("Objective function is nan")
        return obj

    @classmethod
    def poisson_gradient(cls,
                         X,
                         counts,
                         alpha=-3,
                         beta=1,
                         bias=None,
                         use_zero_counts=False):
        if bias is None:
            bias = np.ones((counts.shape[0], 1))

        if sparse.issparse(counts):
            return Poisson_Model_Base._poisson_gradient_sparse(
                X, counts, beta=beta, bias=bias, alpha=alpha)
        else:
            raise NotImplementedError(
                "Poisson model is not implemented for dense")
    @classmethod
    def _poisson_gradient_sparse(cls,
                                 X,
                                 counts,
                                 alpha=-3,
                                 beta=1,
                                 bias=None):
        if bias is None:
            bias = np.ones((counts.shape[0], 1))

        bias = bias.flatten()
        dis = np.sqrt(((X[counts.row] - X[counts.col])**2).sum(axis=1))
        fdis = bias[counts.row] * bias[counts.col] * beta * dis**alpha

        diff = X[counts.row] - X[counts.col]

        grad = -((counts.data / fdis - 1) * fdis * alpha /
                 (dis**2))[:, np.newaxis] * diff

        grad_ = np.zeros(X.shape)

        for i in range(X.shape[0]):
            grad_[i] += grad[counts.row == i].sum(axis=0)
            grad_[i] -= grad[counts.col == i].sum(axis=0)

        return grad_

    @classmethod
    def eval_f(cls,
               x,
               user_data=None):
        n, counts, alpha, beta, bias, use_zero_counts = user_data
        x = x.reshape((n, 3))
        obj = Poisson_Model_Base.poisson_obj(
            x, counts, alpha=alpha, beta=beta, bias=bias)
        x = x.flatten()
        return obj

    @classmethod
    def eval_grad_f(cls,
                    x,
                    user_data=None):
        n, counts, alpha, beta, bias, use_zero_counts = user_data
        x = x.reshape((n, 3))
        grad = Poisson_Model_Base.poisson_gradient(
            x, counts, alpha=alpha, beta=beta, bias=bias)
        x = x.flatten()
        return grad.flatten()

    @classmethod
    def estimate_model(cls,
                   counts,
                   alpha=-3.,
                   beta=1.,
                   ini=None,
                   bias=None,
                   random_state=None,
                   maxiter=10000,
                   verbose=0):
        """
        Estimate the parameters of g
        Parameters
        ----------
        counts : sparse scipy matrix (n, n)
        alpha : float, optional, default: -3
            counts-to-distances mapping coefficient
        beta : float, optional, default: 1
            counts-to-distnances scaling coefficient
        init : ndarray (n, 3), optional, default: None
            initialization point
        bias : ndarray (n, 1), optional, default: None
            bias vector. If None, no bias will be applied to the model
        random_state : {RandomState, int, None}, optional, default: None
            random state object, or seed, or None.
        maxiter : int, optional, default: 10000
            Maximum number of iteration
        verbose : int, optional, default: 0
            verbosity
        Returns
        ------
        X : 3D structure
        """
        n = counts.shape[0]

        if not sparse.isspmatrix_coo(counts):
            counts = sparse.coo_matrix(counts)

        counts.setdiag(0)
        counts.eliminate_zeros()

        random_state = check_random_state(random_state)
        if ini is None:
            ini = 1 - 2 * random_state.rand(n * 3)
        else:
            ini = np.array(ini)

        data = (n, counts, alpha, beta, bias, False)

        results = optimize.fmin_l_bfgs_b(
            Poisson_Model_Base.eval_f,
            ini.flatten(),
            Poisson_Model_Base.eval_grad_f,
            (data, ),
            iprint=verbose,
            maxiter=maxiter,
        )
        results = results[0].reshape(-1, 3)
        return results


class PM1(Poisson_Model_Base):
    """
    """
    algorithm_name = "pm1"
    
    def __init__(self,
                 alpha=-3.,
                 beta=1.,
                 max_iter=5000,
                 random_state=None,
                 n_init=1,
                 n_jobs=1,
                 init="MDS2",
                 verbose=False,
                 bias=None):
        self.max_iter = max_iter
        self.alpha = alpha
        self.beta = beta
        self.random_state = check_random_state(random_state)
        self.n_init = n_init
        self.bias = bias
        self.n_jobs = n_jobs
        self.init = init
        self.verbose = verbose

    def fit(self, counts, lengths=None):
        """
        """
        if not sparse.isspmatrix_coo(counts):
            counts = sparse.coo_matrix(counts)
        if not sparse.issparse(counts):
            counts[np.isnan(counts)] = 0
        if self.init == "MDS2":
            if self.verbose:
                print("Initialing with MDS2")
            mds = multi_dimension_scale.Multi_Dimensional_Scaling_Base()
            X = mds.estimate_model(
                counts,
                alpha=self.alpha,
                beta=self.beta,
                bias=self.bias,
                random_state=self.random_state,
                maxiter=self.max_iter,
                verbose=self.verbose)
        else:
            X = self.init
        X = Poisson_Model_Base.estimate_model(
            counts,
            alpha=self.alpha,
            beta=self.beta,
            ini=X,
            bias=self.bias,
            verbose=self.verbose,
            random_state=self.random_state,
            maxiter=self.max_iter)
        return X


class PM2(Poisson_Model_Base):
    """
    """
    algorithm_name = 'pm2'
    
    def __init__(self,
                 alpha=-3.,
                 beta=1.,
                 max_iter=5000,
                 max_iter_outer_loop=5,
                 random_state=None,
                 n_init=1,
                 n_jobs=1,
                 bias=None,
                 init="MDS2",
                 verbose=False):
        self.max_iter = max_iter
        self.alpha = alpha
        self.beta = beta
        self.random_state = check_random_state(random_state)
        self.n_init = n_init
        self.n_jobs = n_jobs
        self.init = init
        self.max_iter_outer_loop = max_iter_outer_loop
        self.verbose = verbose
        self.bias = bias

    def fit(self, counts):
        """
        """

        if not sparse.isspmatrix_coo(counts):
            counts = sparse.coo_matrix(counts)
        counts.setdiag(0)
        counts.eliminate_zeros()

        if self.init == "MDS2":
            mds = multi_dimension_scale.Multi_Dimensional_Scaling_Base()
            X = mds.estimate_model(
                counts,
                alpha=self.alpha,
                beta=self.beta,
                ini="random",
                verbose=self.verbose,
                bias=self.bias,
                random_state=self.random_state,
                maxiter=self.max_iter)
        elif self.init == "random":
            X = self.init
        else:
            raise ValueError("Unknown initialization strategy")

        self.alpha_ = self.alpha
        self.beta_ = self.beta
        for it in range(self.max_iter_outer_loop):
            self.alpha_, self.beta_ = poisson_model.estimate_alpha_beta(
                counts,
                X,
                bias=self.bias,
                ini=[self.alpha_, self.beta_],
                verbose=self.verbose,
                random_state=self.random_state)
            print(self.alpha_, self.beta_)
            X_ = Poisson_Model_Base.estimate_model(
                counts,
                alpha=self.alpha_,
                beta=self.beta_,
                ini=X,
                verbose=self.verbose,
                bias=self.bias,
                random_state=self.random_state,
                maxiter=self.max_iter)
        return X_

def main():
    a = np.random.randint(100000, size=30).reshape(-1, 3)
    #    a = sparse.coo_matrix(a)
    print(a)
    print(Poisson_Model_Base.estimate_model(a))
#    print('=' * 20)
#    mds = MDS()
#    print(a)
#    print(mds.fit(a))
#    nmds = NMDS()
#    print('=' * 20)
#    print(nmds.fit(a))
#

if __name__ == '__main__':
    main()
