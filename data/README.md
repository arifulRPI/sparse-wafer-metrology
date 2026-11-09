# Data

Two files from the public BOSCH deep-silicon-etch dataset, included unchanged:

| File | What it holds |
|---|---|
| `Si_Oxide_etch_89_points.csv` | 88 wafers × 89 sites, measured in February 2025 with one profilometer (KLA Tencor P-17) and one interferometer. Used columns: `experiment_key`, `lot_number`, `wafer_number`, `X`, `Y` (µm), `stepheight` and `si_etch` (µm). |
| `Si_Oxide_etch_9_points.csv` | The routine 9 sites, measured on the day of etching with a second profilometer (Veeco Dektak 8): 75 labelled wafers, 73 of them also in the 89-site file. Its coordinates are rotated 180° relative to the 89-site file. |

One etch tool processed 10 lots in July–August 2024; lot number follows etch date. The dataset's other files (optical emission spectra, about 8 GB, and process-sensor logs) aren't used yet and aren't included.

**Source and license.** J. Langer et al., *A Multi-Model Dataset for BOSCH Plasma-Etching: Optical Emission Spectra, Process Parameters, and Wafer Measurements for Data-Driven Plasma Modeling*, Zenodo, 2025. [doi:10.5281/zenodo.17122442](https://doi.org/10.5281/zenodo.17122442). Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), which allows redistribution with credit to the authors.
