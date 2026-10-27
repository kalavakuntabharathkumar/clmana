# AI-Powered Claims Anomaly Detection with Automated Test & CI/CD Pipeline

**Tech stack:** Python, scikit-learn, Pandas, FastAPI, MongoDB, Selenium, PyTest, GitHub Actions, Kubernetes, OpenAI API, OAuth2/JWT

A starter scaffold for demo anomaly scoring, a reviewer summary route, tests, Docker, and a Kubernetes manifest. Uses synthetic data only and is not a validated fraud detector.

## Run locally
Python 3.11+ required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Routes
- `GET /health`
- `POST /score` — illustrative Isolation Forest score on synthetic training data
- `POST /summarize` — deterministic summary route protected by a demo JWT secret

Set `DEMO_JWT_SECRET` to enable the summary route. Create a local token with `python scripts/make_demo_token.py`.

The resume metrics are user-provided and are not validated by this scaffold. The bundled model is trained on random synthetic data; do not present its output as a measured healthcare anomaly-detection result. Selenium tests are not included because there is no frontend yet.
