#!/usr/bin/env python3
# icmp_receiver.py
# Requiere: pip install scapy colorama

"""
Prompt utilizado:

Generar un programa, en python3, que permita obtener un mensaje ICMP (basado en un archivo de captura de wireshark) 
transmitido con las siguientes caracteristicas: 
    1. Cada caracter debe enviarse en un paquete independiente. 
    2. El payload de cada paquete ICMP debe tener exactamente 48 bytes, imitando al de un ping real en Linux. 
        * Para lograr esto, se debe generar el patrón típico (0x08, 0x09, 0x0a, ...) que usa ping como relleno. 
        * El primer byte del payload debe ser sustituido por el caracter actual del mensaje.

Como no se sabe cual es el corrimiento utilizado (se usó cifrado cesar), 
genere todas las combinaciones posibles e imprimalas, indicando en verde la opción más probable de ser el mensaje en claro.
"""

import sys
from scapy.all import rdpcap, ICMP
from colorama import Fore, Style

def extract_chars_from_pcap(pcap_file):
    """
    Extrae los caracteres del primer byte del payload de cada paquete ICMP.
    Solo considera ICMP Echo Request.
    """
    packets = rdpcap(pcap_file)
    chars = []
    for pkt in packets:
        if ICMP in pkt and hasattr(pkt[ICMP], "load"):
            payload = bytes(pkt[ICMP].load)
            if len(payload) >= 1:
                chars.append(chr(payload[0]))
    return chars

def caesar_decrypt(text, shift):
    decrypted = ""
    for c in text:
        if 'a' <= c <= 'z':
            decrypted += chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            decrypted += chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        else:
            decrypted += c
    return decrypted

def guess_message(texts):
    """
    Intenta adivinar cuál es el texto más probable usando heurística simple:
    el que tiene más espacios y letras frecuentes en inglés.
    """
    scores = []
    for t in texts:
        score = t.count(' ') + sum(t.count(c) for c in 'etaoinshrdlu')
        scores.append(score)
    best_index = scores.index(max(scores))
    return best_index

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python3 {sys.argv[0]} <archivo.pcap>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    chars = extract_chars_from_pcap(pcap_file)
    encrypted_msg = ''.join(chars) # .rstrip('b')  # eliminar bandera final (no hay que hacer eso ya que la b es parte del mensaje)

    print(f"Mensaje cifrado extraído: {encrypted_msg}\n")
    
    # Generar todas las combinaciones posibles de César
    all_decrypts = [caesar_decrypt(encrypted_msg, shift) for shift in range(26)]

    best_index = guess_message(all_decrypts)

    print("Posibles decodificaciones:")
    for i, dec in enumerate(all_decrypts):
        if i == best_index:
            print(Fore.GREEN + f"Shift {i}: {dec}" + Style.RESET_ALL)
        else:
            print(f"Shift {i}: {dec}")
