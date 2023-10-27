import concurrent.futures
import threading


class EventBus():
    def __init__(self) -> None:
        self.handlers: dict = {}

    def add_handlers(self, event_name: str, handlers: list) -> None:
        for handler in handlers:
            if not self.handlers.get(event_name, None):
                self.handlers[event_name] = {handler}
            else:
                self.handlers[event_name].add(handler)

    def emit(self, event_name: str, event: dict) -> None:
        handlers = self.handlers.get(event_name)

        executor = concurrent.futures.ThreadPoolExecutor(len(handlers))

        futures = [executor.submit(handler, event) for handler in handlers]

        self.spawn_thread(target=self.manage_future_result, kwargs={"futures": futures, "executor": executor})

    def manage_future_result(self, kwargs):
        futures: list[concurrent.futures.Future] = kwargs.get("futures")
        executor: concurrent.futures.Executor = kwargs.get("executor")

        print(f"managing futures in thread {threading.get_ident()}")

        for future in futures:
            try:
                future.result(timeout=5)
            except Exception as e:
                print(e)

        executor.shutdown()

    def spawn_thread(self, target, **kwargs):
        threading.Thread(target=target, kwargs=kwargs).start()
