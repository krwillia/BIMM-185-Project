"""Pathway analysis tools for metabolomic data.
"""

import pandas as _pd
import os as _os
from collections import OrderedDict as _OrderedDict
import re as _re
import itertools as _itertools

class TableOne(object):
    def __init__(self, db, top_vip_file, fold_change=False, total_MRMs=964.0, control=None):
        self.db = db
        self.v = top_vip_file
        self.q = _pd.merge(self.v, self.db, on='MRM Index', how='left')
        self.t = total_MRMs * 1.0
        self.fold_change = fold_change
        self.control = control
        self.table = self._construct_table()
        if self.fold_change:
            self.comps = [x for x in list(self.q.columns) if _re.search(self.control, x)]
            self.out_col = list(_itertools.chain.from_iterable([['Chemical Name', 'Pathway Name', 'VIP Score'], self.comps]))
            self.names_pathways = self.q[self.out_col]
        else:
            self.names_pathways = self.q[['Chemical Name', 'Pathway Name', 'VIP Score']]
            
    headers = _OrderedDict([('measure', u'Measured Pathway (N)'),
               ('exp_prop', u'Expected Pathway Proportion (P = N/1006)'),
               ('exp_hits', u'Expected Hits in Sample of 61 (P * 61)'),
               ('obs', u'Observed Pathway'),
               ('enrich', u'Fold Enrichment (Obs/Exp)'),
               ('impact', u'Impact (Sum VIP Score)'),
               ('frac_impact', u'Fraction of Impact (VIP) Explained (% of 142.4701)'),
               ('inc', u'Increased (Exp/Ctl>1)'),
               ('dec', u'Decreased (Exp/Ctl<1)')])    
   
    def _construct_table(self):             
        grouped = self.q.groupby(['Pathway Index', 'Pathway Name'])
        tableOne = _pd.DataFrame({self.headers['impact']: grouped.sum()['VIP Score']})
        total_vip = tableOne.sum()[0]            
        self.headers['frac_impact'] = u'Fraction of Impact (VIP) Explained (% of {})'.format(total_vip)
        tableOne[self.headers['frac_impact']] = tableOne[self.headers['impact']].div(total_vip)
        tableOne[self.headers['obs']] = grouped.size()
        total_obs = tableOne[self.headers['obs']].sum()
#         if self.fold_change:
#             tableOne[self.headers['dec']] = grouped.apply(lambda x: len(x[x['Fold Change'] < 1]))
#             tableOne[self.headers['inc']] = grouped.apply(lambda x: len(x[x['Fold Change'] >= 1]))

        c_groups = self.db.groupby(['Pathway Index', 'Pathway Name'])
        c_groups_size = c_groups.size()
        c_groups_size.name = self.headers['measure']

        tableOne = tableOne.join(c_groups_size, how='left')
        self.headers['exp_prop'] = u'Expected Pathway Proportion (P = N/{})'.format(int(self.t))
        tableOne[self.headers['exp_prop']] = tableOne[self.headers['measure']].div(self.t)
        self.headers['exp_hits'] = u'Expected Hits in Sample of {0} (P * {0})'.format(total_obs)
        tableOne[self.headers['exp_hits']] = tableOne[self.headers['exp_prop']].mul(total_obs)
        tableOne[self.headers['enrich']] = tableOne[self.headers['obs']] / tableOne[self.headers['exp_hits']]
        return tableOne[self.headers.values()[0:7]]
#         if self.fold_change:
#             return tableOne[self.headers.values()]
#         else:
#             return tableOne[self.headers.values()[0:7]]
        
        

    def to_file(self, file):
        writer = _pd.ExcelWriter(file)
        self.names_pathways.to_excel(writer, 'Metabolites', index=False)
        self.table.reset_index().to_excel(writer, 'Table 1', index=False)
        writer.save()       
        return

def venn(a, b):
    i = a & b
    a_only = a - b
    b_only = b - a
    
    print 'INTERSECTION: {}'.format(len(i))
    print '\n'.join(i)
    
    print 'First: {}'.format(len(a_only))
    print '\n'.join(a_only)
    
    print 'Second: {}'.format(len(b_only))
    print '\n'.join(b_only)
