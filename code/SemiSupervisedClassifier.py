### Author: Ashlynn Wimer
### Date: 3/1/2024
### About: This python script creates a semi-supervised stacking model
###        that attempts to use wordvectors to predict whether 4chan
###        posts are or are not trans related.

# Things needed to stack:
from sklearn.neural_network import MLPClassifier
#from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.ensemble import (StackingClassifier, 
                              BaggingClassifier, 
                              GradientBoostingClassifier,
                              RandomForestClassifier)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

import HelperChan
import pandas as pd
import numpy as np

k=100 # values to add to each category

def make_clf(training_data, testing_data):
    '''
    This function assumes the test train split was made in advanced.
    '''

    vec_train = np.stack(training_data['docsvecs'].values)
    lab_train = training_data['classification'].values 
    
    print(f'Training with {sum(lab_train)} positive values, {len(lab_train) - sum(lab_train)} negative')

    vec_test = np.stack(testing_data['docsvecs'].values)
    lab_test = testing_data['classification'].values

    base_estimators = [
        ('SVC', SVC()),
        ('BaggedLogistics', BaggingClassifier(estimator=LogisticRegression(), 
                                            max_features=.75, 
                                            max_samples=.75, 
                                            bootstrap_features=True, 
                                            n_estimators=10)),
        ('GradientBoost', GradientBoostingClassifier()),
        ('KNN', KNeighborsClassifier(algorithm='ball_tree', 
                                    leaf_size=10, 
                                    n_neighbors=5, p=1)),
        ('DecisionTree', DecisionTreeClassifier())
    ]

    stack_clf = StackingClassifier(estimators=base_estimators, 
                                   final_estimator=MLPClassifier(max_iter=1000))

    stack_clf.fit(vec_train, lab_train)
    
    # Score
    print(stack_clf.score(vec_test, lab_test))
    
    return(stack_clf)

if __name__ == '__main__':

    
    # Read in labeled posts; we have three weeks of them,
    # so we need to read in all weeks worth of posts.
    print('Reading and merging three weeks of labeled data...')
    labeled_posts = pd.concat(
        [
            pd.read_csv('../data/first_pass_labels.csv', index_col='Unnamed: 0'),
            pd.read_csv('../data/lgbt_week_2_classified.csv', index_col='Unnamed: 0'),
            pd.read_csv('../data/lgbt_week_3_classified.csv', index_col='Unnamed: 0')
        ],
        ignore_index=True
    ).drop_duplicates()

    # Acquire docvecs
    print('Getting docvecs..')
    docvecs = pd.read_csv('../data/docvecs.csv')

    # Merge in
    print('Merging things together..')
    labeled_posts = labeled_posts.merge(docvecs, on='id')

    # Fix our vector arrays
    print('Cleaning up vectors..')
    labeled_posts['docsvecs'] = labeled_posts['docsvecs']\
        .apply(HelperChan.very_good_ast_literal_eval)\
        .apply(np.array)

    # Do the test train split; testing data will be held out throughout.
    train = labeled_posts.sample(frac=.6)
    test = labeled_posts.drop(train.index)

    # Used to check model performance.
    vec_test = np.stack(test['docsvecs'].values)
    lab_test = test['classification'].values

    # Read in the unlabeled data to be added to the mix.
    print('Reading in all of our posts and attaching docvecs')
    posts_all = pd.read_csv('../data/preprocessed.csv', index_col='Unnamed: 0')
    posts_all = posts_all.merge(docvecs, on='id')
    posts_all['docsvecs'] = posts_all['docsvecs']\
                                .apply(HelperChan.very_good_ast_literal_eval)\
                                .apply(np.array)
    posts_all = posts_all[~posts_all['id'].isin(test['id'])].reset_index(drop=True)


    # While loop is a placeholder until I determine a more 
    # reasonable cutoff rule.
    i = 0
    while i < 10:
        print('Training classifier.')
        clf = make_clf(train, test)
        print(classification_report(lab_test, clf.predict(vec_test), labels=[0, 1]))

        docvecs = np.stack(posts_all['docsvecs'].values)

        # Get clasifier probabilities for all values.
        probs = clf.predict_proba(docvecs)
        probs_pos = [prob[1] for prob in probs]
        probs_neg = [prob[0] for prob in probs]

        # Get the top 100 most likely positive, negative clasisfications.
        top_k_pos_inds = np.argpartition(probs_pos, -k)[-k:]
        top_k_neg_inds = np.argpartition(probs_neg, -k)[-k:]

        # Find the cutoffs to retrieve those, just so we can report
        # what our cutoff (de jour) is, even if we de facto do not need it.
        cutoff_pos = np.array(probs_pos)[top_k_pos_inds][-1]
        cutoff_neg = 1 - cutoff_pos

        print(f'Using a probability cutoff of {cutoff_pos} for the positive case')

        # Assign our new values
        new_labels = {}
        for ind, id in enumerate(posts_all['id'].values):
            if ind in top_k_neg_inds:
                new_labels[id] = 0
            if ind in top_k_pos_inds:
                new_labels[id] = 1

        # Add them to the training dataset
        newly_labeled = posts_all.copy()[posts_all['id'].isin(new_labels.keys())]
        newly_labeled['classification'] = newly_labeled['id'].apply(lambda x: new_labels[x])

#        print(posts_all)
        to_drop = np.concatenate([top_k_neg_inds, top_k_pos_inds])
        posts_all = posts_all.drop(index=to_drop)\
                            .reset_index(drop=True)


        print(f'Adding the {len(newly_labeled)} new labeled posts to our training dataset.')

        train = pd.concat([train, newly_labeled], ignore_index=True).drop_duplicates('id')

        print(f'New training dataset has {len(train)} posts.')
                                        
        i += 1 

        print('================')
        
        