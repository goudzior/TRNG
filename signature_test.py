import hashlib
import sympy
import generator
import random

# Funkcja, która wylicza skrót (hash) wiadomości
def hash_message(message: str) -> str:
    hash_object = hashlib.sha256()
    hash_object.update(message.encode('utf-8'))
    return hash_object.hexdigest()

def generate_rsa_key_pair():
    def select_prime():
        while True:
            prime_list = generator.generator()  # Generuj nową listę liczb pierwszych
            for prime in prime_list:
                if sympy.isprime(prime):
                    return prime
        # Jeśli nie znaleziono liczby pierwszej na liście, kontynuuj generowanie nowej listy

    # Generujemy dwie liczby pierwsze p i q
    p = select_prime()
    q = select_prime()
    
    while p == q:  # Sprawdź, czy p i q są różne, jeśli nie, wybierz nowe q
        q = select_prime()
    
    # Obliczamy wartość N (klucz publiczny)
    n = p * q
    
    # Obliczamy funkcję Eulera
    phi_n = (p - 1) * (q - 1)
    
    # Wybieramy liczbę e (public_exponent) względnie pierwszą z phi_n
    e = 257
    
    # Obliczamy liczbę d (private_exponent) będącą odwrotnością modulo e względem phi_n
    d = pow(e, -1, phi_n)
    
    # Zwracamy klucze publiczny i prywatny
    public_key = (n, e)
    private_key = (n, d)
    
    return public_key, private_key

# Funkcja szyfrująca wiadomość za pomocą klucza publicznego
def encrypt_message(message: str, public_key: tuple) -> int:
    n, e = public_key
    message_hash = int(hash_message(message), 16)
    encrypted_message = pow(message_hash, e, n)
    return encrypted_message

# Funkcja deszyfrująca wiadomość za pomocą klucza prywatnego
def decrypt_message(encrypted_message: int, private_key: tuple) -> str:
    n, d = private_key
    decrypted_message_hash = pow(encrypted_message, d, n)
    decrypted_message_hash_hex = hex(decrypted_message_hash)[2:]
    return decrypted_message_hash_hex.zfill(64)

# Główna funkcja
def main():
    message = "test message"
    message_hash = hash_message(message)
    print(f"Skrót wiadomości: {message_hash}")

    public_key, private_key = generate_rsa_key_pair()
    print(f"Klucz publiczny: {public_key}")
    print(f"Klucz prywatny: {private_key}")

    encrypted_message = encrypt_message(message, public_key)
    print(f"Zaszyfrowany skrót wiadomości: {encrypted_message}")

    decrypted_message_hash = decrypt_message(encrypted_message, private_key)
    print(f"Odszyfrowany skrót wiadomości: {decrypted_message_hash}")

    # Sprawdzamy, czy odszyfrowany skrót jest taki sam jak oryginalny skrót
    if decrypted_message_hash == message_hash:
        print("Skrót wiadomości został poprawnie odszyfrowany.")
    else:
        print("Skrót wiadomości NIE został poprawnie odszyfrowany.")

    print ("------TEST 1: próba odszyfrowania innym kluczem------")
    _, private_key2 = generate_rsa_key_pair()
    decrypted_message_hash2 = decrypt_message(encrypted_message, private_key2)
    print(f"Odszyfrowany skrót wiadomości: {decrypted_message_hash}")

    if decrypted_message_hash2 == message_hash:
        print("Skrót wiadomości został poprawnie odszyfrowany.")
    else:
        print("Skrót wiadomości NIE został poprawnie odszyfrowany.")

    print ("------TEST 2: Test integralności------")
    public_key2, private_key2 = generate_rsa_key_pair()
    decrypted_message_hash_different = decrypt_message(encrypted_message, private_key2)
    print(f"Odszyfrowany skrót wiadomości: {decrypted_message_hash}")
    
    if decrypted_message_hash_different == message_hash:
        print("Skrót wiadomości został poprawnie odszyfrowany.")
    else:
        print("Skrót wiadomości NIE został poprawnie odszyfrowany.")

    message2 = "test message123"
    message_hash2 = hash_message(message2)
    print(f"Skrót wiadomości: {message_hash2}")

    encrypted_message2 = encrypt_message(message2, public_key2)
    print(f"Zaszyfrowany skrót wiadomości: {encrypted_message2}")

    decrypted_message_hash = decrypt_message(encrypted_message2, private_key2)
    print(f"Odszyfrowany skrót wiadomości: {decrypted_message_hash2}")

    if decrypted_message_hash2 == message_hash2:
        print("Skrót wiadomości został poprawnie odszyfrowany.")
    else:
        print("Skrót wiadomości NIE został poprawnie odszyfrowany.")

    

if __name__ == "__main__":
    main()
