from werkzeug.security import generate_password_hash

hashed_password = generate_password_hash("editor123")  
print(hashed_password)  # Copy this and use it in the SQL query
