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

        executor = concurrent.futures.ThreadPoolExecutor(len(handlers))  # Run one thread for each handler

        futures = [executor.submit(handler, event) for handler in handlers]

        self.spawn_thread(self.manage_futures_result, False, futures, executor) # Manage futures result synchronously in a new thread to avoid block the caller thread.

    def manage_futures_result(self, futures: list[concurrent.futures.Future], executor: concurrent.futures.Executor):
        print(f"managing futures in thread {threading.get_ident()}")

        for future in futures:
            try:
                future.result(timeout=5)
            except Exception as e:
                print(e)

        executor.shutdown()

    def spawn_thread(self, target, daemon, *args, **kwargs):
        threading.Thread(target=target, daemon=daemon, args=args, kwargs=kwargs).start()
