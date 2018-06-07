#!/anaconda/bin/python
"""Preprocess the perturbation experiment data of vaco and widr persisters.

This scripts takes the lumix data and well annotations as input, and writes
the log-fold changes and scaled fold changes as output."""
# coding: utf-8

# # Data preprocessing of PTPN11 KO persister perturbation experiment
#
# Replicates are combined by taking medians
#
# Log2 fold changes of the vaco data are written to files:
# vaco_xx_median_lfc.tsv

import string
import os

import pandas as pd
import numpy as np


# pylint: disable=C0103
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, 'data'))

# # Plate annotation
annot = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151007ff_Evert_II_Anno.xlsx'),
    sheet_name='layout', usecols='A:M'
)
annot = annot.ix[18:25]

# Luminex measurements
# Widr
widr_1 = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151007_Widr_I_lxb_data.xlsx'),
    sheet_name='median'
)
widr_2 = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151009_widr_II_lxb_data.xlsx'),
    sheet_name='median'
)
widr_3 = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151014_Widr_III_lxb_data.xlsx'),
    sheet_name='median'
)
# Vaco
vaco_1 = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151008_Vaco_I_lxb_data.xlsx'),
    sheet_name='median'
)
vaco_2 = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151009_Vaco_II_lxb_data.xlsx'),
    sheet_name='median'
)
vaco_3 = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151014_Vaco_III_lxb_data.xlsx'),
    sheet_name='median'
)

# GEF plate
gef_plate = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151007_GEFplate_lxb_data.xlsx'),
    sheet_name='median'
)
annot_gef = pd.io.excel.read_excel(
    os.path.join(DATA_DIR, '151007ff_Evert_II_Anno.xlsx'),
    sheet_name='annotated GEF counts'
)


# ## Data preparation

# ### Other plates

# Well annotations
annot.columns = ['strain'] + [i + 1 for i in range(12)]
annot.index = list(string.ascii_uppercase[0:8])

# Rename columns
widr_panel = pd.Panel({1: widr_1, 2: widr_2, 3: widr_3})
widr_panel.minor_axis = [c.upper().replace('.', '')
                         for c in widr_panel.minor_axis]
widr_median = widr_panel.median(axis=0)

vaco_panel = pd.Panel({1: vaco_1, 2: vaco_2, 3: vaco_3})
vaco_panel.minor_axis = [c.upper().replace('.', '')
                         for c in vaco_panel.minor_axis]
vaco_median = vaco_panel.median(axis=0)

# Split in seperate DFs
wt_rows = [i for i in widr_panel.major_axis if i[0] in {'B', 'E'}]
ko_rows = [i for i in widr_panel.major_axis if i[0] in {'C', 'F'}]
pe_rows = [i for i in widr_panel.major_axis if i[0] in {'D', 'G'}]

widr_wt_median = widr_median.ix[wt_rows]
widr_ko_median = widr_median.ix[ko_rows]
widr_pe_median = widr_median.ix[pe_rows]

vaco_wt_median = vaco_median.ix[wt_rows]
vaco_ko_median = vaco_median.ix[ko_rows]
vaco_pe_median = vaco_median.ix[pe_rows]

# Rename index


def idx2annot(idx):
    return(annot.ix[idx[0], int(idx[1:])])


widr_wt_median.index = [idx2annot(idx) for idx in widr_wt_median.index]
widr_ko_median.index = [idx2annot(idx) for idx in widr_ko_median.index]
widr_pe_median.index = [idx2annot(idx) for idx in widr_pe_median.index]

vaco_wt_median.index = [idx2annot(idx) for idx in vaco_wt_median.index]
vaco_ko_median.index = [idx2annot(idx) for idx in vaco_ko_median.index]
vaco_pe_median.index = [idx2annot(idx) for idx in vaco_pe_median.index]


# ### Calculate Log2 fold changes

REF_NODES = ['EGFR',  # RTKs
             'MEK', 'ERK', 'P90RSK', 'GSK3AB', 'RPS6',  # MAPK
             'PI3K', 'AKT', 'MTOR',  # AKT
             'JNK', 'CJUN',
             'P38', 'IKBA', 'P53', 'SMAD2']

REF_PERTS = [
    'egf', 'hgf', 'nrg1',
    'plx', 'plx + egf', 'plx + hgf', 'plx + nrg1',
    'mek', 'mek + egf', 'mek + hgf', 'mek + nrg1',
    'erk', 'erk + egf', 'erk + hgf', 'erk + nrg1',
    'akt', 'akt + egf', 'akt + hgf', 'akt + nrg1',
    'pi3k', 'pi3k + egf', 'pi3k + hgf', 'pi3k + nrg1'
    # 'gef', 'gef + egf', 'gef + hgf', 'gef + nrg1'
]


def get_lfc(df_in):
    df = df_in.copy()
    df = np.log2(df / df.ix['Blank'])
    df = df.transpose().drop('Blank', axis=1)
    df = df.ix[REF_NODES]
    df.columns = [c.lower() for c in df.columns]
    df = df[REF_PERTS]
    return df


widr_wt_median_lfc = get_lfc(widr_wt_median)
widr_ko_median_lfc = get_lfc(widr_ko_median)
widr_pe_median_lfc = get_lfc(widr_pe_median)

vaco_wt_median_lfc = get_lfc(vaco_wt_median)
vaco_ko_median_lfc = get_lfc(vaco_ko_median)
vaco_pe_median_lfc = get_lfc(vaco_pe_median)

# Write to file
OUT_PATH = os.path.abspath(
    os.path.join(BASE_DIR, 'out', 'cnr-input')
)

widr_wt_median_lfc.to_csv(os.path.join(
    OUT_PATH, 'widr_wt_median_lfc.tsv'), sep='\t')
widr_ko_median_lfc.to_csv(os.path.join(
    OUT_PATH, 'widr_ko_median_lfc.tsv'), sep='\t')
widr_pe_median_lfc.to_csv(os.path.join(
    OUT_PATH, 'widr_pe_median_lfc.tsv'), sep='\t')

vaco_wt_median_lfc.to_csv(os.path.join(
    OUT_PATH, 'vaco_wt_median_lfc.tsv'), sep='\t')
vaco_ko_median_lfc.to_csv(os.path.join(
    OUT_PATH, 'vaco_ko_median_lfc.tsv'), sep='\t')
vaco_pe_median_lfc.to_csv(os.path.join(
    OUT_PATH, 'vaco_pe_median_lfc.tsv'), sep='\t')
