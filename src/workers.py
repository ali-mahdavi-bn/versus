from multiprocessing import Pool

from backbone.container.container import Provider, Container
from backbone.infrastructure.log._logger import Logger
from backbone.worker.worker import Worker
from product.workers.products_translate import products_translate_worker


def worker_function(worker,logger: Logger = Provider[Container.logger]):
    try:
        return Worker().start_worker(worker)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    workers = [products_translate_worker]

    with Pool(len(workers)) as p:
        results = p.map(worker_function, workers)
