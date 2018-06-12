# Perform CNR for 8 perturbation in the input, scan over eta to create ROC curves.

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

BOUNDS = 5
ETA_VALS_ALL = [0] + list(np.round((np.logspace(-3, 2, 13)), 3))
# Adjust eta values for number of cell lines
# (less cell lines -> less measurements ->
# higher weight per measurement -> lower eta)
ETA_VALS_1 = [e / 4. for e in ETA_VALS_ALL]
ETA_VALS_2 = [e / 2. for e in ETA_VALS_ALL]

THETA_SELECT = 0.01 * 8 / 12
NOISE_VAL = 0.1  # Noise levels to test
NPERT = 8  # Number of perturbation
NREP = 10  # Number of repetitions


def scan_eta(panel, eta_vals, theta, bounds=BOUNDS, maxints=None,
             use_previous=True):
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

# Add noise once and use same "data" for each reconstruction
random.seed(0)
rglob_dict = {
    'wt':   utils.add_noise(rglob_wt, NOISE_VAL),
    'ras':  utils.add_noise(rglob_ras, NOISE_VAL),
    'braf': utils.add_noise(rglob_braf, NOISE_VAL),
    'egfr': utils.add_noise(rglob_egfr, NOISE_VAL)
}
with open("../results/solutions/rglob_noise_npert.pickle", "wb") as handle:
    pickle.dump(rglob_dict, handle)

# rglob_dict = {
#     'wt': rglob_wt,
#     'ras': rglob_ras,
#     'braf': rglob_braf,
#     'egfr': rglob_egfr
# }

sols_npert = {
    "wt": [], "braf": [], "ras": [], "egfr": [],
    "braf_wt": [], "ras_wt": [], "egfr_wt": [],
    "braf_wt_theta": [], "ras_wt_theta": [], "egfr_wt_theta": [],
    "all": [], "all_theta": []
}

for rep in range(NREP):
    reduced_pert_lst = random.sample(PERTURBATIONS, NPERT)
    reduced_perts = utils.flatten_list(reduced_pert_lst)

    # Single cell line panels

    panel_wt = cnr.PerturbationPanel(
        nodes=REF_NODES,
        perts=reduced_pert_lst,
        pert_annot=INHIBITOR_TARGETS,
        ds_acting_perts=[],
        rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
               rglob_dict.items() if cell_line in ["wt"]}
    )
    sols_npert['wt'].append(scan_eta(panel_wt, ETA_VALS_1, theta=0))

    panel_braf = cnr.PerturbationPanel(
        nodes=REF_NODES,
        perts=reduced_pert_lst,
        pert_annot=INHIBITOR_TARGETS,
        ds_acting_perts=[],
        rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
               rglob_dict.items() if cell_line in ["braf"]}
    )
    sols_npert['braf'].append(scan_eta(panel_braf, ETA_VALS_1, theta=0))

    panel_ras = cnr.PerturbationPanel(
        nodes=REF_NODES,
        perts=reduced_pert_lst,
        pert_annot=INHIBITOR_TARGETS,
        ds_acting_perts=[],
        rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
               rglob_dict.items() if cell_line in ["ras"]}
    )
    sols_npert['ras'].append(scan_eta(panel_ras, ETA_VALS_1, theta=0))

    panel_egfr = cnr.PerturbationPanel(
        nodes=REF_NODES,
        perts=reduced_pert_lst,
        pert_annot=INHIBITOR_TARGETS,
        ds_acting_perts=[],
        rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
               rglob_dict.items() if cell_line in ["egfr"]}
    )
    sols_npert['egfr'].append(scan_eta(panel_egfr, ETA_VALS_1, theta=0))

    # Mutant + wt panels

    panel_braf_wt = cnr.PerturbationPanel(
        nodes=REF_NODES,
        perts=reduced_pert_lst,
        pert_annot=INHIBITOR_TARGETS,
        ds_acting_perts=[],
        rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
               rglob_dict.items() if cell_line in ["braf", "wt"]}
    )
    sols_npert['braf_wt'].append(scan_eta(panel_braf_wt, ETA_VALS_2, theta=0))
    sols_npert['braf_wt_theta'].append(scan_eta(panel_braf_wt, ETA_VALS_2,
                                                theta=THETA_SELECT))

    panel_ras_wt = cnr.PerturbationPanel(
        nodes=REF_NODES,
        perts=reduced_pert_lst,
        pert_annot=INHIBITOR_TARGETS,
        ds_acting_perts=[],
        rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
               rglob_dict.items() if cell_line in ["ras", "wt"]}
    )
    sols_npert['ras_wt'].append(scan_eta(panel_ras_wt, ETA_VALS_2, theta=0))
    sols_npert['ras_wt_theta'].append(scan_eta(panel_ras_wt, ETA_VALS_2,
                                               theta=THETA_SELECT))

    panel_egfr_wt = cnr.PerturbationPanel(
        nodes=REF_NODES,
        perts=reduced_pert_lst,
        pert_annot=INHIBITOR_TARGETS,
        ds_acting_perts=[],
        rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
               rglob_dict.items() if cell_line in ["egfr", "wt"]}
    )
    sols_npert['egfr_wt'].append(scan_eta(panel_egfr_wt, ETA_VALS_2, theta=0))
    sols_npert['egfr_wt_theta'].append(scan_eta(panel_egfr_wt, ETA_VALS_2,
                                                theta=THETA_SELECT))

    panel_all = cnr.PerturbationPanel(
        nodes=REF_NODES,
        perts=reduced_pert_lst,
        pert_annot=INHIBITOR_TARGETS,
        ds_acting_perts=[],
        rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
               rglob_dict.items()}
    )
    sols_npert['all'].append(scan_eta(panel_all, ETA_VALS_ALL, theta=0))
    sols_npert['all_theta'].append(scan_eta(panel_all, ETA_VALS_ALL,
                                            theta=THETA_SELECT))

with open("../results/solutions/sols_npert.pickle", "wb") as handle:
    pickle.dump(sols_npert, handle)
