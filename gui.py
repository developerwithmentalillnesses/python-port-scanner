
import threading
import ipaddress
import customtkinter as ctk

from config import SOCKET_CONFIG
from scanner import scan
from results import statistiche


# ============================================================
# CONFIGURAZIONE GRAFICA
# ============================================================

BG = "#050807"
PANEL = "#080E0C"
GREEN = "#00FF9C"
CYAN = "#00E5D4"
RED = "#FF3B55"
YELLOW = "#FFD166"
WHITE = "#C5F7E5"
MUTED = "#527F70"

FONT = "Consolas"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("PORT SCANNER // CYBER SECURITY")
app.geometry("1150x780")
app.minsize(900, 650)
app.configure(fg_color=BG)

app.grid_columnconfigure(0, weight=3)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)


# ============================================================
# FUNZIONI DI SUPPORTO GRAFICO
# ============================================================

def create_label(parent, text, size=13, color=GREEN, bold=False):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=(FONT, size, "bold" if bold else "normal"),
        text_color=color,
        anchor="w"
    )


def create_entry(parent, placeholder, width=180):
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        width=width,
        height=38,
        font=(FONT, 13),
        fg_color=BG,
        text_color=GREEN,
        placeholder_text_color=MUTED,
        border_color=CYAN,
        corner_radius=0
    )


def set_error(message):
    error_label.configure(text=message)


def clear_results():
    results_box.configure(state="normal")
    results_box.delete("1.0", "end")
    results_box.configure(state="disabled")


def add_result_line(text, tag=None):
    results_box.configure(state="normal")

    if tag:
        results_box.insert("end", text + "\n", tag)
    else:
        results_box.insert("end", text + "\n")

    results_box.configure(state="disabled")



# ============================================================
# CYBERPUNK ASCII HEADER
# ============================================================

header = ctk.CTkFrame(
    app,
    fg_color=BG,
    border_color=CYAN,
    border_width=1,
    corner_radius=0
)

header.grid(
    row=0, column=0, columnspan=2,
    sticky="ew", padx=18, pady=(18, 12)
)

header.grid_columnconfigure(0, weight=1)
header.grid_columnconfigure(1, weight=0)

ascii_title = r"""
 ____   ___  ____ _____   ____   ____    _    _   _ _   _ _____ ____
|  _ \ / _ \|  _ \_   _| / ___| / ___|  / \  | \ | | \ | | ____|  _ \
| |_) | | | | |_) || |   \___ \| |     / _ \ |  \| |  \| |  _| | |_) |
|  __/| |_| |  _ < | |    ___) | |___ / ___ \| |\  | |\  | |___|  _ <
|_|    \___/|_| \_\|_|   |____/ \____/_/   \_\_| \_|_| \_|_____|_| \_\
"""

create_label(
    header,
    ascii_title,
    size=9,
    color=GREEN,
    bold=True
).grid(
    row=0, column=0,
    padx=18, pady=(12, 0), sticky="w"
)

create_label(
    header,
    "> SCAN  > ANALYZE  > SECURE",
    size=14,
    color=CYAN,
    bold=True
).grid(
    row=1, column=0,
    padx=20, pady=(0, 14), sticky="w"
)

quote_panel = ctk.CTkFrame(
    header,
    fg_color=PANEL,
    border_color=CYAN,
    border_width=1,
    corner_radius=0
)

quote_panel.grid(
    row=0, column=1, rowspan=2,
    padx=15, pady=12, sticky="nsew"
)

create_label(
    quote_panel,
    "SYSTEM // SECURITY",
    size=11,
    color=CYAN,
    bold=True
).pack(anchor="w", padx=12, pady=(10, 4))

create_label(
    quote_panel,
    "Observe. Analyze.\nUnderstand the network.",
    size=12,
    color=GREEN
).pack(anchor="w", padx=12, pady=(0, 10))

status_label = create_label(
    header,
    "[ READY ]",
    size=12,
    color=GREEN,
    bold=True
)

status_label.grid(
    row=2, column=1,
    padx=15, pady=(0, 10)
)



# ============================================================
# PANNELLO INPUT
# ============================================================

