## Project Introduction

This repository contains the data and codebase for an ongoing project investigating the usage of 4chan's /lgbt/ board by trans people. The most recent version (stored here) is the version for a class. As a note, when my laptop is behaving, routine commits should be made to this repository every 30 minutes by a laptop in my house; these commits just update the data, and do not constitute changes to the codebase or analysis scripts used in the class.

### Important Files

The `code` file contains my code, while `data` contains my data. The most important files are:

* `CorpusCleaner.py` and `embedder.py` are the two scripts which clean my corpus and create doc2vec embeddings of every element in it, repsectively. These scripts are the "data preprocessing scripts" for my classifier model.

* `gptlabeler.ipynb` is used to generate GPT labeled data, as well as to validate GPT's performance on the task. The version left in here was written before I discovered that daily rate limits exist, and as such the annotations imply that I intended to use it to label my full dataset (which I unfortunately could not).

* `Classifier.ipynb` is the script where my actual data classification occurs.

* `4chan_scrape.py` is a webscraper that is called every 30 minutes from a laptop in my house. It is specifically called when Windows Task Scheduler executes `lgbt.bat`, and refers to `constants.txt` to see where it ought output to. Additionally, it logs it's activity in `logs.txt`. 

* `SummaryAnalysis.ipnyb`, `WordCounting.ipynb`, and `TopicAnalysis.ipynb` are my analysis notebooks.

* `HelperChan.py` and `GPTHelper.py` are small helper modules I created.

* `l4beler.py` was used to label 4chan data by hand.

