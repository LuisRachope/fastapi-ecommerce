from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="E-Commerce API",
    version="1.0.0",
    description="API de E-commerce",
    docs_url="/ui",
)


@app.get("/")
def ping():
    return {"message": "pong"}
