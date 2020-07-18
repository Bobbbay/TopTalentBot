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

# TODO:
# * Except only relevant exceptions
# * Consult about increased functionality

moderators = list(reddit.subreddit(sub).moderator())
for submission in reddit.subreddit(sub).new(limit=None):
    print(submission.title)

    # To become a list of !toptalent ratings
    l = []

    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():
        # Find the status comment made by the bot
        if (comment.author == "TheTalentedBot"):
            status = comment.id

        # Criteria: !toptalent, not the submitter or a moderator
        if ((("!toptalent" in comment.body)) and ((not comment.is_submitter) or (comment.author in moderators))):

            # I forget what this does to be honest
            i = []
            for t in comment.body.split():
                try:
                    i.append(float(t))
                except ValueError:
                    pass
            l.append(i[0])

    # Try averaging, if it divides over 0 then nobody
    # has posted, so set the average to 0
    try:
        average = round( sum(l) / len(l) )
    except:
        average = 0

    # Grab the flair of OP, add this post and get the 
    # average number, if there is nothing to grab
    # originally, set a new flair.
    try:
        count_op_str = submission.author_flair_text
        count_op = round(float(count_op_str.replace("ᚬ", "")))
        count_op = (count_op + average) / 2
        op_flair = "{0}ᚬ".format(count_op)
        reddit.subreddit(sub).flair.set(submission.author.name, op_flair, "Talent Points")
    except:
        reddit.subreddit(sub).flair.set(submission.author.name, "{0}ᚬ".format(average), "Talent Points")
    
    #! WIP
    talentLevel = ""

    if (average < 4):
        talentLevel = "That's some Mediocre Talent!"
    elif (average < 6):
        talentLevel = "That's some Average Talent!"
    elif (average < 8):
        talentLevel = "That's some Rising Talent!"
    elif (average < 9):
        talentLevel = "That's some Amazing Talent!"
    elif (average < 10):
        talentLevel = "That's some LEGENDARY Talent!"

    #! END OF WIP

    reply = "{0} You've got an average of **{1}**. \n\n ^Beep ^Boop".format(talentLevel, average)

    # If the submission is not saved, then the bot has
    # not yet commented the status. If it is saved,
    # edit the original comment.
    if submission.saved is False:
        submission.reply(reply).mod.distinguish(sticky=True)
        submission.save()
    else:
        reddit.comment(status).edit(reply).mod.distinguish(sticky=True)
