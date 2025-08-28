import argparse

def cifrado_cesar(texto: str, corrimiento: int) -> str:
    resultado = ""
    for caracter in texto:
        if caracter.isupper():
            resultado += chr((ord(caracter) - 65 + corrimiento) % 26 + 65)
        elif caracter.islower():
            resultado += chr((ord(caracter) - 97 + corrimiento) % 26 + 97)
        else:
            resultado += caracter
    return resultado

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cifrado César en Python")
    parser.add_argument("texto", help="Texto a cifrar")
    parser.add_argument("corrimiento", type=int, help="Número de posiciones para el corrimiento")
    args = parser.parse_args()

    cifrado = cifrado_cesar(args.texto, args.corrimiento)
    print(f"Texto cifrado: {cifrado}")
