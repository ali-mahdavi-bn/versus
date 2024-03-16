class RestartWorker(Exception):
    def __init__(self, time_restart=1):
        super().__init__(time_restart)
