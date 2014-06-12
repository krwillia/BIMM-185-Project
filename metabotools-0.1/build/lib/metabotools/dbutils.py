#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pandas
import periodic_table as _pt

class MetDataBase(pandas.DataFrame):
    def __init__(self):
        pass
        
class A(object):
    def __init__(self, a):
        print 'A called.'
        self.a = a

class B(A):
    def __init__(self, b, a):
        print 'B called.'
        self.b = b
        super(B, self).__init__(a)
        
class C(B):
    def __init__(self, c, b, a):
        print 'C called.'
        self.c = c
        super(C, self).__init__(b, a)

# mrm = pd.read_table('db_files/mtdb/MRM_db.tsv')        
# chem = pd.read_table('db_files/mtdb/chemical_db.tsv')
# pw = pd.read_table('db_files/mtdb/pathway_db.tsv')
# run = pd.read_table('db_files/MRM_lists/full_run.tsv')
e = 0.00054858026

adducts = {
'M+2H': lambda x: (x + (2 * (exact_mass('H') - e))) / 2,
'M-2H': lambda x: (x - (2 * (exact_mass('H') - e))) / 2,
'M+H-H2O': lambda x: (x + (exact_mass('H') - e) - (exact_mass('H2O'))),
'M': lambda x: x,
'M+H-Cl': lambda x: (x + (exact_mass('H') - e) - (exact_mass('Cl'))),
'M+H+Na': lambda x: (x + (exact_mass('H') - e) + (exact_mass('Na') - e)) / 2,
'M+H': lambda x: x + (exact_mass('H') - e),
'M+H2O': lambda x: x + (exact_mass('H2O') - e),
'M+NH4': lambda x: x + (exact_mass('NH4') - e),
'M-H': lambda x: x - (exact_mass('H') - e),
'M-H+H2O': lambda x: (x - (exact_mass('H') - e) + (exact_mass('H2O'))),
'M+Na': lambda x: x + (exact_mass('Na') - e),
'M-H-CH2': lambda x: (x - (exact_mass('H') - e) - (exact_mass('CH2')))}

def db_merge_chem(left, right, how='inner'):
    """Perform a pandas DataFrame merge on 'Chemical Index'.
    
    See pandas.merge for more information.
    
    Parameters
    ----------
    left : DataFrame
    right : DataFrame
    how : {'left', 'right', 'outer', 'inner'}, default 'inner'
        * left: use only keys from left frame (SQL: left outer join)
        * right: use only keys from right frame (SQL: right outer join)
        * outer: use union of keys from both frames (SQL: full outer join)
        * inner: use intersection of keys from both frames (SQL: inner join)
    
    Returns
    -------
    merged : DataFrame
    """
    
    df = pandas.merge(left, right, on='Chemical Index', how=how)
    return df

def db_merge_path(left, right, how='inner'):
    """Perform a pandas DataFrame merge on 'Pathway Index'.
    
    See pandas.merge for more information.
    
    Parameters
    ----------
    left : DataFrame
    right : DataFrame
    how : {'left', 'right', 'outer', 'inner'}, default 'inner'
        * left: use only keys from left frame (SQL: left outer join)
        * right: use only keys from right frame (SQL: right outer join)
        * outer: use union of keys from both frames (SQL: full outer join)
        * inner: use intersection of keys from both frames (SQL: inner join)
    
    Returns
    -------
    merged : DataFrame
    """
    
    df = pandas.merge(left, right, on='Pathway Index', how=how)
    return df
    
def db_merge_name(left, right, how='inner'):
    """Perform a pandas DataFrame merge on 'MRM Name'.
    
    See pandas.merge for more information.
    
    Parameters
    ----------
    left : DataFrame
    right : DataFrame
    how : {'left', 'right', 'outer', 'inner'}, default 'inner'
        * left: use only keys from left frame (SQL: left outer join)
        * right: use only keys from right frame (SQL: right outer join)
        * outer: use union of keys from both frames (SQL: full outer join)
        * inner: use intersection of keys from both frames (SQL: inner join)
    
    Returns
    -------
    merged : DataFrame
    """
    
    df = pandas.merge(left, right, on='MRM Name', how=how)
    return df

def db_merge_mrm(left, right, how='inner'):
    """Perform a pandas DataFrame merge on 'MRM Index'.
    
    See pandas.merge for more information.
    
    Parameters
    ----------
    left : DataFrame
    right : DataFrame
    how : {'left', 'right', 'outer', 'inner'}, default 'inner'
        * left: use only keys from left frame (SQL: left outer join)
        * right: use only keys from right frame (SQL: right outer join)
        * outer: use union of keys from both frames (SQL: full outer join)
        * inner: use intersection of keys from both frames (SQL: inner join)
    
    Returns
    -------
    merged : DataFrame
    """
    
    df = pandas.merge(left, right, on='MRM Index', how=how)
    return df

def db_merge_full(mrm, chemical, pathway):
    """Create a full metabolite database by merging the MRM database, the Chemical 
    database, and the Pathway database.
    
    Parameters
    ----------
    mrm : DataFrame with 'MRM Index' and 'Chemical Index' columns.
    chemical : DataFrame with 'Chemical Index' and 'Pathway Index' columns.
    pathway: DataFrame with 'Pathway Index' column.
    
    Returns
    -------
    merged : DataFrame
    """
    
    df = db_merge_chem(mrm, chemical)
    df = db_merge_path(df, pathway)
    return df

def pathway_count(mrm_list, met_db):
    """Calculate the number of metabolites in each metabolic pathway from a list of MRM 
    IDs.
    
    Parameters
    ----------
    mrm_list : DataFrame of MRM IDs.
    met_db : DataFrame with 'MRM Index' and 'Pathway Index' columns.
    
    Returns
    -------
    merged : Series with hierarchical index.
    """
    
    df = db_merge_mrm(mrm_list, met_db, how='left')
    grouped = df.groupby(['Pathway Index', 'Pathway Name'])
    count = grouped.count()
    return count['Chemical Index']

def db_read_excel(excel_file, db_dict):
    """Read excel table(s) into pandas DataFrame(s).
    
    Parameters
    ----------
    excel_file : String of path to excel workbook.
    db_dict : Dictionary with key being database name and value corresponding to the 
        excel sheet name.
        
    Returns
    -------
    result : Dictionary 
        Pandas DataFrame(s) with keys corresponding to input dictionary.
    """
    
    db = {k : pandas.read_excel(excel_file, v) for k, v in db_dict.iteritems()}
    return db
    
def standardize_mrm_input(input, alias):
        input = pandas.merge(input, alias, on='MRM Name', how='left')
        met_errors = input[input['MRM Index'].isnull()]['MRM Name']
        if len(met_errors) > 0:
            met_errors.to_csv('met_error.log', index=False)
            raise NameError("Some Metabloites are not found in the database. See 'met_error.log'")
        
        return input

def exact_mass(cf):
    c = _pt.ChemicalFormula(cf, pt=_pt.PeriodicTable(_pt.elements_factory(_pt.pt_config_exact)))
    return c.mw()
    
def exact_abundance(cf):
    c = _pt.ChemicalFormula(cf, pt=_pt.PeriodicTable(_pt.elements_factory(_pt.pt_config_exact)))
    return c.abundance()
