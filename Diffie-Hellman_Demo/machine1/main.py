from flask import Flask, jsonify
import socket
import requests

app = Flask(__name__)

p = 23
g = 5
private_key = 6

# Calculate public value
A = pow(g, private_key, p)

@app.route('/trigger1', methods=['POST'])
def trigger1():
    """Trigger1: Diffie-Hellman"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('machine3', 8000))
            s.sendall(str(A).encode())

            # Retry logic for receiving the response
            for _ in range(3):  # Retry up to 3 times
                try:
                    B = int(s.recv(1024).decode())
                    break
                except Exception as e:
                    print(f"Retrying... {e}")

            shared_secret = pow(B, private_key, p)
            print(f"Machine1: Shared Secret is {shared_secret}")

            # Send shared secret to Machine3's broadcast endpoint
            requests.post("http://machine3:3000/broadcast", json={
                "sender": "10.0.0.2",
                "message": f"Shared Secret: {shared_secret}"
            })
        return jsonify({"status": "Trigger 1 executed"}), 200
    except Exception as e:
        return jsonify({"status": f"Error: {str(e)}"}), 500

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)
