# python
import numpy as np
import importlib.util
import inspect
from pathlib import Path


def load_config(path):
    """Load experiment configuration from a Python file."""

    spec = importlib.util.spec_from_file_location("config", path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    return config.EXPERIMENT


def load_matrices(folder):
    """Load matrices from the data folder if they exist."""

    folder = Path(folder)

    matrices = {}

    for name in ["A", "E", "Q", "A11", "A12", "A21", "E11"]:

        file = folder / f"{name}.npy"

        if file.exists():
            matrices[name] = np.load(file)

    return matrices


def call_function(func, matrices, params):
    """
    Call a function passing only the arguments it expects.
    Arguments are taken from matrices or params.
    """

    sig = inspect.signature(func)

    kwargs = {}

    for name in sig.parameters:

        if name in matrices:
            kwargs[name] = matrices[name]

        elif name in params:
            kwargs[name] = params[name]

    return func(**kwargs)


def compute_bounds(exp, matrices, calc, bounds_dict):
    """
    Compute bounds for the experiment.

    If exp.get("bounds") is None, do not compute bounds and return None.
    Handles special conversion for method_2_error when a bounds key is provided.
    """
    bkey = exp.get("bounds", None)
    if bkey is None:
        return None

    if bkey not in bounds_dict:
        raise KeyError(f"Unsupported bounds key: {bkey}")

    result = call_function(bounds_dict[bkey], matrices, exp.get("bounds_params", {}))

    if bkey == "method_2_error":
        lower = calc["dist"] - result["errors"]
        upper = calc["dist"] + result["errors"]

        lower[lower <= 0] = np.min(calc["dist"]) * 1e-12

        return {
            "tau": result["tau"],
            "lower": lower,
            "upper": upper,
        }

    return result


def plot_method1(ax, calc, bounds, tau0, delta):
    """Plot results for method 1.

    - Always plot the computed curve.
    - Plot bounds only if `bounds` is not None.
    - Invert bounds safely: invalid/zero/inf entries become `np.nan`.
    """
    # plot computed reciprocal
    with np.errstate(divide="ignore", invalid="ignore"):
        y_calc = 1.0 / calc["dist"]

    ax.loglog(calc["tau"], y_calc, linewidth=1.9, color="C0")

    # plot bounds only if provided
    if bounds is not None:
        # support both naming conventions returned by different bounds functions
        ub = np.asarray(bounds.get("upper_bounds", bounds.get("upper", np.array([]))), dtype=float)
        lb = np.asarray(bounds.get("lower_bounds", bounds.get("lower", np.array([]))), dtype=float)
        tau_bounds = bounds.get("tau", None)

        if tau_bounds is not None and ub.size and lb.size:
            # compute reciprocals only where finite and positive, else nan
            with np.errstate(divide="ignore", invalid="ignore"):
                inv_ub = np.where((ub > 0) & np.isfinite(ub), 1.0 / ub, np.nan)
                inv_lb = np.where((lb > 0) & np.isfinite(lb), 1.0 / lb, np.nan)

            ax.loglog(tau_bounds, inv_ub, linestyle="-.", linewidth=1.9, color="C1")
            ax.loglog(tau_bounds, inv_lb, linestyle="-.", linewidth=1.9, color="C1")

    if tau0 is not None and np.isfinite(tau0):
        ax.axvline(tau0, linestyle=":", linewidth=1.8, color="C3")

    if delta is not None:
        ax.axvline(delta, linestyle="--", linewidth=1.8, color="C4")


def plot_method2(ax, calc, bounds):
    """Plot results for method 2. Skip bounds if `bounds` is None."""
    ax.loglog(calc["tau"], calc["dist"], linewidth=1.9, color="C0")

    if bounds is None:
        return

    tau_bounds = bounds.get("tau", None)
    lower = bounds.get("lower", None)
    upper = bounds.get("upper", None)

    if tau_bounds is not None and lower is not None:
        ax.loglog(
            tau_bounds,
            lower,
            linestyle="-.",
            linewidth=1.9,
            color="C2",
        )

    if tau_bounds is not None and upper is not None:
        ax.loglog(
            tau_bounds,
            upper,
            linestyle="-.",
            linewidth=1.9,
            color="C2",
        )
