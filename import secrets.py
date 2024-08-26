import secrets

# Generate a secure random token
token = secrets.token_hex(32)
print(token)