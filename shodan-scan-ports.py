import socket
import sys
import os
import subprocess

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

def check_port_nmap(ip, port):
    try:
        cmd = [
            "nmap",
            "-sS",
            "-Pn",
            "-T1",
            "--scan-delay", "100ms",
            "--max-retries", "5",
            "--reason",
            "-p", str(port), ip
        ]

        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        salida = resultado.stdout.lower()

        if f"{port}/tcp open" in salida:
            return "ABIERTO"
        elif f"{port}/tcp closed" in salida:
            return "CERRADO"
        elif f"{port}/tcp filtered" in salida or "host seems down" in salida or "0 hosts up" in salida:
            return "BANEADO"
        else:
            return "DESCONOCIDO"
    except subprocess.TimeoutExpired:
        return "BANEADO"
    except Exception as e:
        print(f"{YELLOW}[!] Error ejecutando nmap en {ip}:{port} - {e}{RESET}")
        return "DESCONOCIDO"

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
            estado = check_port_nmap(ip, port)
            if estado == "ABIERTO":
                print(f"{GREEN}[{ip}:{port}] {estado}{RESET}")
                resultados_abiertos.append(f"{ip}:{port}")
            elif estado == "CERRADO":
                print(f"{RED}[{ip}:{port}] {estado}{RESET}")
            elif estado == "BANEADO":
                print(f"{MAGENTA}[{ip}:{port}] {estado}{RESET}")
            else:
                print(f"{YELLOW}[{ip}:{port}] ESTADO DESCONOCIDO{RESET}")

    print(f"{YELLOW}{'#' * 74}{RESET}")
    print(f"{MAGENTA}{'@' * 74}{RESET}")
    print()

    if resultados_abiertos:
        print(f"{GREEN}Puertos abiertos{BLUE}[{len(resultados_abiertos)}]{GREEN}:{RESET}\n")
        for i, entrada in enumerate(resultados_abiertos):
            print(f"{GREEN}{entrada}{RESET}")
            if i != len(resultados_abiertos) - 1:
                print()
    else:
        print(f"{RED}No se encontraron puertos abiertos.{RESET}")

    print(f"\n{MAGENTA}{'@' * 74}{RESET}")

if __name__ == "__main__":
    try:
        mostrar_portada()

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

            break

        while True:
            archivo_ips = input("Introduce el nombre del archivo con las IPs (por defecto 'ips.txt'): ").strip()
            if not archivo_ips:
                archivo_ips = "ips.txt"

            if os.path.isfile(archivo_ips):
                break
            else:
                print(f"{RED}[!] El archivo '{archivo_ips}' no existe. Inténtalo de nuevo.{RESET}")

        scan_ips_from_file(archivo_ips, puertos)

    except KeyboardInterrupt:
        print(f"\n{RED}=========================> SALISTE DEL PROGRAMA <========================={RESET}")
        sys.exit(0)
