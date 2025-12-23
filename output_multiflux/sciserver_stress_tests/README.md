# Multiflux – SciServer Stress Tests

## Purpose
## Computational Environment
## Test Matrix
## Method Summary
## Output Structure
## Status

## Global Simulation Parameters (Frozen)

| Parameter | Description | Value |
|---------|------------|-------|
| Flow type | Homogeneous Isotropic Turbulence (synthetic, spectral) | HIT |
| Domain size | Periodic cubic domain | \( L = 2\pi \) |
| Grid resolution | Number of points per dimension | \( N = 256, 384, 512 \) |
| Floating precision | Physical fields | float32 |
| Spectral precision | Fourier space | complex64 |
| Random seed | Reproducibility | 42 |
| Spectral slope | Energy spectrum | \( E(k) \sim k^{-5/3} \) |
| Solenoidal projection | Incompressibility enforcement | Yes |
| Invariants used | Feature space | \( |\omega|, Q, \lambda_2, h \) |
| Downsampling factor | Invariant grid | DS = 4 |
| Feature grid size | Per dimension | \( (N/DS)^3 \) |
| Clustering method | Partitioning | MiniBatch K-Means |
| Number of clusters | Initial | \( K = 12 \) |
| Effective cluster cutoff | Volume threshold | 0.5% |
| Output metrics | Reported | \( N_{\mathrm{eff}}, V_i \) |
| Visualization | Slices + histogram | Mid-plane |

