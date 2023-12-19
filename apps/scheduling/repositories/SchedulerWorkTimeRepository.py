from typing import Callable, TypeVar, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.scheduling.models.db.SchedulerWorkTimeDto import SchedulerWorkTimeDto
from common.services.AbstractRepository import AbstractRepository
from datasource.DbLikeDataSource import DbLikeDataSource

T = TypeVar('T')


class SchedulerWorkTimeRepository(AbstractRepository):
    _retries_count = 0
    _retry_timing = 0

    def __init__(self, data_source: DbLikeDataSource):
        super().__init__(data_source)
        self._data_source = data_source

    def set_retries_count(self, count: int) -> 'SchedulerWorkTimeRepository':
        self._retries_count = count
        return self

    def set_retry_timing(self, timing: int) -> 'SchedulerWorkTimeRepository':
        self._retry_timing = timing
        return self

    def process_job(self, name: str, fn: Callable[[SchedulerWorkTimeDto], T]) -> T:
        return self.call_in_transaction(
            lambda sess: self._process_job(sess, name, fn)
        )

    def update_work_time(self, name: str, work_time: int) -> 'SchedulerWorkTimeRepository':
        return self.call_in_transaction(
            lambda sess: self._update_work_time(sess, name, work_time)
        )

    def create_work_time_if_exists(self, name: str, work_time: int) -> SchedulerWorkTimeDto:
        return self.call_in_transaction(
            lambda sess: self._create_work_time_if_exists(sess, name, work_time)
        )

    def _get_scheduler_work_time(self, sess: Session, name: str) -> Optional[SchedulerWorkTimeDto]:
        req = (select(SchedulerWorkTimeDto).where(SchedulerWorkTimeDto.scheduler_name == name)
               .with_for_update(skip_locked=True))
        return sess.execute(req).scalar_one_or_none()

    def _process_job(self, sess: Session, name: str, fn: Callable[[SchedulerWorkTimeDto], T]) -> T:
        scheduler_work_time = self._get_scheduler_work_time(sess, name)

        if scheduler_work_time is None:
            raise Exception(f'Scheduler {name} not found')

        try:
            result = fn(scheduler_work_time)
        except Exception as error:
            self._dec_retries_counter_or_throw(error)
            self._update_work_time(sess, name, scheduler_work_time.time + self._retry_timing)
            result = None

        return result

    def _dec_retries_counter_or_throw(self, ex: Exception):
        if self._retries_count > 0:
            self._retries_count -= 1
        else:
            raise ex

    def _update_work_time(self, sess: Session, name: str, work_time):
        scheduler_work_time = self._get_scheduler_work_time(sess, name)

        if scheduler_work_time is None:
            raise Exception(f'Scheduler {name} not found')

        scheduler_work_time.time = work_time
        sess.add(scheduler_work_time)
        sess.flush([scheduler_work_time])

    def _create_work_time_if_exists(self, sess: Session, name: str, initial_work_time: int) -> SchedulerWorkTimeDto:
        scheduler_work_time = self._get_scheduler_work_time(sess, name)

        if scheduler_work_time is None:
            scheduler_work_time = SchedulerWorkTimeDto(scheduler_name=name, time=initial_work_time)
            sess.add(scheduler_work_time)
            sess.flush([scheduler_work_time])

        return scheduler_work_time

    def get_scheduler_work_time(self, param) -> SchedulerWorkTimeDto:
        return self.call_in_transaction(
            lambda sess: self._get_scheduler_work_time(sess, param)
        )
