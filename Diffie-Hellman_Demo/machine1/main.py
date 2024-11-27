from flask import Flask, jsonify, request
import requests
import random

app = Flask(__name__)

shared_secret = None  # Shared secret storage


@app.route('/trigger1', methods=['POST'])
def trigger1():
    """Trigger1: Diffie-Hellman Exchange"""
    global shared_secret

    try:
        # Generate random values for p and g
        modulo = random.randint(1000, 5000)  # Random prime-like number
        base = random.randint(2, modulo - 1)

        # Generate private key
        private_key = random.randint(1, modulo - 1)

        # Calculate public value
        public_key = pow(base, private_key, modulo)

        # Send base, modulo, and public key to Machine2
        response = requests.post("http://machine3:3000/forward", json={
            "base": base,
            "modulo": modulo,
            "public_key": public_key,
            "source": "10.0.0.2",
            "destination": "10.0.0.3"
        })

        if response.status_code != 200:
            raise ValueError("Failed to exchange keys with Machine2")

        remote_public_key = response.json().get("public_key")

        if not remote_public_key:
            raise ValueError("No public key received from Machine2")

        # Calculate shared secret
        shared_secret = pow(int(remote_public_key), private_key, modulo)
        collect_shared_secret()

        return jsonify({"status": "Trigger 1 executed", "shared_secret": shared_secret}), 200
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500


@app.route('/collect', methods=['GET'])
def collect_shared_secret():
    """Endpoint to retrieve the shared secret and broadcast it."""
    if shared_secret is not None:
        try:
            # Broadcast the shared secret to Machine2
            requests.post("http://machine3:3000/broadcast", json={
                "message": "Shared Secret",
                "sender": "10.0.0.2",
                "data": shared_secret
            })
        except Exception as e:
            app.logger.error(f"Broadcast failed: {e}")

        # Return the shared secret
        return jsonify({
            "sender": "10.0.0.2",
            "message": "Shared Secret:",
            "data": shared_secret
        }), 200

    return jsonify({"error": "Shared secret not yet generated"}), 404



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
