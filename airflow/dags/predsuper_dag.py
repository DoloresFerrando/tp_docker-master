# Cronguru: https://crontab.guru/between-certain-hours
from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
# Email when fail: https://stackoverflow.com/questions/51726248/airflow-dag-customized-email-on-any-of-the-task-failure
#from airflow.operators.email_operator import EmailOperator
#from airflow.utils.trigger_rule import TriggerRule

from super import proceso

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'super',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email': ['doloresferrando@gmail.com'],
    'email_on_failure': False, # to send an e-mail after task fail, you should config SMTP in airflow.cfg and set this to True
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

# define the python function

def get_hourly_demand(**kwargs):
    database = Variable.get("ENERGY_DB")
    host = Variable.get("ENERGY_DB_HOST")
    user = Variable.get("ENERGY_DB_USER")
    password = Variable.get("ENERGY_DB_PASS")
    port = Variable.get("ENERGY_DB_PORT")
    process_ok = _get_hourly_demand(date=kwargs['execution_date'], database=database, host=host
                    , user=user, password=password, port=port, verbose=True)
    print('INFO get_hourly_demand execution: ', kwargs['execution_date'])
    if not process_ok:
        raise ValueError()
    return

def calculate_hourly_demand_forecast(**kwargs):
    database = Variable.get("ENERGY_DB")
    host = Variable.get("ENERGY_DB_HOST")
    user = Variable.get("ENERGY_DB_USER")
    password = Variable.get("ENERGY_DB_PASS")
    port = Variable.get("ENERGY_DB_PORT")
    print('INFO calculate_hourly_demand_forecast execution init: ', kwargs['execution_date'])
    process_ok, error_txt = _calculate_hourly_demand_forecast(database=database, host=host, user=user, password=password
                                                              , port=port, n_lookback=48, n_forecast=24, verbose=True)
    if not process_ok:
        print('ERROR calculate_hourly_demand_forecast. ' + error_txt)
        raise ValueError()
    return

# define the DAG
dag = DAG(
    'superforecast_v1',
    default_args=default_args,
    description='Compras en supermercados a precios constantes. Mensual. Pronostico del proximo mes',
    # Having the schedule_interval as None means Airflow will never automatically schedule a run of the Dag.
    # you can schedule it manually via the trigger button in the Web UI
    #schedule_interval=None
    schedule_interval='@monthly' 
)

# define tasks
t1 = PythonOperator(
    task_id='proceso',
    python_callable= proceso,
    provide_context=True,
    dag=dag,
)



t1 