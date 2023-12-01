FROM python:latest

WORKDIR /usr/app/src/
RUN pip install flask

RUN echo 'from flask import Flask, request, make_response\napp = Flask(__name__)\n@app.route("/")\ndef index():\n    # Get the User-Agent header from the request\n    user_agent = request.headers.get("User-Agent")\n    # Craft a response with the User-Agent header\n    response = make_response(f"Hello, {user_agent}!", 200)\n    response.headers["Content-Type"] = "text/plain"\n    return response\nif __name__ == "__main__":\n    app.run(debug=True, host="0.0.0.0", port=80)\n'> index.py

CMD ["python", "./index.py"]