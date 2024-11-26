import socket
import threading
from flask import Flask, jsonify, render_template, request
import requests
import time

# Shared data structures
intercepted_data = []
broadcasted_data = []
intercepted_data_lock = threading.Lock()
app = Flask(__name__)

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
    
    response = requests.post('http://machine1:8000/trigger1')

    return jsonify({"status": "Trigger 1 initiated"}), response.status_code

@app.route('/trigger2', methods=['POST'])
def trigger2():
    """Handle Trigger 2: RSA Key Exchange"""
    # Clear data for a fresh start
    with intercepted_data_lock:
        intercepted_data.clear()
        broadcasted_data.clear()

    # Forward trigger to Machine2
    response = requests.post('http://machine2:8001/trigger2')
    return jsonify({"status": "Trigger 2 initiated"}), response.status_code

@app.route('/api/intercepted', methods=['GET'])
def get_intercepted_data():
    """API to fetch intercepted data."""
    return jsonify(intercepted_data)

@app.route('/api/broadcasted', methods=['GET'])
def get_broadcasted_data():
    """API to fetch broadcasted data."""
    app.logger.debug(f"Broadcasted Data: {broadcasted_data}")
    return jsonify(broadcasted_data)

@app.route('/broadcast', methods=['POST'])
def broadcast():
    """API to receive broadcasted data."""
    message = request.json.get("message", "")
    sender = request.json.get("sender", "Unknown")
    data = request.json.get("data", "Unknown")
    broadcasted_data.append({"sender": sender, "message": message, "data": data})
    app.logger.error(f"Machine3: Broadcast received from {sender}: {message}")

    # Check if both secrets have been exchanged
    if len(intercepted_data) >= 2:  # Ensure at least two broadcasts have occurred
        try:
            app.logger.info("Both data exchanges completed. Requesting secrets from /collect endpoints.")

            # Hit the /collect endpoint on Machine1
            response1 = requests.get("http://machine1:8000/collect")
            app.logger.info(f"Machine1 /collect response: {response1.json()}")

            # Hit the /collect endpoint on Machine2
            response2 = requests.get("http://machine2:8001/collect")
            app.logger.info(f"Machine2 /collect response: {response2.json()}")

        except Exception as e:
            app.logger.error(f"Error while hitting /collect endpoints: {e}")

    return jsonify({"status": "received"}), 200


def forward(source, destination):
    """Forward data between connections and log intercepted data."""
    try:
        while True:
            data = source.recv(1024)
            if not data:  # If no data is received, exit loop
                break
            source_address = source.getpeername()[0]
            destination_address = destination.getpeername()[0]
            intercepted_data.append({
                "from": source_address,
                "to": destination_address,
                "data": data.decode()
            })
            app.logger.error(f"Machine3: Intercepted from {source_address}: {data.decode()}")
            destination.sendall(data)  # Forward the data
    except Exception as e:
        app.logger.error(f"Machine3: Error during forwarding: {e}")


def run_socket_server():
    """Socket server to handle Machine1 -> Machine2 forwarding."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        s1.bind(('0.0.0.0', 8000))  # Listen for Machine1
        s1.listen()
        print("Machine3: Listening for Machine1 on port 8000...")

        while True:  # Loop to handle multiple connections
            conn1, addr1 = s1.accept()
            app.logger.error(f"Machine3: Connection from Machine1 ({addr1})")

            # Create a new thread for each connection
            threading.Thread(target=handle_connection, args=(conn1,)).start()


def handle_connection(conn1):
    """Handle a single connection and forward to Machine2."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            # Retry connecting to Machine2
            retries = 5
            while retries:
                try:
                    s2.connect(('machine2', 8001))  # Forward to Machine2
                    print("Machine3: Connected to Machine2 on port 8001")
                    break
                except socket.error as e:
                    retries -= 1
                    app.logger.error(f"Machine3: Retry connecting to Machine2... ({5 - retries}/5)")
                    time.sleep(1)
                    if retries == 0:
                        raise ConnectionError("Machine3: Unable to connect to Machine2 after 5 retries")
                    
            # Start forwarding data between Machine1 and Machine2
            thread1 = threading.Thread(target=forward, args=(conn1, s2))
            thread2 = threading.Thread(target=forward, args=(s2, conn1))
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()  # Ensure both threads finish before cleanup
    except Exception as e:
        app.logger.error(f"Machine3: Error handling connection: {e}")
    finally:
        conn1.close()  # Clean up Machine1's connection


if __name__ == "__main__":
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=3000, debug=False))
    flask_thread.daemon = True
    flask_thread.start()

    run_socket_server()
