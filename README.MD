## Context

2019 Novel Coronavirus (2019-nCoV) is a virus (more specifically, a coronavirus) identified as the cause of an outbreak of respiratory illness first detected in Wuhan, China. This project revolves around collection of recent discussions
on a popular social media application called Reddit.

## Scope of the Project

We have used the PRAW API for data mining on popular Coronavirus subreddits. Each subreddit has a post which can be classified under top, rising, new or hot. These datasets are inclusive of each other. These posts will be further divided
into comments. Comments can be tier1, tier2, tier3. Data is stored in the `data/topics` and `data/comments` folder and is triggered systematically using a CRON job. The task can be scheduled using AWS Lambda as well.
Estimated 10000+ comments and topics data can be covered in one run.

![alt text](https://github.com/Nishtha1994/DataEngineering_Airflow/blob/master/RedshiftTables.png?raw=true)

## Data Exploration and Cleaning

Initially, the idea was formulated to use csv instead of json. However, loading into redshift created many issues related to multiple commas in the body structure. Switching to json created the data in distributed manner which would be solved by
using `default_handles` and `orient options`. 
The comment has an associated parent id and is prefixed with tier1,tier2 or tier3 options. We have used a `lambda` function to extract the parent i without the tier so that we can insert in our main table with clear joins.


## Column Description

There are two staging tables from where we are moving the data to the facts table. We can run insightful queries on the facts table to retrieve relevant information.

staging_topics:

type- if the topic is hot or new
title- title of the topic
score- score of the topic
id- unique id
url- url associated
created - timestamp when the topic was created
subreddit- name of subreddit
body- whats defined in the post
is_video- if the topic has video in it
over_18- if parental guidance is required
subreddit_subscribers- how many subscribers the subrreddit has

staging_comments:

comment_id - unique identifier for the comment
comment_parent_id- comment associated with the topic
comment_body- what's definied in the comment
comment_link_id- url associated with the comment
subreddit- type of subreddit

## Project Flow

![alt text](https://github.com/Nishtha1994/DataEngineering_Airflow/blob/master/FlowDiagram.png?raw=true)

## Testing
```bash
select * from staging_topics LIMIT 5;
select * from staging_comments LIMIT 5;
select * from trending LIMIT 5;
select * from subreddit_info LIMIT 5;
```

## Project Run

You can use the following command to access the Airflow UI: `/opt/airflow/start.sh`. You can set the trigger time by editing the time sequence according to your convenience.
![alt text](https://github.com/Nishtha1994/DataEngineering_Airflow/blob/master/Airflow%20Architecture.PNG?raw=true)

## Future Considerations

We can clear interface with run of each steps can be easily identified.This architecture can easily support large amounts of new data, scheduling tasks to 
run regularly, and involving other team members. Team members can be added with the help of IAM roles. We can use SparkSQL to clean and quantify large amounts of data at once.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
Nishtha Bhattacharjee(nishthabhattacharjee94@gmail.com)


