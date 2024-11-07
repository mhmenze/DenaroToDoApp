import secrets

def generate_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for i in range(50))

print("Your Django SECRET_KEY:")
print(generate_secret_key())