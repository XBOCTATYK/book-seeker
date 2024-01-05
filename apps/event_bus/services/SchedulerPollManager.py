from concurrent.futures.thread import ThreadPoolExecutor

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler

from apps.event_bus.model.PollManagerConfig import PollManagerConfig
from apps.event_bus.services.PollManager import PollManager, PollHandler


class SchedulerPollManager(PollManager):
    _config = {}
    _poll_handlers = []
    _poll_scheduler: BaseScheduler

    def __init__(self, config: PollManagerConfig, poll_handlers: list[PollHandler]):
        super().__init__()

        self._poll_handlers = poll_handlers
        self._poll_scheduler = BackgroundScheduler().configure(executors={
            'default': ThreadPoolExecutor(max_workers=config['max_workers'])
        })

        for handler in self._poll_handlers:
            self._poll_scheduler.add_job(handler, 'interval', seconds=config['poll_interval'])

    def start(self):
        self._poll_scheduler.start()

    def stop(self):
        self._poll_scheduler.shutdown(wait=True)

    def add_handler(self, handler: PollHandler):
        self._poll_handlers.append(handler)
