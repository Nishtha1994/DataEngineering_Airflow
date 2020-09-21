CREATE TABLE IF NOT EXISTS staging_topics(type varchar(1000),title varchar(15000),score int,id varchar(1000),url varchar(1000),comms_num int,created bigint,subreddit varchar(1000),body varchar(15000),is_video varchar(1000), over_18 varchar(1000), self_text varchar(1000), shortlink varchar(1000),subreddit_type varchar(1000),subreddit_subscribers varchar(1000),ups int,timestamp bigint);

CREATE TABLE IF NOT EXISTS staging_comments(comment_id varchar(1000),comment_parent_id varchar(1000),comment_body varchar(15000), comment_link_id varchar(1000),subreddit varchar(1000));

CREATE TABLE IF NOT EXISTS trending(type varchar(1000),title varchar(15000),url varchar(1000),created bigint,comment_body varchar(15000),subreddit varchar(1000);

CREATE TABLE IF NOT EXISTS subreddit_info(subreddit varchar(1000),over_18 varchar(1000),subreddit_type varchar(1000),subreddit_subscribers varchar(1000);



