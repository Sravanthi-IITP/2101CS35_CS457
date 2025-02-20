import os
import base64
import time
import psutil
import matplotlib.pyplot as plt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Constants for cryptographic operations
SALT_LENGTH = 16
KEY_LENGTH = 32  # 256-bit key size
BLOCK_SIZE = 16  # AES block size
ITERATION_COUNT = 100000

def generate_encryption_key(password: str) -> bytes:
    """Generate a secure encryption key from the password using PBKDF2 with SHA-256."""
    salt = os.urandom(SALT_LENGTH)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATION_COUNT,
        backend=default_backend()
    )
    derived_key = kdf.derive(password.encode())
    return salt + derived_key  # Return key along with the salt for storage

def apply_padding(data: bytes) -> bytes:
    """Ensure that the data is a multiple of the block size by adding padding."""
    padding_length = BLOCK_SIZE - len(data) % BLOCK_SIZE
    padding = bytes([padding_length] * padding_length)
    return data + padding

def remove_padding(data: bytes) -> bytes:
    """Remove padding from data after decryption."""
    padding_length = data[-1]
    return data[:-padding_length]

def encrypt_data_gcm(plaintext: bytes, key: bytes) -> str:
    """Encrypt the plaintext with AES-256 in GCM mode and return a Base64 encoded string with the tag."""
    iv = os.urandom(BLOCK_SIZE)  # Generate a random initialization vector
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    paddeddata=apply_padding(plaintext)
    ciphertext = encryptor.update(paddeddata) + encryptor.finalize()
    return base64.b64encode(iv + encryptor.tag + ciphertext).decode('utf-8')

def decrypt_data_gcm(ciphertext_base64: str, key: bytes) -> bytes:
    """Decrypt a Base64 encoded ciphertext using AES-256-GCM and return the plaintext."""
    data = base64.b64decode(ciphertext_base64)
    iv = data[:BLOCK_SIZE]
    tag = data[BLOCK_SIZE:BLOCK_SIZE + 16]
    ciphertext = data[BLOCK_SIZE + 16:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    paddeddata= decryptor.update(ciphertext) + decryptor.finalize()
    return remove_padding(paddeddata)

def save_encrypted_data_to_file(filename: str, data: str):
    """Save encrypted data to a file as a Base64 string."""
    with open(filename, 'w') as f:
        f.write(data)

def load_encrypted_data_from_file(filename: str) -> str:
    """Load encrypted data from a Base64 encoded file."""
    with open(filename, 'r') as f:
        return f.read()

def encrypt_file_to_base64(input_file: str, output_file: str, password: str):
    """Encrypt a file and save the encrypted data as Base64."""
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    key = generate_encryption_key(password)
    encrypted_text = encrypt_data_gcm(plaintext, key[16:])  # Use the key excluding the salt
    save_encrypted_data_to_file(output_file, base64.b64encode(key).decode('utf-8') + ":" + encrypted_text)

def decrypt_file_from_base64(input_file: str, output_file: str, password: str):
    """Decrypt a Base64 encoded file and save the decrypted content."""
    encrypted_data = load_encrypted_data_from_file(input_file)
    key_base64, ciphertext_base64 = encrypted_data.split(":")
    salt = base64.b64decode(key_base64)[:SALT_LENGTH]
    key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATION_COUNT,
        backend=default_backend()
    ).derive(password.encode())
    decrypted_content = decrypt_data_gcm(ciphertext_base64, key)
    with open(output_file, 'wb') as f:
        f.write(decrypted_content)

def evaluate_performance():
    """Test and evaluate the performance of encryption and decryption."""
    input_sizes = [2**10, 2**15, 2**20]  # Test with 1KB, 32KB, and 1MB
    encryption_times = []
    decryption_times = []
    memory_usage = []
    cpu_usage = []

    password = "testpassword"

    for size in input_sizes:
        # Generate random data to test
        plaintext = os.urandom(size)

        # Measure memory and CPU usage before the operation
        process = psutil.Process()
        memory_before = process.memory_info().rss
        cpu_before = process.cpu_percent(interval=None)

        # Measure encryption time
        start_time = time.time()
        key = generate_encryption_key(password)
        encrypt_data_gcm(plaintext, key[16:])
        encryption_duration = time.time() - start_time

        # Measure memory and CPU usage after encryption
        memory_after = process.memory_info().rss
        cpu_after = process.cpu_percent(interval=None)

        # Store the results for encryption
        encryption_times.append(encryption_duration)
        memory_usage.append(memory_after - memory_before)
        cpu_usage.append(cpu_after - cpu_before)

        # Measure decryption time
        ciphertext = encrypt_data_gcm(plaintext, key[16:])
        start_time = time.time()
        decrypt_data_gcm(ciphertext, key[16:])
        decryption_duration = time.time() - start_time
        decryption_times.append(decryption_duration)

    # Plot performance results
    plt.figure(figsize=(15, 10))

    # Plot encryption and decryption times
    plt.subplot(2, 2, 1)
    plt.plot(input_sizes, encryption_times, label="Encryption Time", marker="o")
    plt.plot(input_sizes, decryption_times, label="Decryption Time", marker="o")
    plt.xlabel("Input Size (Bytes)")
    plt.ylabel("Time (Seconds)")
    plt.title("Encryption and Decryption Time")
    plt.legend()
    plt.grid()

    # Plot memory usage
    plt.subplot(2, 2, 2)
    plt.bar([str(size) for size in input_sizes], memory_usage, color="grey")
    plt.xlabel("Input Size (Bytes)")
    plt.ylabel("Memory Usage (Bytes)")
    plt.title("Memory Usage")
    plt.grid()

    # Plot CPU usage
    plt.subplot(2, 2, 3)
    plt.bar([str(size) for size in input_sizes], cpu_usage, color="lightyellow")
    plt.xlabel("Input Size (Bytes)")
    plt.ylabel("CPU Usage (%)")
    plt.title("CPU Usage")
    plt.grid()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    try:
        # Encrypt and decrypt a sample file
        encrypt_file_to_base64("input.txt", "encrypted_output.txt", "testpassword")
        print("File encryption completed successfully.")
        
        decrypt_file_from_base64("encrypted_output.txt", "decrypted_output.txt", "testpassword")
        print("File decryption completed successfully.")
        
        # Verify if the decrypted file matches the original
        with open("input.txt", "rb") as original_file:
            original_data = original_file.read()
        
        with open("decrypted_output.txt", "rb") as decrypted_file:
            decrypted_data = decrypted_file.read()
        
        if original_data == decrypted_data:
            print("Decryption verified: content matches the original.")
        else:
            print("Decryption failed: content does not match the original.")

        # Run performance tests
        evaluate_performance()

    except Exception as e:
        print(f"Error occurred: {e}")
