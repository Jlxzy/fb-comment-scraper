# Facebook Comment Scraper

*Author - Joel Foster*

A Python library that can be used to scrape comments from a Facebook post without API access. Requires slight human
interaction to bypass anti-bot measures.

## Usage

First, copy the [fb_comment_scraper.py](fb_comment_scraper.py) file into the working directory of your project, then
import the class into your project using:

```python
from fb_comment_scraper import FbCommentScraper
```
Once imported, initialise a new instance of the class, with your Facebook account email, password, and the URL of the
post you wish to be scraped:

```python
scraper = FbCommentScraper(email="your.email@example.com", password="password1234", post_url="https://www.facebook.com/xxx")
```
Once initialised, the ```scrape()``` method of the class can then be called, which begins the scraping process, for
example by calling:
```python
scraper.scrape()
```
The scraping process involves logging in to the user's account, and this usually requires manual intervention from the
user to complete the anti-bot captchas, so the program waits for the user to complete this and prompts the user to
confirm when to resume automation.

Once the program completes the scraping process and parses the results, a resultant list of comments are stored in the
class instance variable ```comments```. Each comment in this list is stored as a tuple of [string, string, string], where the
first string is the name of the commenter, the second is the comment content, and the third is the URL to the original
comment.

For example, the value of the object's comments can be copied to a local variable, such as:
```python
comments = scraper.comments
```

## Processing results

Results of the scraping can be processed in any way you require, but a few examples include storing the comments in a
text file, picking a random comment from the list of comments, or analysing patterns, trends, etc. in the comments.

### Storing comments in a text file

The following example illustrates a simple way to store the resulting comments in a text file, each line containing the
name, comment content, and URL of a comment in the list.

```python
with open("comments.txt", "w") as f:
    for name, text, link in scraper.comments:
        f.write(f"{name}: {text} - {link}\n")
```

### Picking a random comment

Here is a simple way to pick a random comment from the list of all scraper comments, using
[Python's random library](https://docs.python.org/3/library/random.html).

```python
import random

random_comment = random.choice(scraper.comments)
```
