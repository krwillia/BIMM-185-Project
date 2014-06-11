import pandas as pd
import numpy as np
import metabotools.dbutils as dbu



file_read = raw_input("Enter the name of the Mass Spectrometry csv file: ")
var = True
check = raw_input("Would you like to perform name standarding? (yes/no)")

while var == True:
	try:
		if check == 'yes' or 'Yes' or 'y' or 'Y':
			print 'Now Performing name standardizing:'
			a = pd.read_csv(file_read)
			group = raw_input("Standardizing: Enter the name of the column that you initially sort by: ")
			sample = raw_input("Standardizing: Enter the name of the column that is a subset of the initial column: ")
			a = a.set_index([group,sample])
			col = a.columns
			c = pd.DataFrame({'MRM Name': col})
			alias = pd.read_excel('MasterDatabase_v2.0.6_cyto.xlsx','Alias')
			chem = pd.read_excel('MasterDatabase_v2.0.6_cyto.xlsx','Chemical')
			mrm = pd.read_excel('MasterDatabase_v2.0.6_cyto.xlsx','MRM')
			q = dbu.db_merge_name(c,alias,how = 'left')
			q = dbu.db_merge_mrm(q,mrm,how = 'left')
			q = dbu.db_merge_chem(q,chem,how = 'left')
			new_col = q['Cytoscape Synonym'].where(q['Cytoscape Synonym'], q['MRM Name_y'])
			s = a
			s.columns = new_col
			s.to_csv("New Data.csv")
			print "The name standardized file is created, named 'New Data.csv'"
			q = pd.read_csv('New Data.csv')
			var = False
		else:
			q = pd.read_csv(file_read) 
			var = False
	except:
		print 'File not found, please type again'
		file_read = raw_input("Enter the name of the Mass Spectrometry csv file: ")
var = True

print 'Now running Z-Score Calculations'
group = raw_input("Enter the name of the column that you initially sort by: ")
sample = raw_input("Enter the name of the column that is a subset of the initial column: ")


while var == True:
	try:
		q = q.set_index([group,sample])
		var = False
	except:
		print 'One or both of those columns where not found. Please type again'
		group = raw_input("Enter the name of the column that you initially sort by: ")
		sample = raw_input("Enter the name of the column that is a subset of the initial column: ")
var = True

log = raw_input("Considering the dataset, which log would you like to take? Type either 'log10', 'log2', 'natural log' or 'none': ")
if log == 'log10':
	q = np.log10(q)
if log == 'log2':
	q = np.log2(q)
if log == 'natural log':
	q = np.log1p(q)


control = raw_input("Enter the name of the control group named within the .csv file: ")
while var == True:
	try:
		mean_control = q.loc[control].mean()
		std_control = q.loc[control].std()
		var = False
	except:
		print "The control group was not found in the data. Please enter it again"
		control = raw_input("Enter the name of the control group named within the .csv file: ")
var = True

condition = 'yes'
while condition == 'yes':
	experimental = raw_input("Enter the name of the experimental group: ")
	output_file = raw_input("Enter the name of the file you want generated, ending with .csv: ")
	while var == True:
		try:
			q.loc[experimental].mean().sub(mean_control).div(std_control).to_csv(output_file)
			var = False
		except:
			print "The experimental group was not found, please try again"
			experimental = raw_input("Enter the name of the experimental group: ")
	condition = raw_input("Do you want to compare against another experimental group with this dataset? (yes/no) ")

var = True
Second_condition = raw_input("Would you like to compare the differences between two experimental groups with regards to the control? (yes/no) ")
while Second_condition == 'yes':
	a = raw_input("Enter the name of the first group you would like to compare agaisnt: ")
	b = raw_input("Enter the name of the second group you would like to compare agaisnt: ")
	c = raw_input("Enter the name of the output file, ending in .csv: ")
	while var == True:
		try:
			q.loc[a].mean().sub(q.loc[b].mean()).div(q.loc[b].std()).to_csv(c)
			var = False
		except:
			print "One or both of the comparison groups was not found, please type both again:"
			a = raw_input("Enter the name of the first group you would like to compare agaisnt: ")
			b = raw_input("Enter the name of the second group you would like to compare agaisnt: ")
	Second_condition = raw_input("Would you like to compare another dataset? (yes/no)")
	
	
	
	
	
	
