# -*- coding: utf-8 -*-
# @Time    : 8/11/20 15:01
# @Author  : Sikun Xu
# @FileName: sampler.py
# @Software: PyCharm

import numpy as np
from scipy.stats import norm, multivariate_normal

import matplotlib.pyplot as plt
import seaborn as sns


class SamplerSuperClass(object):
    def __init__(self):
        """

        """
        # parameters
        pass

        # attributes
        pass


class MetropolisHastings(SamplerSuperClass):
    """
    Reference
    ----------
    Andrieu, Christophe, et al. "An introduction to MCMC for machine learning." Machine learning 50.1-2 (2003): 5-43.
    """

    def __init__(self, target_dstn_func, proposal_dstn_func='gaussian', algorithm='metropolis', gaussian_proposal_sd=10,
                 gaussian_proposal_mean=0):
        """
        TODO

        Parameters
        ----------
        target_dstn_func:

        proposal_dstn_func: default to gaussian

        algorithm: independent or metropolis, default to metropolis. This parameter will only be used when
        proposal_dstn_func parameter is not specified
            1. Independent refers to independent sampler, meaning the proposal distribution is independent of the
            current state, i.e. q(next|current) = q(next)
            2. Metropolis refers to Metropolis algorithm, meaning the proposal distribution is a symmetric random walk,
            i.e. q(next|current) = q(current|next)

        gaussian_proposal_sd: standard deviation of the proposal gaussian distribution, default to 10. This parameter
        will only be used when the proposal distribution is not specified.

        gaussian_proposal_mean: mean of the proposal gaussian distribution, default to 0. This parameter is only used
        when algorithm==independent

        """
        # parameters
        self.algorithm = algorithm  # self.algorithm must be defined before self.proposal_dstn_func
        self.gaussian_proposal_mean = gaussian_proposal_mean
        self.gaussian_proposal_cov = gaussian_proposal_sd
        # target and proposal functions
        self.target_dstn_func = target_dstn_func
        self.proposal_dstn_func = proposal_dstn_func

        # init super
        super(MetropolisHastings, self).__init__()

        # attributes
        self.dimension = None

    def fit(self, dim, num_samples):
        """
        TODO
        """
        # update attributes
        self.dimension = dim
        self.proposal_dstn_func = self._init_proposal_dstn_with_gaussian() if self.proposal_dstn_func == 'gaussian' \
            else self.proposal_dstn_func

        # 1. initialization
        x_arr = np.zeros(shape=(num_samples, self.dimension))

        # 2. main loop
        for idx in range(1, num_samples):
            current_x = x_arr[idx-1]
            # 2.1 sample next_state from proposal distribution q(next|current)
            next_x = self._sample_from_proposal_dstn(current_x)  # x_arr[idx] take the idx-row, shape=(d, )

            # 2.2 acceptance check
            x_arr[idx] = next_x if self._acceptance_check(current_x, next_x) else current_x

        # return
        return x_arr

    def _sample_from_proposal_dstn(self, current_x, size=1) -> float:
        """
        Sample from proposal distribution

        Parameters
        ----------
        current_x: current state, numpy array with shape=(d, )
        """
        return self.proposal_dstn_func(current_x, size)

    def _calculate_proposal_dstn_probability(self, current_x, next_x):
        """
        TODO
        """
        if self.algorithm == 'independent' and self.dimension == 1:
            return norm.pdf(
                next_x,
                self.gaussian_proposal_mean,
                self.gaussian_proposal_cov,
            )
        elif self.algorithm == 'independent' and self.dimension > 1:
            return multivariate_normal.pdf(
                next_x,
                self.gaussian_proposal_mean,
                self.gaussian_proposal_cov
            )
        elif self.algorithm == 'metropolis' and self.dimension == 1:
            return norm.pdf(
                next_x,
                current_x,
                self.gaussian_proposal_cov,
            )
        elif self.algorithm == 'metropolis' and self.dimension > 1:
            return multivariate_normal.pdf(
                next_x,
                current_x,
                self.gaussian_proposal_cov
            )
        else:
            raise Exception('Error in initializing proposal distribution with algorithm {} and dimension {}'.format(
                self.algorithm, self.dimension
            ))

    def _acceptance_check(self, current_x, next_x) -> bool:
        """
        TODO
        """
        return np.random.rand() < self._calculate_acceptance_probability(current_x, next_x)

    def _calculate_acceptance_probability(self, current_state, next_state) -> float:
        """
        TODO
        """

        numerator = self.target_dstn_func(next_state) * self._calculate_proposal_dstn_probability(current_state,
                                                                                                  next_state)
        denominator = self.target_dstn_func(current_state) * self._calculate_proposal_dstn_probability(next_state,
                                                                                                       current_state)
        return min(1, numerator / denominator)

    def _init_proposal_dstn_with_gaussian(self):
        """
        Return function that generates gaussian probability. This method is only called when the proposal_dstn_func
        is set to default value (gaussian)

        Return
        ----------
        gaussian_dstn_func: a function that generates probability following gaussian distribution
        """
        if self.algorithm == 'independent' and self.dimension == 1:
            self.gaussian_proposal_cov = self.gaussian_proposal_cov
            return lambda mean, size: np.random.normal(
                self.gaussian_proposal_mean,
                self.gaussian_proposal_cov,
                size
            )
        elif self.algorithm == 'independent' and self.dimension > 1:
            self.gaussian_proposal_mean = np.repeat(self.gaussian_proposal_mean, self.dimension)
            self.gaussian_proposal_cov = np.diag(
                np.repeat(self.gaussian_proposal_cov, self.dimension)
            )
            return lambda mean, size: np.random.multivariate_normal(
                self.gaussian_proposal_mean,
                self.gaussian_proposal_cov,
                size
            )
        elif self.algorithm == 'metropolis' and self.dimension == 1:
            self.gaussian_proposal_cov = self.gaussian_proposal_cov
            return lambda mean, size: np.random.normal(
                mean,
                self.gaussian_proposal_cov,
                size
            )
        elif self.algorithm == 'metropolis' and self.dimension > 1:
            self.gaussian_proposal_cov = np.diag(
                np.repeat(self.gaussian_proposal_cov, self.dimension)
            )
            return lambda mean, size: np.random.multivariate_normal(
                mean,
                self.gaussian_proposal_cov,
                size
            )
        else:
            raise Exception('Error in initializing proposal distribution with algorithm {} and dimension {}'.format(
                self.algorithm, self.dimension
            ))


if __name__ == '__main__':
    def target_dstn_func_(x):
        return 0.3 * np.exp(-0.2 * x ** 2) + 0.7 * np.exp(-0.2 * (x - 10) ** 2)

    MH_obj = MetropolisHastings(
        target_dstn_func=target_dstn_func_,
        gaussian_proposal_sd=10,
    )
    result = MH_obj.fit(dim=1, num_samples=5000)

    # visualization
    sns.set()
    fig, ax = plt.subplots()
    sns.distplot(result, ax=ax, label='MH Sampler', norm_hist=True, kde=False, bins=40)
    plot_x = np.linspace(-5, 16, 500)
    plot_y = target_dstn_func_(plot_x) / 4.5
    sns.lineplot(plot_x, plot_y, ax=ax, label='Target Distribution')
    plt.show()
