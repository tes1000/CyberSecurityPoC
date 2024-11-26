from flask import Flask, jsonify
import socket
import requests
import threading

app = Flask(__name__)

# Diffie-Hellman Parameters
p = 23
g = 5
private_key = 6

# Calculate public value
A = pow(g, private_key, p)

# Thread-safe storage for shared secret
shared_secret_lock = threading.Lock()
shared_secret = None  # Initialize as None


@app.route('/trigger1', methods=['POST'])
def trigger1():
    """Trigger1: Diffie-Hellman Exchange"""
    global shared_secret

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('machine3', 8000))
            s.sendall(str(A).encode())

            # Retry logic for receiving the response
            B = None
            for _ in range(5):  # Retry up to 5 times
                try:
                    data = s.recv(1024)  # Receive data
                    app.logger.debug(f"s.recv returned raw data: {data}")  # Log raw bytes
                    if not data:  # Check if no data was received
                        raise ConnectionError("No data received; connection may be closed")
                    data = data.decode().strip()  # Decode and strip whitespace
                    app.logger.debug(f"s.recv decoded data: {data}")  # Log decoded string
                    if not data.isdigit():  # Validate numeric content
                        raise ValueError(f"Non-numeric data received: {data}")
                    B = int(data)  # Parse into an integer
                    break  # Exit loop if successful
                except Exception as e:
                    app.logger.error(f"Retrying... {e}")

            if B is None:
                raise ValueError("Failed to receive valid public key (B) from Machine3")

            # Calculate shared secret
            calculated_secret = pow(B, private_key, p)
            app.logger.error(f"Machine1: Shared Secret is {calculated_secret}")

            # Store the shared secret in a thread-safe manner
            with shared_secret_lock:
                shared_secret = calculated_secret

            # Send shared secret to Machine3's broadcast endpoint
            requests.post("http://machine3:3000/broadcast", json={
                "sender": "10.0.0.2",
                "message": "Shared Secret:",
                "data": calculated_secret
            })
        return jsonify({"status": "Trigger 1 executed"}), 200
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"status": f"Error: {str(e)}"}), 501


@app.route('/trigger2', methods=['POST'])
def trigger2():
    """Trigger2: RSA Exchange Simulation"""
    try:
        print("Machine1: Performing RSA key exchange...")
        requests.post("http://machine3:3000/broadcast", json={
            "sender": "Machine1",
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
    app.run(host='0.0.0.0', port=8000, debug=False)
