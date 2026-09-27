from config import STATUS
import errno

class ScanResult:
    status_config = STATUS
    result_map =  {
        0 : {
            "status": STATUS["STATUS_OPEN"],
            "error": None
        },
        errno.ECONNREFUSED:{
            "status":STATUS["STATUS_CLOSED"],
            "error":"Connection refused"
        },
        errno.ENETUNREACH:{
            "status":"Rete non raggiungibile",
            "error":"Rete non raggiungibile"
        },
        errno.ETIMEDOUT:{
            "status": "TimedOut",
            "error": "TimedOut"
        }
    }

    def __init__(self, port, status, servizio, error, error_code):
        self.port = port
        self.status = status
        self.servizio = servizio
        self.error = error
        self.error_code = error_code

    def is_open(self):
        if self.status == ScanResult.status_config["STATUS_OPEN"]:
            return True
        else:
            return False

    def is_closed(self):
        if self.status == ScanResult.status_config["STATUS_CLOSED"]:
            return True
        else:
            return False

    def has_error(self):
        if not self.is_open() and not self.is_closed():
            return True
        else:
            return False