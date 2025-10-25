import uuid
import queue
import threading
import multiprocessing
from pprint import pprint

from src.worker import worker


class Manager:
    def __init__(self):
        self.task_queue: multiprocessing.Queue = multiprocessing.Queue()
        self.result_queue: multiprocessing.Queue = multiprocessing.Queue()
        self.tasks: dict[str, tuple[str, str, float, bool]] = {}

        listener_thread = threading.Thread(target=self._listener, daemon=True)
        listener_thread.start()

        self.workers = []
        for _ in range(3):
            p = multiprocessing.Process(target=worker, args=(self.task_queue, self.result_queue))
            p.start()
            self.workers.append(p)

    def add_task(self, expr: str) -> str:
        t: str = str(uuid.uuid4())
        self.task_queue.put((t, expr))
        self.tasks.setdefault(t, ("", "", 0, False))
        return t

    def get_task_by_id(self, uid: str) -> tuple[str, str, float, bool]:
        if not self.tasks.get(uid):
            raise KeyError
        return self.tasks[uid]

    def get_all_tasks(self) -> dict[str, tuple[str, str, float, bool]]:
        return self.tasks

    def update_task(self, uid: str, value: tuple[str, str, float, bool]):
        if not self.tasks.get(uid):
            raise KeyError
        self.tasks[uid] = value


    def _listener(self):
        while True:
            try:
                task_id, expr, value, error = self.result_queue.get(timeout=0.1)
                if error:
                    self.tasks[task_id] = ("", "", -1, True)
                else:
                    self.tasks[task_id] = (task_id, expr, value, False)
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                break

    def shutdown(self):
        for _ in range(len(self.workers)):
            self.task_queue.put(None)
        for p in self.workers:
            p.join(timeout=2)
            if p.is_alive():
                p.kill()
