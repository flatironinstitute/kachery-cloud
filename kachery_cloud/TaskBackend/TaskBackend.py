import string
import random
from typing import Callable, Dict, Union
from .TaskClient import TaskClient
from ._run_task import _run_task

try:
    from dask.distributed import Client, Future, LocalCluster
except:
    raise Exception('Unable to import from dask.distributed. Use: pip install dask[distributed]')


class TaskBackend:
    def __init__(self, *, project_id: Union[str, None]=None, num_workers=1, threads_per_worker=4) -> None:
        self._project_id = project_id
        self._registered_task_handlers: Dict[str, TaskHandler] = {}
        self._num_workers = num_workers
        self._threads_per_worker = threads_per_worker
    def register_task_handler(self, *, task_type: str, task_name: str, task_function: Callable):
        self._registered_task_handlers[task_name] = TaskHandler(
            task_type=task_type,
            task_name=task_name,
            task_function=task_function
        )
    def run(self):
        dask_cluster = LocalCluster(n_workers=self._num_workers, threads_per_worker=self._threads_per_worker)
        dask_client = Client(dask_cluster)
        task_client = TaskClient(project_id=self._project_id)
        task_jobs: Dict[str, TaskJob] = {}
        def handle_task_request(*, task_type: str, task_name: str, task_input: dict, task_job_id: str):
            if task_name in self._registered_task_handlers:
                print(f'Task: {task_name}')
                task_handler = self._registered_task_handlers[task_name]
                if task_handler._task_type != task_type:
                    raise Exception(f'Mismatch in task type: {task_handler.task_type} <> {task_type}')
                if task_job_id in task_jobs:
                    tj = task_jobs[task_job_id]
                    result_future: Future = tj._result_future
                    if result_future.status == 'pending':
                        print(f'Task already running: {task_name}')
                        return
                result_future: Future = dask_client.submit(
                    _run_task,
                    pure=False,
                    task_type=task_handler._task_type,
                    task_name=task_handler._task_name,
                    task_job_id=task_job_id,
                    task_function=task_handler._task_function,
                    task_input=task_input,
                    project_id=self._project_id
                )
                # seems to be important to store the result future in memory
                # hypothesis: if the result is not used, it may get garbage collected and not actually run
                task_jobs[task_job_id] = TaskJob(
                    task_type=task_handler._task_type,
                    task_name=task_handler._task_name,
                    task_input=task_input,
                    task_job_id=task_job_id,
                    result_future=result_future
                )
        listener = task_client.listen_for_task_requests(handle_task_request)
        try:
            while True:
                listener.wait(1)
        finally:
            dask_cluster.close() # important, otherwise all the workers get restarted
            listener.stop()

class TaskHandler:
    def __init__(self, *, task_type: str, task_name: str, task_function: Callable) -> None:
        self._task_type = task_type
        self._task_name = task_name
        self._task_function = task_function
    def run_task(self, *, task_input: dict):
        return self._task_function(**task_input)

class TaskJob:
    def __init__(self, *,
        task_type: str,
        task_name: str,
        task_input: dict,
        task_job_id: str,
        result_future: Future
    ) -> None:
        self._task_type = task_type
        self._task_name = task_name
        self._task_input = task_input
        self._task_job_id = task_job_id
        self._result_future = result_future

def _random_string(num: int):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(num))