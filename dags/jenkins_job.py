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
    'curl -I -X POST http://Phani:11bcabf573419a1b38f178b9de116c0f4d@34.16.152.234:8080/job/gradle/build '
    '-H "Jenkins-Crumb:fa017a59c1c5b739c282fae1d5f674c587407a7fb471f98d73a6714de2ddce1d"'
)

trigger_jenkins_task = BashOperator(
    task_id='trigger_jenkins_task',
    bash_command=jenkins_command,
    dag=dag,
)

trigger_jenkins_task
