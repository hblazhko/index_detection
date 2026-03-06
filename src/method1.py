import numpy as np
from scipy.linalg import eig
from numpy.linalg import cond
from scipy.linalg import svdvals

def method_1(A, E, tau_min=-20, tau_max=2, tau_number=300):
    """
    Compute reciprocal of smallest absolute eigenvalue of the reversal pencil
    lambda A + (E + tau I) over logspace taus.
    """
    k = A.shape[0]
    taus = np.logspace(tau_min, tau_max, tau_number)
    I = np.eye(k)

    distances = np.empty(tau_number)

    for j, tau in enumerate(taus):
        CE = E + tau * I
        ev = eig(CE, A)[0]
        distances[j] = np.min(np.abs(ev))

    return {
        'tau': taus,
        'dist': 1 / distances,
    }


def compute_tau0(A, E, A11, E11, tau_min=-20, tau_max=2, tau_number=300):
    """Compute tau0 from Theorem 1.1., equation (1.3). """
    taus = np.logspace(tau_min, tau_max, tau_number)

    sigma_min_E11 = np.linalg.svd(E11, compute_uv=False)[-1]
    norm_A11 = np.linalg.norm(A11)

    I = np.eye(E.shape[0])

    tau0 = None

    for tau in taus:

        eigs = eig(A, E + tau * I, left=False, right=False)

        rhs = norm_A11 / (tau + sigma_min_E11)

        if np.abs(eigs).max() > rhs:
            tau0 = tau

    if tau0 is None:
        return 0.0

    return tau0


def method_1_bounds_th_1_1(A, E, A12, A21, E11, delta=1e-15,
                           tau_min=-20, tau_max=2, tau_number=300):
    """Bounds from Theorem 1.1 (explicit block structure). """
    taus = np.logspace(tau_min, tau_max, tau_number)

    A12A21 = A12 @ A21

    norm_A = np.linalg.norm(A)
    norm_E11 = np.linalg.norm(E11)
    norm_A12A21 = np.linalg.norm(A12A21)

    sigma_min_A12A21 = svdvals(A12A21)[-1]
    sigma_min_E11 = svdvals(E11)[-1]

    lower_bounds = np.empty(tau_number)
    upper_bounds = np.empty(tau_number)

    I = np.eye(A.shape[0])

    for j, tau in enumerate(taus):
        _, V = eig(E + tau * I, A)
        kappa_V = cond(V)

        gamma = delta * kappa_V * (tau + norm_A) / (tau * (tau - delta))

        lower = np.sqrt(sigma_min_A12A21 / ((norm_E11 + 2 * tau) * tau)) - gamma
        upper = np.sqrt(norm_A12A21 / (sigma_min_E11 * tau)) + gamma

        lower_bounds[j] = max(lower, 0.0)
        upper_bounds[j] = upper

    return {
        'tau': taus,
        'lower_bounds': lower_bounds,
        'upper_bounds': upper_bounds,
    }


def method_1_bounds_cor_2_3(A, E, delta=1e-15,
                             tau_min=-20, tau_max=2, tau_number=300):
    """Bounds from Corollary 2.3 (E positively diagonalizable)."""
    taus = np.logspace(tau_min, tau_max, tau_number)

    norm_A = np.linalg.norm(A)
    norm_E = np.linalg.norm(E)

    sigma_min_A = svdvals(A)[-1]
    sigma_min_E = svdvals(E)[-1]

    _, V = eig(E)
    kappa_V_E = cond(V)

    kappa_V_E2 = kappa_V_E**2
    kappa_V_E32 = kappa_V_E**1.5

    lower_bounds = np.empty(tau_number)
    upper_bounds = np.empty(tau_number)

    I = np.eye(A.shape[0])

    for j, tau in enumerate(taus):
        _, V = eig(E + tau * I, A)
        kappa_V = cond(V)

        gamma = delta * kappa_V * kappa_V_E2 * (tau + norm_A * kappa_V_E) / (tau * (tau - delta))

        lower = sigma_min_A / (kappa_V_E * np.sqrt(norm_E * kappa_V_E + 2 * tau) * np.sqrt(tau)) - gamma
        upper = norm_A * kappa_V_E32 / (np.sqrt(sigma_min_E) * np.sqrt(tau)) + gamma

        lower_bounds[j] = lower
        upper_bounds[j] = upper

    return {
        'tau': taus,
        'lower_bounds': lower_bounds,
        'upper_bounds': upper_bounds,
    }


def method_1_bounds_cor_2_2(A, E, A12, A21, E11, delta=1e-6,
                           tau_min=-20, tau_max=2, tau_number=300):
    """Bounds from Corollary 2.2 (explicit block structure, Delta_E = 0). """
    taus = np.logspace(tau_min, tau_max, tau_number)

    A12A21 = A12 @ A21

    norm_E11 = np.linalg.norm(E11)
    norm_A12A21 = np.linalg.norm(A12A21)

    sigma_min_A12A21 = svdvals(A12A21)[-1]
    sigma_min_E11 = svdvals(E11)[-1]

    lower_bounds = np.empty(tau_number)
    upper_bounds = np.empty(tau_number)

    I = np.eye(A.shape[0])

    for j, tau in enumerate(taus):
        _, V = eig(E + tau * I, A)
        kappa_V = cond(V)

        gamma = delta * kappa_V / tau

        lower = np.sqrt(sigma_min_A12A21 / ((norm_E11 + 2 * tau) * tau)) - gamma
        upper = np.sqrt(norm_A12A21 / (sigma_min_E11 * tau)) + gamma

        lower_bounds[j] = max(lower, 0.0)
        upper_bounds[j] = max(upper, 0.0)

    return {
        'tau': taus,
        'lower_bounds': lower_bounds,
        'upper_bounds': upper_bounds,
    }

