import socket
import threading

def forward(source, destination):
    try:
        while True:
            data = source.recv(1024)
            if not data:
                print(f"Machine3: Connection closed by {source.getpeername()}")
                break
            # Identify which machine sent the data
            source_address = source.getpeername()[0]
            print(f"Machine3: Intercepted data from {source_address}: {data.decode()}")
            destination.sendall(data)
    except (ConnectionResetError, OSError) as e:
        pass
    finally:
        source.close()
        destination.close()
        
# Set up listener for Machine1
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
    s1.bind(('0.0.0.0', 8000))  # Listen for Machine1
    s1.listen()
    print("Machine3: Listening for Machine1 on port 8000...")
    conn1, addr1 = s1.accept()
    print(f"Machine3: Connection from Machine1 ({addr1})")

    # Connect to Machine2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        s2.connect(('machine2', 8001))  # Forward traffic to Machine2
        print("Machine3: Connected to Machine2 on port 8001")

        # Start forwarding traffic
        threading.Thread(target=forward, args=(conn1, s2)).start()
        threading.Thread(target=forward, args=(s2, conn1)).start()
