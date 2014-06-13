BIMM-185-Project
================
README


Z-SAM

Author Ken Williams



SUMMARY

This program uses a Z-Scoring algorithm as well as a name standardizing algorithm to create a Cytoscape ready .csv file.
It takes in a .csv file that should include a mutliple sample system that should include in the columns, the 
group type followed by individual samples. The remaining columns should be the metabolite names. 
The following is a walkthrough on how to use this program



WALKTHROUGH

Running the python script


  IMPORTANT! Make sure that numpy, pandas, and metabotools are installed!
  Numpy can be found at http://www.numpy.org/
  Pandas can be found at http://pandas.pydata.org/
  Metabatools are located within this github file https://github.com/krwillia/BIMM-185-Project
  
  Make sure that the following files are in the Same Directory:
    Data.csv and MasterDatabase_v2.0.6_cyto.xlsx

  Open terminal and change to the current directory that contains the python script
    ex. ..MyComputer$ cd Desktop

  run the script by typing
    python Z-SAM.py

  The program will then ask for the data file that should be used.
  Make sure that the data file that you are measuring is in the dame directory.

  for example:
    Enter the name of the Mass Spectrometry csv file:  Data.csv

  The Program will then ask if you would like to standardize the names. This then means that it will cross reference 
  the MasterDatabase_v2.0.6_cyto file, to change any chemical to the synonym that is present in the cytoscape file. 
  Typing yes will do this, as well as spit out a new data file called New Data.csv. It will then ask you:
  
    Standardizing: Enter the name of the column that you initially sort by: 
    here type in the largest group, so for instance if you're comparing a 'type or group' as opposed to a 
    sample or individual you would enter 'Type' or 'Group'
    
    Standardizing: Enter the name of the column that is a subset of the initial column: 
    Here type in the other set, so the 'Individual' or the 'Sample'
  
  The program will then ask you the same questions, so repeat what was done before.
  ex:
    Enter the name of the column that you initially sort by: Group
    Enter the name of the column that is a subset of the initial column: Sample
    
  Next the program will call for a type of taking a log of the data.
  Enter whichever you would prefer.
    Considering the dataset, which log would you like to take? Type either 'log10', 'log2', 'natural log' or 'none': log2
    
  Next the Program will ask for the control group that you would like to compare agaisnt. Make sure that this what is
  within the .csv file that you are using. Otherwise you may have an error where the program will ask you to repeat.
  ex:
    Enter the name of the control group named within the .csv file: FMR KO-Sal
    
  Next it wil ask for the experimental group you want to compare agaisnt.
  Same as before, make sure that it is spelled the same.
  ex:
    Enter the name of the experimental group: FMR KO-Sur
    
  Next it will for the name of the output file that you would like to generate.
  ex:
    Enter the name of the file you want generated, ending with .csv: Output.csv
    
  Next the program will ask if you would like to repeat the preceding with other groups within the same dataset.
  You may choose yes or no, and it will repeat the same as before.
  
  *****A potential problem with this is after the .csv file has been generated, you need to manually add one top row
  and name the left column metabolite, and the right column, Whichever is useful, such as Z-Score******
  
  Should this for whatever reason not work, there is a file name 'Sur vs Sal.csv' attached that will act
  as a model for this program.
  
Uploading to Cytoscape

  Open the Metabolism.cys file in cytoscape.
  
  There is a button that will allow you to 'Import Table from file' Click this (otherwise File->Import->File...)
  Select the file that was just generated through the python script.
  
  Don't change anything in the window that popped up, and hit OK
  (Otherwise make sure that the following are selected
    Where to Import Table Data: To a Network Collection
    Network Collection : Total_Metabolism
    Key Column: Shared Name
    Import data as: Node Table Columns
    and case sensitive
    
  Make sure that the Table Panel is viewable, under the view tab
  
  Next View the control panel, and select 'Style' and make sure at the bottom of the table 'Node' is selected
  
  From here then click the 'Fill Color' dropdown
  
  Under Column, select the column that was just added, like Z-Score, it will be the name added in the step above,
  that was annotated with the ******
  
  Now under mapping type, select Continous mapping. Already the nodes that are within the graph have been changed 
  to varioud shades of black and white. You man double click the black white gradient box. 
  A new window pops up, and you may move the triangles at the top of the box, as well as double click them to change
  their color.
  
  You could also select Min/Max to change the maximum and minimum values to try and understand the data better. 
  Cytoscape by default bases these off of the current dataset. However if the min and max of the Z-Score is -40, and 
  0.4, the gradient would be a misnomer, and should be changed. 
  The add button will insert a new gradient triangle that can be used to adjust the gradients. For isntance this
  should be changed to white, while the postive triangle is set to red, and the negative is set to green.
  
  The graph is now set up and complete. You can use the Network, under Control Panel to move through the graph for
  Analysis.
  
  
TROUBLESHOOTING
  
  The Z-Score script can run into problems if there are repeat names within the Data file, so make sure to 
  delete repeated metabolite names before running the script.
  
  Adding a new network to the Cytoscape file
    Sif Files were used to main graph, and their implementation can be found here:
    http://wiki.cytoscape.org/Cytoscape_User_Manual/Network_Formats
    
    Essentially open a text editor, and type each metabolite followed by a tab, typing 'mm' then another tab
    followed by each metabolite they interact with, seperated by tabs. Save the file so that it ends in .SIF
      ex:
          Node A  mm  Node B  Node C
          Node B  mm  Node A
          Node C  mm  Node A  
          
    You can then open this with cytoscape and it will already make the graph. You can then copy and past this into
    the Metabolism graph and add edges as needed. 
    
  Naming Issues
    Should you add any new nodes to the Metabolism graph make sure to look for the Cytoscape Synonym column in the 
    Master_Database File and add/change so that the Cytoscape Synonym column matches exactly what the respective node
    is in the Metabolism.cys file.
    
  If there are any question other remaining questions, feel free to ask me at krwillia@ucsd.edu
          
  
  
  
  
    
  
    


