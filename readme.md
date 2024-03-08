### Project Pitch (aka the thing for class)

4chan is a site with a reputation for trolls, fascist sentiments, and discrimination. However, the image
board website is also home to /lgbt/, a subforum dedicated to usage by queer individuals. This can seem
paradoxical: what are queer people doing on a site known for (among other things) hating queer people?
Reading posts on the site reveals a further paradox, in that many trans people seem to be using the site
to build indentity and as a tool for transition work. These seeming contradictions give rise to a few
research questions.
1. In what ways do trans and gender non-conforming identity groups interact and make use of 4chan's /lgbt/ board?
2. Do the patterns of trans identity building seen on 4chan's /lgbt/ board match those reported on
other websites, such as Susan's Place and Tumblr?
3. While 4chan is a largely anonymous board, the account creation affordances are cited by boyd as a 
tool for identity building on social network sites. To what extent do trans and gender non-conforming users of 
4chan's /lgbt/ board make use of these affordances?


My data for this is a collection of posts scraped from 4chan every 30 minutes (by the 
`code/4chan_scrape.py` file) and stored in this repository (currently in `data/lgbt_week_1.csv`).
The data has is structured, with the name of the user making the post (if applicable) and the thread
the user is posting in both being stored in the csv. I do not currently have labels for the data,
but intend to label some of the posts by hand as "concerning trans or gender nonconforming people" based on a 
codebook developed on random samples of other posts (not stored on this repo).

For my analysis, I want to focus on posts concerning trans people *or* those directly replying to posts
concerning trans people. To do so, I need to develop a supervised model, based on hand labeled data,
which labels posts about trans people. I will validate this model against a few basic hypotheses,
namely on the expectation that /chasergen/, /mtfgen/, and /ftmgen/ will all have many posts concerning 
trans people, while threads like /gaygen/ should have relatively few such posts. From these posts,
I plan to use a fine-tuned LLM to determine which posts are staking gender related identity claims,
which will allow me to consider in what ways trans users are building identity on /lgbt/ (e.g. 
comparisons between users with tripcodes and those without, consideration of where in threads
users are making identity claims, etc). Lastly, I'll use k-SVD to determine what topics people discussing
trans people are talking about.


### Current Project Status 
This is a git repository made as part of a computational content analysis project
investigating which identity groups use 4chan's /lgbt/ board, and how.

As of now I'm at the data collection stage. I have a web scraper (`code/4chan_scrape.py`)
that is called every hour from a local device to scrape 4chan and then push the
results to this repo in `data/lgbt_week_1.csv`. This strategic (mis)use of 
github will lead to an amusing number of commits to this repository from my
account, but -- as it's the most convenient and expedient way for me to automate
my web scraping -- I'm just running with it.

I expect to conclude my scrapeing after a week or three, at which time it 
will _also_ be the moment for me to start more formal data analysis. Expect
updates here. 
