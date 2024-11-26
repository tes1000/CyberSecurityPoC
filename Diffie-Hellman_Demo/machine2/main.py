from flask import Flask, jsonify, request
import threading
import socket
import requests
import time

app = Flask(__name__)

# Parameters for Diffie-Hellman
p = 23
g = 5
private_key = 15
B = pow(g, private_key, p)

# Thread-safe storage for shared secret
shared_secret_lock = threading.Lock()
shared_secret = None  # Initialize as None


def socket_server():
    """Run the Diffie-Hellman socket server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 8001))
        s.listen()
        print("Machine2: Listening for connections on port 8001...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


def handle_client(conn, addr):
    """Handle an individual Diffie-Hellman client connection."""
    global shared_secret

    try:
        app.logger.error(f"Machine2: Connection from {addr}")
        A = int(conn.recv(1024).decode())  # Receive public key A
        conn.sendall(str(B).encode())  # Send public key B to the client

        # Calculate shared secret
        calculated_secret = pow(A, private_key, p)
        app.logger.error(f"Machine2: Shared Secret is {calculated_secret}")

        # Store shared secret in a thread-safe manner
        with shared_secret_lock:
            shared_secret = calculated_secret

        # Send shared secret to Machine3's broadcast endpoint
        requests.post("http://machine3:3000/broadcast", json={
            "sender": "10.0.0.3",
            "message": "Shared Secret:",
            "data": calculated_secret
        })
    except Exception as e:
        app.logger.error(f"Machine2: Error handling client {addr}: {e}")
    finally:
        conn.close()


@app.route('/trigger1', methods=['POST'])
def trigger1():
    """Trigger1: Start Diffie-Hellman exchange (no-op for server)."""
    return jsonify({"status": "Machine2 is listening for Diffie-Hellman connections"}), 200


@app.route('/trigger2', methods=['POST'])
def handle_rsa_exchange():
    """Trigger2: RSA Key Exchange."""
    try:
        print("Machine2: Simulating RSA key exchange...")
        requests.post("http://machine3:3000/broadcast", json={
            "sender": "Machine2",
            "message": "RSA Key Exchange Complete. Secret Collected."
        })
        return jsonify({"status": "Trigger 2 executed"}), 200
    except Exception as e:
        return jsonify({"status": f"Error: {str(e)}"}), 500


@app.route('/collect', methods=['GET'])
def collect_shared_secret():
    """Endpoint to retrieve the shared secret."""
    global shared_secret

    # Access shared secret in a thread-safe manner
    with shared_secret_lock:
        if shared_secret is not None:
            return jsonify({"shared_secret": shared_secret}), 200
        else:
            return jsonify({"error": "Shared secret not yet generated"}), 404


if __name__ == "__main__":
    # Run the socket server in a separate thread
    threading.Thread(target=socket_server, daemon=True).start()

    # Run the Flask server
    app.run(host='0.0.0.0', port=8002, debug=False)
