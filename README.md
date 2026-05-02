# Tuning the Brain Rhythms: How Internal Coherence Influences Network Entrainment by tACS

Code repository for the paper:

> **Tuning the brain rhythms: How internal coherence influences network entrainment by tACS**  
> *Chaos, Solitons & Fractals* (2025)  
> doi: [10.1016/j.chaos.2025.014341](https://www.sciencedirect.com/science/article/abs/pii/S0960077925014341)

---

## Overview

We study how the endogenous synchrony of a recurrent excitatory–inhibitory (E-I)
spiking neural network determines its susceptibility to entrainment by transcranial
alternating current stimulation (tACS). Using a biophysically plausible NEST model
we sweep stimulation frequency (5–55 Hz) and amplitude (0–10 pA) across three
synchrony regimes (low / medium / high) and quantify entrainment via the
Phase-Locking Value (PLV), Fano Factor, and Q-factor of the resonance peak.

**Key findings**
- Highly synchronised networks resist entrainment except near their intrinsic resonance frequency.
- Weakly synchronised networks entrain broadly across frequencies.
- The resonance sharpness (Q-factor) scales with baseline coherence.

---

## Repository structure

```
ei_ac_tacs/
│
├── src/
│   ├── simulate.py    ← NEST E-I network + tACS (core simulator)
│   ├── analysis.py    ← PLV, Fano factor, Q-factor, order parameter, …
│   ├── io_utils.py    ← save / load .npz and CSV outputs
│   └── plot_utils.py  ← all figure-generation functions
│
├── sweep.py           ← parameter sweep (freq × amp × synch × trials)
│
├── notebooks/
│   ├── 01_single_simulation.ipynb   ← run one simulation and inspect
│   ├── 02_baseline_activity.ipynb   ← baseline raster + FFT
│   ├── 03_plv_vs_frequency.ipynb    ← Fig. 3 – PLV vs stim. frequency
│   ├── 04_plv_heatmap.ipynb         ← Fig. 3 – heatmaps
│   ├── 05_q_factor.ipynb            ← Q-factor of resonance peak
│   ├── 06_fano_factor.ipynb         ← Fano factor
│   ├── 07_spike_coherence.ipynb     ← spike-phase analysis
│   └── 08_significance.ipynb        ← Wilcoxon tests
│
├── data/
│   └── metadata_ei-ac.csv           ← summary of all simulations + simulation results
│
├── figures/                         ← generated .eps figures
│
├── requirements.txt
└── README.md
```

---

## Installation

### Prerequisites

- Python ≥ 3.10
- [NEST simulator](https://www.nest-simulator.org/) ≥ 3.0

for nest I have used the docker image `nest/nest-simulator:3.8`. 

### Python dependencies

```bash
pip install -r requirements.txt
```

---

## Quick start
### 0. start environment using Docker

To fully reproduce the simulation environment, you can either run the Docker container manually or use the included `docker-compose.yml` file for a one-command setup.

1. Make sure [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed.

2. From the root of the repository, run:

```bash
docker-compose up 
```
3. Once the container starts, you’ll see a Jupyter Notebook access link in the terminal (e.g. http://localhost:8080/). Open it in your browser to get started. 


### 1. Single simulation

```python
from src.simulate import simulate
from src.analysis  import analyze_response
from src.plot_utils import plot_baseline_activity, plot_single_trial

# Run a 10-second simulation with 30 Hz tACS at 6 pA amplitude
response = simulate(
    T=10_000,
    ac_freq_ex=30, ac_amp_ex=6,
    ac_freq_in=30, ac_amp_in=6,
    rate_input_ex=16_500,
    rate_input_in=17_000,
)

results = analyze_response(response)
print(f"PLV (exc): {results['plv_ac_pop_exc']:.3f}")
print(f"Fano factor: {results['fano_factor_ex']:.3f}")

plot_baseline_activity(response)
plot_single_trial(response, results)
```

### 2. Full parameter sweep

```bash
# Runs all 3 × 4 × 11 × 9 = 1188 simulations (~hours on a workstation)
python sweep.py

# Only the high-synchrony regime
python sweep.py --synch high_synch

# Dry run (no simulation, just print the config)
python sweep.py --dry-run
```

### 3. Reproduce figures

After the sweep has finished and `data/metadata_ei-ac.csv` exists:

```python
import pandas as pd
from src.plot_utils import plot_plv_vs_freq, plot_plv_heatmap, plot_q_factor

metadata = pd.read_csv("data/metadata_ei-ac.csv")

plot_plv_vs_freq(metadata, synch_level="high_synch", savepath="figures/plv_high.eps")
plot_plv_heatmap(metadata, synch_level="high_synch", savepath="figures/heatmap_high.eps")
plot_q_factor(metadata, savepath="figures/qfactor.eps")
```

Or run the notebooks in `notebooks/` sequentially.

---

## Data

Each simulation produces three files under
`data/<synch_level>/amplitude_<amp>/frequency_<freq>/trial_<n>/`:

| File | Contents |
|------|----------|
| `response.npz` | Full NEST output (spike times, senders, multimeter) |
| `analysis.csv` | Per-neuron Kuramoto order parameter |
| `time_statistics.csv` | Time-series: population activity, phase, AC waveform |

`data/metadata_ei-ac.csv` aggregates all key metrics (PLV per band, Fano factor,
dominant frequencies) in one table for easy analysis.

---

## Citation

```bibtex
@article{ei_ac_tacs_2025,
  title   = {Tuning the brain rhythms: How internal coherence influences
             network entrainment by tACS},
  journal = {Chaos, Solitons \& Fractals},
  year    = {2025},
  doi     = {10.1016/j.chaos.2025.014341},
}
```

<!--
---

 ## License

MIT License — see `LICENSE`. -->


