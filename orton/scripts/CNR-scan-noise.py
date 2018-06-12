import os
import sys

import random
import pickle
import cnr
import numpy as np
import pandas as pd
from mypyutils import utils

# ----------------------------------------------------------------------------
# Inputs

random.seed(29121982)

f_imap = "../results/simulations/imap.tsv"
fSimResults = '../results/simulations/ortonModel-knockdown-mutWT.tsv'
fSimResults_mutRAS = '../results/simulations/ortonModel-knockdown-mutRAS.tsv'
fSimResults_mutBRAF = '../results/simulations/ortonModel-knockdown-mutBRAF.tsv'
fSimResults_mutEGFR = '../results/simulations/ortonModel-knockdown-mutEGFR.tsv'

REF_IMAP = pd.read_csv(f_imap, sep='\t', index_col=0)

rglob_wt = pd.read_csv(fSimResults, sep='\t', index_col=0)
rglob_ras = pd.read_csv(fSimResults_mutRAS, sep='\t', index_col=0)
rglob_braf = pd.read_csv(fSimResults_mutBRAF, sep='\t', index_col=0)
rglob_egfr = pd.read_csv(fSimResults_mutEGFR, sep='\t', index_col=0)

# Round the rglob matrices to prevent numerical instabilities
rglob_wt = np.round(rglob_wt, 3)
rglob_ras = np.round(rglob_ras, 3)
rglob_braf = np.round(rglob_braf, 3)
rglob_egfr = np.round(rglob_egfr, 3)


# # Set constants

BOUNDS = 10
ETA_VALS_ALL = [0] + list(np.round((np.logspace(-4, 2, 13)), 5))
# ETA_VALS_ALL.prepend(0)
# Adjust eta values for number of cell lines
# (less cell lines -> less measurements ->
# higher weight per measurement -> lower eta)
ETA_VALS_1 = [e / 4. for e in ETA_VALS_ALL]
ETA_VALS_2 = [e / 2. for e in ETA_VALS_ALL]
THREADS = 48

THETA_SELECT = 0.01
NOISE_VALS = [0.1, 0.2, 0.5, 1]  # Noise levels to test
NREP = 10  # Number of repetitions for each noise level


def scan_eta(panel, eta_vals, theta, bounds=BOUNDS, maxints=None,
             use_previous=False):
    """Find solution for several eta values"""
    sol_lst = list()
    sol_previous = None
    for eta in eta_vals:
        print('\nSolving for eta = ' + str(eta))
        p = cnr.CnrProblem(
            panel, eta=eta, theta=theta, maxints=maxints, bounds=bounds
        )

        # Restrict maximum number of threads
        p.cpx.parameters.threads.set(24)

        # Use earlier solution as starting point, may prevent suboptimal
        # solutions
        if sol_previous and use_previous:
            p.initialize_from_solution(sol_previous)

        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sol = cnr.CnrResult(p)
            sol_lst.append(sol)
            sol_previous = sol

    return sol_lst


REF_NODES = list(rglob_wt.index)
REF_NODES == list(rglob_wt.index) == list(rglob_braf.index)

# None of the perturbations is acting downstream.
DOWNSTREAM_ACTING_PERTS = []
PERTURBATIONS = [[s] for s in rglob_wt.columns]
INHIBITOR_TARGETS = {x: x.replace('Knockdown', "") for x in rglob_wt.columns}

rglob_dict = {
    'wt': rglob_wt,
    'ras': rglob_ras,
    'braf': rglob_braf,
    'egfr': rglob_egfr
}

sols_noise = dict()
panel_lst = [
    "wt", "braf", "ras", "egfr",
    "braf_wt", "braf_wt_theta",
    "ras_wt", "ras_wt_theta",
    "egfr_wt", "egfr_wt_theta",
    "all", "all_theta"
    ]

# Intialize solutions
for panel in panel_lst:
    sols_noise[panel] = dict()
    for noise in NOISE_VALS:
        sols_noise[panel][noise] = list()

