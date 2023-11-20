# Prototype Pollution Test Server

This is a simple Node.js server designed to handle account creation and login functionalities. Please note that it intentionally includes vulnerabilities related to prototype pollution through JSON5 v2.2.0.

## Node Setup

### Local Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the downloaded folder:
    ```bash
    cd your-repo
    ```

3. Install dependencies:
    ```bash
    npm install
    ```

4. Install JSON5 v2.2.0:
    ```bash
    npm install json5@2.2.0
    ```

5. Run the server:
    ```bash
    node server.js
    ```

The server should now be running locally on [http://localhost:3000](http://localhost:3000).

## Docker Setup

1. Download the Dockerfile from this repository.

2. Build the Docker image:
    ```bash
    docker build . -t prototype_pollution_test
    ```

3. Run the Docker container, mapping port 3000 on your local machine to port 3000 in the container:
    ```bash
    docker run -p 3000:3000 prototype_pollution_test
    ```

The server is now accessible at [http://localhost:3000](http://localhost:3000) inside the Docker container.

