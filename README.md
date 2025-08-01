# Entrainment of Population Activity to tACS for Different Levels of Network Synchronization

This repository contains Jupyter notebooks used for simulating, analyzing, and visualizing how a spiking neural network entrains to transcranial alternating current stimulation (tACS) under different levels of internal network synchronization. The simulations were performed using the NEST Simulator (v3.8) inside a Docker container.

## 🧠 Project Overview

We explored how varying intrinsic synchrony in a recurrent excitatory-inhibitory network affects its susceptibility to rhythmic entrainment by weak external inputs mimicking tACS. The simulations were conducted using a biologically inspired AdEx spiking neuron model, and the analysis focused on population and single-neuron phase locking, Arnold tongues, frequency tracking, and synchrony metrics.

All results and figures in the related manuscript were generated using the notebooks in this repository.

## 🗂 Repository Structure
.
├── notebooks/ # Jupyter notebooks for simulation and analysis
│ ├── 01_generate_data.ipynb
│ ├── 02_analyze_locking.ipynb
│ ├── 03_plot_figures.ipynb
│ └── ...
├── figures/ # Output figures from the manuscript
├── data/ # Optional: generated or processed simulation results
├── README.md # This file
├── requirements.txt # Python dependencies (used outside Docker)
└── LICENSE # Open-source license (MIT)


## 🚀 Getting Started

### 🐳 Recommended: Run via Docker

To fully reproduce the simulation environment, you can either run the Docker container manually or use the included `docker-compose.yml` file for a one-command setup.

#### Option 1: Using Docker Compose (easiest)

1. Make sure [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed.

2. From the root of the repository, run:

```bash
docker-compose up
```
3. Once the container starts, you’ll see a Jupyter Notebook access link in the terminal (e.g. http://localhost:8080/). Open it in your browser to get started.
