EXPERIMENT = {

    "seed": 1,

    "data_folder": "data/example1",

    "method": "method_2",

    "method_params": {
        "delta": 1e-15,
        "samples_number": 20,
        "h": 1e-3,
        "tau_min": -20,
        "tau_max": 2,
        "tau_number": 300
    },

    "bounds": "method_2_error",

    "bounds_params": {
        "delta": 1e-15,
        "tau_min": -20,
        "tau_max": 2,
        "tau_number": 300
    },

    "calculate_tau0": False,

    "plot": {
        "grid": True,
        "ylim": (1e-11, 1e1)
    }
}