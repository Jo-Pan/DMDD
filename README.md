# DMDD

This Github include code for data generation process and the machine learning model experiments.

DMDD data can be downloaded from here: https://drive.google.com/drive/folders/1UFX821sKCIBhVlaCVfj0HXjBWhIdXxji?usp=sharing
- main.csv: includes dataset spans in each paper
- ml_datasetname_inputs_flv0.p: includes processed substring including dataset mentions/ 

  You may load it into python by: 
  ```
  X, y, X_pids = pickle.load(open("../data/ml_datasetname_inputs_flv0.p", "rb"))
  ```
- ml_datasetname_inputs_flv0_sectionTitles.p: includes the section titles where each record is extracted from the paper. 
