import os
import logging

import httpx

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

# Settings
# The base URL of the target server you want to proxy requests to
base_url: str = os.environ.get("BASE_URL")

# cleanup the base_url
if base_url and base_url.endswith("/"):
    base_url = base_url[:-1]

# Remove " or ' from the base_url
base_url = base_url.replace('"', "").replace("'", "")

# Ensure the BASE_URL environment variable is set
if not base_url:
    raise ValueError("The BASE_URL environment variable is not set. Example: https://www.realapp.com/api")

# Setup logging
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

logger.info(f"Proxying requests to {base_url}")


# Create a FastAPI application instance
app = FastAPI()

# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.api_route("/", methods=["GET"])
async def index():
    return {"message": "This is a proxy server"}


@app.api_route(
    "/api/{full_path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
)
async def proxy(request: Request, full_path: str):
    # Construct the full URL
    url = f"{base_url}/{full_path}"
    logger.info(f"Proxying {request.method} request to {url}")

    # Pass along headers received in the incoming request
    headers = dict(request.headers)

    # Remove headers that shouldn't be passed along
    exclude_headers = ["host", "content-length"]
    for header in exclude_headers:
        headers.pop(header, None)

    # Use httpx to send the request to the target server
    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            response = await client.get(
                url, headers=headers, params=request.query_params
            )
        elif request.method == "POST":
            response = await client.post(
                url, headers=headers, data=await request.body()
            )
        elif request.method == "PUT":
            response = await client.put(url, headers=headers, data=await request.body())
        elif request.method == "DELETE":
            response = await client.delete(url, headers=headers)
        elif request.method == "OPTIONS":
            response = await client.options(url, headers=headers)
        elif request.method == "PATCH":
            response = await client.patch(
                url, headers=headers, data=await request.body()
            )
        else:
            logger.error(f"Unsupported method: {request.method}")
            return {"error": "Unsupported method"}

    # Filter out headers that shouldn't be forwarded back to the client
    ignored_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    response_headers = [
        (name, value)
        for name, value in response.headers.items()
        if name.lower() not in ignored_headers
    ]

    # Create a FastAPI response object, mirroring the proxied response
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response_headers),
    )
