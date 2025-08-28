"""
Prompt utilizado:

Eres un experto en redes, Necesito un programa en Python 3 que haga lo siguiente: 
    1. El programa debe enviar un mensaje caracter por caracter utilizando paquetes ICMP Echo Request (ping). 
    2. El mensaje debe recibirse como parámetro desde la línea de comandos. 
    3. Cada caracter debe enviarse en un paquete independiente. 
    4. El payload de cada paquete ICMP debe tener exactamente 48 bytes, imitando al de un ping real en Linux. 
        * Para lograr esto, se debe generar el patrón típico (0x08, 0x09, 0x0a, ...) que usa ping como relleno. 
        * El primer byte del payload debe ser sustituido por el caracter actual del mensaje. 
    5. Al final, el programa debe añadir una letra b como bandera de fin de transmisión (último caracter). 
    6. Ejemplo de uso en consola: sudo python3 icmp_sender.py "larycxpajorj h bnpdarmjm nw anmnb"
"""

# icmp_sender.py
# Envia un string caracter por caracter en el payload de un paquete ICMP
# Payload imita al ping estándar (48 bytes) con el primer byte sustituido
# Uso: sudo python3 icmp_sender.py

from scapy.all import IP, ICMP, send
import sys

def send_icmp_message(message, target="google.com"):
    # message += "b" <- gpt entendio que se agrega una b xd
    seq = 1

    for ch in message:
        # Payload base (48 bytes, como hace ping en Linux)
        payload = bytes(range(0x08, 0x08 + 48))
        # Sustituimos el primer byte por el caracter a enviar
        payload = ch.encode() + payload[1:]

        pkt = IP(dst=target)/ICMP(type=8, code=0, seq=seq)/payload
        print(f"[+] Enviando caracter '{ch}' en ICMP seq={seq}")
        send(pkt, verbose=0)
        seq += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: sudo python3 {sys.argv[0]} \"<mensaje>\" [destino]")
        sys.exit(1)

    mensaje = sys.argv[1]
    destino = "google.com"

    send_icmp_message(mensaje, destino)
