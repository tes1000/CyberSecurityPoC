import socket
import time

# Diffie-Hellman Parameters
p = 23  
g = 5   
private_key = 15  

B = pow(g, private_key, p)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('0.0.0.0', 8001))
    s.listen()
    conn, addr = s.accept()
    with conn:
        A = int(conn.recv(1024).decode())
        # print(f"Machine2: Received public value A = {A}")  # Log received public key
        conn.sendall(str(B).encode())
        # print(f"Machine2: Sent public value B = {B}")  # Log public key
        
time.sleep(5)
# Calculate shared secret
shared_secret = pow(A, private_key, p)
print(f"Machine2: Shared Secret is {shared_secret}")
