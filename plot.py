# python
import argparse
import os
import logging
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt

from src.utils import load_config, load_matrices, call_function, compute_bounds
from src.method1 import compute_tau0
from src.method2 import method_2, method_2_error
from src.method1 import method_1, method_1_bounds_cor_2_2, method_1_bounds_cor_2_3, method_1_bounds_th_1_1
from src.utils import plot_method1, plot_method2

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


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Plot experiment results for index_detection")
    p.add_argument("config", help="Path to experiment config (python file or json)")
    p.add_argument("--save", "-s", metavar="OUT", help="Save plot to path (PNG/PDF). If omitted, show interactively.")
    p.add_argument("--no-show", action="store_true", help="Do not call plt.show() (useful in CI).")
    return p


def run_plot(config_path: str, save_path: Optional[str] = None, show: bool = True) -> plt.Figure:
    exp = load_config(config_path)
    if not isinstance(exp, dict):
        raise ValueError("Loaded config must be a dict-like object")

    seed = exp.get("seed")
    if seed is not None:
        np.random.seed(seed)

    data_folder = exp.get("data_folder")
    if not data_folder:
        raise KeyError("config missing required key: data_folder")
    matrices = load_matrices(data_folder)

    method_name = exp.get("method")
    if method_name not in METHODS:
        raise KeyError(f"Unsupported method: {method_name}")

    method_fun = METHODS[method_name]
    method_params = exp.get("method_params", {})

    calc = call_function(method_fun, matrices, method_params)

    bounds = compute_bounds(exp, matrices, calc, BOUNDS)

    tau0 = None
    delta = None
    if method_name == "method_1":
        if exp.get("calculate_tau0", False):
            tau0 = call_function(compute_tau0, matrices, method_params)
        delta = exp.get("bounds_params", {}).get("delta")

    fig, ax = plt.subplots()
    ax.set_box_aspect(4 / 7)

    if method_name == "method_1":
        plot_method1(ax, calc, bounds, tau0, delta)
    else:
        plot_method2(ax, calc, bounds)

    plot_opts = exp.get("plot", {})
    if plot_opts.get("grid"):
        ax.grid(True)
    if "ylim" in plot_opts:
        ax.set_ylim(*plot_opts["ylim"])
    if "xlim" in plot_opts:
        ax.set_xlim(*plot_opts["xlim"])

    plt.tight_layout()

    if save_path:
        out_dir = os.path.dirname(save_path) or "."
        os.makedirs(out_dir, exist_ok=True)
        fig.savefig(save_path)
        logging.info("Saved figure to %s", save_path)

    if show and not save_path and not plt.isinteractive():
        plt.show()

    return fig


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run_plot(args.config, save_path=args.save, show=not args.no_show)


if __name__ == "__main__":
    main()
