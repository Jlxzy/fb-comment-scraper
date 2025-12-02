import random
from env_secrets import EMAIL, PASSWORD # login details can be stored as constants in a seperate python file such as env_secrets.py
from fb_comment_scraper import FbCommentScraper # import the comment scraper class

# initialise FbCommentScraper object with your account email, password, and the url of the post you want to scrape
scraper = FbCommentScraper(email=EMAIL, password=PASSWORD, post_url="https://www.facebook.com/xxxxxxxxxxxxxxxxxxxx")
scraper.scrape() # call the scrape() method to begin the scraping process

# once the scraper has finished scraping, all comments will be stored in the comments attribute of the scraper object
comments = scraper.comments # list of comment tuples, each comment containing strings for name of commenter,
                            # comment content, and url of comment

# an example of processing the retrieved comments, which picks a random commenter from the list of comments
commenters = []

# add every unique commenter name to a list of commenters
for comment in comments:
    name = comment[0]

    if not name in commenters:
        commenters.append(comment[0])

random_commenter = random.choice(commenters) # pick a random name

print(f"The name of the random commenter picked is {random_commenter}")
