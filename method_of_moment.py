import numpy as np
import scipy.optimize

def MyFunction(z, mu_hat, sigma2_hat, skew_hat):
    a = z[0]
    mu = z[1]
    sigma = z[2]

    F = np.empty((3))
    F[0] = a + mu - mu_hat
    F[1] = np.power(sigma, 2) + np.power(mu, 2) - sigma2_hat
    F[2] =( mu * (3*np.power(sigma,2) + 2*np.power(mu, 2))/((np.power(sigma, 2) + np.power(mu, 2))**(3/2)) ) - skew_hat

    return F

# zGuess = np.array([1,1,1])
# z = scipy.optimize.fsolve(MyFunction, zGuess, args=(0.0003757276611566701, 0.0004764892998391251,0.29824503829301885))
# print(z)

