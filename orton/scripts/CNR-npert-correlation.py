# Perform CNR for multiple values of the number of perturbations in the input.
# Use fixed number of edges.

import sys

import random
import pickle
import cnr
import numpy as np
import pandas as pd
import utils

# Constants
random.seed(29121982)

NPERT_VALS = [2, 4, 6, 8, 10]
NREP = 50
THETA_BASE = 0.01
ETA_BASE = 0.01
BOUNDS = 10
NOISE_VAL = 0.1  # Noise levels to test

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

REF_NODES = list(rglob_wt.index)
REF_NODES == list(rglob_wt.index) == list(rglob_braf.index)

# None of the perturbations is acting downstream.
DOWNSTREAM_ACTING_PERTS = []
PERTURBATIONS = [[s] for s in rglob_wt.columns]
INHIBITOR_TARGETS = {x: x.replace('Knockdown', "") for x in rglob_wt.columns}

sols_npert = {
    "wt": dict(), "braf": dict(), "ras": dict(), "egfr": dict(),
    # "braf_wt": dict(), "ras_wt": dict(), "egfr_wt": dict(),
    "braf_wt_theta": dict(), "ras_wt_theta": dict(), "egfr_wt_theta": dict(),
    # "all": dict(),
    "all_theta": dict(),
    # Also add entry to store the global response matrices
    "rglob_full": dict()
}

