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

jenkins_server_url = '34.16.152.234:8080'  # Replace with your Jenkins server URL
jenkins_username = 'Phani'
jenkins_password = 'mjrr'
job_name = 'gradle'

trigger_jenkins_task = BashOperator(
    task_id='trigger_jenkins_task',
    bash_command=f'curl -X POST -u {jenkins_username}:{jenkins_password} {jenkins_server_url}/job/{job_name}/build',
    dag=dag,
)

trigger_jenkins_task


# curl -X POST http://34.16.152.234:8080/job/gradle/build --user Phani:mjrr -H 'Jenkins-Crumb: 6b3a16e39caa9388642c5c5c309aa6215ce272ed590e4a6cc8d221e9e77b6f05'
#
#
#
# curl -v -X POST http://34.16.152.234:8080/job/gradle/buildWithParameters?param=value --user Phani:117084d48630cc0d6245f985b4bc711864