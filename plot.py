import sys
import numpy as np
import matplotlib.pyplot as plt
import importlib.util
from pathlib import Path

from src.method1 import (
    method_1,
    method_1_bounds_cor_2_2,
    method_1_bounds_cor_2_3,
    method_1_bounds_th_1_1,
    compute_tau0
)
from src.method2 import method_2, method_2_error


METHODS = {
    "method_1": method_1,
    "method_2": method_2,
}

BOUNDS = {
    "method_1_bounds_th_1_1": method_1_bounds_th_1_1,
    "method_1_bounds_cor_2_2": method_1_bounds_cor_2_2,
    "method_1_bounds_cor_2_3": method_1_bounds_cor_2_3,
    "method_2_error": method_2_error,
}

METHOD_ARGS = {
    "method_1": ["A", "E"],
    "method_2": ["A", "E"],
}

BOUNDS_ARGS = {
    "method_1_bounds_th_1_1": ["A", "E", "A12", "A21", "E11"],
    "method_1_bounds_cor_2_2": ["A", "E", "A12", "A21", "E11"],
    "method_1_bounds_cor_2_3": ["A", "E"],
    "method_2_error": ["A"],
}

TAU0_ARGS = ["A", "E", "A11", "E11"]


def load_config(path):

    spec = importlib.util.spec_from_file_location("config", path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    return config.EXPERIMENT


def load_matrices(folder):

    folder = Path(folder)
    matrices = {}

    for name in ["A", "E", "Q", "A11", "A12", "A21", "E11"]:
        file = folder / f"{name}.npy"
        if file.exists():
            matrices[name] = np.load(file)

    return matrices


def select_args(names, matrices):

    return {k: matrices[k] for k in names if k in matrices}


def main():

    if len(sys.argv) < 2:
        raise ValueError("Usage: python plot.py config/experiment.py")

    config_path = sys.argv[1]
    save = "--save" in sys.argv

    exp = load_config(config_path)

    if "seed" in exp:
        np.random.seed(exp["seed"])

    matrices = load_matrices(exp["data_folder"])

    method_fun = METHODS[exp["method"]]
    bounds_fun = BOUNDS[exp["bounds"]]

    method_args = select_args(METHOD_ARGS[exp["method"]], matrices)

    calc = method_fun(**method_args, **exp["method_params"])

    if exp["bounds"] == "method_2_error":

        n = matrices["A"].shape[0]

        bounds = bounds_fun(
            n,
            **exp["bounds_params"]
        )

    else:

        bounds_args = select_args(BOUNDS_ARGS[exp["bounds"]], matrices)

        bounds = bounds_fun(**bounds_args, **exp["bounds_params"])

    delta = exp["bounds_params"].get("delta", None)

    tau0 = None

    if exp.get("calculate_tau0", False):

        tau0_args = select_args(TAU0_ARGS, matrices)

        tau0 = compute_tau0(
            **tau0_args,
            **exp["method_params"]
        )

    fig, ax = plt.subplots()

    ax.set_box_aspect(4 / 7)

    if exp["method"] == "method_1":

        ax.loglog(calc["tau"], 1 / calc["dist"], linewidth=1.9, color="C0")

        ax.loglog(
            bounds["tau"],
            1 / bounds["upper_bounds"],
            linestyle="-.",
            linewidth=1.9,
            color="C1",
        )

        ax.loglog(
            bounds["tau"],
            1 / bounds["lower_bounds"],
            linestyle="-.",
            linewidth=1.9,
            color="C1",
        )

    else:

        ax.loglog(calc["tau"], calc["dist"], linewidth=1.9, color="C0")

        ax.loglog(
            bounds["tau"],
            bounds["lower"],
            linestyle="-.",
            linewidth=1.9,
            color="C2",
        )

        ax.loglog(
            bounds["tau"],
            bounds["upper"],
            linestyle="-.",
            linewidth=1.9,
            color="C2",
        )

    if tau0 is not None and np.isfinite(tau0):
        ax.axvline(tau0, linestyle=":", linewidth=1.8, color="C3")

    if delta is not None:
        ax.axvline(delta, linestyle="--", linewidth=1.8, color="C4")

    plot = exp.get("plot", {})

    if plot.get("grid", False):
        ax.grid(True)

    if "ylim" in plot:
        ax.set_ylim(*plot["ylim"])

    if "xlim" in plot:
        ax.set_xlim(*plot["xlim"])

    plt.tight_layout()

    if save:
        plt.savefig("figure.pdf")
    else:
        plt.show()


if __name__ == "__main__":
    main()