from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator

from datacleaner import data_cleaner

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 8, 8),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('store_dag',default_args=default_args,schedule_interval='@daily', template_searchpath=['/usr/local/airflow/sql_files'], catchup=True)

t1 = BashOperator(
    task_id='check_file_exists',
    bash_command='shasum ~/store_files_airflow/raw_store_transactions.csv',
    retries=2,
    retry_delay=timedelta(seconds=15),
    dag=dag
)

def clean_data():
    # Call your data cleaning function here
    data_cleaner()

t2 = PythonOperator(
    task_id='clean_raw_csv',
    python_callable=clean_data,  # Call the function you defined
    dag=dag
)

# t3 = MySqlOperator(
#     task_id='Create_mysql_table',
#     mysql_conn_id="mysql_conn",
#     sql="create_table.sql"
# )
t3 = MySqlOperator(task_id='create_mysql_table', mysql_conn_id="mysql_conn", sql="create_table.sql")
t1 >> t2 >> t3
