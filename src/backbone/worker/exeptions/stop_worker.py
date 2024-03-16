class StopWorker(Exception):
    def __init__(self, *,conditional_start,time_check_conditional=None):
        super().__init__(conditional_start,time_check_conditional)
