import praw
import madlibs
import random
import time
import doctest


def get_topic_comments(submission):
    ''' (submission) -> list
    Extracts all the comments from submission and returns all comments as a list.
    '''
    submission.comments.replace_more(limit=None) #Get all of the comments from the submission
    return submission.comments.list() #Return all of the comments in the submission as a list



def filter_comments_from_authors(comments_list, author_names):
    '''(list, list) -> list
    Returns a list of comments with only replies from authors in author_names.
    '''
    author_comments = []
    
    for comment in comments_list: #Iterate through each comment in the list of comments
        if str(comment.author) in author_names: #If the name of the author is found in the list of author_names, append that comment to a special list
            author_comments.append(comment)
    
    return author_comments #Return the list that has all the comments from authors in author_names



def filter_out_comments_replied_to_by_authors(comments_list, author_names):
    '''(list, list) -> list
    Returns the original list of comments without comments that have replies from authors in author_names.
    '''
    author_comments = filter_comments_from_authors(comments_list, author_names)
    #Filter out all of the specified author's comments from comments_list and add to another list
    
    for comment in comments_list[:]: #Iterate through all the comments and remove all the comments written by the author
        if comment in author_comments:
            comments_list.remove(comment)
    
    author_replies = []
    
    for comment in comments_list: #Iterate through each comment and load the replies of that specific comment into a list
        comment_replies = comment.replies.list()
        
        for reply in comment_replies: #Iterate through each reply and if the author of that reply is in author_names, append the comment to author_replies
            if reply.author in author_names:
                author_replies.append(comment)
                break
    
    for comment in comments_list[:]: #Iterate through all the comments and remove comments that the author has replied to
        if comment in author_replies:
            comments_list.remove(comment)

    return comments_list



def get_authors_from_topic(submission):
    ''' (submission) -> dict
    Returns a dictionary that has each author's comment count as a key-value pair.
    '''
    number_comments = {} #Create a dictionary that will eventually have each author's name and the number of comments they have submitted
    all_comments = get_topic_comments(submission) #Load all comments from the submission into a list and save it into a variable
    
    for comment in all_comments: #Iterate through all the comments in the list
        if comment.author == None: #If the comment has been deleted, move onto the next comment
            continue
        if comment.author.name not in number_comments: #If the author of the comment is not yet in the dictionary, add the author as a key to the dictionary
            number_comments[comment.author.name] = 1
        else: #If the author of the comment is in the dictionary, add one to the value of the author's key
            number_comments[comment.author.name] += 1
    
    return number_comments



def select_random_submission_url(reddit, url, subreddit, replace_limit):
    ''' (reddit, str, str, int) -> submission
    Rolls a dice to determine which submission object to return.
    '''
    random_number = random.randint(1,6) #Generate a random number between 1 and 6 
    hot_submission = []
    
    if random_number in [1,2]: #If the random number is 1 or 2, load the comments from the specified submission url
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=replace_limit)
        
        return submission
    
    else: #If the random number is not 1 or 2, choose a random submission from the subreddit and return the object
        for submission in reddit.subreddit(subreddit).top(limit=None): #Iterate through all the top submissions in the subreddit
            hot_submission.append(submission) #Make a list with all of the top submissions
        random_submission = random.randint(0,len(hot_submission)-1) #Choose a top submission at random to return 
        
        return hot_submission[random_submission]



def post_reply(submission, username):
    ''' (submission, str) -> None
    Posts a comment or reply with the madlib sentence generated from the madlibs module to a specified submission under the username.
    '''
    comments_list = get_topic_comments(submission) #Get all the comments in the submission in a list
    madlib_comment = madlibs.generate_comment() #Generate a madlibs string from the madlibs module
    author_comments = filter_comments_from_authors(comments_list, username) #Create a list with only the author's comments
    
    if len(author_comments) == 0: #If there are no comments from the author, reply to the submission with the madlibs string
        submission.reply(madlib_comment)
    
    else: #If there are comments from the author
        for comment in comments_list: #Iterate through all the comments in the submission
            if comment.author == None: #If the comment is deleted, move onto the next comment
                continue
            
            elif comment.author.name == username: #If the author has written a comment
                comments_list = filter_out_comments_replied_to_by_authors(comments_list, [username]) #Filter out all the comments the author has replied to
                random_number = random.randint(0,len(comments_list)-1)
                reply_comment = comments_list[random_number] #Choose a random comment that the author has not replied to
                reply_comment.reply(madlib_comment) #Reply to the random comment with the madlibs string



def bot_daemon(reddit, url, replace_limit, subreddit, username):
    ''' (reddit, str, int, str, str) -> None
    Chooses a random submission in the subreddit to post a comment or reply, and repeats the action an infinite amount of times in 60 second intervals.
    '''
    while True:
        submission = select_random_submission_url(reddit, url, subreddit, replace_limit) #Select a submission from the subreddit
        post_reply(submission, username) #Post either a comment or reply to the submission with the madlibs string
        time.sleep(60) #Pause for 60 seconds before looping the code again
            


if __name__ == "__main__":
    reddit = praw.Reddit("bot", config_interpolation = "basic") #Creates a reddit object
    doctest.testmod()
    
'''
url = "https://www.reddit.com/r/csssmu/comments/te5jw8/dee_buhger_appreciation_post/"
username = "gerkingbot"
replace_limit = None
subreddit = "csssmu"
bot_daemon(reddit, url, replace_limit, subreddit, username)
'''
