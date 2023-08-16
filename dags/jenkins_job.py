from airflow import DAG
from airflow.models import Connection
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import jenkins

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

def trigger_jenkins_job(**kwargs):
    jenkins_conn = Connection.get_connection_from_secrets('jenkins_conn')

    server = jenkins.Jenkins(
        jenkins_conn.host,
        username=jenkins_conn.login,
        password=jenkins_conn.password
    )

    # Replace 'gradle' with your actual Jenkins job name
    job_name = 'gradle'

    # Trigger the Jenkins job
    server.build_job(job_name, parameters={'param1': 'value1', 'param2': 'value2'})

trigger_jenkins_task = PythonOperator(
    task_id='trigger_jenkins_task',
    python_callable=trigger_jenkins_job,
    provide_context=True,
    dag=dag,
)
