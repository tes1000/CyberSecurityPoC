import threading
from flask import Flask, jsonify, render_template, request
import requests
import time

# Shared data structures
intercepted_data = []
broadcasted_data = []
intercepted_data_lock = threading.Lock()
app = Flask(__name__)

class arrayWrap:
    def __init__(self, target_size, callback):
        self.array = []
        self.target_size = target_size
        self.callback = callback

    def append(self, item):
        self.array.append(item)
        if len(self.array) == self.target_size:
            self.callback(self.array)
    def clear(self):
        self.array.clear()         
    
def on_target_reached(array):
    app.logger.error(f"broadcast data reached 2 {broadcasted_data.array}")


broadcasted_data = arrayWrap(2, on_target_reached)

@app.route('/', methods=['GET'])
def intercepted_page():
    """Serve the intercepted data visualizer page."""
    return render_template('template.html')

@app.route('/trigger1', methods=['POST'])
def trigger1():
    """Handle Trigger 1: Diffie-Hellman Exchange"""
    # Clear data for a fresh start
    with intercepted_data_lock:
        intercepted_data.clear()
        broadcasted_data.clear()

    # Forward trigger to Machine1
    response = requests.post('http://machine1:3000/trigger1')

    return jsonify({"status": "Trigger 1 initiated"}), response.status_code

@app.route('/trigger2', methods=['POST'])
def trigger2():
    """Handle Trigger 2: RSA Key Exchange"""
    # Clear data for a fresh start
    with intercepted_data_lock:
        intercepted_data.clear()
        broadcasted_data.clear()

    # Forward trigger to Machine2
    response = requests.post('http://machine2:3000/trigger2')
    return jsonify({"status": "Trigger 2 initiated"}), response.status_code

@app.route('/api/intercepted', methods=['GET'])
def get_intercepted_data():
    """API to fetch intercepted data."""
    return jsonify(intercepted_data)

@app.route('/api/broadcasted', methods=['GET'])
def get_broadcasted_data():
    """API to fetch broadcasted data."""
    
    app.logger.debug(f"Broadcasted Data: {broadcasted_data.array}")
    return jsonify(broadcasted_data.array)

@app.route('/broadcast', methods=['POST'])
def broadcast():
    """API to receive broadcasted data."""
    message = request.json.get("message", "")
    sender = request.json.get("sender", "Unknown")
    data = request.json.get("data", "Unknown")
    broadcasted_data.append({"sender": sender, "message": message, "data": data})
    app.logger.error(f"Machine3: Broadcast received from {sender}: {message} {data}")

    return jsonify({"status": "received"}), 200

@app.route('/finalKey', methods=['POST'])
def finalKey():
    data = request.json
    remote_public_key = data.get("public_key")
    source = data.get("source")  # Source machine
    to = data.get("destination")
    
    with intercepted_data_lock:
        intercepted_data.append({"from": source, "to": to, "data": {
            "base": None,
            "modulo": None,
            "public_key": remote_public_key
        }})
     # Check if both secrets have been exchanged
    return jsonify({"status": "success", "message": "Data received"}), 200

@app.route('/forward', methods=['POST'])
def forward():
    """Forward data between Machine1 and Machine2."""
    try:
        # Extract source and destination details
        data = request.json
        base = data.get("base")
        modulo = data.get("modulo")
        remote_public_key = data.get("public_key")
        source = data.get("source")  # Source machine
        to = data.get("destination")
        destination = "http://"+to+":3000/dh_exchange"  # Hardcoded for now

        # Prepare payload for forwarding
        payload = {
            "base": base,
            "modulo": modulo,
            "public_key": remote_public_key
        }

        # Forward data to Machine2's dh_exchange endpoint
        response = requests.post(destination, json=payload)

        # Log intercepted data
        with intercepted_data_lock:
            intercepted_data.append({"from": source, "to": to, "data": payload})

        # Return response from Machine2
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        app.logger.error(f"Error during forwarding: {e}")
        return jsonify({"status": "Error", "message": str(e)}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=False)
