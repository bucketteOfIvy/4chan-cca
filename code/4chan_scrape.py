from pandas import DataFrame, concat 
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
# from datetime import datetime
import pandas as pd
import logging
import spacy
import re

URL_REGEX = r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
POST_REF_REGEX = r'>>[\d]{8}'

nlp = spacy.load('en_core_web_sm')

# TODO: test to see if this works on other boards

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
    # stolen from https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url

    rv = re.sub(URL_REGEX, ' ', content)
    rv = re.sub(POST_REF_REGEX, '\n', content)
    
    return rv

def get_thread_subject(soup):
    '''
    Given the soup for a thread, finds the thread's subject.

    Inputs:
      soup (BeautifulSoup): BeautifulSoup for a 4chan thread.

    Returns: string containing the thread's subject
    '''
    subject = soup.find('span', class_='subject')

    if not subject:
        first_post = soup.find('div', class_='post')
        subject = first_post.find('a', title='Reply to this post').get_text()
        return subject

    if subject.get_text().strip() == '':
        first_post = soup.find('div', class_='post')
        subject = first_post.find('a', title='Reply to this post').get_text()
        return subject
    
    return subject.get_text()

def scrape_thread(url):
    '''
    Function which scrapes all posts from a given 4chan thread and 
    outputs them in a pandas DataFrame.

    Inputs:
      url (str): url of the thread
    
    Returns: DataFrame containing 
                subject: subject heading for the post, or ID of lead post
                id: id for the post itself
                author: username, if available, anonymous otherwise
                date: the date the post was made, MM/DD/YYYY
                time: time, in HH:MM:SS
                content: raw content of the post
                clean_content: content of the post without URLS, refs
                refs: other posts referenced by this one
                urls: other websites referenced by this post
    '''
    session = HTMLSession()

    #### Extract content and render
    req = session.get(url)
    req.html.render()
    soup = bs(req.text, 'html.parser')

    posts = [post for post in\
             soup.find_all('div', class_='post')]
    
    subject = get_thread_subject(soup)

    ### Sort content from posts        
    post_content, date, time, post_id, posters = [], [], [], [], []
    clean_contents, refs, links = [], [], []
    for post in posts:
        poster = post.find('span', class_='name').get_text()
        time_dirty = post.find('span', class_='dateTime').get_text()
        num = post.find('a', title='Reply to this post').get_text()
        content = post.find('blockquote', class_='postMessage').get_text()

        references = get_references(content)
        links_to = get_urls(content)

        clean_content = remove_links(content)

        post_content.append(content)
        date.append(re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{2}', time_dirty)[0])
        time.append(re.search(r'[0-9]{2}:[0-9]{2}:[0-9]{2}', time_dirty)[0])
        post_id.append(num)
        posters.append(poster)
        clean_contents.append(clean_content)
        refs.append(references)
        links.append(links_to)

    return DataFrame({'subject':[subject for i, _ in enumerate(post_content)],\
                      'id':post_id, \
                        'author':posters, \
                          'date':date,\
                          'time':time,\
                      'content':post_content, \
                        'clean_content':clean_contents,\
                        'refs':refs,\
                          'urls':links})

def get_threads(soup):
    '''
    Function which finds all the threads from a given
    4chan page.

    Inputs: 
      url (str): url of the thread.

    Returns: list of urls pointing to threads.
    '''
    replylinks = [replylink['href'] for replylink\
                  in soup.find_all('a', class_='replylink')\
                    if replylink.text == 'Click here']

    return(replylinks)

def get_posts_from_page(url):
    '''
    Extract all posts from every thread on a given page.

    Inputs: 
      url (str): url of the page.
    
    Returns: Pandas DataFrame containing post content, post time, post id,
      and poster for all threads on the page.
    '''
    session = HTMLSession()
    req = session.get(url)
    req.html.render()
    soup = bs(req.text, 'html.parser')

    threads = [url + thread for thread in get_threads(soup)]
    logging.info('Got threads!\n', threads)

    df = scrape_thread(threads.pop())
    
    for thread in threads:
        df = concat([df, scrape_thread(thread)], ignore_index=True)
    
    return df

def get_all_current_posts(board):
    '''
    Get all posts currently on 4chan's /lgbt/. This heavily abuses the fact
    that 4chan has 10 pages worth of posts at any time.
    
    Returns: DataFrame of 4chan posts sorted by thread subject, with post id, 
      post contents, poster, and post time. 
    '''
    reqs = [HTMLSession().get(f'https://boards.4chan.org/{board}/{i}')\
            for i in range(1, 11)]
    logging.info("Made reqs!")
    
    soups = []
    for req in reqs:
        # might be necessary to make a copy 
        req.html.render()
        soups.append(bs(req.text, 'html.parser'))
    logging.info('Made soups!')
    
    threads = []
    for soup in soups:
        rel_threads = get_threads(soup)
        threads.extend([f'https://boards.4chan.org/{board}/' + thread\
                        for thread in rel_threads]) 
    logging.info(f'Got threads! {len(threads)} in total, {len(list(set(threads)))} unique!')

    logging.info(f'Scraping thread number 0...')
    df = scrape_thread(threads.pop())

    for i, thread in enumerate(threads):
        logging.info(f'Scraping thread number {i+1}...')
        ## Adding this to test something weird
        print(f'Scraping thread numbe {i+1}...')
        df = concat([df, scrape_thread(thread)], ignore_index=True)
    
    logging.info('Returning a dataframe!')
    return df

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, filename='logs.txt',
                            format='%(asctime)-15s %(levelname)-8s %(message)s')

    with open('constants.txt', 'r') as f:
        board = f.readline().strip()
        save_path = f.readline().strip()

    df = get_all_current_posts(board)
        
    ## New Save

    print('Reading old data...')
    
    try:
        old_df = pd.read_csv(save_path)
    except FileNotFoundError:
        logging.info(f"No old file found. Saving to {save_path}")
        df.to_csv(save_path, index=False)
        logging.info('Saved!')
        exit()        

    logging.info(f'Pulled {len(df)} posts, merging into dataframe of {len(old_df)} posts...')
    
    df = concat([old_df, df], ignore_index=True)
    df['id'] = df['id'].astype(str)
    df.drop_duplicates(subset=['id'], inplace=True)
    
    logging.info(f'Resultant dataframe has {len(df)} posts')
    logging.info(f'It also has {df["subject"].nunique()} unique threads')
    print('Saving..')
    df.to_csv(save_path, index=False)

    logging.info('=' * 40)