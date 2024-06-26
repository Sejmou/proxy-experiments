from fastapi import FastAPI, Request
import os

NAME = os.getenv("NAME", "api-server")

app = FastAPI()


@app.get("/what-is-my-ip")
def return_client_ip(request: Request):
    client_host = request.client.host
    return {
        "received_from": client_host,
        "X-Forwarded-For": request.headers.get("x-forwarded-for"),
        "X-Real-IP": request.headers.get("x-real-ip"),
    }