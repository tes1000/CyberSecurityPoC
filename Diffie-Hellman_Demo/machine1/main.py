import socket
import time

p = 23  
g = 5  
private_key = 6 

A = pow(g, private_key, p)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('machine3', 8000))
    s.sendall(str(A).encode())
    # print(f"Machine1: Sent public value A = {A}")  # Log public key
    B = int(s.recv(1024).decode())
    
time.sleep(5)
shared_secret = pow(B, private_key, p)
print(f"Machine1: Shared Secret is {shared_secret}")
