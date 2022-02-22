from dags import multi_tenant_test

tasks = multi_tenant_test.dag.tasks

for task in tasks:
  print(f'Kubernetes Service Account for task ({task.name}): {task.service_account_name}')
