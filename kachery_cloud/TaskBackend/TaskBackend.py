import string
import random
from typing import Callable, Dict, Union
from .TaskClient import TaskClient
from ._run_task import _run_task
from ..get_project_id import get_project_id

try:
    from dask.distributed import Client, Future, LocalCluster
except:
    raise Exception('Unable to import from dask.distributed. Use: pip install dask[distributed]')


class TaskBackend:
    def __init__(self, *, project_id: Union[str, None]=None, backend_id: Union[str, None]=None, num_workers=1, threads_per_worker=4) -> None:
        if project_id is None:
            project_id = get_project_id()
        self._project_id = project_id
        self._backend_id = backend_id
        self._registered_task_handlers: Dict[str, TaskHandler] = {}
        self._num_workers = num_workers
        self._threads_per_worker = threads_per_worker
    def register_task_handler(self, *,
        task_type: str,
        task_name: str,
        task_function: Callable,
        extra_kwargs: Union[dict, None]=None,
        can_pickle: bool=True
    ):
        if self._registered_task_handlers.get(task_name, None) is None:
            self._registered_task_handlers[task_name] = TaskHandler(
                task_type=task_type,
                task_name=task_name,
                task_function=task_function,
                extra_kwargs=extra_kwargs,
                can_pickle=can_pickle
            )
    def run(self):
        task_names = sorted(list(self._registered_task_handlers.keys()))
        for task_name in task_names:
            handler = self._registered_task_handlers[task_name]
            print(f'Task handler: {task_name} ({handler._task_type})')
        project_id = self._project_id
        print(f'Listening for tasks on project {project_id}')
        dask_cluster = LocalCluster(n_workers=self._num_workers, threads_per_worker=self._threads_per_worker)
        dask_client = Client(dask_cluster)
        task_client = TaskClient(project_id=project_id)
        task_jobs: Dict[str, TaskJob] = {}
        def handle_task_request(*, task_type: str, task_name: str, task_input: dict, task_job_id: str, backend_id: Union[str, None]=None):
            if self._backend_id is not None:
                if self._backend_id != backend_id:
                    return
            if task_name in self._registered_task_handlers:
                print(f'Task: {task_name}')
                task_handler = self._registered_task_handlers[task_name]
                if task_handler._task_type != task_type:
                    raise Exception(f'Mismatch in task type: {task_handler.task_type} <> {task_type}')
                if task_job_id in task_jobs:
                    tj = task_jobs[task_job_id]
                    result_future: Future = tj._result_future
                    if result_future is not None:
                        if result_future.status == 'pending':
                            print(f'Task already running: {task_name}')
                            return
                if task_handler._can_pickle:
                    result_future: Future = dask_client.submit(
                        _run_task,
                        pure=False,
                        task_type=task_handler._task_type,
                        task_name=task_handler._task_name,
                        task_job_id=task_job_id,
                        task_function=task_handler._task_function,
                        task_input=task_input,
                        project_id=self._project_id,
                        extra_kwargs=task_handler._extra_kwargs
                    )
                else:
                    _run_task(
                        task_type=task_handler._task_type,
                        task_name=task_handler._task_name,
                        task_job_id=task_job_id,
                        task_function=task_handler._task_function,
                        task_input=task_input,
                        project_id=self._project_id,
                        extra_kwargs=task_handler._extra_kwargs
                    )
                    result_future = None

                # seems to be important to store the result future in memory
                # hypothesis: if the result is not used, it may get garbage collected and not actually run
                task_jobs[task_job_id] = TaskJob(
                    task_type=task_handler._task_type,
                    task_name=task_handler._task_name,
                    task_input=task_input,
                    task_job_id=task_job_id,
                    # result_future=result_future
                    result_future=None
                )
        listener = task_client.listen_for_task_requests(handle_task_request)
        try:
            while True:
                listener.wait(10)
        finally:
            dask_cluster.close() # important, otherwise all the workers get restarted
            listener.stop()

class TaskHandler:
    def __init__(self, *,
        task_type: str,
        task_name: str,
        task_function: Callable,
        extra_kwargs: Union[dict, None]=None,
        can_pickle: bool=True
    ) -> None:
        self._task_type = task_type
        self._task_name = task_name
        self._task_function = task_function
        self._extra_kwargs = extra_kwargs if extra_kwargs is not None else {}
        self._can_pickle = can_pickle
    def run_task(self, *, task_input: dict):
        return self._task_function(**task_input, **self._extra_kwargs)

class TaskJob:
    def __init__(self, *,
        task_type: str,
        task_name: str,
        task_input: dict,
        task_job_id: str,
        result_future: Union[Future, None]
    ) -> None:
        self._task_type = task_type
        self._task_name = task_name
        self._task_input = task_input
        self._task_job_id = task_job_id
        self._result_future = result_future

def _random_string(num: int):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(num))