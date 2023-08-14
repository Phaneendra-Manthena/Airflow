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

jenkins_server_url = 'http://34.16.152.234:8080'  # Replace with your Jenkins server URL
jenkins_username = 'Phani'
jenkins_password = 'mjrr'
job_name = 'gradle'
crumb = 'fa017a59c1c5b739c282fae1d5f674c587407a7fb471f98d73a6714de2ddce1d'  # Replace with your crumb

trigger_jenkins_task = BashOperator(
    task_id='trigger_jenkins_task',
    bash_command=f'curl -X POST -u {jenkins_username}:{jenkins_password} -H "Jenkins-Crumb: {crumb}" {jenkins_server_url}/job/{job_name}/build',
    dag=dag,
)

trigger_jenkins_task


#
# curl -s 'http://34.16.152.234:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'
#
#
# wget -q --auth-no-challenge --user Phani --password mjrr --output-document - 'http://34.16.152.234:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'