# -*- coding: utf-8 -*-
# @Time    : 8/11/20 15:01
# @Author  : Sikun Xu
# @FileName: mcmc_helper.py
# @Software: PyCharm

import numpy as np
from scipy.stats import norm, multivariate_normal


class SamplerSuperClass(object):
    def __init__(self):
        """
        TODO

        """
        # parameters
        pass

        # attributes
        pass


class GaussianProposal(object):
    """
    TODO
    """

    def __init__(self, mean, scale):
        """
        TODO

        Parameters:
        ----------
        mean:

        cov:

        dim: dimension of the random variable (vector), if no dimension is provided, then the will take the size of the
        mean provided

        """
        # parameters
        self.mean = mean
        self.scale = scale

        # attributes
        self.dimension = 1 if isinstance(self.mean, int) or isinstance(self.mean, float) else len(self.mean)

    def sample(self, mean=None, size=1):
        """
        TODO

        Parameters:
        ----------
        mean:

        size:

        """
        # attributes
        mean = self.mean if mean is None else mean

        if self.dimension == 1:
            return np.random.normal(
                loc=mean,
                scale=self.scale,
                size=size,
            )
        else:
            return np.random.multivariate_normal(
                mean=mean,
                cov=self.scale,
                size=size,
            )

    def pdf(self, x, mean=None) -> float:
        """
        TODO

        Parameters:
        ----------
        x:

        mean:
        """
        # attributes
        mean = self.mean if mean is None else mean

        # calculate pdf
        if self.dimension == 1:
            return norm.pdf(
                x,
                mean,
                self.scale,
            )
        else:
            return multivariate_normal.pdf(
                x,
                mean,
                self.scale,
            )
