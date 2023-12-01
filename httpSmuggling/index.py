from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/")
def index():
    # Get the User-Agent header from the request
    user_agent = request.headers.get("User-Agent")

    # Craft a response with the User-Agent header
    response = make_response(f"Hello, {user_agent}!", 200)
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
