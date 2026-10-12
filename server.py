from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

KEY_FILE = "server_key.key"

if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    
    print(f"[*] New key has been created: {key}")
    
else:
    with open(KEY_FILE, "rb") as key:
        key=key.read()

SECRET_PASSWORD = "1234"

@app.route("/get_key", methods=["POST"])
def get_key():
    data = request.get_json()
    password = data.get("password")
    
    if password is not None:
        if password != SECRET_PASSWORD:
            return jsonify({"error": "Wrong password!"}), 401
        
    return jsonify({"key": key.decode()})
    
if __name__ == "__main__":
    print("SERVER IS RUNNING")
    app.run(host="127.0.0.1", port=5000)