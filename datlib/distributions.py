# distributions.py

import numpy as np

def normal_distribution(mean , sd, x = np.linspace(-10, 10, 1000)):
    prob_density = 1/(np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    return prob_density

def t_distribution(x, df):
    x = np.linspace(-5, 5, 1000) # large number of points will ensure accuracy
    # transform flat array of x values into t distribution
    t_distribution = ((1+x**2/df)**(-(df+1)/2))/(sc.beta(.5, .5*df)*np.sqrt(df))
    return t_distribution

def lognormal_distribution(mean, sd, x = np.linspace(-5, 5, 1000)):
    density_points = (1 / x*sd*np.sqrt(2*math.pi))*math.e**(-(np.log(x)-mean)**2 / (2*sd**2))
    return density_points

def binomial_distribution(x, n, p):
    return float(math.factorial(n)) / (
        math.factorial(x) * math.factorial(n - x)) * p**x * (1 - p)**(n - x)

def poisson_distribution(x, mean):
    p = ((mean**x) * (math.e**-mean)) / math.factorial(x)
    return p
