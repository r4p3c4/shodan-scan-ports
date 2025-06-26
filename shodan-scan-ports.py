import socket
import sys
import os

# Códigos de color ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

def mostrar_portada():
    print(f"""{BLUE}
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@                                                                        @
@                   {RED}S H O D A N - S C A N - P O R T S{BLUE}                    @
@                                                                        @
@            {MAGENTA}Suscríbete a mí canal de YouTube para más Hacking{BLUE}           @
@                                                                        @
@{GREEN}            =========> https://cuty.io/youtubehack <=========   {BLUE}        @
@                                                                        @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
{RESET}""")

def check_port(ip, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip.strip(), port))
            return result == 0
    except Exception as e:
        print(f"{YELLOW}[!] Error con {ip}:{port} - {e}{RESET}")
        return False

def procesar_entrada_puertos(puerto_input):
    puertos = set()
    duplicados = set()
    errores = []
    partes = puerto_input.split(",")

    for parte in partes:
        parte = parte.strip()
        if "-" in parte:
            try:
                inicio, fin = map(int, parte.split("-"))
                if 1 <= inicio <= 65535 and 1 <= fin <= 65535 and inicio <= fin:
                    for p in range(inicio, fin + 1):
                        if p in puertos:
                            duplicados.add(p)
                        puertos.add(p)
                else:
                    errores.append(f"Rango inválido: {parte}")
            except ValueError:
                errores.append(f"Rango mal formado: {parte}")
        elif parte.isdigit():
            num = int(parte)
            if 1 <= num <= 65535:
                if num in puertos:
                    duplicados.add(num)
                puertos.add(num)
            else:
                errores.append(f"Puerto fuera de rango: {num}")
        else:
            errores.append(f"Formato inválido: {parte}")

    return sorted(puertos), duplicados, errores

def scan_ips_from_file(filename, ports):
    resultados_abiertos = []

    with open(filename, 'r') as file:
        ips = file.readlines()

    for ip in ips:
        ip = ip.strip()
        if not ip:
            continue

        print(f"{YELLOW}{'#' * 74}{RESET}")
        print(f"{YELLOW}IP: {ip}{RESET}")
        print(f"{BLUE}{'- ' * 37}{RESET}")

        for port in ports:
            status = check_port(ip, port)
            if status:
                print(f"{GREEN}[{ip}:{port}] ABIERTO{RESET}")
                resultados_abiertos.append(f"{ip}:{port}")
            else:
                print(f"{RED}[{ip}:{port}] CERRADO{RESET}")

    print(f"{YELLOW}{'#' * 74}{RESET}")
    print(f"{MAGENTA}{'@' * 74}{RESET}")
    if resultados_abiertos:
        print(f"{GREEN}Puertos abiertos:{RESET}")
        for entrada in resultados_abiertos:
            print(f"{GREEN}{entrada}{RESET}")
    else:
        print(f"{RED}No se encontraron puertos abiertos.{RESET}")
    print(f"{MAGENTA}{'@' * 74}{RESET}")

if __name__ == "__main__":
    try:
        mostrar_portada()

        # Bucle para validación de puertos
        while True:
            puerto_input = input("Introduce uno o más puertos o rangos (ej. 80,443,1000-1010): ").strip()
            puertos, duplicados, errores = procesar_entrada_puertos(puerto_input)

            if errores:
                print(f"{RED}[!] Se encontraron errores en la entrada de puertos:{RESET}")
                for e in errores:
                    print(f"{RED}    - {e}{RESET}")
                print(f"{YELLOW}Por favor, vuelve a introducir los puertos correctamente.{RESET}\n")
                continue

            if duplicados:
                print(f"{YELLOW}[!] Algunos puertos fueron ignorados por estar duplicados:{RESET}")
                for d in sorted(duplicados):
                    print(f"{YELLOW}    - Puerto duplicado o ya incluido en un rango: {d}{RESET}")

            break  # todo válido

        # Bucle para validación del archivo
        while True:
            archivo_ips = input("Introduce el nombre del archivo con las IPs (por defecto 'ips.txt'): ").strip()
            if not archivo_ips:
                archivo_ips = "ips.txt"

            if os.path.isfile(archivo_ips):
                break
            else:
                print(f"{RED}[!] El archivo '{archivo_ips}' no existe. Inténtalo de nuevo.{RESET}")

        # Ejecutar escaneo
        scan_ips_from_file(archivo_ips, puertos)

    except KeyboardInterrupt:
        print(f"\n{RED}=========================> SALISTE DEL PROGRAMA <========================={RESET}")
        sys.exit(0)
