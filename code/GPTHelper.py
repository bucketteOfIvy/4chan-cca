### Author: Ashlynn Wimer
### Date: 3/4/2024
### About: This python module contains helper functions for interacting with 
###         the OpenAI API. It's currently small and poorly designed, but I
###         plan to develop it further.

def create_example_messages(train_posts, content_col='content', classification_col='classification', system_role=None):
    '''
    Given a DataFrame of 4chan posts, creates example messages for fine-tuning gpt3.5-turbo. 
    Note that every message provided in the train_posts variable will be used.

    Inputs: 
       train_posts (DataFrame): DataFrame of classified 4chan posts.
       content_col (str): Name of the column containing the relevant content. Defaults 'content'
       classification_col (str): Name of the column containing the classification of the post. Defaults 'classification'
       system_role (str): Description of the role the system should play; if None, defaults to a prewritten prompt
         about classifying /lgbt/ posts as about or not about trans people.
       
    Returns: list of dictionaries for fine tuning.  
    '''
    examples = []

    system_role = 'You are a classifier which reads the raw content of posts from 4chan\'s /lgbt/ board, and says whether or not they discuss trans people or trans-related topics. If the post is about trans people, respond "Yes". Otherwise, respond "No".'    
    for _, post in train_posts.iterrows():
        
        user_prompt = \
        f'''
        Does the following message discuss trans people or trans-related topics? Yes or No.
        
        MESSAGE: {post[content_col]}
        '''

        assistant_content = 'Yes' if post[classification_col] == 1 else 'No'

        new_example = \
            {'messages':
                [
                    {'role': 'system', 'content': system_role},
                    {'role': 'user', 'content':user_prompt},
                    {'role':'assistant', 'content':assistant_content}
                ]
            }
        
        examples.append(new_example)

    return examples