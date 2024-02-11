### Author: Ashlynn Wimer
### Date: 2/11/2024
### About: This is a script that shows the user 4chan posts and then prompts them
###        to label the post as either "about trans people" or "not."
###        It then saves the resultant labels to the sample-data DataFrame.
### About -v: Sample posts are pulled from the `lgbt_tokenized.csv` dataset,
###           which is a series of posts from 4chan's /lgbt/ board that were
###           pulled by occassional manual calls to the `4chan_scrape.py`
###           script made every few days.

from random import randint
import pandas as pd
# TODO: make this funnier iff you plan on using it on others 
print('''Welcome to l4beler.py, the world's most innovative 4chan post labeling module (\j).''')

while True:
    rsp = input("How many posts would you like to label?\n")
    try:
        int(rsp)
    except:
        print("Silly goose.")
        continue
    print(f"Awesome, I'll label {int(rsp)} posts!")
    break

print(f"Grabbing {int(rsp)} random posts..")

# Read and subset
posts = pd.read_csv('../data/lgbt_tokenized.csv')
rows = [randint(0, len(posts)) for i in range(int(rsp))]
posts = posts.loc[rows, :]

print('100 posts grabbed! Prepare yourself for ~classifying~')

classes = {}
for ind, post in posts.iterrows():
    # TODO implement the "grab prior post" function
    print('-' * 20)
    print(post['content'])
    while True:
        rsp = input('If this is a trans related post, type "1". Otherwise, type "0".\n')
        if rsp in ['0', '1']:
           classes[ind] = int(rsp)
           break
        else:
            print("Urghhghgh please give a *valid* response.")
print(post)
print(classes)
cldf = pd.DataFrame({'classification':classes.values()}, index=classes.keys())
print(cldf)
posts = posts.merge(cldf, left_index=True, right_index=True)
print(posts)
filename = input("""What would you like the filename of your classification to be?
                  Note that this will already save in the ../data/ directory.\n""")
posts.to_csv(f'../data/{filename}')