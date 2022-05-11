import json
import os
import numpy as np
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pickle
import pandas as pd

def get_datasets(URL):
    """
    Get datasets relating to a paper
    
    Testing urls:
    URL = "https://paperswithcode.com/paper/age-and-gender-classification-from-ear-images"
    URL = "https://paperswithcode.com/paper/mobilenets-efficient-convolutional-neural"
    URL = "https://paperswithcode.com/paper/minibatch-gibbs-sampling-on-large-graphical"
    URL = "https://paperswithcode.com/paper/tvqa-localized-compositional-video-question"
    """
    out = {
        'datasets_used_lower': [],
        'datasets_used_full': [],
        'datasets_introduced_lower':[],
        'datasets_introduced_full':[],
    }
    used = True
    introduced = False

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    mydivs = soup.find_all("div", {"class": "paper-datasets"})
    results = mydivs[0].find_all(['p','a'])
    for r in results:
        text = r.text.strip()
        if text == 'Add Datasets':
            continue
        elif text == 'Introduced in the Paper:':
            introduced = True
            used = False
            continue
        elif text == 'Used in the Paper:':
            introduced = False
            used = True
            continue

        if used:
            out['datasets_used_full'].append(text)
            out['datasets_used_lower'].append(r["href"].replace("/dataset/", ""))
        elif introduced:
            out['datasets_introduced_full'].append(text)
            out['datasets_introduced_lower'].append(r["href"].replace("/dataset/", ""))
    return out
 
def crawl_dataset_names(old_papers=[], input_file="./input/papers-with-abstracts.json"):
    print("For each paper in Paper_With_Code, we are now crawling the dataset names being mentioned/introduced in the paper.")
    file = json.load(open(input_file))
    i = 0
    error = []
    for r in tqdm(range(len(file))):
        i += 1
        if file[r]['paper_url'] in old_papers:
            continue
        
        out = {
                'datasets_used_lower': [],
                'datasets_used_full': [],
                'datasets_introduced_lower':[],
                'datasets_introduced_full':[],
            }

        try: 
            out = get_datasets(file[r]["paper_url"])
        except:
            error.append(r)
            print("error:", error)

        for k in out.keys():
            file[r][k] = out[k]
        

        if i % 1000 == 0 or i == len(file):
            with open(input_file.replace(".json", "-datasets.json"), 'w') as f:
                json.dump(file, f)
            pickle.dump( error, open( "./input/error.p", "wb" ) )
            print("error:", error, f"nError={len(error)}")