for NPERT in NPERT_VALS:
    # Adapt theta to NPERT
    theta = THETA_BASE  # * NPERT / 12
    eta = ETA_BASE  # NPERT / 12

    sols_npert['wt'][NPERT] = []
    sols_npert['braf'][NPERT] = []
    sols_npert['ras'][NPERT] = []
    sols_npert['egfr'][NPERT] = []
    sols_npert['braf_wt_theta'][NPERT] = []
    sols_npert['ras_wt_theta'][NPERT] = []
    sols_npert['egfr_wt_theta'][NPERT] = []
    sols_npert['all_theta'][NPERT] = []
    sols_npert['rglob_full'][NPERT] = []

    for rep in range(NREP):

        # Add noise once and use same "data" for each reconstruction
        rglob_dict = {
            'wt':   utils.add_noise(rglob_wt, NOISE_VAL),
            'ras':  utils.add_noise(rglob_ras, NOISE_VAL),
            'braf': utils.add_noise(rglob_braf, NOISE_VAL),
            'egfr': utils.add_noise(rglob_egfr, NOISE_VAL)
        }
        sols_npert['rglob_full'][NPERT].append(rglob_dict)

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
        p = cnr.CnrProblem(panel_wt, eta=eta/4, theta=theta/4, bounds=BOUNDS)
        p.cpx.parameters.threads.set(24)
        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sols_npert['wt'][NPERT].append(cnr.CnrResult(p))
        else:
            # If solution is not feasible, add None to keep matched to rglob
            # index.
            sols_npert['wt'][NPERT].append(None)

        panel_braf = cnr.PerturbationPanel(
            nodes=REF_NODES,
            perts=reduced_pert_lst,
            pert_annot=INHIBITOR_TARGETS,
            ds_acting_perts=[],
            rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
                   rglob_dict.items() if cell_line in ["braf"]}
        )
        p = cnr.CnrProblem(panel_braf, eta=eta/4, theta=theta/4, bounds=BOUNDS)
        p.cpx.parameters.threads.set(24)
        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sols_npert['braf'][NPERT].append(cnr.CnrResult(p))
        else:
            # If solution is not feasible, add None to keep matched to rglob
            # index.
            sols_npert['braf'][NPERT].append(None)

        panel_ras = cnr.PerturbationPanel(
            nodes=REF_NODES,
            perts=reduced_pert_lst,
            pert_annot=INHIBITOR_TARGETS,
            ds_acting_perts=[],
            rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
                   rglob_dict.items() if cell_line in ["ras"]}
        )
        p = cnr.CnrProblem(panel_ras, eta=eta/4, theta=theta/4, bounds=BOUNDS)
        p.cpx.parameters.threads.set(24)
        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sols_npert['ras'][NPERT].append(cnr.CnrResult(p))
        else:
            # If solution is not feasible, add None to keep matched to rglob
            # index.
            sols_npert['ras'][NPERT].append(None)

        panel_egfr = cnr.PerturbationPanel(
            nodes=REF_NODES,
            perts=reduced_pert_lst,
            pert_annot=INHIBITOR_TARGETS,
            ds_acting_perts=[],
            rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
                   rglob_dict.items() if cell_line in ["egfr"]}
        )
        p = cnr.CnrProblem(panel_egfr, eta=eta/4, theta=theta/4, bounds=BOUNDS)
        p.cpx.parameters.threads.set(24)
        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sols_npert['egfr'][NPERT].append(cnr.CnrResult(p))
        else:
            # If solution is not feasible, add None to keep matched to rglob
            # index.
            sols_npert['egfr'][NPERT].append(None)

        #  Mutant + wt panels
        panel_braf_wt = cnr.PerturbationPanel(
            nodes=REF_NODES,
            perts=reduced_pert_lst,
            pert_annot=INHIBITOR_TARGETS,
            ds_acting_perts=[],
            rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
                   rglob_dict.items() if cell_line in ["braf", "wt"]}
        )
        p = cnr.CnrProblem(panel_braf_wt, eta=eta/2, theta=theta/2, bounds=BOUNDS)
        p.cpx.parameters.threads.set(24)
        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sols_npert['braf_wt_theta'][NPERT].append(cnr.CnrResult(p))
        else:
            # If solution is not feasible, add None to keep matched to rglob
            # index.
            sols_npert['braf_wt_theta'][NPERT].append(None)

        panel_ras_wt = cnr.PerturbationPanel(
            nodes=REF_NODES,
            perts=reduced_pert_lst,
            pert_annot=INHIBITOR_TARGETS,
            ds_acting_perts=[],
            rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
                   rglob_dict.items() if cell_line in ["ras", "wt"]}
        )
        p = cnr.CnrProblem(panel_ras_wt, eta=eta/2, theta=theta/2, bounds=BOUNDS)
        p.cpx.parameters.threads.set(24)
        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sols_npert['ras_wt_theta'][NPERT].append(cnr.CnrResult(p))
        else:
            # If solution is not feasible, add None to keep matched to rglob
            # index.
            sols_npert['ras_wt_theta'][NPERT].append(None)

        panel_egfr_wt = cnr.PerturbationPanel(
            nodes=REF_NODES,
            perts=reduced_pert_lst,
            pert_annot=INHIBITOR_TARGETS,
            ds_acting_perts=[],
            rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
                   rglob_dict.items() if cell_line in ["egfr", "wt"]}
        )
        p = cnr.CnrProblem(panel_egfr_wt, eta=eta/2, theta=theta/2, bounds=BOUNDS)
        p.cpx.parameters.threads.set(24)
        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sols_npert['egfr_wt_theta'][NPERT].append(cnr.CnrResult(p))
        else:
            # If solution is not feasible, add None to keep matched to rglob
            # index.
            sols_npert['egfr_wt_theta'][NPERT].append(None)

        panel_all = cnr.PerturbationPanel(
            nodes=REF_NODES,
            perts=reduced_pert_lst,
            pert_annot=INHIBITOR_TARGETS,
            ds_acting_perts=[],
            rglob={cell_line: rglob[reduced_perts] for cell_line, rglob in
                   rglob_dict.items()}
        )
        p = cnr.CnrProblem(panel_all, eta=eta, theta=theta, bounds=BOUNDS)
        p.cpx.parameters.threads.set(24)
        p.cpx.solve()
        if p.cpx.solution.is_primal_feasible():
            sols_npert['all_theta'][NPERT].append(cnr.CnrResult(p))
        else:
            # If solution is not feasible, add None to keep matched to rglob
            # index.
            sols_npert['all_theta'][NPERT].append(None)


with open("../results/solutions/sols_npert_correlations.pickle", "wb") as handle:
    pickle.dump(sols_npert, handle)
