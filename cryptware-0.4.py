#File-security-version-0.4

#Saving the key in the server to improve security and limit accessebility

from cryptography.fernet import Fernet, InvalidToken
from pathlib import Path
import requests
from getpass import getpass

SERVER_URL = "http://127.0.0.1:5000/get_key"



def get_key(need_password=True):
    if need_password:
        password = getpass("Enter your password: ")
    else:
        password = None
    
    try:
        response = requests.post(
            SERVER_URL,
            json={"password": password},
            timeout=5
        )
        
        if response.status_code == 200:
            print("[+] Key has been created")
            return response.json()["key"].encode()
        else:
            print("Wrong password or server error")
            return None
        
    except Exception as e:
        print("[!] Could not connect to the server")
        print(e)
        return None



def encrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file: #r b = read, bytes - read data in bytes
        file_data = file.read()
    
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file: # w b = write, bytes - write data in bytes
        file.write(encrypted_data)
        
def decrypt(filename, key):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    
    original_data = f.decrypt(encrypted_data)
    
    with open(filename, "wb") as file:
        file.write(original_data)


def encrypt_folder(foldername, key):
    f = Fernet(key)
    
    for child in foldername.glob("*"):
        if child.is_file():
            try:
                f.decrypt(child.read_bytes()) #checks if content is encrypted without saving data to the file as function. is decription succesfull prints(Error)
                print(f"[*] Already Encrypted {child}")
            except InvalidToken:
                encrypt(child, key)
                print(f"[*] Encrypting: {child}")
            
        elif child.is_dir():
            encrypt_folder(child, key)
            
            
def decrypt_folder(foldername, key):
    for child in foldername.glob("*"):
        if child.is_file():
            print(f"[*] Decrypting: {child}")
            decrypt(child, key)
            
        elif child.is_dir():
            decrypt_folder(child, key)


def main():  
    target = Path(input("Input target name: "))
    
    action = input("Encrypt or Decrypt? [e/d]")
    
    if action == "e":
        key = get_key(need_password=False)
        if target.is_file():
            encrypt(target, key)
        elif target.is_dir():
            encrypt_folder(target, key)
            
    elif action == "d":
        key = get_key(need_password=True)     
        if target.is_file():
            decrypt(target, key)
        elif target.is_dir():
            decrypt_folder(target, key)
            
if __name__ == "__main__":
    main()