from datetime import datetime, timedelta
from typing import Optional

from apscheduler.schedulers.base import BaseScheduler

from apps.scheduling.repositories.SchedulerWorkTimeRepository import SchedulerWorkTimeRepository


class TimedSchedulerInformer:
    _scheduler: BaseScheduler = None
    _scheduler_work_time_repository: SchedulerWorkTimeRepository = None
    _worktime_interval: Optional[timedelta] = None

    def __init__(self,
                 scheduler: BaseScheduler,
                 scheduler_work_time_repository: SchedulerWorkTimeRepository
                 ):
        self._scheduler = scheduler
        self._scheduler_work_time_repository = scheduler_work_time_repository

    def set_worktime_interval(self, interval: timedelta):
        self._worktime_interval = interval

    def get_next_work_time(self, name: str) -> datetime:
        if self._worktime_interval is None:
            raise Exception(f'Worktime interval for {name} not set')

        scheduler_last_work_time = self._scheduler_work_time_repository.get_scheduler_work_time(name)

        if scheduler_last_work_time is None:
            scheduler_last_work_time = self._scheduler_work_time_repository.create_work_time_if_exists(name, 1)

        now = int(datetime.now().timestamp())
        scheduler_last_work_time_int = scheduler_last_work_time.time

        if scheduler_last_work_time_int < now:
            scheduler_last_work_time_int = now + 2000
            self._scheduler_work_time_repository.update_work_time(
                name,
                int(self._get_next_running_time(scheduler_last_work_time.time))
            )

        formatted_datetime = datetime.fromtimestamp(scheduler_last_work_time_int)

        return formatted_datetime

    def _get_next_running_time(self, previous_running_time: int) -> float:
        current_time = int(datetime.now().timestamp())
        task_interval = self._worktime_interval.total_seconds()
        return ((current_time - previous_running_time) / task_interval + 1) * task_interval + previous_running_time


