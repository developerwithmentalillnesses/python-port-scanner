import time
from config import SOCKET_CONFIG
from cli import insert_ip, insert_range, filter_choise, show_result
from scanner import scan, filter_result, statistiche

def main():
    ip = insert_ip()
    port_range = insert_range(SOCKET_CONFIG)
    filter_ch = filter_choise()
    inizio = time.perf_counter()
    scansioni = scan(ip, port_range, SOCKET_CONFIG)
    fine = time.perf_counter()
    tempo = fine - inizio
    filtro = filter_result(scansioni, filter_ch)
    stats = statistiche(scansioni)
    show_result(filtro, stats, tempo)

if __name__ == '__main__':
    main()