input_panel = ctk.CTkFrame(
    app,
    fg_color=PANEL,
    border_color=CYAN,
    border_width=1,
    corner_radius=0
)
input_panel.grid(
    row=1, column=0, columnspan=2,
    sticky="ew", padx=18, pady=(0, 12)
)

input_panel.grid_columnconfigure(0, weight=3)
input_panel.grid_columnconfigure(1, weight=1)
input_panel.grid_columnconfigure(2, weight=1)

create_label(
    input_panel, "IP ADDRESS", color=CYAN, bold=True
).grid(row=0, column=0, padx=15, pady=(12, 5), sticky="w")

create_label(
    input_panel, "PORTA INIZIALE", color=CYAN, bold=True
).grid(row=0, column=1, padx=10, pady=(12, 5), sticky="w")

create_label(
    input_panel, "PORTA FINALE", color=CYAN, bold=True
).grid(row=0, column=2, padx=10, pady=(12, 5), sticky="w")

ip_entry = create_entry(input_panel, "Es. 192.168.1.1")
ip_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")

min_port_entry = create_entry(input_panel, "1", width=100)
min_port_entry.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="ew")

max_port_entry = create_entry(input_panel, "1024", width=100)
max_port_entry.grid(row=1, column=2, padx=10, pady=(0, 15), sticky="ew")

# Valori predefiniti per facilitare il primo test
min_port_entry.insert(0, "1")
max_port_entry.insert(0, "1024")

scan_button = ctk.CTkButton(
    input_panel,
    text="[ SCAN ]",
    command=lambda: scan_clicked(),
    height=42,
    font=(FONT, 14, "bold"),
    fg_color=GREEN,
    hover_color=CYAN,
    text_color=BG,
    corner_radius=0
)
scan_button.grid(
    row=2, column=0, columnspan=3,
    padx=15, pady=(0, 12), sticky="ew"
)

error_label = create_label(
    input_panel, "", size=12, color=RED
)
error_label.grid(
    row=3, column=0, columnspan=3,
    padx=15, pady=(0, 10), sticky="w"
)


# ============================================================
# RISULTATI SCANSIONE
# ============================================================

results_panel = ctk.CTkFrame(
    app,
    fg_color=PANEL,
    border_color=CYAN,
    border_width=1,
    corner_radius=0
)
results_panel.grid(
    row=2, column=0,
    sticky="nsew", padx=(18, 6), pady=(0, 12)
)
results_panel.grid_rowconfigure(1, weight=1)
results_panel.grid_columnconfigure(0, weight=1)

create_label(
    results_panel,
    "RESULTS // RISULTATI SCANSIONE",
    size=15,
    color=CYAN,
    bold=True
).grid(row=0, column=0, padx=15, pady=12, sticky="w")

results_box = ctk.CTkTextbox(
    results_panel,
    fg_color="#020403",
    text_color=GREEN,
    border_color=CYAN,
    border_width=1,
    corner_radius=0,
    font=("Consolas", 13),
    wrap="none"
)
results_box.grid(
    row=1, column=0,
    sticky="nsew", padx=12, pady=(0, 12)
)

# Colori delle righe dei risultati
results_box.tag_config("open", foreground=GREEN)
results_box.tag_config("closed", foreground=RED)
results_box.tag_config("error", foreground=YELLOW)
results_box.tag_config("header", foreground=CYAN)

results_box.insert(
    "end",
    " PORT  | STATUS      | SERVICE          | ERROR\n"
    "-------+-------------+------------------+----------------------\n"
)
results_box.configure(state="disabled")


# ============================================================
# PANNELLO STATISTICHE
# ============================================================

stats_panel = ctk.CTkFrame(
    app,
    fg_color=PANEL,
    border_color=CYAN,
    border_width=1,
    corner_radius=0
)
stats_panel.grid(
    row=2, column=1,
    sticky="nsew", padx=(6, 18), pady=(0, 12)
)
stats_panel.grid_columnconfigure(0, weight=1)

create_label(
    stats_panel,
    "STATISTICS",
    size=15,
    color=CYAN,
    bold=True
).grid(row=0, column=0, padx=15, pady=12, sticky="w")

