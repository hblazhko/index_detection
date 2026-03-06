# python
"""Utilities for config/matrix loading, optional bounds computation, and plotting."""
import numpy as np
import importlib.util
import inspect
from pathlib import Path


def load_config(path):
    """Load experiment configuration from a Python file that provides EXPERIMENT."""
    spec = importlib.util.spec_from_file_location("config", path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    return config.EXPERIMENT


def load_matrices(folder):
    """Load named matrices from the data folder if the corresponding `.npy` files exist."""
    folder = Path(folder)

    matrices = {}
    # Load only the files the rest of the code expects.
    for name in ["A", "E", "Q", "A11", "A12", "A21", "E11"]:
        file = folder / f"{name}.npy"
        if file.exists():
            matrices[name] = np.load(file)

    return matrices


def call_function(func, matrices, params):
    """
    Call `func` passing only the arguments it expects.
    Parameters are taken from `matrices` or from `params` (config).
    """
    sig = inspect.signature(func)
    kwargs = {}

    # Build kwargs by matching parameter names.
    for name in sig.parameters:
        if name in matrices:
            kwargs[name] = matrices[name]
        elif name in params:
            kwargs[name] = params[name]

    return func(**kwargs)


def compute_bounds(exp, matrices, calc, bounds_dict):
    """
    Compute bounds according to the experiment config.

    If `exp["bounds"]` is None, no bounds are computed and None is returned.
    If the chosen bounds key is `method_2_error`, convert the returned
    `errors` array into explicit lower/upper arrays matching `calc["dist"]`.
    """
    bkey = exp.get("bounds", None)
    if bkey is None:
        return None

    if bkey not in bounds_dict:
        raise KeyError(f"Unsupported bounds key: {bkey}")

    result = call_function(bounds_dict[bkey], matrices, exp.get("bounds_params", {}))

    # Special handling for method_2_error which provides error bars.
    if bkey == "method_2_error":
        lower = calc["dist"] - result["errors"]
        upper = calc["dist"] + result["errors"]

        # Ensure lower bound is positive (avoid plotting non-positive values).
        lower[lower <= 0] = np.min(calc["dist"]) * 1e-12

        return {
            "tau": result["tau"],
            "lower": lower,
            "upper": upper,
        }

    return result


def plot_method1(ax, calc, bounds, tau0, delta):
    """Plot results for method 1. """
    # Compute reciprocal safely
    with np.errstate(divide="ignore", invalid="ignore"):
        y_calc = 1.0 / calc["dist"]

    ax.loglog(calc["tau"], y_calc, linewidth=1.9, color="C0")

    # Plot bounds if provided by config.
    if bounds is not None:
        ub = np.asarray(bounds.get("upper_bounds", bounds.get("upper", np.array([]))), dtype=float)
        lb = np.asarray(bounds.get("lower_bounds", bounds.get("lower", np.array([]))), dtype=float)
        tau_bounds = bounds.get("tau", None)

        if tau_bounds is not None and ub.size and lb.size:
            # Only invert finite and positive entries; otherwise set to nan.
            with np.errstate(divide="ignore", invalid="ignore"):
                inv_ub = np.where((ub > 0) & np.isfinite(ub), 1.0 / ub, np.nan)
                inv_lb = np.where((lb > 0) & np.isfinite(lb), 1.0 / lb, np.nan)

            ax.loglog(tau_bounds, inv_ub, linestyle="-.", linewidth=1.9, color="C1")
            ax.loglog(tau_bounds, inv_lb, linestyle="-.", linewidth=1.9, color="C1")

    # Optional vertical markers for tau0 and delta if provided.
    if tau0 is not None and np.isfinite(tau0):
        ax.axvline(tau0, linestyle=":", linewidth=1.8, color="C3")

    if delta is not None:
        ax.axvline(delta, linestyle="--", linewidth=1.8, color="C4")


def plot_method2(ax, calc, bounds):
    """Plot results for method 2."""
    ax.loglog(calc["tau"], calc["dist"], linewidth=1.9, color="C0")

    if bounds is None:
        return

    tau_bounds = bounds.get("tau", None)
    lower = bounds.get("lower", None)
    upper = bounds.get("upper", None)

    # Plot provided lower/upper curves if available.
    if tau_bounds is not None and lower is not None:
        ax.loglog(tau_bounds, lower, linestyle="-.", linewidth=1.9, color="C2")

    if tau_bounds is not None and upper is not None:
        ax.loglog(tau_bounds, upper, linestyle="-.", linewidth=1.9, color="C2")
