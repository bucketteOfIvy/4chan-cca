### Author: Ashlynn Wimer
### Date: 2/11/2024
### About: This is a script that shows the user 4chan posts and then prompts them
###        to label the post as either "about trans people" or "not."
###        It then saves the resultant labels to the sample-data DataFrame.
### About -v: Sample posts are pulled from the `lgbt_tokenized.csv` dataset,
###           which is a series of posts from 4chan's /lgbt/ board that were
###           pulled by occassional manual calls to the `4chan_scrape.py`
###           script made every few days.

import HelperChan as hc
import pandas as pd
# TODO: make this funnier iff you plan on using it on others 
print('''Welcome to l4beler.py, the world's most innovative 4chan post labeling module (\j).''')

def limited_input(prompt, is_valid_response=lambda x: (x in ['0', '1']), condition='Either 0 or 1.'):
    '''
    Force user to respond with a response as defined by the function is_valid_Response.
    '''
    while True:
        rsp = input(prompt)
        if is_valid_response(rsp):
            return rsp
        else:
            print(f'Response is not valid, must satisfy: {condition}')

def is_pos_int(x):
    '''
    Function which returns True if x can be coerced to int, and False otherwise.
    '''
    try:
        if int(x) > 0:
            return True
        return False
    except:
        return False

num_to_grab = limited_input('How many posts would you like to label?\n', 
                            is_valid_response=is_pos_int, 
                            condition='is positive integer')

print(f"Awesome, I'll grab {int(num_to_grab)} posts!")

print(f"Grabbing {int(num_to_grab)} random posts..")

# Read and subset
posts = pd.read_csv('../data/lgbt_week_1.csv')
sampled_posts = posts.sample(n=int(num_to_grab))

print(f'{len(sampled_posts)} posts grabbed! Prepare yourself for ~classifying~')

classes = {}
for ind, post in sampled_posts.iterrows():
    print('-' * 20)
    try:
        backref = hc.content_with_back_reference(post['content'], posts)
    except TypeError:
        # fix this later -.-
        print("Failed to retrieve proper backref. Presenting post without context.")
        backref = post['content']
    print(backref)
    rsp = limited_input('\n:: If this is a trans related post, type "1". Otherwise, type "0". ::\n')
    classes[ind] = int(rsp)

print(classes)
cldf = pd.DataFrame({'classification':classes.values()}, index=classes.keys())
print(cldf)
sampled_posts = sampled_posts.merge(cldf, left_index=True, right_index=True)

filename = input("""What would you like the filename of your classification to be?
                  Note that this will already save in the ../data/ directory.\n""")
try:
    sampled_posts.to_csv(f'../data/{filename}')
except:
     sampled_posts.to_csv('../data/woops_there_was_an_error_lol.csv')