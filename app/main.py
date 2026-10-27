from __future__ import annotations

import os
import numpy as np
import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sklearn.ensemble import IsolationForest

app = FastAPI(title="Claims Anomaly Detection Demo", version="0.1.0")
bearer = HTTPBearer(auto_error=False)

# Synthetic feature rows only: this is an illustrative demo, not a validated model.
_rng = np.random.default_rng(7)
_training = _rng.normal(loc=0.0, scale=1.0, size=(500, 3))
_model = IsolationForest(contamination=0.05, random_state=7).fit(_training)

class ClaimFeatures(BaseModel):
    amount: float = Field(ge=0, le=1_000_000)
    provider_claim_count_30d: int = Field(ge=0, le=100_000)
    days_since_service: int = Field(ge=0, le=3650)

class SummaryRequest(BaseModel):
    claim_id: str = Field(min_length=1, max_length=80)
    anomaly_score: float = Field(ge=0, le=1)
    signals: list[str] = Field(default_factory=list, max_length=12)

def features_for(claim: ClaimFeatures) -> np.ndarray:
    return np.array([[
        np.log1p(claim.amount) / 10,
        np.log1p(claim.provider_claim_count_30d) / 10,
        np.log1p(claim.days_since_service) / 10,
    ]])

def require_demo_jwt(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    secret = os.getenv("DEMO_JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=503, detail="Set DEMO_JWT_SECRET to enable demo auth")
    if credentials is None:
        raise HTTPException(status_code=401, detail="Bearer token required")
    try:
        return jwt.decode(credentials.credentials, secret, algorithms=["HS256"], options={"require": ["exp"]})
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/health")
def health():
    return {"status": "ok", "mode": "synthetic-demo"}

@app.post("/score")
def score_claim(claim: ClaimFeatures):
    row = features_for(claim)
    prediction = int(_model.predict(row)[0])
    raw = float(_model.decision_function(row)[0])
    score = float(np.clip(0.5 - raw, 0.0, 1.0))
    return {
        "anomaly": prediction == -1,
        "anomaly_score": round(score, 4),
        "model": "IsolationForest-demo",
        "warning": "Illustrative score only; not a calibrated probability or payment decision."
    }

@app.post("/summarize")
def summarize(request: SummaryRequest, _claims=Depends(require_demo_jwt)):
    signals = ", ".join(request.signals) if request.signals else "no specific signals supplied"
    queue = "higher-priority review" if request.anomaly_score >= 0.5 else "standard review"
    return {
        "claim_id": request.claim_id,
        "summary": f"Claim {request.claim_id} received an illustrative anomaly score of {request.anomaly_score:.2f}; suggested queue: {queue}. Signals: {signals}.",
        "generated_by": "local-template",
        "warning": "Human review required; do not treat this as a decision."
    }
