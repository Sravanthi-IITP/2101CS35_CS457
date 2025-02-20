import hashlib
import os
import json

# File to store user data
USER_DATA_FILE = 'user_data.json'

# Load user data from file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save user data to file
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_data, file)

# Generate a salt
def generate_salt():
    return os.urandom(16).hex()

# Hash the password with SHA-256 and a salt
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# Register a new user
def register_user(username, password):
    user_data = load_user_data()
    if username in user_data:
        print("Username already exists.")
        return False
    
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    user_data[username] = {'salt': salt, 'hashed_password': hashed_password}
    save_user_data(user_data)
    print("User registered successfully.")
    return True

# Authenticate a user
def authenticate_user(username, password):
    user_data = load_user_data()
    if username not in user_data:
        print("Username not found.")
        return False
    
    salt = user_data[username]['salt']
    hashed_password = user_data[username]['hashed_password']
    if hash_password(password, salt) == hashed_password:
        print("Login successful.")
        return True
    else:
        print("Incorrect password.")
        return False

# Main function to demonstrate the system
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
        
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            authenticate_user(username, password)
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()