def clean_pwc():
    print("----- Cleaning PWC -------")
    features = ['datasets', 'paper_url_pdf', 'repo_url', 'is_official', 'mentioned_in_paper', 'mentioned_in_github', 'framework', 'title','proceeding',
            'tasks', 'date', 'methods', ]
    bool_feats = ['is_official', 'mentioned_in_paper', 'mentioned_in_github',]
    
    df0 = pd.DataFrame(json.load(open('./input/papers-with-abstracts-datasets.json')))
    df1 = pd.DataFrame(json.load(open('./input/links-between-papers-and-code.json')))
    
    
    print(f"Total number of repos {len(df1):,}")
    val, ct = np.unique(df1["paper_url"].astype(str), return_counts=True)
    df1_ = df1[df1.paper_url.isin(val[ct==1])] #the papers with unique github url
    print(f"1) We only keep {len(df1_):,} repos with unique paper_url, which means these papers only have 1 github repo. [nRepo={len(df1_):,}]")

    temp = df1[~df1.paper_url.isin(df1_.paper_url)]
    val_ = np.unique(temp["paper_url"].astype(str))
    text = f"2) For the remaining {len(temp):,} repos, they links to {len(val_):,} papers." 


    subset = temp[temp.mentioned_in_paper]
    val, ct = np.unique(subset["paper_url"].astype(str), return_counts=True)

    addons = subset[subset.paper_url.isin(val[ct==1])]
    text += f" {len(addons):,} repos are the only repo being mentioned in paper (mentioned_in_paper=True)." 

    df1_ = pd.concat([df1_, addons])
    assert len(df1_) == len(np.unique(df1_.paper_url))
    removed = len(df1[df1.paper_url.isin(addons.paper_url)]) - len(addons)
    text += f"We keep these repos, and removed {removed:,} repos which link to the same set of papers. [nRepo={len(df1_):,}]"
    print(text)


    temp = df1[~df1.paper_url.isin(df1_.paper_url)]
    val_ = np.unique(temp["paper_url"].astype(str))
    text = f"3) For the remaining {len(temp):,} repos, they links to {len(val_):,} papers."

    subset = temp[temp.is_official]
    val, ct = np.unique(subset["paper_url"].astype(str), return_counts=True)
    addons = subset[subset.paper_url.isin(val[ct==1])]
    assert len(addons) == len(np.unique(addons.paper_url))
    text += f" {len(val[ct==1]):,} of them are the only official repo (is_official=True). "

    removed = len(df1[df1.paper_url.isin(addons.paper_url)]) - len(addons)
    df1_ = pd.concat([df1_, addons])

    text += f"We keep these repos, and removed {removed:,} repos which link to the same set of papers.[nRepo={len(df1_):,}]"
    print(text)


    temp = df1[~df1.paper_url.isin(df1_.paper_url)]
    val_ = np.unique(temp["paper_url"].astype(str))
    text = f"4) For the remaining {len(temp):,} repos, they links to {len(val_):,} papers. For each paper, we keep the first repo appeared in the dataset." 

    addons = temp.groupby('paper_url').first().reset_index()
    assert len(addons) == len(np.unique(addons.paper_url))
    removed = len(df1[df1.paper_url.isin(addons.paper_url)]) - len(addons)
    df1_ = pd.concat([df1_, addons])
    text += f"we keep {len(addons):,} repos and removed {removed:,} repos. [nRepo={len(df1_):,}]"
    print(text)
    print(" ")
    
    df = df0.merge(df1_, on="paper_url", how='left')
    print(f"0) Merged df. nRows = {len(df):,}")
    temp = df[pd.notna(df["arxiv_id"])]
    unique_aid, ct = np.unique(temp["arxiv_id"], return_counts=True)
    unique_aid = unique_aid[ct==1]
    print(f"    unique arxiv_id = ({len(unique_aid):,}, {len(unique_aid)*100/len(temp):.2f}% of all non-na, {len(unique_aid)*100/len(df):.2f}% of all records)")
    df = df[df.arxiv_id.isin(unique_aid)]
    print(f"1) Keep only papers with unique arxiv_id, nPapers= {len(df):,}")

    with_datasets = (df.datasets_introduced_full + df.datasets_used_full).apply(lambda x: len(x)) > 0
    with_methods = df.methods.apply(lambda x: len(x)) > 0
    with_framework = pd.notna(df.framework) & (df.framework.str.lower() != "none")

    print(f"2) Find papers with target labels: ")
    print(f"    - with dataset names = {sum(with_datasets):,}, {sum(with_datasets)*100/len(df):.2f}%")
    print(f"    - with methods = {sum(with_methods):,}, {sum(with_methods)*100/len(df):.2f}%")
    print(f"    - with framework = {sum(with_framework):,}, {sum(with_framework)*100/len(df):.2f}%")
    temp = with_datasets & with_methods & with_framework
    print(f"    - with dataset names, methods and frameworks  = {sum(temp):,}, {sum(temp)*100/len(df):.2f}%")

    df = df[with_datasets + with_methods + with_framework]
    print(f"3) Keep papers with at least 1 target labels: {len(df):,}")
    
    df.to_csv("./input/pwc.csv")
    papers_to_be_downloaded = df['arxiv_id'].to_list()
pickle.dump( papers_to_be_downloaded, open( "./data/20200705v1/full/arxiv_id_to_be_downloaded_V2.p", "wb" ) )
    print("----- PWC is now cleaned -------")