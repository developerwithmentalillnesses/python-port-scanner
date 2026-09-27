import errno
import socket

print(errno.ETIMEDOUT)

errori = {errno.ETIMEDOUT : '{"Port" : port, "Status": "|ERRORE|: TimedOut err", "Servizio" : "-", "errori" : risultato}'}
risultato = errno.ETIMEDOUT
if risultato in errori:
    print(errori[risultato])