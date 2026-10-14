import socket
from models import ScanResult

def check_port(ip, porta, timeout):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        risultato = s.connect_ex((ip,porta))

    return risultato

def scan(ip, range_ports,timeout):

    lista_porte = []
    for port in range(range_ports[0], range_ports[1]+1):
        risultato = check_port(ip, port, timeout)     
        scansione= ScanResult(
            port,
            risultato)
        lista_porte.append(scansione)

    return lista_porte

