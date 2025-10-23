from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
def send_pong():
    return {"message": "pong"}
