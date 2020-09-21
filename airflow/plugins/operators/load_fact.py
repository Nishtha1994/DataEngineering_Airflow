from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'
   
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 create_sql_stmt="",
                 aws_credentials_id="",
                 append_data="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.create_sql_stmt=create_sql_stmt
        self.aws_credentials_id = aws_credentials_id
        self.append_data=append_data
        
        # Map params here
        # Example:
        # self.conn_id = conn_id

    def execute(self, context):
        self.log.info('Executing: and loading facts table')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if self.append_data == True:
            sql_statement = 'INSERT INTO %s %s' % (self.table_name, self.create_sql_stmt)
            redshift.run(sql_statement)
        else:
            sql_statement = 'DELETE FROM %s' % self.table_name
            redshift.run(sql_statement)
            sql_statement = 'INSERT INTO %s %s' % (self.table_name, self.create_sql_stmt)
            redshift.run(sql_statement)

        
