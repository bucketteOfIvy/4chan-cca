### Author: Ashlynn Wimer
### Last Modified: 2/16/2024
### About: Module containing helper functions for working with 
###        4chan data.
import warnings 
import pandas as pd
import regex as re
import networkx as nx
import ast

### Constants
URL_REGEX = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
POST_REF_REGEX = r'>>[0-9]{8}'


### Basic content wrangling functions

def get_urls(content):
    '''
    Retrieve all URLS in a post.
    '''
    return re.findall(URL_REGEX, content)

def get_references(content):
    '''
    Retrieve all post ids referenced by this post.
    '''
    return re.findall(POST_REF_REGEX, content)

def remove_links(content):
    '''
    Cleans content, deleting all URLs and links.
    
    Inputs: (str) content

    Returns: (str) content without links 
    '''
    rv = re.sub(URL_REGEX, ' ', content)
    rv = re.sub(POST_REF_REGEX, '\n', content)
    
    return rv


### Presentation-ish functions

# TODO: Consider making this recursive just for the lol's.
def content_with_back_reference(post, posts):
    '''
    Given a post from 4chan (row from posts DataFrame), replace the reference 
    tags in the post with an actual copy of that post from the posts DataFrame.
    If the post is not in the posts DataFrame, throw a warning and return
    the initial post.

    Inputs:
      post (str): content of the post to be expanded upon.
      posts (DataFrame): DataFrame containing 4chan posts to weed through.

    Returns (str): Content of the post to be expanded upon with all instances
      of prior posts reference replaced with the referenced post, iff available.
    '''
    # Find references
    references = get_references(post)
    
    # Find the referenced posts
    found_refs = []
    content_col = posts.columns.tolist().index('content')
    for ref in references:
        matches = posts['id'] == int(ref.strip('>>'))     
        if sum(matches) == 1:
            # index of the content row
            # anything else returns a Series, for some reason
            mtch = posts[matches].iloc[0, content_col]
            found_refs.append(mtch)
        elif sum(matches) == 0:
            warnings.warn(f'WARNING: {ref.strip(">>")} not found in posts DataFrame.')
            found_refs.append(ref)
        elif sum(matches) >= 1:
            raise ValueError('Posts DataFrame has duplicate entries.')

    # Replace references
    for old, new in zip(references, found_refs):
        post = re.sub(old, f"<ref>{repr(new)}</ref>\n", post)

    return post

def standardize_date(date):
    '''
    Standardize a date split by / to a %Y-%m-%d format.
    '''
    m, d, y = date.split('/')
    return f"20{y[-2:]}-{m.rjust(2, '0')}-{d.rjust(2, '0')}"
    #return f"{m.rjust(2, '0')}/{d.rjust(2, '0')}/{y[-2:]}"


def make_datetime(posts):
    '''
    Given a set of 4chan posts, fix the dates.

    Assumes that date is stored in "date" and time in "time", following
    the %m/%d/%y and %H:%M:%S formats, respectively.
    
    Returns: datetime column for posts.
    '''
    datetime = posts['date'].apply(standardize_date) + ' ' + posts['time']
    
    datetime.apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S'))
    return datetime    

def label_heads(posts):
    '''
    Returns a column with 1 for the head posts and 0 for replies.
    '''
    is_head = []

    threads = set()
    for _, post in posts.iterrows():
        if post['subject'] in threads:
            is_head.append(0)
        else:
            threads.add(post['subject'])
            is_head.append(1)

    return is_head
    

class NetworkChan:

    def __init__(self, posts):
        '''
        Creates a network view of all thread in posts.
        '''
        self.posts = posts
        self.posts['datetime'] = make_datetime(self.posts)
        self.posts = self.posts.sort_values(['subject', 'datetime']).reset_index(drop=True)
        self.posts['is_head'] = label_heads(self.posts)

        
    def make_graphs(self):
        '''
        Actually make the graphs this class is here to get.
        '''
        self.graphs = self.__build_networks()


    def __make_network_from_thread(self, thread):
        '''
        Given a specific thread, make a network from that thread.
        
        Takes in a set of posts from the same thread, returns a  
        '''
        graph = nx.DiGraph()

        head = None
        for _, post in thread.iterrows():
            graph.add_node(post['id'])

            if post['is_head']:
                head = post['id']
                continue
            
            references = get_references(str(post['content']))

            makes_reference = any([(int(ref.strip('>>')) in graph.nodes)\
                                   for ref in references])

            if not makes_reference:
                graph.add_edge(post['id'], head)
                continue

            for ref in references:
                if int(ref.strip('>>')) in graph.nodes:
                    graph.add_edge(post['id'], int(ref.strip('>>')))
        
        return graph

    def __build_networks(self):
        '''
        Build a graph for every thread
        '''
        threads = [self.posts[self.posts['subject'] == thread]\
                   for thread in self.posts['subject'].unique()]

        graphs = [self.__make_network_from_thread(thread) for thread in threads]
        
        return graphs

#### Functions with niche-use cases

def very_good_ast_literal_eval(strarr):
    '''
    Ast literal eval, but tailored towards ensuring that
    the string representation of a list it reads in is *actually*
    in the format of a list.

    inputs: 
      strarr (str): string representation of a list.
    
    Returns: list version of strarr 
    '''
    strarr = re.sub(r'\[ ', '[', strarr)
    strarr = re.sub(r'\s{2,}', ' ', strarr)
    strarr = re.sub(r'\s', ',', strarr)
    try:
        return ast.literal_eval(strarr)
    except ValueError:
        print('Yell at the maker of HelperChan to make strarr more robust.')
        print(f'Show them this:\n{strarr}')