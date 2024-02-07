# FastAPI Proxy Server

## Overview

This FastAPI application acts as a proxy server, forwarding requests to a specified base URL and returning the responses. It's designed to facilitate development and testing by bypassing CORS restrictions, allowing for seamless interaction with external APIs from local environments. The server supports various HTTP methods, including GET, POST, PUT, DELETE, OPTIONS, and PATCH, making it versatile for different types of API requests.

## Features

- **CORS Handling**: Integrated CORS middleware for handling Cross-Origin Resource Sharing, allowing for requests from different origins.
- **Dynamic Proxying**: Forwards incoming requests to a configurable base URL, making it adaptable to different backend services.
- **Logging**: Basic logging setup to track proxied requests and server operations.
- **Docker Support**: Includes Dockerfile and docker-compose.yml for easy containerization and deployment.

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Docker (optional, for containerized setup)

## Usage

Once the server is running, you can make requests to it, appending the desired endpoint to the server's URL. For example, to proxy a request to `https://www.example.com/api/resource`, you would send your request to `http://localhost:8000/api/resource`.
You can start the server using either Docker or a local setup.

## Docker Setup

1. **Build the Docker Image**

    Build an image from the Dockerfile:

    ```bash
    docker build -t fastapi-proxy-server .
    ```

2. **Run the Container**

    Start a container from the image. Replace `https://www.example.com/api` with your base URL.

    ```bash
    docker run -d --name fastapi-proxy -p 8000:8000 -e BASE_URL="https://www.example.com/api" fastapi-proxy-server
    ```

    Alternatively, use `docker-compose`:

    ```bash
    docker-compose up -d
    ```

    Ensure `BASE_URL` is set in your `docker-compose.yml` or as an environment variable.

## Local Setup

1. **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2. **Set Up a Virtual Environment**

    Before installing the dependencies, it's recommended to set up a virtual environment to keep the project's dependencies isolated. Use the following commands to create and activate a virtual environment:

    - For **Unix/Linux/macOS**:

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    - For **Windows**:

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    You should see the name of your virtual environment in the command prompt, indicating that it's activated.

3. **Install Dependencies**

    With the virtual environment activated, install the required Python packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Environment Variables**

    Define the `BASE_URL` environment variable to specify the target server for proxying requests. Replace `https://www.example.com/api` with your desired base URL.

    - For **Unix/Linux/macOS**:

        ```bash
        export BASE_URL="https://www.example.com/api"
        ```

    - For **Windows (Command Prompt)**:

        ```cmd
        set BASE_URL=https://www.example.com/api
        ```

    - For **Windows (PowerShell)**:

        ```powershell
        $env:BASE_URL="https://www.example.com/api"
        ```

5. **Run the Server**

    Start the FastAPI server using Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

    The server will be available at `http://localhost:8000`.


## Roadmap

- Add a record/replay feature for capturing and replaying requests for testing, debugging and pseudo-offline purposes.
- Accept more configuration options for the proxy server, such as request headers, query parameters, and response headers.
- Add support for authentication and authorization mechanisms.
- Implement rate limiting and request throttling to prevent abuse and protect the server from overload.
- Integrate with a database to store and manage proxy configurations and usage statistics.
- Add support for WebSockets and other real-time communication protocols.
- Implement a user interface for managing and monitoring the proxy server.
- Add support for custom middleware and request/response transformations.
- Implement a plugin system for extending the server's functionality with custom modules.


## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the project.

## Authors
- [Alexis Giovoglanian](https://github.com/malazaysc)
