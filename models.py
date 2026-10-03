from config import STATUS
import errno
import socket

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
        },
        errno.WSAEWOULDBLOCK:{
            "status":"Errore",
            "error":"Operazione non completata"
        }
    }

    def __init__(self, port, risultato,):
        self.port = port
        self.risultato = risultato
        self.status = self.get_status()
        self.error_code = self.get_error_code()
        if self.is_open():
            self.service = self.get_service()
        else:
            self.service = "-"
        

    def get_service(self):
        try:
            s = socket.getservbyport(self.port)
            return s
        except OSError:
            return "Unknown"

    def get_status(self):
        status = self.get_result()
        return status

    def get_result(self):
        result = ScanResult.result_map.get(
            self.risultato, 
        {
            "status":"Sconosciuto",
            "error": f"Codice {self.risultato} non classificato"
        })
        return result

    def get_error_code(self):
        return None if self.risultato == 0 else self.risultato

    def is_open(self):
        if self.status["status"] == ScanResult.status_config["STATUS_OPEN"]:
            return True
        else:
            return False

    def is_closed(self):
        if self.status["status"] == ScanResult.status_config["STATUS_CLOSED"]:
            return True
        else:
            return False

    def has_error(self):
        if not self.is_open() and not self.is_closed():
            return True
        else:
            return False