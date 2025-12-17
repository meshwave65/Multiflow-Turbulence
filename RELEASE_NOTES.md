# **RELEASE_NOTES.md — Multiflux HIT Synthetic Turbulence (CPU Phase I)**

**Version: v1.0-cpu384**
**Date: December 2025**

---

## **Important Note About DOI**

The DOI **10.5281/zenodo.17887596** refers **only to the scientific artifact generated in Stage 1** (paper template and academic materials).
This release (CPU Phase I) does **not** yet have its own Zenodo DOI.

A dedicated DOI will be generated once the full dataset is deposited as a Zenodo record.

---

## **Summary**

This release marks the completion of **Phase I: CPU-based spectral synthetic turbulence generation and multiflux decomposition**, culminating in a fully reproducible **384³** homogeneous isotropic turbulence (HIT) realization, with complete invariant computation and stable multiflux partitioning.

All materials are provided under the
**Creative Commons Attribution–NonCommercial–ShareAlike 4.0 License (CC BY-NC-SA 4.0)**.

This dataset constitutes the computational foundation for the manuscript under preparation.

---

# **Included in this Release**

## **1. Full Synthetic HIT Fields**

Resolutions included:

* **64³**
* **128³**
* **192³**
* **256³**
* **384³** (maximum CPU resolution)

All generated via:

* spectral Fourier synthesis
* Kolmogorov (k^{-5/3}) spectrum
* exact solenoidal projection

---

## **2. Invariant Computation**

* vorticity magnitude ( |\omega| )
* Q-criterion
* ( \lambda_2 ) (eigenvalue of ( S^2 + \Omega^2 ))
* full velocity gradient tensor (A_{ij})
* computed using spectral differentiation

---

## **3. Multiflux Decomposition**

* k-means clustering (k = 12)
* standardized invariant triplet
* cluster volume fractions
* multi-threshold analysis (0.1–2.0%)
* **stable N_eff = 12 across all resolutions**

---

## **4. Visualizations**

* XY / XZ / YZ midplane slices
* complete labeled cluster maps
* histograms and colormaps

---

## **5. Reports and Data**

Each resolution directory contains:

* `report.txt`
* `cluster_volumes.csv`
* `meta.json`
* full PNG visualizations

---

## **6. CPU Phase Closure**

This release officially concludes **all CPU-based spectral runs**.

Larger resolutions (512³, 768³, 1024³) or time-dependent studies will require:

* CUDA GPU
* 64–128+ GB RAM
* HPC-level FFT acceleration

---

# **Changelog**

### **Added**

* Complete multi-resolution HIT dataset (64³ → 384³)
* Invariant computations and multiflux clustering
* Optimized FFT-based 384³ implementation
* CC BY-NC-SA 4.0 license

### **Changed**

* Directory structure clean-up
* Added definitive 384³ reference dataset

### **Removed**

* Obsolete notebook checkpoints
* Temporary scripts

---

# **License**

This release is licensed under:
**CC BY-NC-SA 4.0**

Commercial use of the Multiflux methodology requires prior written authorization.

---

# **Contact**

Exclusive channel for the CFD Online community:
**[cfd-online@meshwave.com.br](mailto:cfd-online@meshwave.com.br)**

---

# **End of Release Notes**
