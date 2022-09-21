import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta,datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
#from airflow.operators.postgres_operator import PostgresOperator
#from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

local_tz=pendulum.timezone("America/Halifax")

default_args={
    'start_date':datetime(2022,9,9,18,44,0,0,tzinfo=local_tz),
    'owner':'Dave',
    'retries':2,
    'retry_delay':timedelta(minutes=1),
    'email_on_failure':True,
}

with DAG (
    dag_id='postgres_dag',
    description='Postgres Operator dag to come to life',
    default_args=default_args,
    schedule_interval='@daily'
) as dag:
    task1=PostgresOperator(
        task_id='postgres_table_creation',
        postgres_conn_id=''
    )
