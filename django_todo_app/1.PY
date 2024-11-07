from cryptography.fernet import Fernet

encryption_key = Fernet.generate_key()
print(encryption_key.decode())  # Print or save as needed