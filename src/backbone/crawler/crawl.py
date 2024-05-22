import time
from typing import Protocol, Callable, Type

from backbone.container.container import Provider, Container
from backbone.crawler.exeptions.break_worker import BreakWorkerSpider
from backbone.crawler.exeptions.don_finished_worker import DonFinishedWorkerSpider
from backbone.crawler.exeptions.don_worker import DonWorkerSpider
from backbone.crawler.exeptions.restart_worker import RestartWorkerSpider
from backbone.crawler.exeptions.stop_worker import StopWorkerSpider
from backbone.crawler.helper.adapter.abstract_crawl import AbstractCrawl
from backbone.crawler.helper.helpers.response import Response
from backbone.infrastructure.log.logger import Logger


class SpiderProtocol(Protocol):
    def from_crawler(self): pass


class Crawler(AbstractCrawl):

    def __init__(self, lifespan=None):

        (self._lifespan(lifespan)) if lifespan else None
        self._time_start_worker_stopped = None
        self._conditional_start = None

        self._is_crawling = True
        self._is_run_worker = True

    def _stop_worker(self):
        self._is_run_worker = False

    def _start_worker(self):
        self._is_run_worker = True

    def _lifespan(self, lifespan):
        lifespan()

    def _run_flow(self, request):
        content = Response(request=request)
        if next_flow := request.callback(content):
            for nf in next_flow:
                self._run_flow(request=nf)

    def start(self, spider, conditional_break=None, logger: Logger = Provider[Container.logger]):
        logger.info(f"starting spider {spider.__name__}")
        for request in spider().from_crawler():
            if conditional_break and not conditional_break():
                logger.info("spider break")
                break
            self._run_flow(request=request)

    def start_supress_error(self, spider, conditional_break=None,
                            logger: Logger = Provider[Container.logger]):
        logger.info(f"starting spider {spider.__name__}")

        for request in spider().from_crawler():
            if conditional_break and not conditional_break():
                logger.info("spider break")
                break
            try:
                self._run_flow(request=request)
            except Exception as e:
                logger.info(f"Spider Error: {e}")

    def start_worker(self, spider: Type[SpiderProtocol], conditional_break=None, time_sleep_next_every_run=300,
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
                logger.info(f"Execute Spider {spider.__name__}")
                for request in spider().from_crawler():
                    if request:
                        self._run_flow(request=request)
                time.sleep(time_sleep_next_every_run)
            except BreakWorkerSpider:
                logger.info("Worker Break :(")
                break
            except DonWorkerSpider:
                logger.info("Worker Don... :)")
                time.sleep(time_sleep_next_every_run)
            except DonFinishedWorkerSpider:
                logger.info("Worker Don... :)")
                logger.info("Worker Finished... :)")
                break
            except RestartWorkerSpider:
                logger.info("Worker restart... :)")
                continue
            except StopWorkerSpider as e:
                self._conditional_start = e.args[0]
                self._time_start_worker_stopped = e.args[1] or time_sleep_next_every_run / 2
                logger.info("Worker Stopped :|")
                time.sleep(self._time_start_worker_stopped)
            except Exception as e:
                logger.error(f"Worker Error: {e} ")
                logger.debug(f"Run worker in next time {time_sleep_next_every_run}s")
                time.sleep(time_sleep_next_every_run)
