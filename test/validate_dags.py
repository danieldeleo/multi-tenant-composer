import importlib.util
import sys
from pathlib import Path

dag_dir = Path('dags/')
dags = dag_dir.glob('**/*.py')
for dag in dags:
  # Import dag source files directly
  # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
  spec = importlib.util.spec_from_file_location(dag.name, dag.absolute())
  module = importlib.util.module_from_spec(spec)
  sys.modules[dag.name] = module
  spec.loader.exec_module(module)
  tasks = module.dag.tasks
  for task in tasks:
    print(
      f'Kubernetes Service Account for dag ({dag.name})' +
      f'and task ({task.name}): {task.service_account_name}')
