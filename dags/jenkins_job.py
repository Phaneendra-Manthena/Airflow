from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 8, 14),
    'retries': 1,
}

dag = DAG(
    'trigger_jenkins_dag',
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
)

jenkins_command = (
    'curl -I -X POST http://Phani:11bcabf573419a1b38f178b9de116c0f4d@34.125.61.238:8080/job/gradle/build -H "Jenkins-Crumb:338fbe4952e517ed1ad3ff4780c17db66231022bdcae929d7532d5e9b3a7a19e"'
)

trigger_jenkins_task = BashOperator(
    task_id='trigger_jenkins_task',
    bash_command=jenkins_command,
    dag=dag,
)

trigger_jenkins_task
