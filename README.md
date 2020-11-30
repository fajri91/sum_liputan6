# Liputan6: Summarization Corpus for Indonesian Language

## About

Liputan6 is the first large-scale Indonesian corpus for Abstractive and Extractive summarization.
This data has two sets:

| Data          | Train    | Dev      | Test      |
| ------------- | :-------:| --------:|  --------:|
| Canonical     | 193,883  | 10,972   | 10,972    |
| Xtreme        | 193,883  |  4,948   |  3,862    |

Liputan6 is registered as a new dataset in [IndoLEM](https://indolem.github.io/) (Indonesian resource collection encompassing seven NLP tasks). 

## Paper
Fajri Koto, Jey Han Lau, and Timothy Baldwin. [_Liputan6: A Large-scale Indonesian Dataset for Text Summarization_](https://arxiv.org/pdf/2011.00679.pdf). In Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing (AACL-IJCNLP 2020)

## Obtaining Liputan6 Data

#### Disclaimer
According to Indonesian Copyright Law Number 28 Year 2014, this corpus can be used for academic research. It is STRONGLY FORBIDDEN to use this corpus as well as any summarization models created using this corpus for commercialized activities.
We highly encourage for another respective researcher to not re-distribute the dataset.

#### Way1 - By filling the form

Please fill this [form](https://docs.google.com/forms/d/1bFkimFsZoswKCbUa76yHqi9hizLrJYne-1G_r5unfww/edit?usp=sharing). A url to download Liputan6 corpus will be sent to your email address.

#### Way2 - By running the codes

* First, please download a json file, containing urls of Liputan6 [here](https://drive.google.com/file/d/17eZ6D-iKBA5rmD8KQg0vr9tvobqmWUT9/view?usp=sharing). Put file `url.json` in this repository.
* Please run the following codes (tested in Python 3.7). If you want to increase `number of thread`, please adjust the code manually.
```
pip install -r requirements.txt
python 0_download.py
python 1_preprocessing.py
python 2_create_extractive_label.py
python 3_get_xtreme.py
```
* If you want to run pointer generator network, and BERT-based summarization model, data preparation is as followed:
```
python 4_make_data_files_pg.py
python 5_make_data_files_presumm_mbert.py
```

## Training neural models:

* Pointer Generator Network: [PG](https://github.com/becxer/pointer-generator/).
* Bert-based summarization Model: [PreSumm](https://github.com/nlpyang/PreSumm).

## Test Set Output

We also provide test set output as reported in our paper. You can download them [here](https://drive.google.com/file/d/10t5IzDXPCejNNZkVCgdI2KNt4CFxr6jG/view?usp=sharing).

| Model                 | R1   | R1   | RL   |
| ----------------------|:-----|------|-----:|
| Lead-2                |36.68 | 20.23|33.71 |
| PTGen                 |36.10 | 19.19|33.56 |    
| BertExt (mBERT)       |37.51 | 20.15|34.57 |    
| BertAbs (mBERT)       |39.48 | 21.59|36.72 |    
| BertExtAbs (mBERT)    |39.81 | 21.84|37.02 |
| BertExt (indoBERT)    |38.03 | 20.72|35.07 |    
| BertAbs (indoBERT)    |40.94 | **23.01**|37.89 |    
| BertExtAbs (indoBERT) |**41.08** |22.85 |**38.01**|


## Evaluation

Please install [pyrouge](https://github.com/bheinzerling/pyrouge) for evaluating the summary.


