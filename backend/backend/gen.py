from cryptography.fernet import Fernet

def generate_fernet_key():
    # Generate a new Fernet key
    key = Fernet.generate_key()
    print("Fernet Encryption Key:")
    print(key.decode())  # Print the key as a string for easier copying

    # Optionally save the key to a file
    with open("fernet_key.txt", "w") as file:
        file.write(key.decode())
        print("\nKey saved to 'fernet_key.txt'. Please store it securely.")

if __name__ == "__main__":
    generate_fernet_key()
