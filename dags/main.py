import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta,datetime
from airflow.operators.bash import BashOperator

local_tz=pendulum.timezone("America/Halifax")

default_args={
    'start_date':datetime(2022,9,9,17,50,0,0,tzinfo=local_tz),
    'owner':'RBC',
    'retries':2,
    'retry_delay':timedelta(minutes=1),
    'email_on_failure':True,
}

with DAG (
    dag_id='first_dag',
    description='First dag to come to life',
    default_args=default_args,
    schedule_interval='42 19 * * 1-5'
) as first_dag:

    task1=BashOperator(
    task_id='first_bash',
    bash_command="echo Tolu on this one"
    )

    task2=BashOperator(
        task_id='second_bash',
        bash_command='cd ~/airflow && ls'

    )
    task3=BashOperator(
        task_id='third_bash',
        bash_command='echo interesting'
    )
    task1 >>[task2,task3]