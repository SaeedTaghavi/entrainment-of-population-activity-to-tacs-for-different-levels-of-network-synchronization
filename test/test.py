from pathlib import Path
import sys
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.simulate import simulate
from src.analysis import analyze_response

response = simulate(T=2000)

results = analyze_response(response)

print("Dominant frequency:", results["dominant_frequency"])
print("Fano factor:", results["fano_factor"])
print("PLV:", results["plv"])

np.savez_compressed("data/test_response.npz", response=response)
np.savez_compressed("data/test_analysis.npz", **results)


from src.plot_utils import plot_population_and_raster

plot_population_and_raster(response, population="ex", t_start=1000)