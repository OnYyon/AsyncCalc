import uuid
import queue
import threading
import multiprocessing
from typing import Iterator

from src.worker import worker


class Manager:
    def __init__(self):
        self._task_queue: multiprocessing.Queue = multiprocessing.Queue()
        self._result_queue: multiprocessing.Queue = multiprocessing.Queue()
        self.tasks: dict[str, tuple[str, str, float, bool, str]] = {}

        self._listener_thread = threading.Thread(target=self._listener, daemon=True)
        self._listener_thread.start()

        self._workers = []
        for i in range(3):
            p = multiprocessing.Process(target=worker, args=(f"{i}", self._task_queue, self._result_queue))
            p.start()
            self._workers.append(p)

    def add_task(self, expr: str) -> str:
        t: str = str(uuid.uuid4())
        self._task_queue.put((t, expr))
        self.tasks.setdefault(t, ("", "", 0, False, ""))
        return t

    def get_task_by_id(self, uid: str) -> tuple[str, str, float, bool, str]:
        if not self.tasks.get(uid):
            raise KeyError
        return self.tasks[uid]

    def get_all_tasks(self) -> Iterator[tuple[str, tuple[str, str, float, bool, str]]]:
        for k, v in self.tasks.items():
            yield k, v

    def update_task(self, uid: str, value: tuple[str, str, float, bool, str]):
        if not self.tasks.get(uid):
            raise KeyError
        self.tasks[uid] = value

    def _listener(self):
        while True:
            try:
                task_id, expr, value, error, error_text = self._result_queue.get(timeout=0.1)
                if error:
                    self.tasks[task_id] = ("", "", -1, True, error_text)
                else:
                    self.tasks[task_id] = (task_id, expr, value, False, "")
            except queue.Empty:
                continue
            except KeyboardInterrupt:
                break

    def shutdown(self):
        for _ in range(len(self._workers)):
            self._task_queue.put(None)
        for p in self._workers:
            p.join(timeout=2)
            if p.is_alive():
                p.kill()
        self._listener_thread.join()
