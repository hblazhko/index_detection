# index_detection

Code and data for reproducing the numerical experiments in the paper **“Index Detection.”**

The repository implements two numerical procedures (`method_1` and `method_2`) together with several theoretical bounds derived in the paper.  
Experiments are configured through a Python configuration file and executed using a command-line plotting script.

The main entry point is **`plot.py`**, which:

1. Loads matrices from a dataset
2. Runs the selected numerical method
3. Optionally computes theoretical bounds
4. Produces a log–log plot of the results

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<username>/index_detection.git
cd index_detection
```

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```


---

# Quick Usage

Run the plotting script with a configuration file defining an `EXPERIMENT` dictionary.

### Interactive plot

```bash
python plot.py config/experiment1.py
```

### Save plot to file

```bash
python plot.py config/experiment1.py --save results/plot.png

```

---

# Command-Line Arguments

`plot.py` accepts the following arguments:

| Argument | Description |
|--------|-------------|
| `config` | Path to the experiment configuration file |
| `--save`, `-s OUT` | Save the produced figure to `OUT` (PNG or PDF) |
| `--no-show` | Do not display the plot interactively |

Example:

```bash
python plot.py config/experiments.py --save figures/run1.pdf --no-show
```

---

# Repository Structure

```
index_detection/
│
├── plot.py                # Main experiment runner and plotting script
├── requirements.txt       # Python dependencies
│
├── src/
│   ├── method1.py         # Implementation of method 1 and its bounds
│   ├── method2.py         # Implementation of method 2 and its bounds
│   └── utils.py           # Helper utilities (loading data, plotting, etc.)
│
├── config/
│   └── experiment1.py     # Example experiment configuration
│
└──data/
    └── example1           # Matrix datasets (.npy files)
```

---
## Configuration

Experiments are defined by a Python config containing an `EXPERIMENT` dictionary.

### Required fields

#### `data_folder`

Path to a directory containing the `.npy` matrices used in the experiment.

Example:

```
data/run1/
    A.npy
    E.npy
    Q.npy
```

Possible files include `A.npy`, `E.npy`, `Q.npy`, `A11.npy`, `A12.npy`, `A21.npy`, `E11.npy` (depending on the experiment).

#### `method`

Specifies which numerical method to run:

```
method_1
method_2
```

---

### Method parameters

Optional parameters passed to the selected method:

```python
"method_params": {...}
```

Typical values:

**method_1**
```python
tau_min = -20
tau_max = 2
tau_number = 300
```

**method_2**
```python
samples_number = 10
h = np.exp(-3)
tau_min = -20
tau_max = 2
tau_number = 300
```

---

### Optional fields

**Random seed**

```python
"seed": 42
```

**Bounds**

Optional theoretical bounds to plot:

```
method_1_bounds_th_1_1
method_1_bounds_cor_2_2
method_1_bounds_cor_2_3
method_2_error
None
```

Example:

```python
"bounds": "method_1_bounds_th_1_1"
```

**Bounds parameters**

```python
"bounds_params": {
    "delta": 1e-15,
    "tau_min": -20,
    "tau_max": 2,
    "tau_number": 300
}
```

**Compute τ₀ (method_1 only)**

```python
"calculate_tau0": True
```

**Plot options**

```python
"plot": {
    "grid": True,
    "xlim": [1e-4, 1e2],
    "ylim": [1e-8, 1e2]
}
```

# Minimal Configuration Example

Example file: `config/my_experiment.py`

```python
EXPERIMENT = {
    "data_folder": "data/example1",

    "method": "method_1",

    "method_params": {},

    "seed": 42,

    "bounds": "method_1_bounds_th_1_1",

    "bounds_params": {
        "delta": 1e-15
    },

    "calculate_tau0": True,

    "plot": {
        "grid": True,
        "xlim": [1e-4, 1e2],
        "ylim": [1e-8, 1e2]
    }
}
```

Run it using:

```bash
python plot.py config/my_experiment.py
```

Other example configurations are available in the `config/` directory.