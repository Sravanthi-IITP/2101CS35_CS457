import random
import math
import time
import psutil
import matplotlib.pyplot as plt

def is_prime(n, k=5):
   
    if n <= 1:
        return False
    for p in [2, 3, 5, 7, 11, 13]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    """Generate a prime number with the specified number of bits."""
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = extended_gcd(b, a % b)
        return g, y, x - (a // b) * y

def modinv(e, phi):
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

def generate_keypair(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    while p == q:
        q = generate_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
  
    e, n = public_key
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    max_size = (n.bit_length() // 8) - 1
    plaintext_bytes = plaintext
    ciphertext_chunks = []
    for i in range(0, len(plaintext_bytes), max_size):
        chunk = plaintext_bytes[i : i + max_size]
        chunk_int = int.from_bytes(chunk, byteorder='big')
        ciphertext_chunk = pow(chunk_int, e, n)
        ciphertext_chunks.append(str(ciphertext_chunk))
    return ' '.join(ciphertext_chunks)

def decrypt(private_key, ciphertext):
    
    d, n = private_key
    ciphertext_chunks = ciphertext.split()
    decrypted_bytes = b""
    for chunk in ciphertext_chunks:
        chunk_int = int(chunk)
        plaintext_int = pow(chunk_int, d, n)
        decrypted_bytes += plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, byteorder='big')
    return decrypted_bytes

def file_encrypt_decrypt(input_file, output_file, key, mode='encrypt'):
    """Encrypt or decrypt a file."""
    with open(input_file, 'rb') as f:
        data = f.read()
    if mode == 'encrypt':
        processed_data = encrypt(key, data)
        with open(output_file, 'w') as f:
            f.write(processed_data)
    elif mode == 'decrypt':
        with open(input_file, 'r') as f:
            encrypted_data = f.read()
        processed_data = decrypt(key, encrypted_data)
        with open(output_file, 'wb') as f:
            f.write(processed_data)
    else:
        raise ValueError("Invalid mode. Use 'encrypt' or 'decrypt'.")

def performance_test():
    bits = 2048
    public_key, private_key = generate_keypair(bits)
    message_sizes = [64, 128, 256, 512, 1024, 2048]
    encryption_times = []
    decryption_times = []
    memory_usages = []
    cpu_usages = []
    for size in message_sizes:
        message = b'a' * size
        start_time = time.time()
        ciphertext = encrypt(public_key, message)
        encryption_times.append(time.time() - start_time)
        start_time = time.time()
        decrypted_message = decrypt(private_key, ciphertext)
        decryption_times.append(time.time() - start_time)
        memory_usages.append(psutil.Process().memory_info().rss / 1024 / 1024)
        cpu_usages.append(psutil.cpu_percent(interval=1))
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.plot(message_sizes, encryption_times, marker='o')
    plt.title('Encryption Time vs Message Size')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Time (seconds)')
    plt.subplot(2, 2, 2)
    plt.plot(message_sizes, decryption_times, marker='o')
    plt.title('Decryption Time vs Message Size')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Time (seconds)')
    plt.subplot(2, 2, 3)
    plt.plot(message_sizes, memory_usages, marker='o')
    plt.title('Memory Usage vs Message Size')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('Memory Usage (MB)')
    plt.subplot(2, 2, 4)
    plt.plot(message_sizes, cpu_usages, marker='o')
    plt.title('CPU Usage vs Message Size')
    plt.xlabel('Message Size (bytes)')
    plt.ylabel('CPU Usage (%)')
    plt.tight_layout()
    plt.show()

def main():
    bits = 2048
    public_key, private_key = generate_keypair(bits)
    print("Public Key:", public_key)
    print("Private Key:", private_key)
    input_file = 'input.txt'
    encrypted_file = 'encrypted.txt'
    decrypted_file = 'decrypted.txt'
    file_encrypt_decrypt(input_file, encrypted_file, public_key, mode='encrypt')
    print(f"File '{input_file}' encrypted to '{encrypted_file}'.")
    file_encrypt_decrypt(encrypted_file, decrypted_file, private_key, mode='decrypt')
    print(f"File '{encrypted_file}' decrypted to '{decrypted_file}'.")
    performance_test()

if __name__ == "__main__":
    main()
