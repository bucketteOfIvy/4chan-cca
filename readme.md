# Introduction

People use social media to support their offline social transitions, raising the need to understand how social media platforms and their affordances enable such usage. Nonetheless, prior research has heavily focused on the usage of social network sites, such as Facebook, Tumblr, or Twitter, limiting the affordances explored to those prominent on social network sites. Towards understanding how different affordances influence transitioners ability to undergo social transitions online, we undertake a case study of how transgender people use 4chan's /lgbt/ board as a tool for social transition. We construct a Discourse Atom Topic Model from nearly 69,000 posts about trans people and ideas of transness on /lgbt/. Through exploration of the topics in the posts, we find evidence that psuedoanonymity -- or the ability to hide ones identity in physical space while constructing a digital persona -- may be a sufficient affordance for transition friendly social media, and discover co-usage of social network sites by to expand or sidestep the affordances offered by 4chan. Our lays the foundation for future studies attempting to understand the usage of social media to aid in transition outside of social network sites. 

## Codebase

All code was ran in a Python 3.11 environment. The `code` file contains my code, while `data` contains much of my data. The most important files are:

* `CorpusCleaner.py` and `embedder.py` are the two scripts which clean my corpus and create doc2vec embeddings of every element in it, repsectively. These scripts are the "data preprocessing scripts" for my classifier model.

* `gptlabeler.ipynb` is used to generate GPT labeled data, as well as to validate GPT's performance on the task. The version left in here was written before I discovered that daily rate limits exist, and as such the annotations imply that I intended to use it to label my full dataset (which I unfortunately could not).

* `Classifier.ipynb` is the script where my actual data classification occurs.

* `4chan_scrape.py` is a webscraper that is called every 30 minutes from a laptop in my house. It is specifically called when Windows Task Scheduler executes `lgbt.bat`, and refers to `constants.txt` to see where it ought output to. Additionally, it logs it's activity in `logs.txt`. <b>With regards to grading, please disregard any commits to these files after the submission deadline</b>.

* `SummaryAnalysis.ipnyb`, `WordCounting.ipynb`, and `TopicAnalysis.ipynb` are my analysis notebooks. `SummaryAnalysis.ipynb` features summary statistics calculation, while `WordCounting.ipynb` features word counting approaches and `TopicAnalysis.ipynb` is where topic vectors were found and analyzed.

* `HelperChan.py` and `GPTHelper.py` are small helper modules I created for working with 4chan data and GPT, respectively.

* `l4beler.py` is a command line utiltiy which was used to label 4chan data by hand en masse. 

Rerunning my final analysis should be achievable via the three ipython notebooks. However, any data preprocessing reconducted should be expected to achieve slightly different results due to randomness inherent to methods like Discourse Atom Topic Modelling.

Lastly, some of our datasets were too large for GitHub, and can instead be found on [Box](https://uchicago.box.com/s/ggwcch1trhudxreny8nz0zibfwgc4iwo). 

## License

This project is licensed under the GNU General Public License v3.0. The full license can be read [here]().
