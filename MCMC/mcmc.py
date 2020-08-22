# -*- coding: utf-8 -*-
# @Time    : 8/10/20 17:45
# @Author  : Sikun Xu
# @FileName: mcmc.py
# @Software: PyCharm

from MCMC.mcmc_helper import *
from scipy import integrate

import matplotlib.pyplot as plt
import seaborn as sns


class GibbsSampling:
    """
    TODO
    """
    def __init__(self):
        """

        """
        pass


class MetropolisHastings(SamplerSuperClass):
    """
    Reference
    ----------
    Andrieu, Christophe, et al. "An introduction to MCMC for machine learning." Machine learning 50.1-2 (2003): 5-43.
    """

    def __init__(self, target_dstn, proposal_dstn, algorithm='metropolis'):
        """
        TODO

        Parameters
        ----------
        target_dstn: PDF of the target distribution, no need to be normalized

        proposal_dstn: has sample and pdf method

        algorithm: independent or metropolis, default to metropolis. This parameter will only be used when
        proposal_dstn_func parameter is not specified
            1. Independent refers to independent sampler, meaning the proposal distribution is independent of the
            current state, i.e. q(next|current) = q(next)
            2. Metropolis refers to Metropolis algorithm, meaning the proposal distribution is a symmetric random walk,
            i.e. q(next|current) = q(current|next)

        """
        # parameters
        self.algorithm = algorithm  # self.algorithm must be defined before self.proposal_dstn_func
        # target and proposal functions
        self.target_dstn = target_dstn
        self.proposal_dstn = proposal_dstn

        # init super
        super(MetropolisHastings, self).__init__()

        # attributes
        self.dimension = self.proposal_dstn.dimension

    def fit(self, num_samples):
        """
        TODO
        """
        # 1. initialization
        x_arr = np.zeros(shape=(num_samples, self.dimension))

        # 2. main loop
        for idx in range(1, num_samples):
            current_x = x_arr[idx-1]
            # 2.1 sample next_state from proposal distribution q(next|current)
            next_x = self.proposal_dstn.sample(mean=current_x)

            # 2.2 acceptance check
            x_arr[idx] = next_x if self._acceptance_check(current_x, next_x) else current_x

        # return
        return x_arr

    def _calculate_proposal_dstn_probability(self, current_x, next_x):
        """
        TODO
        """
        if self.algorithm == 'independent':
            return self.proposal_dstn.pdf(x=next_x,)
        elif self.algorithm == 'metropolis':
            return self.proposal_dstn.pdf(x=next_x, mean=current_x,)
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

        numerator = self.target_dstn(next_state) * self._calculate_proposal_dstn_probability(current_state, next_state)
        denominator = self.target_dstn(current_state) * self._calculate_proposal_dstn_probability(next_state,
                                                                                                  current_state)
        return min(1, numerator / denominator)


if __name__ == '__main__':

    # unnormalized target distribution
    def target_dstn_func_(x: float) -> float:
        return 0.3 * np.exp(-0.2 * x ** 2) + 0.7 * np.exp(-0.2 * (x - 10) ** 2)

    # proposal distribution
    proposal_dstn_obj = GaussianProposal(mean=0, scale=10)

    # MCMC object
    MH_obj = MetropolisHastings(
        target_dstn=target_dstn_func_,
        proposal_dstn=proposal_dstn_obj,
    )
    result = MH_obj.fit(num_samples=5000)

    # visualization
    # data preparation
    # x and y for normalized target distribution
    plot_x = np.linspace(-5, 16, 500)
    norm_const = integrate.quad(target_dstn_func_, -np.inf, np.inf)[0]  # normalization constant
    plot_y = target_dstn_func_(plot_x) / norm_const  # use numerical integration to get the normalized distribution
    # plot
    sns.set()
    fig, ax = plt.subplots()
    sns.distplot(result, ax=ax, label='MH Sampler', norm_hist=True, kde=False, bins=50)
    sns.lineplot(plot_x, plot_y, ax=ax, label='Target Distribution')
    plt.show()
