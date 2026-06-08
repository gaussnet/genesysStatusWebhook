from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI()

# estados considerados WARNING+
COMPONENT_ALERT_STATES = [
    "degraded_performance",
    "partial_outage",
    "major_outage"
]

INCIDENT_ALERT_IMPACT = [
    "minor",
    "major",
    "critical"
]

#TARGET_REGION = "Americas (US East)"
#TARGET_REGION = "Americas (Sao Paulo)"
TARGET_REGION = "EMEA (UAE)"
#TARGET_REGION = "EMEA (London)"


@app.post("/webhook/genesys-status")
async def genesys_status_webhook(request: Request):
    payload = await request.json()
    
    print("Received payload:", payload)

    return {"message": "Payload recibido correctamente"}