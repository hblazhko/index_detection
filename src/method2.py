import numpy as np
from scipy.linalg import eig
from numpy.linalg import cond
from scipy.linalg import svdvals

def method_2(A, E, samples_number=10, h=np.exp(-3), tau_min=-20, tau_max=2, tau_number=300):
    """
    Compute the distance of the eigenvalues of the perturbed Cayley transform
    (E - hA)^{-1}(E + hA) + tau X to -1 averaged over random Gaussian perturbations X.
    """
    k = A.shape[0]
    taus = np.logspace(tau_min, tau_max, tau_number)

    M = np.linalg.solve(E - h * A, E + h * A)

    dist = np.empty((samples_number, tau_number))

    for js in range(samples_number):
        X = np.random.randn(k, k)
        X = X @ X.T
        X /= np.linalg.norm(X) ** 2

        for jn, tau in enumerate(taus):
            eigenvalues = eig(M + tau * X, left=False, right=False)
            dist[js, jn] = np.min(np.abs(eigenvalues + 1))

    dist = dist.mean(axis=0)

    return {
        'tau': taus,
        'dist': dist,
    }


def method_2_error(n, delta=1e-15, tau_min=-20, tau_max=2, tau_number=300):
    """Error estimate from Theorem 1.2"""

    taus = np.logspace(tau_min, tau_max, tau_number)

    beta = n * np.sqrt(
        11
        + 4 * np.sqrt(2)
        + np.sqrt(np.pi) / (2 * n**(3/2))
        + (4 * np.sqrt(2) + 4) / n
        + np.sqrt(np.pi) * (8 * np.sqrt(2) + 12) / np.sqrt(n)
    )

    coef = delta * beta

    errors = coef / taus

    return {
        'tau': taus,
        'errors': errors,
    }
