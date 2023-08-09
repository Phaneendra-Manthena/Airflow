from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator

from datacleaner import data_cleaner

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

default_args = {
    'owner': 'Airflow',
    'start_date': datetime(2023, 8, 8),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('store_dag', default_args=default_args, schedule_interval='@daily', template_searchpath=['/usr/local/airflow/sql_files'], catchup=True) as dag:

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

    t3 = MySqlOperator(
        task_id='create_mysql_table',
        mysql_conn_id="mysql_conn",
        sql="create_table.sql",
        dag=dag
    )

    t4 = MySqlOperator(
        task_id='insert_into_table',
        mysql_conn_id="mysql_conn",
        sql="insert_into_table.sql",
        dag=dag
    )

    t5 = MySqlOperator(
        task_id='select_from_table',
        mysql_conn_id="mysql_conn",
        sql="select_from_table.sql",
        dag=dag
    )

    # Delete existing files before running the task
    delete_files = BashOperator(
        task_id='delete_existing_files',
        bash_command='rm -f /store_files_mysql/location_wise_profit.csv /store_files_mysql/store_wise_profit.csv',
        dag=dag
    )

    t6 = BashOperator(
        task_id='move_file1',
        bash_command='cat ~/store_files_airflow/location_wise_profit.csv && mv ~/store_files_airflow/location_wise_profit.csv ~/store_files_airflow/location_wise_profit_%s.csv' % yesterday_date,
        dag=dag
    )
    t7 = BashOperator(
        task_id='move_file2',
        bash_command='cat ~/store_files_airflow/store_wise_profit.csv && mv ~/store_files_airflow/store_wise_profit.csv ~/store_files_airflow/store_wise_profit_%s.csv' % yesterday_date,
        dag=dag
    )

    t1 >> t2 >> t3 >> t4 >> t5 >> delete_files >> [t6, t7]
