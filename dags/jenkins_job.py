from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG(
    dag_id="jenkins_dag",
    schedule_interval="@daily",
    start_date=datetime(2023, 8, 14),  # Define an appropriate start date
)

start_jenkins = BashOperator(
    task_id="start_jenkins",
    bash_command="/usr/bin/sudo systemctl start jenkins",
    dag=dag,
)
