EXPERIMENT = {

    "seed": 1,

    "data_folder": "data/example1",

    "method": "method_1",

    "method_params": {
        "tau_min": -20,
        "tau_max": 2,
        "tau_number": 300
    },

    "bounds": "method_1_bounds_th_1_1",

    "bounds_params": {
        "delta": 1e-15,
        "tau_min": -20,
        "tau_max": 2,
        "tau_number": 300
    },

    "calculate_tau0": True,

    "plot": {
        "grid": True,
        "ylim": (1e-14, 1e5)
    }
}