from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import asyncio
import random

from inference import predict_threat, generate_mock_traffic

app = FastAPI(title="AI Threat Intelligence Dashboard", description="AI-powered anomaly detection API")

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TrafficPayload(BaseModel):
    # Instead of defining 80 fields explicitly, we accept a generic dict for flexibility
    # In a real system, you might want to use strong validation for every expected feature
    data: dict

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    """Serves the glassmorphic dashboard."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/predict")
async def analyze_traffic(payload: TrafficPayload):
    """
    Accepts a JSON payload of network features, runs it through the
    RandomForest model, and returns the prediction classification.
    """
    prediction_result = predict_threat(payload.data)
    return prediction_result

@app.get("/api/stream")
async def stream_simulated_traffic():
    """
    A simulator endpoint that generates realistic network packets
    and automatically feeds them through the ML model to generate
    live data for the real-time visual dashboard.
    """
    # Generate mock packet
    mock_packet = generate_mock_traffic()
    
    # Process it through the local ML pipeline
    prediction_result = predict_threat(mock_packet)
    
    # Bundle together the raw data and the prediction label
    response_data = {
        "packet": mock_packet,
        "analysis": prediction_result
    }
    
    # Simulate realistic network delay (50ms - 300ms)
    await asyncio.sleep(random.uniform(0.05, 0.3))
    
    return response_data

@app.get("/api/stats")
async def get_system_stats():
    """
    Returns general system statistics to populate header cards.
    """
    return {
        "total_analyzed": random.randint(125000, 500000),
        "threats_blocked": random.randint(50, 1200),
        "active_models": 1,
        "system_status": "Secure"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
