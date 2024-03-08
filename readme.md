## Project Introduction

This is the code repository for a recent short and preliminary analysis of transgender usage of 4chan that aimed to understand the ways in which 4chan's /lgbt/ board is used as a piece of social transition machinery by transgender users. While the first stage of the analysis has been concluded + conducted for MACS 60000, I intend to continue and refine the analysis next quarter.

## Navigating this Repository

The two main directories in this repository are `code` and `data`, which contain precisely what their titles imply: my code and my data. As an overview of the codebase:

* `4chan_scrape.py` is the file used to actually scrape my data. It refers to `constants.txt` to determine where to save it's results, and is called when taskmanager runs `lgbt.bat` on a local system every thirty minutes. It also outputs logs to `logs.txt`, but those are used entirely for debug purposes.

* `CorpusCleaner.py`, `embedder.py`, `gptlabeler.ipnyb`, and `Classifier.ipynb` form the classification pipeline for this project, with `CorpusCleaner.py` cleaning posts so that `embedder.py` can construct document vectors from the post which `Classifier.ipynb` classifies with the aid of a modified training set consisting of hand labeled data and gpt-labeled data from `gptlabeler.ipynb`. 

* `GPTHelper.py` and `HelperChan.py` are two small modules written to aid in interaction with my data. 

* `SummaryAnalysis.ipynb`, `TopicAnalysis.ipynb`, and `WordCounting.ipynb` contain all analysis presented in my paper as well as some additional undiscussed analysis.

* `SemiSupervisedClassifier.ipynb` and `gptlabeler.ipynb` contain evidence of my less-than-successful attempts at classifier construction.