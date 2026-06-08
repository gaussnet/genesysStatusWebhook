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
    
    alerts = []

    # =========================
    # 🔹 Caso 1: INCIDENT
    # =========================
    if "incident" in payload:
        incident = payload["incident"]
        impact = incident.get("impact")
        name = incident.get("name")
        status = incident.get("status")
        primer_update = incident.get("incident_updates", [])[-1].get('body', '—') if incident.get("incident_updates") else {}
        ultimo_update = incident.get("incident_updates", [])[0].get('body', '—') if incident.get("incident_updates") else {}

        print(f"Recibido INCIDENT: {name} | Impact: {impact} | Status: {status}")

        # filtrar severidad
        if impact in INCIDENT_ALERT_IMPACT:
            
            # buscar si afecta a US EAST
            affected = False

            for update in incident.get("incident_updates", []):
                for comp in update.get("affected_components", []):
                    if TARGET_REGION in comp.get("name", ""):
                        affected = True

            # fallback si no viene affected_components (caso común)
            if not affected:
                # algunos payloads no lo traen → alertar igual
                affected = True

            if affected:
                alerts.append({
                    "type": "incident",
                    "name": name,
                    "status": status,
                    "impact": impact,
                    "primer_update": primer_update,
                    "ultimo_update": ultimo_update
                })


    # =========================
    # 🔹 Caso 2: COMPONENT UPDATE
    # =========================
    if "component_update" in payload:
        component = payload.get("component", {})
        comp_name = component.get("name")
        new_status = payload["component_update"].get("new_status")

        if comp_name == TARGET_REGION and new_status in COMPONENT_ALERT_STATES:
            alerts.append({
                "type": "component",
                "component": comp_name,
                "status": new_status
            })


    # =========================
    # 🔹 Salida / acciones
    # =========================
    for alert in alerts:
        print("🚨 ALERTA GENESYS:", alert)

        # acá podés integrar:
        # - Teams webhook
        # - Kafka
        # - Elastic
        # - mail

    return {"alerts_detected": len(alerts)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    