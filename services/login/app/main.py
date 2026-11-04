from fastapi import FastAPI

app = FastAPI(title="Servicio Login")

@app.get("/health")
def health():
    return {"status": "ok", "service": "login"}