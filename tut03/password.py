import re

def validate_password(password, criteria):
    if len(password) < 8:
        print(f"Password '{password}' is too short (less than 8 characters). Skipping.")
        return False  # Indicate skip, but don't count as invalid yet

    valid = True

    if 1 in criteria:  # Uppercase
        if not re.search(r"[A-Z]", password):
            valid = False
    if 2 in criteria:  # Lowercase
        if not re.search(r"[a-z]", password):
            valid = False
    if 3 in criteria:  # Numbers
        if not re.search(r"[0-9]", password):
            valid = False
    if 4 in criteria:  # Special characters (!, @, #)
        if not re.search(r"^[a-zA-Z0-9!@#]*$", password):  # Check only allowed special chars
            valid = False
        if password.count('!') + password.count('@') + password.count('#') > 3:
            valid = False

    return valid


# Part 2: Password Validator with Skip from user input
def validate_from_input():
    criteria = list(map(int, input("Enter criteria numbers (1-4, comma-separated): ").split(",")))

    num_passwords = int(input("Enter the number of passwords to check: "))
    password_list = []
    for i in range(num_passwords):
        password = input(f"Enter password {i+1}: ")
        password_list.append(password)

    for password in password_list:
        if validate_password(password, criteria):
            print(f"Password '{password}' is valid.")
        elif len(password) >= 8:  # Only print invalid if length is sufficient.
            print(f"Password '{password}' is invalid.")


# Part 3: Password Validator with Skip from input file input.txt
def validate_from_file():
    try:
        with open("input.txt", "r") as f:
            passwords = [line.strip() for line in f]
    except FileNotFoundError:
        print("Error: input.txt not found. Create the file with passwords.")
        return

    criteria = list(map(int, input("Enter criteria numbers (1-4, comma-separated): ").split(",")))
    valid_count = 0
    invalid_count = 0
    skipped_count = 0

    for password in passwords:
        result = validate_password(password, criteria)
        if result is True:
            valid_count += 1
        elif result is False and len(password) >= 8:  # Only count as invalid if length is sufficient.
            invalid_count += 1
        else:  # Implicitly handles the skipped passwords
            skipped_count += 1

    print(f"Total Valid Passwords: {valid_count}")
    print(f"Total Invalid Passwords: {invalid_count}")
    print(f"Total Skipped Passwords: {skipped_count}")


# Choose which part to run:
choice = input("Enter 1 for input validation or 2 for file validation: ")

if choice == "1":
    validate_from_input()
elif choice == "2":
    validate_from_file()
else:
    print("Invalid choice.")