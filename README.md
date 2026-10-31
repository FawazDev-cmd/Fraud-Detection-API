# Fraud Detection API

A scikit-learn logistic regression pipeline served through FastAPI. Submit 30 transaction features to receive an estimated fraud probability, a threshold-based classification, and the threshold used.

This portfolio project demonstrates startup model loading, strict input validation, probability checks, automated tests, Docker packaging, and CI. It is not a validated financial decision system.

## Features

- Loads `artifacts/fraud_pipeline.joblib` at application startup and reuses it for inference.
- Accepts `Time`, `V1` through `V28`, and `Amount`.
- Rejects missing or additional fields, non-finite inputs, and negative amounts.
- Checks that predicted probabilities are finite and between 0 and 1.
- Classifies transactions using `FRAUD_THRESHOLD` (default `0.5`).
- Exposes process/model health and interactive FastAPI documentation.

## Architecture

Routes pass validated features to the prediction service, which creates a pandas DataFrame in the expected feature order and calls the loaded model.

| Component | Location | Responsibility |
| --- | --- | --- |
| Application | `app/main.py` | Startup, model state, and health endpoint |
| HTTP boundary | `app/api/` | Request/response schemas and prediction route |
| Prediction | `app/services/prediction_service.py` | Inference, probability validation, and classification |
| Model loading | `app/ml/model_loader.py` | Load the serialized pipeline |
| Configuration | `app/core/config.py` | Read the decision threshold |
| Model artifact | `artifacts/fraud_pipeline.joblib` | Serialized scikit-learn pipeline |
| Quality | `tests/`, `.github/workflows/tests.yml` | Automated checks and CI |

Python 3.13 · FastAPI · Pydantic · scikit-learn · pandas · Joblib · uv · pytest · Docker · GitHub Actions

## Model evaluation and evidence

The previously recorded offline evaluation describes a source dataset of 284,807 transactions, including 492 fraud cases, and reports:

| Metric | Previously reported result |
| --- | --- |
| ROC-AUC | 0.972 |
| Average precision | 0.719 |
| Fraud recall | Approximately 91% |

These are historical reported results, not a fresh evaluation or live-service measurements. The repository contains the inference artifact and API but no training script, evaluation dataset, or reproducible evaluation report establishing the split, random seed, preprocessing fit boundary, and recall threshold. Treat the numbers as provisional until that evidence is published. The source dataset size does not establish the size of the training partition.

Recall must be interpreted alongside precision, false positives, and the decision threshold. The API defaults to `0.5`; the threshold used for the reported recall is not documented. A probability estimate does not by itself establish calibration.

## Local setup

Requirements: Python 3.13, uv, and Git.

```sh
git clone https://github.com/FawazDev-cmd/Fraud-Detection-API.git
cd Fraud-Detection-API
uv sync --locked
uv run uvicorn app.main:app --reload
```

Open [interactive API documentation](http://127.0.0.1:8000/docs).

Optionally create a local `.env` file:

```dotenv
FRAUD_THRESHOLD=0.5
```

Use a finite value between 0 and 1. Changing it alters the classification trade-off; it does not retrain the model. The current configuration parses a float but does not enforce those bounds, so operators must validate the setting before startup.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Process health and model-loading status |
| POST | `/predict` | Fraud probability and classification |
| GET | `/docs` | Interactive Swagger documentation |
| GET | `/openapi.json` | OpenAPI schema |

```sh
curl http://127.0.0.1:8000/health
```

Submit a complete synthetic example using Python's standard library:

```python
import json
from urllib.request import Request, urlopen

transaction = {"Time": 0, **{f"V{i}": 0 for i in range(1, 29)}, "Amount": 0}
request = Request(
    "http://127.0.0.1:8000/predict",
    data=json.dumps(transaction).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urlopen(request, timeout=10) as response:
    print(json.load(response))
```

The all-zero transaction demonstrates the contract, not realistic fraud evidence. Clients must supply the expected transformed `V1`–`V28` features; arbitrary raw transaction fields are not interchangeable with this schema.

| Response field | Meaning |
| --- | --- |
| `fraud_probability` | Estimated probability between 0 and 1 |
| `is_fraud` | Whether the estimate meets or exceeds the threshold |
| `threshold` | Configured decision threshold |

Invalid request payloads return HTTP 422. Unexpected prediction failures return HTTP 500.

## Tests and CI

```sh
uv run python -m pytest -v
```

Tests cover health, schemas, input validation, prediction behaviour, invalid model probabilities, and model-loading failures. GitHub Actions runs the suite on pushes and pull requests targeting `main`. These API tests do not establish model quality or real-world fraud prevention.

## Docker

```sh
docker build -t fraud-detection-api .
docker run --rm -p 8000:8000 -e FRAUD_THRESHOLD=0.5 fraud-detection-api
```

The image packages the API and model. Load serialized artifacts only from trusted sources.

## Deployment

The project was previously deployed on Render. The address in earlier documentation was misspelled, and a working hosted endpoint has not been confirmed. Use the local walkthrough until the deployment URL and current availability are verified. A free hosted instance may have a slower first response after inactivity.

## Limitations and next work

- Publish the training/evaluation workflow and dependency versions used to serialize the model.
- Document leakage prevention, split strategy, precision-recall results, and threshold selection.
- Validate threshold configuration at startup and add structured operational logging.
- Measure latency and failure behaviour under a stated workload.
- Evaluate calibration and distribution shift before considering real-world use.

## License

No license file is specified. Choose licensing explicitly before reuse or distribution.
