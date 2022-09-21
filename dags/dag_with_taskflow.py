import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta,datetime
from airflow.operators.python import PythonOperator
from airflow.decorators import dag,task

local_tz=pendulum.timezone("America/Halifax")

default_args={
    'start_date':datetime(2022,9,9,18,44,0,0,tzinfo=local_tz),
    'owner':'Dave',
    'retries':2,
    'retry_delay':timedelta(minutes=1),
    'email_on_failure':True,
}

@dag(
    dag_id='first_task_mode_dag',
    description='Task  dag to come to life',
    default_args=default_args,
    schedule_interval='@daily'
)

def simple_etl():

    @task()
    def name():
        return 'Layo'
    @task()
    def age():
        return 10

    @task()
    def greet(name,age):
        print(f"My name is {name},I'm {age}")

    name=name()
    age=age()
    greet(name=name,age=age)
greet_dag=simple_etl()