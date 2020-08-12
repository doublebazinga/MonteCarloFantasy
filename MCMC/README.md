# Markov Chain Monte Carlo
(Murphy K. P. 2012, Ch24) The basic idea behind MCMC is to construct a Markov Chain on the state space X whose
stationary distribution is the target density p^{*}(x) of interest

## Gibbs Sampling
(The reference to this section is Murphy K. P. 2012, Ch24.2)

* Gibbs sampling is also known as Glauber dynamics or the heat bath method. 
* Gibbs sampling is the MCMC analog of coordinate descent. 

### Basic Idea 
* We sample each variable in turn, conditioned on the values of all the other variables in the distribution


# Reference
1. Andrieu, Christophe, et al. "An introduction to MCMC for machine learning." Machine learning 50.1-2 (2003): 5-43.
2. Murphy, Kevin P. Machine learning: a probabilistic perspective. MIT press, 2012.