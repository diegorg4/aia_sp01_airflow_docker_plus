from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.exceptions import AirflowException

from pathlib import Path
from datetime import datetime

PARENT_PATH_NAME = str(Path(__file__).parent.parent)

class HttpSensor(BaseSensorOperator):
    def __init__(self, http_conn_id, file="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_conn_id = http_conn_id
        self.file = file

    def poke(self, context):
        hook = HttpHook(http_conn_id=self.http_conn_id, method='GET')
        response = hook.run(f'assignment-python-1:8000/api/v1/{self.file}')
        print(response.text)
        self.executed = True
        if response.status_code == 200:
            return True
        raise AirflowException(f"Test validation did not met the requirements: /api/v1/{self.file}")

with DAG (dag_id="validate_test_results",
          description="Validate the test results of extract and transform.py files",
          start_date=datetime(2023,4,14),
          schedule_interval="@once"
          ) as dag:
            
    task_validate_extract = HttpSensor(
            file="test-extract",
            task_id='t_http_validate_extract',
            http_conn_id='http_default',
            dag=dag)
    
    task_validate_transform = HttpSensor(
            file="test-transform",
            task_id='t_http_validate_transform',
            http_conn_id='http_default',
            dag=dag)
    
    end_task = BashOperator(task_id="bash_task",
                         bash_command="echo EVERYTHING OK!")

    task_validate_extract >> task_validate_transform >> end_task