for noise in NOISE_VALS:
    for i in range(NREP):

        rglob_dict_noise = {cl: utils.add_noise(
            rglob, noise) for cl, rglob in rglob_dict.items()}

        # Make the panels with the noisy rglob matrices
        def build_panel(use_rglob):
            return cnr.PerturbationPanel(
                nodes=REF_NODES,
                perts=PERTURBATIONS,
                pert_annot=INHIBITOR_TARGETS,
                ds_acting_perts=[],
                rglob=use_rglob
            )

        # Single cell lines
        panel_wt_noise = build_panel({"wt": rglob_dict_noise["wt"]})
        panel_braf_noise = build_panel({"braf": rglob_dict_noise["braf"]})
        panel_ras_noise = build_panel({"ras": rglob_dict_noise["ras"]})
        panel_egfr_noise = build_panel({"egfr": rglob_dict_noise["egfr"]})
        # MUT + wt
        panel_braf_wt_noise = build_panel(
            {cl: rglob_dict_noise[cl] for cl in ["braf", "wt"]}
        )
        panel_ras_wt_noise = build_panel(
            {cl: rglob_dict_noise[cl] for cl in ["ras", "wt"]}
        )
        panel_egfr_wt_noise = build_panel(
            {cl: rglob_dict_noise[cl] for cl in ["egfr", "wt"]}
        )
        # All cell lines combined
        panel_all_noise = build_panel(rglob_dict_noise)

        # Perform the network reconstructions
        # Single cell lines
        sols_noise['wt'][noise].append(
            scan_eta(panel_wt_noise, ETA_VALS_1, theta=0, use_previous=True)
        )
        sols_noise['braf'][noise].append(
            scan_eta(panel_braf_noise, ETA_VALS_1, theta=0, use_previous=True)
        )
        sols_noise['ras'][noise].append(
            scan_eta(panel_ras_noise, ETA_VALS_1, theta=0, use_previous=True)
        )
        sols_noise['egfr'][noise].append(
            scan_eta(panel_egfr_noise, ETA_VALS_1, theta=0, use_previous=True)
        )
        # MUT + WT
        sols_noise['braf_wt'][noise].append(
            scan_eta(
                panel_braf_wt_noise, ETA_VALS_1,
                use_previous=True, theta=0
            )
        )
        sols_noise['braf_wt_theta'][noise].append(
            scan_eta(
                panel_braf_wt_noise, ETA_VALS_1,
                use_previous=True, theta=THETA_SELECT
            )
        )
        # MUT + WT
        # BRAF
        sols_noise['braf_wt'][noise].append(
            scan_eta(
                panel_braf_wt_noise, ETA_VALS_1,
                use_previous=True, theta=0
            )
        )
        sols_noise['braf_wt_theta'][noise].append(
            scan_eta(
                panel_braf_wt_noise, ETA_VALS_1,
                use_previous=True, theta=THETA_SELECT
            )
        )
        # RAS
        sols_noise['ras_wt'][noise].append(
            scan_eta(
                panel_ras_wt_noise, ETA_VALS_1,
                use_previous=True, theta=0
            )
        )
        sols_noise['ras_wt_theta'][noise].append(
            scan_eta(
                panel_ras_wt_noise, ETA_VALS_1,
                use_previous=True, theta=THETA_SELECT
            )
        )
        # EGFR
        sols_noise['egfr_wt'][noise].append(
            scan_eta(
                panel_egfr_wt_noise, ETA_VALS_1,
                use_previous=True, theta=0
            )
        )
        sols_noise['egfr_wt_theta'][noise].append(
            scan_eta(
                panel_egfr_wt_noise, ETA_VALS_1,
                use_previous=True, theta=THETA_SELECT
            )
        )

        # All cell lines combined
        sols_noise['all'][noise].append(
            scan_eta(panel_all_noise, ETA_VALS_ALL, theta=0.0,
                     use_previous=True)
        )
        sols_noise['all_theta'][noise].append(
            scan_eta(panel_all_noise, ETA_VALS_ALL, theta=THETA_SELECT,
                     use_previous=True)
        )

    for panel, solutions in sols_noise.items():
        filename = "-".join(["sols", panel, str(noise)]) + ".pickle"
        path = os.path.join(
            "..", "results", "solutions", "20171114-scan-noise", filename
            )
        with open(path, "wb") as handle:
            pickle.dump(sols_noise[panel][noise], handle)

path = os.path.join(
    "..", "results", "solutions", "20171114-scan-noise", "all-solutions.pickle"
    )
with open(path, "wb") as handle:
    pickle.dump(sols_noise, handle)