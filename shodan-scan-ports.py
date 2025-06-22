import socket
import sys

# Códigos de color ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def check_port(ip, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip.strip(), port))
            return result == 0
    except Exception as e:
        print(f"{YELLOW}[!] Error con {ip}: {e}{RESET}")
        return False

def scan_ips_from_file(filename, port):
    try:
        with open(filename, 'r') as file:
            ips = file.readlines()

        for ip in ips:
            ip = ip.strip()
            if not ip:
                continue
            status = check_port(ip, port)
            if status:
                print(f"{GREEN}[{ip}:{port}] ABIERTO{RESET}")
            else:
                print(f"{RED}[{ip}:{port}] CERRADO{RESET}")
    except FileNotFoundError:
        print(f"{RED}[!] Archivo '{filename}' no encontrado.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    # Solicitar el puerto
    try:
        port = int(input("Introduce el puerto que deseas escanear: ").strip())
    except ValueError:
        print(f"{RED}[!] El puerto debe ser un número entero válido.{RESET}")
        sys.exit(1)

    # Solicitar el archivo con IPs
    archivo_ips = input("Introduce el nombre del archivo con las IPs: ").strip()

    # Ejecutar escaneo
    scan_ips_from_file(archivo_ips, port)
