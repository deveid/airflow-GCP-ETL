import pendulum
from airflow import DAG
from airflow.utils import timezone
from airflow.operators.dummy_operator import DummyOperator
from datetime import timedelta,datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

local_tz=pendulum.timezone("America/Halifax")

def greet(ti):
    name=ti.xcom_pull(task_ids='python_task_2',key='name')
    dir=ti.xcom_pull(task_ids='bash_dir')
    print(f"hELLO {name}")
    print(dir)

def get_name(ti):
    ti.xcom_push(key='name',value='Layo')


default_args={
    'start_date':datetime(2022,9,9,18,44,0,0,tzinfo=local_tz),
    'owner':'Dave',
    'retries':2,
    'retry_delay':timedelta(minutes=1),
    'email_on_failure':True,
}

with DAG (
    dag_id='first_py_dag',
    description='Python Operator dag to come to life',
    default_args=default_args,
    schedule_interval='@daily'
) as py_dag:

    task1=PythonOperator(
        task_id='python_task_1',
        python_callable=greet,
        op_kwargs={'name':'Bayo'}
    )

    task2=PythonOperator(
        task_id='python_task_2',
        python_callable=get_name
    )

    task3=BashOperator(
        task_id='bash_dir',
        bash_command='cd ~/Documents && ls',
        do_xcom_push=True
    )

    [task2,task3] >> task1