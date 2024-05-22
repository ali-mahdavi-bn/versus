import time
from typing import Callable

from backbone.container.container import Container, Provider
from backbone.infrastructure.log.logger import Logger
from backbone.worker.abstract_worker import AbstractWorker
from backbone.worker.exeptions.break_worker import BreakWorker
from backbone.worker.exeptions.don_finished_worker import DonFinishedWorker
from backbone.worker.exeptions.don_worker import DonWorker
from backbone.worker.exeptions.message_worker import MessageWorker
from backbone.worker.exeptions.restart_worker import RestartWorker
from backbone.worker.exeptions.stop_worker import StopWorker


class Worker(AbstractWorker):

    def __init__(self, lifespan=None):

        self._time_start_worker_stopped = None
        self._conditional_start = None
        (self._lifespan(lifespan)) if lifespan else None

        self._is_crawling = True
        self._is_run_worker = True

    def _stop_worker(self):
        self._is_run_worker = False

    def _start_worker(self):
        self._is_run_worker = True

    def _lifespan(self, lifespan):
        lifespan()

    def start(self, worker_ref, conditional_break=None,logger: Logger = Provider[Container.logger]):
        logger.info(f"starting Worker {worker_ref.__name__}")
        worker_ref()

    def start_worker(self, worker_ref: Callable, conditional_break=None, time_sleep_next_every_run=300,
                     logger: Logger = Provider[Container.logger]):
        logger.info("🚀Worker Running...")
        while True:
            if self._conditional_start:
                logger.warning("Try Start Worker")
                try:
                    if self._conditional_start():
                        self._start_worker()
                        logger.info("Worker Started")
                except Exception:
                    logger.warning("Fail Try Start Worker")
                    time.sleep(self._time_start_worker_stopped)
                    continue

            if conditional_break and not conditional_break():
                logger.info("Worker Break...")
                break

            try:
                logger.info(f"Execute Worker {worker_ref.__name__}")
                worker_ref()
                time.sleep(time_sleep_next_every_run)
            except BreakWorker as e:
                logger.info("Worker Break :(")
                break
            except DonWorker as e:
                logger.info("Worker Don... :)")
                time.sleep(time_sleep_next_every_run)
            except DonFinishedWorker as e:
                logger.info("Worker Don... :)")
                logger.info("Worker Finished... :)")
                break
            except RestartWorker as e:
                time_restart = e.args[0] or time_sleep_next_every_run / 2
                logger.info("Worker restart... :)")
                time.sleep(time_restart)
            except StopWorker as e:
                self._conditional_start = e.args[0]
                self._time_start_worker_stopped = e.args[1] or time_sleep_next_every_run / 2
                logger.info("Worker Stopped :|")
                time.sleep(self._time_start_worker_stopped)
            except MessageWorker as e:
                logger.info(str(e))
            except Exception as e:
                logger.error(f"Worker Error: {str(e)} ")
                logger.debug(f"Run worker in next time {time_sleep_next_every_run}s")
                time.sleep(time_sleep_next_every_run)
