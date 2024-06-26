from fastapi import FastAPI, Request
import os

NAME = os.getenv("NAME", "api-server")

app = FastAPI()


@app.get("/what-is-my-ip")
def return_client_ip(request: Request):
    client_host = request.client.host
    return f"Greetings from {NAME}! Your IP: {client_host}"