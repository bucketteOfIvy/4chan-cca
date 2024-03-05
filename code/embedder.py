import gensim.models.doc2vec as d2v
import pandas as pd
import ast
from tqdm import tqdm
tqdm.pandas()

if __name__ == '__main__':
    corpus = pd.read_csv('../data/preprocessed.csv', index_col='Unnamed: 0')
    corpus['tokens'] = corpus['tokens'].apply(ast.literal_eval)
    
    print('Creating tagged documents...')
    taggedDocs = []
    for index, row in corpus.iterrows():
        taggedDocs.append(
            d2v.TaggedDocument(
                words=[str(word) for word in row['tokens']],
                tags=[row['id']]))
    corpus['TaggedDocs'] = [d2v.TaggedDocument(
        words=[[str(word) for word in row['tokens']]], 
        tags=row['id']) for _, row in corpus.iterrows()]

    print('Running doc2vec...')
    chanD2V = d2v.Doc2Vec(documents=taggedDocs, vector_size=100, dm=0)

    print('Extracting document vectors...')
    docvecs = [chanD2V.docvecs[post] for post in corpus['id'].tolist()]

    corpus['docsvecs'] = docvecs

    print('Saving..')
    corpus.to_csv('../data/full_corpus.csv')
