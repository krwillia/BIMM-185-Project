#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Utility functions for working with MetaboAnalyst ready files.

Files ready to be analyzed with MetaboAnalyst will have the following format:

    * Sample names as rows
    * Metabolite log2(AUCs) as columns
    * First column will be sample names
    * Second column will group name
    
"""

import pandas as _pandas

class MetaboliteConcentrationTable(object):
    def __init__(self, df, ctrl=None, exp=None):
        self.control = ctrl
        self.exp = exp
        self.dataframe = df.set_index(['Group', 'Sample'])
        self.group_means = self.dataframe.mean(level=0)
        self.ratios = self.calculate_group_ratios()
        self.targets = _pandas.DataFrame({'MRM Name': list(self.dataframe.columns)})

    def calculate_group_ratios(self):
        return {'{} / {}'.format(x, self.control): self.ratio(self.group_means.ix[x], self.group_means.ix[self.control]) for x 
                                                                              in self.exp}
                                                                              
    def ratio(self, num, den):
        return num / den
        

         