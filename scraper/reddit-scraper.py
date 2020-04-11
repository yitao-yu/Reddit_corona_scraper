#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import praw
from datetime import datetime
import threading


# In[2]:


reddit = praw.Reddit(client_id='P26uUpjfnflDVg', client_secret="L9oHqikaIVKSm-aXv-a7E-x8Yi8",
                     password='password', user_agent='script by /u/CandlesTaken',
                     username='username')


# In[3]:


class Post:
    commentforrest = reddit.submission('3hahrw').comments
    comment = []
    upvote_count = 0
    def __init__(self, subreddit, title, created_time,Pid):
        self.subreddit = subreddit
        self.title = title
        self.created_time = created_time
        self.Pid = Pid


# In[4]:


class Comment:
    def __init__(self, body,Cid):
        self.Cid = Cid
        self.body = body


# In[12]:


def submissionstream(subreddits,submissions):#stream#
    string = str("")
    for i in range(0,len(subreddits)):
        if (i != 0):
            string += "+"+str(subreddits[i].title)
        else:
            string += str(subreddits[i].title)
    for submission in reddit.subreddit(string).stream.submissions():
        print(str(submission.subreddit.title) + "; " + submission.title+"; "+str(datetime.utcfromtimestamp(submission.created_utc))+";"+str(submission.score))
        dt = datetime.utcfromtimestamp(submission.created_utc)
        post = Post(submission.subreddit.title, submission.title, dt, submission.id)
        submissions.append(post)
    return submissions


# In[13]:


def submissionsupdate(subreddits,submissions):#called at the end of the day#
    for submission in submissions:
        post = reddit.submission(id=submission.Pid)
        submission.upvote_count = post.score
        submission.commentforrest = post.comments
        for comment in submission.commentforrest:
            submission.comment.append(Comment(comment.body, comment.id))
        print("update_done!")
    return comments


# In[14]:


def hot(subreddits,hots):
    print("doing hots!")
    for sub in subreddits:
        hotposts = sub.hot(limit = 50)
        for submission in hotposts:
            print(str(submission.subreddit.title) + "; " + submission.title+"; "+str(datetime.utcfromtimestamp(submission.created_utc))+";"+str(submission.score))
            dt = datetime.utcfromtimestamp(submission.created_utc)
            post = Post(submission.subreddit.title, submission.title, dt, submission.id)
            post.upvote_count = submission.score
            hots.append(post)
    return hots, datetime.utcnow()


# In[15]:


subreddits = [reddit.subreddit('CoronavirusUS'),reddit.subreddit('CoronavirusUK'),reddit.subreddit('CoronavirusNewYork'),reddit.subreddit('CoronavirusCA'),reddit.subreddit('CoronavirusMichigan')]


# In[16]:


submissions = []
hots = []


# In[ ]:


submissionstream(subreddits,submissions)


# In[ ]:


submissionsupdate(subreddits,submissions)


# In[ ]:


hot(subreddits,hots)


# In[19]:


def csvwriter(submissions,hots):
    pass

def csvhelper(file):
    pass


# In[ ]:




