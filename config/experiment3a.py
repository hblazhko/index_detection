EXPERIMENT = {

    "seed": 1,

    "data_folder": "data/example3a",

    "method": "method_1",

    "method_params": {
        "tau_min": -20,
        "tau_max": 2,
        "tau_number": 300
    },

    "bounds": "method_1_bounds_cor_3_3",

    "bounds_params": {
        "delta": 3*1e-15,
        "tau_min": -20,
        "tau_max": 2,
        "tau_number": 300
    },

    "calculate_tau0": True,

    "plot": {
        "grid": True,
        "ylim": (1e-25, 1e5)
    }
}