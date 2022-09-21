import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta,datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.bigquery_check_operator import BigQueryCheckOperator


local_tz=pendulum.timezone("America/Halifax")
#Config Variables
BQ_PROJECT="quick-keel-213611"
BQ_DATASET="gc_dataset"
default_args={
    'start_date':datetime(2022,9,9,18,44,0,0,tzinfo=local_tz),
    'owner':'Dave',
    'retries':2,
    'retry_delay':timedelta(minutes=1),
    'email_on_failure':True,
}

with DAG (
    dag_id='bigquery_dag',
    description='BigQuery Operator dag to come to life',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:

    task1=BigQueryCheckOperator(
        task_id='check_query_big_query_table',
        bigquery_conn_id='gcp_conn',
        use_legacy_sql=False,
        sql="""
           select id from githubarchive.day.20220914
        """
    )
    task2=BigQueryOperator(
        task_id='query_big_query_table',
        bigquery_conn_id='gcp_conn',
        use_legacy_sql=False,
        sql="""
           select id from githubarchive.day.20220914
        """
    )
    task3=BigQueryOperator(
        task_id='write_query_big_query_table',
        bigquery_conn_id='gcp_conn',
        use_legacy_sql=False,
        sql="""
        select * from githubarchive.day.20220914 where actor.id=66800817
            """,
        write_disposition='WRITE_TRUNCATE',
        allow_large_results=True,
        destination_dataset_table='{0}.{1}.66800817'.format(BQ_PROJECT,BQ_DATASET)

    )
    task1 >> [task2,task3]
