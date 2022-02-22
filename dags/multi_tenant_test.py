"""An example for running multi-tenant workloads"""
import airflow
import datetime
from airflow import models
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import \
  KubernetesPodOperator

default_args = {
  'start_date': airflow.utils.dates.days_ago(0),
  'retries': 0,
}

# If you are running Airflow in more than one time zone
# see https://airflow.apache.org/docs/apache-airflow/stable/timezone.html
# for best practices
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

with models.DAG(
    dag_id='multi_tenant_test',
    schedule_interval=datetime.timedelta(days=1),
    start_date=YESTERDAY) as dag:
  # Only name, namespace, image, and task_id are required to create a
  # KubernetesPodOperator. In Cloud Composer, currently the operator defaults
  # to using the config file found at `/home/airflow/composer_kube_config if
  # no `config_file` parameter is specified. By default it will contain the
  # credentials for Cloud Composer's Google Kubernetes Engine cluster that is
  # created upon environment creation.

  auth_list = KubernetesPodOperator(
    # The ID specified for the task.
    task_id='gcloud-auth-list',
    # Name of task you want to run, used to generate Pod ID.
    name='gcloud-auth-list',
    # Entrypoint of the container, if not specified the Docker container's
    # entrypoint is used. The cmds parameter is templated.
    cmds=['gcloud'],
    arguments=['auth', 'list'],
    # The namespace to run within Kubernetes, default namespace is
    # `default`. There is the potential for the resource starvation of
    # Airflow workers and scheduler within the Cloud Composer environment,
    # the recommended solution is to increase the amount of nodes in order
    # to satisfy the computing requirements. Alternatively, launching pods
    # into a custom namespace will stop fighting over resources.
    namespace='test6',
    # Docker image specified. Defaults to hub.docker.com, but any fully
    # qualified URLs will point to a custom repository. Supports private
    # gcr.io images if the Composer Environment is under the same
    # project-id as the gcr.io images and the service account that Composer
    # uses has permission to access the Google Container Registry
    # (the default service account has permission)
    image='gcr.io/google.com/cloudsdktool/cloud-sdk:latest',
    service_account_name='test6-service-acct')

  bq_query = KubernetesPodOperator(
    # The ID specified for the task.
    task_id='bq-query',
    # Name of task you want to run, used to generate Pod ID.
    name='bq-query',
    # Entrypoint of the container, if not specified the Docker container's
    # entrypoint is used. The cmds parameter is templated.
    cmds=['bq'],
    arguments=[
      'query',
      '--nouse_legacy_sql',
      'CREATE OR REPLACE TABLE `danny-bq`.testing.tpcds_100T_store_sales AS SELECT * FROM bigquerybench.tpcds_100T.store_sales'
    ],
    # The namespace to run within Kubernetes, default namespace is
    # `default`. There is the potential for the resource starvation of
    # Airflow workers and scheduler within the Cloud Composer environment,
    # the recommended solution is to increase the amount of nodes in order
    # to satisfy the computing requirements. Alternatively, launching pods
    # into a custom namespace will stop fighting over resources.
    namespace='test6',
    # Docker image specified. Defaults to hub.docker.com, but any fully
    # qualified URLs will point to a custom repository. Supports private
    # gcr.io images if the Composer Environment is under the same
    # project-id as the gcr.io images and the service account that Composer
    # uses has permission to access the Google Container Registry
    # (the default service account has permission)
    image='gcr.io/google.com/cloudsdktool/cloud-sdk:latest',
    service_account_name='test6-service-acct')
  auth_list >> bq_query
