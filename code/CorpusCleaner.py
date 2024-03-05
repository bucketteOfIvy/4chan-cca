### Author: Ashlynn Wimer
### Date: 3/1/2024
### About: This script generates a document embedding for *all*
###        of the posts in my corpus, and then attaches the a doc
###        vector to each image.

# I also need a very specific cleanup to occur, so we write that below.
def cleaner_tokens(soiled_tokens):
    '''
    Cleans up a few messes in my tokens.

    Inputs:
      soiled_tokens (list of strings): the dirty tokens

    Returns: list of tokens without any punctuation.
    '''
    rv = []
    for value in soiled_tokens:
        if value not in ['<', '+', '>', ':', ';', '=', '/', '\\']:
            rv.append(value)
    return rv

import gensim.models.doc2vec as d2v
import HelperChan
import pandas as pd
import spacy
from tqdm import tqdm
tqdm.pandas()

try:
    nlp = spacy.load("en")
except OSError:
    nlp = spacy.load("en_core_web_sm")

# moved this here from lucem_illud just to ensure I can debug it as needed.
def word_tokenize(word_list, model=nlp, MAX_LEN=30000000):
    tokenized = []
    if type(word_list) == list and len(word_list) == 1:
        word_list = word_list[0]

    if type(word_list) == list:
        word_list = ' '.join([str(elem) for elem in word_list]) 
    # since we're only tokenizing, I remove RAM intensive operations and increase max text size

    model.max_length = MAX_LEN
    doc = model(word_list, disable=["parser", "tagger", "ner", "lemmatizer"])
    
    for token in doc:
        if not token.is_punct and len(token.text.strip()) > 0:
            tokenized.append(str(token.text))
    return tokenized


if __name__ == '__main__':
    print('Reading in three weeks of data..')
    week1 = pd.read_csv('../data/lgbt_week_1.csv')[['subject', 'id', 'content']]
    week2 = pd.read_csv('../data/lgbt_week_2.csv')[['subject', 'id', 'content']]
    week3 = pd.read_csv('../data/lgbt_week_3.csv')[['subject', 'id', 'content']]

    corpus = pd.concat(
        [week1, week2, week3], ignore_index=True
    ).drop_duplicates('id')

    print(f'Read in corpus! Is of shape {corpus.shape}')

    print('Preprocessing corpus..')
    print('Backreffing...')
    corpus['clean_content'] = corpus['content']\
                                .progress_apply(lambda x: HelperChan.content_with_back_reference(str(x), corpus))\
                                .progress_apply(HelperChan.remove_links)

    print('Tokenizing...')
    corpus['tokens'] = corpus['clean_content']\
                        .progress_apply(word_tokenize)\
                        .progress_apply(cleaner_tokens)

    corpus.to_csv('../data/preprocessed.csv')
    
