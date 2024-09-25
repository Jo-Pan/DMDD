# DMDD: A Large-Scale Dataset for Dataset Mentions Detection
The recognition of dataset names is a critical task for automatic information extraction in scientific literature, enabling researchers to understand and identify research opportunities. However, existing corpora for dataset mention detection are limited in size and naming diversity. In this paper, we introduce the Dataset Mentions Detection Dataset (DMDD), the largest publicly available corpus for this task. DMDD consists of the DMDD main corpus, comprising 31,219 scientific articles with over 449,000 dataset mentions weakly annotated in the format of in-text spans, and an evaluation set, which comprises 450 scientific articles manually annotated for evaluation purposes. We use DMDD to establish baseline performance for dataset mention detection and linking. By analyzing the performance of various models on DMDD, we are able to identify open problems in dataset mention detection. We invite the community to use our dataset as a challenge to develop novel dataset mention detection models.

This Github include code for data generation process and the machine learning model experiments.

DMDD data can be downloaded from here: https://drive.google.com/drive/folders/1UFX821sKCIBhVlaCVfj0HXjBWhIdXxji?usp=sharing
- main.csv: includes dataset spans in each paper
- ml_datasetname_inputs_flv0.p: includes processed substring including dataset mentions/ 

  You may load it into python by: 
  ```
  X, y, X_pids = pickle.load(open("../data/ml_datasetname_inputs_flv0.p", "rb"))
  ```
- ml_datasetname_inputs_flv0_sectionTitles.p: includes the section titles where each record is extracted from the paper. 


```
@article{pan-etal-2023-dmdd,
    title = "{DMDD}: A Large-Scale Dataset for Dataset Mentions Detection",
    author = "Pan, Huitong  and
      Zhang, Qi  and
      Dragut, Eduard  and
      Caragea, Cornelia  and
      Latecki, Longin Jan",
    journal = "Transactions of the Association for Computational Linguistics",
    volume = "11",
    year = "2023",
    address = "Cambridge, MA",
    publisher = "MIT Press",
    url = "https://aclanthology.org/2023.tacl-1.64",
    doi = "10.1162/tacl_a_00592",
    pages = "1132--1146",
}
```
