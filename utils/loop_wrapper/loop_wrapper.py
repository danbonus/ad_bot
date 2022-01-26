import asyncio
from asyncio import AbstractEventLoop, get_event_loop
from typing import Any, Callable, Coroutine, List, Optional, Union

from vkbottle import LoopWrapper as StockWrapper
from vkbottle.modules import logger

from .delayed_task import DelayedTask

Task = Coroutine[Any, Any, Any]


class LoopWrapper(StockWrapper):
    """ Loop Wrapper for vkbottle manages startup, shutdown and main tasks,
    creates loop and runs it forever """

    def __init__(
        self,
        *,
        on_startup: Optional[List[Task]] = None,
        on_shutdown: Optional[List[Task]] = None,
        auto_reload: Optional[bool] = None,
        auto_reload_dir: Optional[str] = None,
        tasks: Optional[List[Task]] = None,
    ):
        self.on_startup = on_startup or []
        self.on_shutdown = on_shutdown or []
        self.auto_reload = auto_reload or False
        self.auto_reload_dir = auto_reload_dir or "."
        self.tasks = tasks or []
        self.loop: AbstractEventLoop = get_event_loop()

    def run_forever(self, loop: Optional[AbstractEventLoop] = None):
        """ Runs startup tasks and makes the loop running forever """

        if not len(self.tasks):
            logger.warning("You ran loop with 0 tasks. Is it ok?")

        loop = loop or self.loop

        try:
            [loop.run_until_complete(startup_task) for startup_task in self.on_startup]

            for task in self.tasks:
                loop.create_task(task)

            loop.run_forever()
        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
        finally:
            [loop.run_until_complete(shutdown_task) for shutdown_task in self.on_shutdown]
            if loop.is_running():
                loop.close()

    def create_task(self, task: Union[Task, Callable[..., Task]], *args, **kwargs):
        """ Adds tasks to be ran in run_forever
        :param task: coroutine / coroutine function with zero arguments
        """

        if asyncio.iscoroutinefunction(task) or isinstance(task, DelayedTask):  # type: ignore
            print("It's delayed!")
            self.loop.create_task(task(*args, **kwargs))  # type: ignore
        elif asyncio.iscoroutine(task):  # type: ignore
            self.loop.create_task(task)  # type: ignore
        else:
            raise TypeError("Task should be coroutine or coroutine function")

    def create_interval(
        self, func: Callable, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, **kwargs
    ):

        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        self.create_task(DelayedTask(seconds, func), **kwargs)

    def create_timer(
        self, func: Callable, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, **kwargs
    ):

        seconds += minutes * 60
        seconds += hours * 60 * 60
        seconds += days * 24 * 60 * 60

        self.create_task(DelayedTask(seconds, func, do_break=True), **kwargs)
