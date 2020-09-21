"""
Grab data, start with Reddit, as json blobs and store them in S3.
1. Connect to reddit
2. Grab json data
3. Store json in S3
"""
import datetime as dt
import praw
import boto3
import json
import pandas as pd
import time
import random
from config import SUBREDDITS
import boto
import os

def getVarFromFile(filename):
    import imp
    f = open(filename)
    global data
    data = imp.load_source('data', '', f)
    f.close()
getVarFromFile('dwh.cfg')
client = boto3.client(
    's3',
    aws_access_key_id=data.aws_access_key_id_value,
    aws_secret_access_key=data.aws_secret_access_key_value
)
client.create_bucket(Bucket=data.Bucket_value)
s3_resource = boto3.resource("s3", region_name="us-east-1")

def upload_objects():
    try:
        bucket_name = "nishtha-capstone" #s3 bucket name
        root_path = '/home/workspace/data/' # local folder for upload

        my_bucket = s3_resource.Bucket(bucket_name)

        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\","/")
            directory_name = path.replace(root_path,"")
            for file in files:
                my_bucket.upload_file(os.path.join(path, file), directory_name+'/'+file)

    except Exception as err:
        print(err)


def data_for_submissions(sub,submissions,type):
    now = dt.datetime.utcnow()
    formatted_date = now.strftime("%Y-%m-%d-%H-%M-%S")
    topics_dict = { "title":[],
                "score":[],
                "id":[],
                "url":[], 
                "comms_num": [],
                "created": [],
                "subreddit": [],
                "body":[],
                "is_video":[],
                "over_18":[],
               "selftext":[], 
                "shortlink": [],
                "subreddit_type": [],
                "subreddit_subscribers":[],
                "ups":[]
                  }
    comments_dict = {
            "comment_id" : [],      #unique comm id
            "comment_parent_id" : [],   # comment parent id
            "comment_body" : [],   # text in comment
            "comment_link_id" : [],  #link to the comment
            "subreddit": []
        }
    for submission in submissions:
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["subreddit"].append(submission.subreddit)
        topics_dict["body"].append(submission.title)
        topics_dict["is_video"].append(submission.is_video)
        topics_dict["over_18"].append(submission.over_18)
        topics_dict["selftext"].append(submission.selftext)
        topics_dict["shortlink"].append(submission.shortlink)
        topics_dict["subreddit_type"].append(submission.subreddit_type)
        topics_dict["subreddit_subscribers"].append(submission.subreddit_subscribers)
        topics_dict["ups"].append(submission.ups)
        
        submission.comments.replace_more(limit = 1)
        for comment in submission.comments.list():
                comments_dict["comment_id"].append(comment.id)
                comments_dict["comment_parent_id"].append(comment.parent_id)
                comments_dict["comment_body"].append(comment.body)
                comments_dict["comment_link_id"].append(comment.link_id) 
                comments_dict["subreddit"].append(str(comment.subreddit))
    
    topics_data = pd.DataFrame(topics_dict)
    comments_data=pd.DataFrame(comments_dict)
    comments_data['comment_parent_id']=comments_data['comment_parent_id'].map(lambda x: str(x)[3:])
    topics_data.insert(0, 'Type', type)
    def get_date(created):
        return dt.datetime.fromtimestamp(created)
    _timestamp = topics_data["created"].apply(get_date)
    topics_data = topics_data.assign(timestamp = _timestamp)
    print(topics_data)
    topics_data.to_json('/home/workspace/data/to00pics/'+sub+"_"+type+"_"+formatted_date+"_topics.json",default_handler=str,orient='records', lines=True)
    comments_data.to_json('/home/workspace/data/comments/'+sub+"_"+type+"_"+formatted_date+"_comments.json",default_handler=str, orient='records', lines=True)  
    

reddit = praw.Reddit(client_id='', \
                     client_secret='', \
                     user_agent='covid-data2', \
                     username='', \
                     password='')
idx = random.randint(0, len(SUBREDDITS)-1)
start = time.time()

for sub in SUBREDDITS:
    subreddit = reddit.subreddit(sub)
    type="hot"
    print("Pulling posts from {}, {}.".format(sub, "hot"))
    data_for_submissions(sub,subreddit.hot(),type)
    
    type="new"
    subreddit = reddit.subreddit(sub)
    print("Pulling posts from {}, {}.".format(sub, "new"))
    data_for_submissions(sub,subreddit.new(),type)
    
    type="top"
    subreddit = reddit.subreddit(sub)
    print("Pulling posts from {}, {}.".format(sub, "top"))
    data_for_submissions(sub,subreddit.top(),type)
    
    type="rising"
    subreddit = reddit.subreddit(sub)
    print("Pulling posts from {}, {}.".format(sub, "rising"))
    data_for_submissions(sub,subreddit.rising(),type)
    

if __name__ == '__main__':
    upload_objects()