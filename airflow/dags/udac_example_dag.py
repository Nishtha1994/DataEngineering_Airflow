from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,DataQualityOperator)
from helpers import SqlQueries
from airflow.operators.postgres_operator import PostgresOperator
from airflow.contrib.operators.ssh_operator import SSHOperator



default_args = {
    'owner': 'nishtha',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stream_data = SSHOperator(
    task_id="stream_data",
    command='cd /home/workspace;python main.py;',
    dag=dag)



create_tables_task = PostgresOperator(
  task_id="create_tables",
  dag=dag,
  sql='create_tables.sql',
  postgres_conn_id="redshift"
)

stage_topics_to_redshift = StageToRedshiftOperator(
   task_id='Stage_topics',
   dag=dag,
   redshift_conn_id="redshift",
   table="staging_topics",
   s3_bucket="reddit-stream",
   s3_key="topics",
   aws_credentials_id="aws_credentials",
   json_path="auto"
)


stage_comments_to_redshift = StageToRedshiftOperator(
    task_id='Stage_comments',
    dag=dag,
    redshift_conn_id="redshift",
    table="staging_comments",
    s3_bucket="reddit-stream",
    s3_key="comments",
    aws_credentials_id="aws_credentials",
    json_path="auto"
)

load_trending_table = LoadFactOperator(
    task_id='Load_trending_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="trending",
    create_sql_stmt=SqlQueries.trending_insert,
    aws_credentials_id="aws_credentials",
    append_data="True"
)

load_subreddit_info_table = LoadFactOperator(
    task_id='Load_subreddit_info_table',
    dag=dag,
    redshift_conn_id="redshift",
    table="subreddit_info",
    create_sql_stmt=SqlQueries.subreddit_info_insert,
    aws_credentials_id="aws_credentials",
    append_data="True"
)


run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> stream_data
stream_data >>  create_tables_task
create_tables_task >> stage_topics_to_redshift
stage_topics_to_redshift >> stage_comments_to_redshift
stage_comments_to_redshift >> load_trending_table
load_trending_table >> load_subreddit_info_table
load_subreddit_info_table  >> run_quality_checks
run_quality_checks >> end_operator