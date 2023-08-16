from airflow import DAG
from airflow.providers.jenkins.hooks.jenkins import JenkinsHook
from airflow.operators.python_operator import PythonOperator
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

def trigger_jenkins_job(**kwargs):
    jenkins_hook = JenkinsHook(jenkins_conn_id='jenkins_conn')
    server = jenkins_hook.get_jenkins_server()

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

# Set up task dependencies if needed
# Example: trigger_jenkins_task >> other_task

# It's not needed to call 'trigger_jenkins_task' separately at the end
