from datetime import datetime

from DateTime import DateTime
from apscheduler.schedulers.base import BaseScheduler

from apps.scheduling.repositories.SchedulerWorkTimeRepository import SchedulerWorkTimeRepository


class TimedSchedulerInformer:
    _scheduler: BaseScheduler = None
    _scheduler_work_time_repository: SchedulerWorkTimeRepository = None

    def __init__(self,
                 scheduler: BaseScheduler,
                 scheduler_work_time_repository: SchedulerWorkTimeRepository
                 ):
        self._scheduler = scheduler
        self._scheduler_work_time_repository = scheduler_work_time_repository

    def get_next_work_time(self, name: str) -> datetime:
        scheduler_last_work_time = self._scheduler_work_time_repository.get_scheduler_work_time(name)

        if scheduler_last_work_time is None:
            scheduler_last_work_time = self._scheduler_work_time_repository.create_work_time_if_exists(name, 1)

        datetime_unformatted = DateTime(scheduler_last_work_time.time)
        formatted_datetime = datetime.fromtimestamp(datetime_unformatted.time)

        return formatted_datetime

