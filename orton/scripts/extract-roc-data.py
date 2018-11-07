import utils
import cplex
import pickle
import cnr
import numpy as np
import pandas as pd

# Load the data
# CNR results
path = "../results/solutions/20171114-scan-noise/all-solutions.pickle"
with open(path, "rb") as handle:
    sols = pickle.load(handle)
# Reference interaction map
REF_IMAP = pd.read_csv("../results/simulations/imap.tsv", sep='\t', index_col=0)


# Define the helper functions
def tpr(imap, ref_imap):
    "True positive rate"
    tp = ((imap == 1) & (ref_imap == 1)).sum().sum()
    p = ref_imap.sum().sum()
    return(tp/p)


def fpr(imap, ref_imap):
    "False positive rate"
    fp = ((imap == 1) & (ref_imap == 0)).sum().sum()
    # Subtract diagonal from # of negatives
    n = (ref_imap == 0).sum().sum() - REF_IMAP.shape[0]
    return(fp/n)


def get_df(sols_lst, panel, noise):
    "Extract dataframe with fpr and tpr from list of solutions"
    l = [(fpr(sol.imap, REF_IMAP), tpr(sol.imap, REF_IMAP))
         for sol in utils.flatten_list(sols_lst)]
    # Sort base on fpr
    l.sort(key=lambda tup: tup[0])
    x, y = zip(*l)
    df = pd.DataFrame({
        "fpr": x, "tpr": y, "panel": [panel]*len(x), "noise": [noise]*len(x)
        })
    return df

df_lst = []
for panel, s_dd in sols.items():
    for noise, s_d in s_dd.items():
        df_lst.append(get_df(s_d, panel, noise))
df = pd.concat(df_lst)

df.to_csv("../results/solutions/noise_roc_data.tsv", sep="\t", index=False)
