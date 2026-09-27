import socket
import errno
import ipaddress
import time
from config import CONFIG,STATUS
from models import ScanResult


outcomes = {0 : STATUS["STATUS_OPEN"],
            errno.ECONNREFUSED:STATUS["STATUS_CLOSED"],
            errno.ENETUNREACH:"Rete non raggiungibile",
            errno.ETIMEDOUT:"TimedOut"}
error_messages = {0: None,
            errno.ECONNREFUSED:"Connection refused ",
            errno.ENETUNREACH:"Rete non raggiungibile",
            errno.ETIMEDOUT:"TimedOut"}


def insert_ip():
    while True:
        ip_input = input("Inserisci l'IP: ")
        try:
            ip = ipaddress.ip_address(ip_input)
        except ValueError:
            print(f"L'IP {ip_input} non è valido")
            continue
        print(f"IP Inserito: {ip_input}")
        return ip_input

def insert_range(config):
    while True:
        port_selector = input("Seleziona il range di porte da verificare (porta_minima, porta_massima): ")
        ps = port_selector.split(",")
        if len(ps) != 2:
            print("Devi selezionare 2 porte, la più bassa e la più alta")
            continue
        try:
            intps = [int(ps[0]), int(ps[1])]
            if intps[0] < config["PORT_MIN"]:
                print(f'le porte non possono essere più piccole di {config["PORT_MIN"]}')
                continue
            
            elif intps[1] > config["PORT_MAX"]:
                print(f'le porte sono limitate a {config["PORT_MAX"]}')
                continue

            elif intps[1] <= intps[0]:
                print("hai invertito l'ordine delle porte")
                continue
        except ValueError:
            print("Devi selezionare 2 numeri")
            continue

        return intps

def check_port(ip, porta, config):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(config["SOCKET_TIMEOUT"])
        risultato = s.connect_ex((ip,porta))

    return risultato

def get_error_message(errore):
    messaggio = error_messages.get(errore, f"Errore Sconosciuto")
    return messaggio

def scan(ip, range_ports,config):

    lista_porte = []
    for port in range(range_ports[0], range_ports[1]+1):
        risultato = check_port(ip, port, config)
        service = "-"
        codice_errore = risultato
        if risultato == 0:
            service = get_service(port)
            codice_errore = None


             
        scansione= ScanResult(
            port,
            outcomes.get(risultato, "Errore Sconosciuto"),
            service,
            get_error_message(risultato),
            codice_errore
            )
        
     

            


        lista_porte.append(scansione)

    return lista_porte

def get_service(port):
    try:
        s = socket.getservbyport(port)
        return s
    except OSError:
        return "Unknown"

def filter_result(scansioni):
    while True:
        try:
            filter_selector = int(input("Quali porte vuoi vedere?\n1. Tutte le porte\n2. Solo le porte aperte\n3. Solo le porte chiuse\n4. Solo errori\n"))
            if filter_selector > 4 or filter_selector < 1:
                print("Devi scegliere un numero tra 1 e 4")
                continue
        except ValueError:
            print("Devi Scegliere un numero")
            continue


        
        if filter_selector == 2:
            porte_aperte = []    
            for scansione in scansioni:
                if scansione.is_open():
                    porte_aperte.append(scansione)
            return porte_aperte
        elif filter_selector == 3:
            porte_chiuse = []
            for scansione in scansioni:
                if scansione.is_closed():
                    porte_chiuse.append(scansione)
            return porte_chiuse
        elif filter_selector == 4:
            errori = []
            for scansione in scansioni:
                if scansione.has_error():
                    errori.append(scansione)
            return errori
        else:
            return scansioni

def statistiche(scansioni):
    
    porte_aperte = 0
    porte_chiuse = 0
    errori = 0
    porte_scansionate = 0

    for scansione in scansioni:
        porte_scansionate += 1
        if scansione.is_open():
            porte_aperte +=1
        elif scansione.is_closed():
            porte_chiuse += 1
        else:
            errori +=1
    
    return {
        "porte_scansionate": porte_scansionate,
        "porte_aperte": porte_aperte,
        "porte_chiuse": porte_chiuse,
        "errori": errori
    }

def show_result(scansioni, stat, tempo):
    print("=" * 52)
    print(" " * 8 + "Port Scanner")
    print("=" * 52)
    print("\nPORT     STATUS      SERVICE      ERRORI       CODICE ERRORE")
    print("-" * 52)
    for scansione in scansioni:
        port = scansione.port
        status = scansione.status
        service = scansione.servizio
        error = scansione.error
        error_code = scansione.error_code 
        print(f"{port:<8} {status:<11} {service:<12} {error:<12} {error_code}\n")
    print("=" * 52)
    

    print(f'\nPorte scansionate: {stat["porte_scansionate"]}\nPorte aperte: {stat["porte_aperte"]}\nPorte chiuse: {stat["porte_chiuse"]}\nErrori: {stat["errori"]}\nOperazione finita in {tempo:.2f} secondi')

def main():
    ip = insert_ip()
    port_range = insert_range(CONFIG)
    inizio = time.perf_counter()
    scansioni = scan(ip, port_range, CONFIG)
    fine = time.perf_counter()
    tempo = fine - inizio
    filtro = filter_result(scansioni)
    stats = statistiche(scansioni)
    show_result(filtro, stats, tempo)

if __name__ == '__main__':
    main()