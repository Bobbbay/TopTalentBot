import praw
import os

sub = "BobbbayBots"

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
password = os.environ.get('pass')

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent='r/TopTalent bot',
                     username='TheTalentedBot')

# Scan through all flairs and delete them
reddit.subreddit(sub).flair.delete_all()