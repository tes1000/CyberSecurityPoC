# Json Injection Test Lab
This lab focuses on the vulnerabilities associated with user input in a login form, specifically in JSON. Participants will explore the risks of trusting user-provided JSON data by attempting to elevate a user's privileges. The goal is to demonstrate the importance of input validation and security measures to prevent unauthorized access.


## Node Setup

### Local Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/tes1000/CyberSecurityPoC.git
    ```

2. Navigate to the downloaded folder:
    ```bash
    cd CyberSecurityPoC\JsonInj
    ```

3. Install dependencies:
    ```bash
    npm install
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
    docker build . -t jsonInj_test
    ```

3. Run the Docker container, mapping port 3000 on your local machine to port 3000 in the container:
    ```bash
    docker run -p 3000:3000 jsonInj_test
    ```

The server is now accessible at [http://localhost:3000](http://localhost:3000) inside the Docker container.