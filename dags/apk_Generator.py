from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 8, 16),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

dag = DAG(
    'apk_Generator',
    schedule_interval=None,
    default_args=default_args,
    catchup=False,
)

t1 = PythonOperator(
    task_id='parsing',
    python_callable=parseYaml,
    dag=dag,
)
