import ipaddress

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

def filter_choise():
    while True:
        try:
            filter_selector = int(input("Quali porte vuoi vedere?\n1. Tutte le porte\n2. Solo le porte aperte\n3. Solo le porte chiuse\n4. Solo errori\n"))
            if filter_selector > 4 or filter_selector < 1:
                print("Devi scegliere un numero tra 1 e 4")
                continue
        except ValueError:
            print("Devi Scegliere un numero")
            continue
        return filter_selector

def show_result(scansioni, stat, tempo):
    print("=" * 52)
    print(" " * 8 + "Port Scanner")
    print("=" * 52)
    print("\nPORT     STATUS      SERVICE      ERRORI       CODICE ERRORE")
    print("-" * 52)
    for scansione in scansioni:
        port = scansione.port
        status = scansione.status["status"]
        service = scansione.service
        error = scansione.status["error"]
        error_code = scansione.error_code 
        print(f"{port:<8} {status:<11} {service:<12} {error} {error_code}\n")
    print("=" * 52)
    

    print(f'\nPorte scansionate: {stat["porte_scansionate"]}\nPorte aperte: {stat["porte_aperte"]}\nPorte chiuse: {stat["porte_chiuse"]}\nErrori: {stat["errori"]}\nOperazione finita in {tempo:.2f} secondi')
