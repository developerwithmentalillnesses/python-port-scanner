import customtkinter
import ipaddress
from config import SOCKET_CONFIG
from scanner import scan
from results import filter_result, statistiche
app = customtkinter.CTk()  
app.title("Port Scanner")  
app.geometry("800x600")    


title_label = customtkinter.CTkLabel(app, text="PORT SCANNER")
title_label.pack(pady=20)  


ip_address_label = customtkinter.CTkLabel(app, text="Ip address:")
ip_address_label.pack(pady=15)


ip_address_entry = customtkinter.CTkEntry(app)
ip_address_entry.pack(padx=20, pady=30)

min_port_label = customtkinter.CTkLabel(app, text="Porta iniziale")
min_port_label.pack(pady=20)

min_port_entry = customtkinter.CTkEntry(app)
min_port_entry.pack(pady=20)

max_port_label = customtkinter.CTkLabel(app, text="Porta Finale")
max_port_label.pack(pady=20)

max_port_entry = customtkinter.CTkEntry(app)
max_port_entry.pack(pady=20)

errorlabel = customtkinter.CTkLabel(app, text="")
errorlabel.pack(pady=20)

resultlabel = customtkinter.CTkLabel(app, text="")
resultlabel.pack(pady=20)

def get_ip():

    ip_input = ip_address_entry.get()
    try:
        ip = ipaddress.ip_address(ip_input)
        return ip_input
    except ValueError:
        errorlabel.configure(text="IP non valido")

def get_ports():
    try:
        min_port_str = min_port_entry.get()
        max_port_str = max_port_entry.get()

        if not min_port_str or not max_port_str:
            errorlabel.configure(text="Tutti i campi devono essere riempiti")
            return

        min_port = int(min_port_str)
        max_port = int(max_port_str)

        if not (SOCKET_CONFIG["PORT_MIN"] <= min_port <= SOCKET_CONFIG["PORT_MAX"]) or not (SOCKET_CONFIG["PORT_MIN"] <= max_port <= SOCKET_CONFIG["PORT_MAX"]):
            errorlabel.configure(text=f"Le porte devono essere tra i {SOCKET_CONFIG['PORT_MIN']} e i {SOCKET_CONFIG['PORT_MAX']}")
            return

        if max_port < min_port:
            errorlabel.configure(text="Non puoi invertire le porte")
            return
        errorlabel.configure(text="")
        return [min_port, max_port]

    except ValueError:
        errorlabel.configure(text="Deve essere un numero")


def scan_clicked():

    ip = get_ip()
    if ip:
        ports = get_ports()
        if ports:
            scansione = scan(ip, ports, SOCKET_CONFIG["SOCKET_TIMEOUT"])
            filtro = filter_result(scansione, 1)
            stats = statistiche(filtro)
            resultlabel.configure(text=stats) # un botto provvisorio chat <3

    else:
        return 


scan_button = customtkinter.CTkButton(app,text="Scan",command=scan_clicked)
scan_button.pack(pady=20)




app.mainloop()  