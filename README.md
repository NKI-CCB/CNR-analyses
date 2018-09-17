# Comparative network reconstruction analyses

This repository contains the code used to perform the analyses in our publication:
"Comparative Network Reconstruction using Mixed Integer Programming", Bosdriesz et al., Bioinformatics (2018) https://doi.org/10.1093/bioinformatics/bty616

The code for the CNR method has it's own repository: https://github.com/NKI-CCB/cnr

Contents of this repository:

* **/orton**: contains code to simulate and reconstruct the orton model. This corresponds to Fig 2 and Fig S2-S5. It contains the following files:

  * ortonModelExtended.pkl - pickle object with orton model description
  * odemod.py - python module to perform orton model simulations
  * Model-simulations.ipyn - Notebook in which the simulations are performed
  * Model-calculate-true-rloc.ipyn - Notebook to estimate the true local response coefficients directly from the orton model.
  * CNR-plot-roc.R - **Fig 2B and S2**. Requires first `running scripts/CNR-scan-noise.py` and `scripts/extract-roc-data.py`
  * CNR-scan-theta.ipyn - **Fig 2C**
  * CNR-plot-reconstruction.ipyn - **Fig 2D and S3**
  * CNR-plot-npert.R **Fig 2EF, S4 and S5**. Requires first running `scripts/CNR-npert-correlation.py`, `scripts/CNR-npert-correlation-priornetwork.py` and `CNR-analyze-npert-correlation.ipynb`

* **/ptpn11ko-persisters**: contains the perturbation data and the network reconstruction of the VACO, VACO PTPN11 KO, and VACO persister cells. This corresponds to **Fig 3C and 4**.
