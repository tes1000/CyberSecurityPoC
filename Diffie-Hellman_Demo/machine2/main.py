from flask import Flask, jsonify, request
import random
import requests

app = Flask(__name__)

shared_secret = None  # Shared secret storage


@app.route('/dh_exchange', methods=['POST'])
def dh_exchange():
    """Handle Diffie-Hellman Exchange"""
    global shared_secret

    try:
        data = request.json
        base = data.get("base")
        modulo = data.get("modulo")
        remote_public_key = data.get("public_key")
        #source = data.get("source")
        
        if not base or not modulo or not remote_public_key:
            raise ValueError("Invalid input for Diffie-Hellman exchange")

        # Generate private key
        private_key = random.randint(1, modulo - 1)

        # Calculate public value
        public_key = pow(base, private_key, modulo)

        # Calculate shared secret
        shared_secret = pow(remote_public_key, private_key, modulo)
        app.logger.info(f"Machine2: Shared Secret is {shared_secret}")

        # Send shared secret to Machine3
        requests.post("http://machine3:3000/finalKey", json={
            "public_key": public_key,
            "source": "10.0.0.3",
            "destination": "10.0.0.2"
        })
        
        collect_shared_secret()
        
        return jsonify({"public_key": public_key}), 200
    except Exception as e:
        app.logger.error(f"Error during Diffie-Hellman exchange: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500


@app.route('/collect', methods=['GET'])
def collect_shared_secret():
    """Endpoint to retrieve the shared secret and broadcast it."""
    if shared_secret is not None:
        try:
            requests.post("http://machine3:3000/broadcast", json={
                "message": "Shared Secret",
                "sender": "10.0.0.3",
                "data": shared_secret
            })
        except Exception as e:
            app.logger.error(f"Broadcast failed: {e}")

        # Return the shared secret
        return jsonify({
            "sender": "10.0.0.3",
            "message": "Shared Secret:",
            "data": shared_secret
        }), 200

    return jsonify({"error": "Shared secret not yet generated"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
