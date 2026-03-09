EXPERIMENT = {

    "seed": 1,

    "data_folder": "data/example2",

    "method": "method_1",

    "method_params": {
        "delta": 1e-15,
        "tau_min": -20,
        "tau_max": 2,
        "tau_number": 300
    },

    "bounds": "method_1_bounds_cor_2_3",

    "bounds_params": {
        "delta": 1e-15,
        "tau_min": -20,
        "tau_max": 2,
        "tau_number": 300
    },

    "calculate_tau0": False,

    "plot": {
        "grid": True,
        "ylim": (1e-22, 1e1)
    }
}