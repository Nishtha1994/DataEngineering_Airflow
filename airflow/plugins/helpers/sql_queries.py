class SqlQueries:
    trending_insert = ("""SELECT topics.type,topics.title,topics.url,topics.created,comments.comment_body,comments.subreddit
            from staging_topics AS topics join staging_comments AS comments 
            on (topics.id = comments.comment_parent_id)
            AND (topics.subreddit = comments.subreddit)
            """)
    subreddit_info_insert=("""
           SELECT subreddit,over_18,subreddit_type,subreddit_subscribers 
            from staging_topics
            """)
