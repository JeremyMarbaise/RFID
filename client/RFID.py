import serial
import requests
import json
import time
import jwt
import datetime

# Configuration
ARDUINO_PORT = 'COM10'  # Change to your port
BAUD_RATE = 115200
API_URL = "https://authentication-server-gtgcc2bwapcddzhj.germanywestcentral-01.azurewebsites.net/auth/login"
API_DELEVERIES_URL="https://apiserver-bsdfh4gmduh8bsep.francecentral-01.azurewebsites.net/v1/me/order/deliveries"
JWT_SECRET = "3Y1rsl+Yv4YG0OUT+pdKf1FNQ+ms2RbrZWbJroT1anySlxtaFn4NVxyWuKrSE6nw,"  # Should match server
JWT_ISSUER = "your_issuer_name"
JWT_AUDIENCE = "your_audience_name"
JWT_EXPIRY_MINUTES = 480  # Or whatever your server uses




def main():
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow serial connection to initialize
    
    while True:
        print("\nNFC Client ID Manager")
        print("1. Read Client ID from NFC")
        print("2. Write Client ID to NFC")
        print("3. Generate JWT from NFC")
        print("4. Exit")
        
        choice = input("Select action: ")
        
        if choice == "1":
            read_client_id(ser)
        elif choice == "2":
            write_client_id(ser)
        elif choice == "3":
            generate_jwt_from_nfc(ser)
        elif choice == "4":
            break
        else:
            print("Invalid choice")

def read_client_id(ser):
    ser.write(b"READ\n")
    while True:
        line = ser.readline().decode().strip()
        if line.startswith("CLIENT_ID:"):
            print(f"Client ID: {line[10:]}")
            break
        elif line:
            print(line)

def write_client_id(ser):
    client_id = input("Enter Client ID to write: ")
    if not client_id:
        print("Client ID cannot be empty")
        return
    
    if len(client_id) > 16:
        print("Client ID too long (max 15 chars)")
        return
    
    print("Place NFC tag near reader...")
    ser.write(f"WRITE:{client_id}\n".encode())
    
    while True:
        line = ser.readline().decode().strip()
        if line == "WRITE_SUCCESS":
            print("Write successful!")
            break
        elif line == "WRITE_FAILED":
            print("Write failed")
            break
        elif line:
            print(line)

def generate_jwt_from_nfc(ser):
    print("Place NFC tag near reader...")
    ser.write(b"READ\n")
    
    client_id = None
    while True:
        line = ser.readline().decode().strip()
        if line.startswith("CLIENT_ID:"):
            client_id = line[10:]
            break
        elif line:
            print(line)
    
    if client_id:
        print(f"\nClient ID found: {client_id}")
        jwt=generate_local_jwt(client_id, "DELIVERY_AGENT")
        headers = {
        "Authorization": f"Bearer {jwt}"
        }
        response = requests.get(API_DELEVERIES_URL, headers=headers)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4))  # or response.text
        else:
            print(f"Request failed: {response.status_code} - {response.text}")
        
        

  
    
def generate_local_jwt(client_id, role):
    now = datetime.datetime.utcnow()
    payload = {
        'sub': client_id,
        'Role': role,
        'iss': JWT_ISSUER,
        'aud': JWT_AUDIENCE,
        'exp': now + datetime.timedelta(minutes=JWT_EXPIRY_MINUTES)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

if __name__ == "__main__":
    main()