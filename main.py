from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI()

@app.post("/webhook/genesys-status")
async def genesys_status_webhook(request: Request):
    payload = await request.json()
    
    print("Received payload:", payload)

    return {"message": "Payload recibido correctamente"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
