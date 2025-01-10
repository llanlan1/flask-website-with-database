from werkzeug.security import generate_password_hash

# Generate a password hash for 'tester'
password = 'super-secret'
hashed_password = generate_password_hash(password)
print(hashed_password)

# Generate a password hash for 'admin'
password = 'important!'
hashed_password = generate_password_hash(password)
print(hashed_password)


pbkdf2:sha256:260000$0ekJZYcP3HUQpqsN$a592424ef23346055fbcef062610a86e8c6e358139aa914d8851b37a3d11460a
pbkdf2:sha256:260000$Jk9S1so3UKhvaba8$711c1a9d4b282d9afc74784efaa3bb32be386129a65fa40a987530d54e8fbae2

INSERT INTO users (username, password_hash) VALUES ('tester', 'pbkdf2:sha256:260000$0ekJZYcP3HUQpqsN$a592424ef23346055fbcef062610a86e8c6e358139aa914d8851b37a3d11460a');
INSERT INTO users (username, password_hash) VALUES ('admin', 'pbkdf2:sha256:260000$Jk9S1so3UKhvaba8$711c1a9d4b282d9afc74784efaa3bb32be386129a65fa40a987530d54e8fbae2');
