# Paleogeography files associated with DeepMIP-Eocene-Phase 2

The notebooks here are used to compare and generate a combine into a new paleogeography for use in Phase 2 of the early Eocene MIP.

Details on the experimental design for DeepMIP-Eocene-p2 can be found [here](https://egusphere.copernicus.org/preprints/2026/egusphere-2025-6135/). Some of the files produced by these notebooks can be found on the [Zenodo](https://zenodo.org/records/17899195).

Contents of the notebooks are as follows:
* [1_eocene_paleogeography_exploration.ipynb](1_eocene_paleogeography_exploration.ipynb): this notebook compares a number of different Eocene paleogeographies (largely, their paleotopography), e.g. relative to ETOPO. It also produces one of the paper figures.
* [2_new_eocene_paleogeography.ipynb](2_new_eocene_paleogeography.ipynb): **this notebook creates the new paleogeography for 51 Ma.** It does this by combining different paleogeographies per region as well as removes major artefacts where possible. Note that all paleogeographies that are being combined are first rotated into the preferred plate tectonic model/reference frame prior to merging.
* [3_new_eocene_paleogeography-PETM.ipynb](3_new_eocene_paleogeography-PETM.ipynb): similar to notebook 2 in execution, but this notebook creates a **PETM (56 Ma) paleogeography**.
* [4_rotate_paleogeography.ipynb](4_rotate_paleogeography.ipynb): this notebook rotates the paleogeography (by essentially shifting the *whole* grid) into new references frames and/or times. Please note that doing this 'shift' from 55 Ma <--> 51 Ma here will *not* account for changes in relative plate motion between the models.
* [5_reconstructing_points_DeepMIP.ipynb](5_reconstructing_points_DeepMIP.ipynb): this notebook calculates the 51 Ma coordinates for DeepMIP2-eocene-Phase 2 for a set of points (i.e. from an excel spreadsheet). Any spreadsheet/csv could be used here, as long as you have a present-day lat/lon

Input files such as the various netcdfs required and shapefiles used within the notebooks are also included. Plate tectonic files were downloaded in the notebooks, via [`plate_model_manager`](https://github.com/GPlates/plate-model-manager).

Please reach out with any questions, issues, or comments!
