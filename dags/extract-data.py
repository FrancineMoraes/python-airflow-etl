import airflow
from tasks import etl_tasks
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Define default arguments
args = {
    'owner': 'Francine Moraes',
    'start_date': airflow.utils.dates.days_ago(1)
}

# Define a new Dag using default arguments
dag = DAG(
    dag_id='extract_data',
    default_args=args,
    schedule_interval=None
)

with dag:

    extract_data = PythonOperator(
        task_id='extract_data_from_files',
        python_callable=etl_tasks.read_and_store_files,
        provide_context=True,
        dag=dag
    )