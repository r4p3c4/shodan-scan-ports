import socket
import sys

# Códigos de color ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_port(ip, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip.strip(), port))
            return result == 0
    except Exception as e:
        print(f"{YELLOW}[!] Error con {ip}:{port} - {e}{RESET}")
        return False

def scan_ips_from_file(filename, ports):
    try:
        with open(filename, 'r') as file:
            ips = file.readlines()

        for ip in ips:
            ip = ip.strip()
            if not ip:
                continue

            # Encabezado: línea amarilla + IP + línea azul con "- -"
            print(f"{YELLOW}{'#' * 66}{RESET}")
            print(f"{YELLOW}IP: {ip}{RESET}")
            print(f"{BLUE}{'- ' * 33}{RESET}")  # 33 * 2 = 66 chars wide

            for port in ports:
                status = check_port(ip, port)
                if status:
                    print(f"{GREEN}[{ip}:{port}] ABIERTO{RESET}")
                else:
                    print(f"{RED}[{ip}:{port}] CERRADO{RESET}")

        # Línea final global
        print(f"{YELLOW}{'#' * 66}{RESET}")

    except FileNotFoundError:
        print(f"{RED}[!] Archivo '{filename}' no encontrado.{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    # Solicitar los puertos
    puerto_input = input("Introduce uno o más puertos separados por comas (ej. 80,443,3389): ").strip()
    try:
        puertos = [int(p.strip()) for p in puerto_input.split(",") if p.strip().isdigit()]
        if not puertos:
            raise ValueError
    except ValueError:
        print(f"{RED}[!] Debes introducir al menos un puerto válido (números enteros).{RESET}")
        sys.exit(1)

    # Solicitar el archivo con IPs
    archivo_ips = input("Introduce el nombre del archivo con las IPs (ej. lista.txt): ").strip()

    # Ejecutar escaneo
    scan_ips_from_file(archivo_ips, puertos)