scanned_value = create_label(
    stats_panel, "SCANNED: 0", color=WHITE
)
scanned_value.grid(row=1, column=0, padx=15, pady=8, sticky="w")

open_value = create_label(
    stats_panel, "OPEN: 0", color=GREEN, bold=True
)
open_value.grid(row=2, column=0, padx=15, pady=8, sticky="w")

closed_value = create_label(
    stats_panel, "CLOSED: 0", color=RED, bold=True
)
closed_value.grid(row=3, column=0, padx=15, pady=8, sticky="w")

error_value = create_label(
    stats_panel, "ERRORS: 0", color=YELLOW, bold=True
)
error_value.grid(row=4, column=0, padx=15, pady=8, sticky="w")

ctk.CTkFrame(
    stats_panel,
    height=2,
    fg_color=CYAN,
    corner_radius=0
).grid(
    row=5, column=0,
    sticky="ew", padx=12, pady=12
)

create_label(
    stats_panel,
    "SCAN PROGRESS",
    size=13,
    color=CYAN,
    bold=True
).grid(
    row=6, column=0,
    padx=15, pady=(0, 8), sticky="w"
)

progress_bar = ctk.CTkProgressBar(
    stats_panel,
    height=12,
    corner_radius=0,
    fg_color="#14251F",
    progress_color=GREEN
)

progress_bar.grid(
    row=7, column=0,
    padx=15, pady=5, sticky="ew"
)

progress_bar.set(0)

progress_label = create_label(
    stats_panel,
    "0%",
    size=12,
    color=GREEN,
    bold=True
)

progress_label.grid(
    row=8, column=0,
    padx=15, pady=5, sticky="e"
)


ctk.CTkFrame(
    stats_panel,
    height=2,
    fg_color=CYAN,
    corner_radius=0
).grid(row=5, column=0, sticky="ew", padx=12, pady=12)

create_label(
    stats_panel,
    "TARGET",
    size=14,
    color=CYAN,
    bold=True
).grid(row=6, column=0, padx=15, pady=(0, 8), sticky="w")

target_ip_value = create_label(
    stats_panel, "IP: -", color=WHITE
)
target_ip_value.grid(row=7, column=0, padx=15, pady=5, sticky="w")

target_ports_value = create_label(
    stats_panel, "PORTS: -", color=WHITE
)
target_ports_value.grid(row=8, column=0, padx=15, pady=5, sticky="w")

target_timeout_value = create_label(
    stats_panel, f"TIMEOUT: {SOCKET_CONFIG['SOCKET_TIMEOUT']}s",
    color=WHITE
)
target_timeout_value.grid(row=9, column=0, padx=15, pady=5, sticky="w")


# ============================================================
# FOOTER
# ============================================================

footer = ctk.CTkFrame(
    app,
    fg_color=BG,
    border_color=CYAN,
    border_width=1,
    corner_radius=0
)
footer.grid(
    row=3, column=0, columnspan=2,
    sticky="ew", padx=18, pady=(0, 18)
)
footer.grid_columnconfigure(0, weight=1)

footer_label = create_label(
    footer,
    "> In attesa di una scansione...",
    size=12,
    color=GREEN
)
footer_label.grid(row=0, column=0, padx=15, pady=12, sticky="w")


# ============================================================
# LOGICA GUI
# ============================================================

def get_input_values():
    """Valida gli input e restituisce IP e intervallo porte."""

    ip_text = ip_entry.get().strip()
    min_text = min_port_entry.get().strip()
    max_text = max_port_entry.get().strip()

    if not ip_text or not min_text or not max_text:
        raise ValueError("Compila tutti i campi.")

    try:
        ip = str(ipaddress.IPv4Address(ip_text))
    except ipaddress.AddressValueError:
        raise ValueError("Inserisci un indirizzo IPv4 valido.")

    try:
        min_port = int(min_text)
        max_port = int(max_text)
    except ValueError:
        raise ValueError("Le porte devono essere numeri interi.")

    port_min = SOCKET_CONFIG["PORT_MIN"]
    port_max = SOCKET_CONFIG["PORT_MAX"]

    if not port_min <= min_port <= port_max:
        raise ValueError(
            f"La porta iniziale deve essere tra {port_min} e {port_max}."
        )

    if not port_min <= max_port <= port_max:
        raise ValueError(
            f"La porta finale deve essere tra {port_min} e {port_max}."
        )

    if max_port < min_port:
        raise ValueError(
            "La porta finale non può essere inferiore a quella iniziale."
        )

    return ip, [min_port, max_port]


