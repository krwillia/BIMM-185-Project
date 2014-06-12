#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Script for running Table One analysis.
"""

import dbutils as _dbutils
import pw_analysis as _pw_analysis
import mautils as _mautils
import pandas as _pandas
import numpy as _numpy
import argparse as _argparse

parser = _argparse.ArgumentParser()
parser.add_argument("-v", "--vip_file", type=str, help="Optional reference genome to use in alignment.")
parser.add_argument("-d", "--data_file", type=str, help="Optional reference genome to use in alignment.")
parser.add_argument("-db", "--database", type=str, help="Optional reference genome to use in alignment.")
parser.add_argument("-o", "--out_file", type=str, help="Optional reference genome to use in alignment.")
parser.add_argument("-ctrl", "--control", type=str, help="Optional reference genome to use in alignment.")
parser.add_argument("-exp", "--experiment", type=str, help="Optional reference genome to use in alignment.")
parser.add_argument("-t", "--targets", type=str, default=None, help="Optional reference genome to use in alignment.")

args = parser.parse_args()

db_file = args.database
vip_file = args.vip_file
data_file = args.data_file
out_file = args.out_file
control = args.control
experiment = args.experiment.split(',')
target_file = args.targets

db_dict = {'a': 'Alias',
           'c': 'Chemical',
           'm': 'MRM',
           'p': 'Pathway'}
    
def main():
    db_parts = _dbutils.db_read_excel(db_file, db_dict)
    db = _dbutils.db_merge_full(db_parts['m'], db_parts['c'], db_parts['p'])
    
    data = _pandas.read_csv(data_file)
    col = data.columns
    if not data[data[col[2]] > 100].empty:
        data = data.set_index(['Group', 'Sample'])
        data = _numpy.log2(data)
        data = data.reset_index()
        print '*****Converted to log2. Check input file to confirm.*****'
        
    ma_data = _mautils.MetaboliteConcentrationTable(data, ctrl=control, exp=experiment)
        
    if target_file:
        g = _pandas.read_table(target_file)
    else:
        g = ma_data.targets
        
    g = _dbutils.standardize_mrm_input(g, db_parts['a'])
    g = _pandas.DataFrame({'MRM Index': g['MRM Index']})
    db = _dbutils.db_merge_mrm(g, db, how='left')
    if not db[db['Chemical Index'].isnull()].empty:
        pass
        
    v = _pandas.read_table(vip_file)
    v = _dbutils.standardize_mrm_input(v, db_parts['a'])
    
    fc = _pandas.DataFrame(ma_data.ratios).reset_index()
    col = list(fc.columns)
    col[0] = 'MRM Name'
    fc.columns = col
    v = _dbutils.db_merge_name(v, fc, how='left')
    
    t = _pw_analysis.TableOne(db, v, fold_change=True, total_MRMs=len(db), control=control)
    t.to_file(out_file)

    
    
if __name__ == '__main__':
    main()