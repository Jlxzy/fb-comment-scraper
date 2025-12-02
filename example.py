from env_secrets import EMAIL, PASSWORD # login details can be stored as constants in a seperate python file such as env_secrets.py
from fb_comment_scraper import FbCommentScraper # import the comment scraper class

# initialise FbCommentScraper object with your account email, password, and the url of the post you want to scrape
scraper = FbCommentScraper(email=EMAIL, password=PASSWORD, post_url="https://www.facebook.com/xxxxxxxxxxxxxxxxxxxx")
scraper.scrape() # call the scrape() method to begin the scraping process

# once the scraper has finished scraping, all comments will be stored in the comments attribute of the scraper object
comments = scraper.comments # list of comment tuples, each comment containing strings for name of commenter,
                            # comment content, and url of comment

# an example of processing the retrieved comments, which saves each comment to a text file
with open("comments.txt", "w") as f:
    for name, text, link in comments:
        f.write(f"{name}: {text} - {link}\n")