def scan_clicked():
    """Avvia una scansione senza bloccare la finestra."""

    if scan_button.cget("state") == "disabled":
        return

    try:
        ip, ports = get_input_values()
    except ValueError as exc:
        set_error(str(exc))
        return

    set_error("")
    scan_button.configure(state="disabled", text="[ SCANNING... ]")
    status_label.configure(text="[ SCANNING ]", text_color=YELLOW)
    footer_label.configure(
        text="> Scansione in corso... attendere."
    )

    target_ip_value.configure(text=f"IP: {ip}")
    target_ports_value.configure(
        text=f"PORTS: {ports[0]} - {ports[1]}"
    )

    clear_results()
    add_result_line(
        " PORT  | STATUS      | SERVICE          | ERROR",
        "header"
    )
    add_result_line(
        "-------+-------------+------------------+----------------------",
        "header"
    )
    progress_bar.set(0)
    progress_label.configure(text="SCANNING...")
    
    worker = threading.Thread(
        target=run_scan,
        args=(ip, ports),
        daemon=True
    )
    worker.start()


def run_scan(ip, ports):
    """Esegue il core dello scanner nel thread di lavoro."""

    try:
        results = scan(
            ip,
            ports,
            SOCKET_CONFIG["SOCKET_TIMEOUT"]
        )
        stats = statistiche(results)

        app.after(
            0,
            lambda: display_results(ip, ports, results, stats)
        )

    except Exception as exc:
        message = str(exc)
        app.after(0, lambda: scan_failed(message))


def display_results(ip, ports, results, stats):
    """Aggiorna la GUI nel thread principale."""

    clear_results()

    add_result_line(
        " PORT  | STATUS      | SERVICE          | ERROR",
        "header"
    )
    add_result_line(
        "-------+-------------+------------------+----------------------",
        "header"
    )

    for result in results:
        status_info = result.status

        # Nel modello ScanResult, status è un dizionario.
        status = status_info.get("status", "Unknown")
        error = status_info.get("error") or "-"
        service = getattr(result, "service", "-") or "-"

        if result.is_open():
            tag = "open"
            status_text = "OPEN"
        elif result.is_closed():
            tag = "closed"
            status_text = "CLOSED"
        else:
            tag = "error"
            status_text = status.upper()

        line = (
            f" {result.port:<5} | "
            f"{status_text:<11} | "
            f"{service:<16} | "
            f"{error}"
        )
        add_result_line(line, tag)

    scanned_value.configure(
        text=f"SCANNED: {stats['porte_scansionate']}"
    )
    open_value.configure(
        text=f"OPEN: {stats['porte_aperte']}"
    )
    closed_value.configure(
        text=f"CLOSED: {stats['porte_chiuse']}"
    )
    error_value.configure(
        text=f"ERRORS: {stats['errori']}"
    )

    status_label.configure(
        text="[ COMPLETE ]",
        text_color=GREEN
    )
    footer_label.configure(
        text="> Scansione completata. Risultati pronti."
    )

    scan_button.configure(
        state="normal",
        text="[ SCAN ]"
    )

    progress_bar.set(1)
    progress_label.configure(text="100%")


def scan_failed(message):
    """Mostra un errore e riabilita il pulsante."""

    status_label.configure(
        text="[ ERROR ]",
        text_color=RED
    )
    footer_label.configure(
        text="> Scansione non completata."
    )
    set_error(f"Errore durante la scansione: {message}")

    scan_button.configure(
        state="normal",
        text="[ SCAN ]"
    )


# ============================================================
# AVVIO
# ============================================================

app.mainloop()
