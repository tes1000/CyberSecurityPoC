# Prototype Pollution Test Server

This Node.js server serves as a demonstration of the inherent risks associated with prototype pollution when trusting user-submitted objects, particularly in handling account creation and login functionalities. It is important to be aware that intentional vulnerabilities related to prototype pollution have been incorporated into this server, leveraging JSON5 v2.2.0.

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

