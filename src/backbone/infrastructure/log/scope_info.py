import socket
import uuid
import structlog
import sys


class ScopeInformation:
    def __init__(self):
        self.host_scope_info = {
            "MachineName": socket.gethostname(),
            "EntryPoint": sys.argv[0]
        }

        self.request_scope_info = {
            "RequestId": str(uuid.uuid4())
        }

    def enrich_log_entry(self, logger, log_method, event_dict):
        event_dict["host_scope_info"] = self.host_scope_info
        event_dict["request_scope_info"] = self.request_scope_info
        return event_dict
