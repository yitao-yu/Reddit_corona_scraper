#!/usr/bin/env python
# coding: utf-8

# In[28]:


import time
import praw
from datetime import datetime
import threading
import pandas as pd


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


# In[25]:


def submissionsupdate(subreddits,submissions):#called at the end of the day#
    for submission in submissions:
        post = reddit.submission(id=submission.Pid)
        submission.upvote_count = post.score
        submission.commentforrest = post.comments
        for comment in submission.commentforrest:
            submission.comment.append(Comment(comment.body, comment.id))
    print("update_done!")
    return submissions


# In[14]:


def hot(subreddits,hots):
    for sub in subreddits:
        hotposts = sub.hot(limit = 50)
        for submission in hotposts:
            dt = datetime.utcfromtimestamp(submission.created_utc)
            post = Post(submission.subreddit.title, submission.title, dt, submission.id)
            post.upvote_count = submission.score
            hots.append(post)
        print(sub.title+" done!")
    return hots, datetime.utcnow()


# In[48]:


def csvwriter(submissions,hots):
    stream_dic = {"subreddit":[],
                  "Pid":[],
                  "title":[],
                  "upvote":[],
                  "date":[]}
    comment_dic = {"Cid":[],
                   "Pid":[],
                   "body":[]}
    hot_dic = {"subreddit":[],
               "Pid":[],
               "title":[],
               "upvote":[],
               "date":[]}
    for post in submissions:
        stream_dic["subreddit"].append(post.subreddit)
        stream_dic["Pid"].append(post.Pid)
        stream_dic["title"].append(post.title)
        stream_dic["upvote"].append(post.upvote_count)
        stream_dic["date"].append(post.created_time)
        for comment in post.comment:
            comment_dic["Cid"].append(comment.Cid)
            comment_dic["Pid"].append(post.Pid)
            comment_dic["body"].append(comment.body)
    for post in hots:
        hot_dic["subreddit"].append(post.subreddit)
        hot_dic["Pid"].append(post.Pid)
        hot_dic["title"].append(post.title)
        hot_dic["upvote"].append(post.upvote_count)
        hot_dic["date"].append(post.created_time)
    dt = str(datetime.utcnow()).split(" ")[0]
    df_stream = pd.DataFrame(stream_dic)
    df_comment = pd.DataFrame(comment_dic)
    df_hot = pd.DataFrame(hot_dic)
    df_stream.to_csv(str('stream'+dt+'.csv'))
    df_comment.to_csv(str('comment'+dt+'.csv'))
    df_hot.to_csv(str('hot'+dt+'.csv'))


# In[15]:


subreddits = [reddit.subreddit('CoronavirusUS'),reddit.subreddit('CoronavirusUK'),reddit.subreddit('CoronavirusNewYork'),reddit.subreddit('CoronavirusCA'),reddit.subreddit('CoronavirusMichigan')]


# In[16]:


submissions = []
hots = []


# In[22]:


submissionstream(subreddits,submissions)


# In[24]:


submissionsupdate(subreddits,submissions)


# In[26]:


hot(subreddits,hots)


# In[49]:


csvwriter(submissions,hots)


# In[ ]:




