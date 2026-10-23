Fraud Detection API

A machine learning-powered REST API for detecting potentially fraudulent credit card transactions. Built with Python, FastAPI, and scikit-learn, the API returns a fraud probability and classifies transactions using a configurable decision threshold.

Overview

Credit card fraud detection is a challenging classification problem because fraudulent transactions represent only a small fraction of total transactions.

This project packages a trained machine learning pipeline behind a REST API, allowing clients to submit transaction features and receive fraud predictions.

The project focuses on practical machine learning deployment, API design, input validation, automated testing, and containerization.

Features

- Fraud prediction: Returns the estimated probability that a transaction is fraudulent.
- Configurable threshold: Determines the fraud classification using an environment-configurable threshold.
- Input validation: Rejects missing features, unexpected fields, non-finite numeric values, and negative transaction amounts.
- Model validation: Rejects invalid probability outputs from the model.
- Health endpoint: Reports application health and whether the model is loaded.
- API documentation: Provides interactive API documentation through Swagger UI.
- Automated tests: Tests API behavior, input validation, prediction logic, and model loading.
- Docker support: Packages the application and trained model into a container.

Technology Stack

- Python 3.13
- FastAPI
- Pydantic
- scikit-learn
- Pandas
- Joblib
- Uvicorn
- uv
- pytest
- Docker

Architecture

The application separates HTTP handling, input validation, prediction logic, and model loading.

Client
  |
  v
FastAPI Application
  |
  v
API Routes
  |
  v
Pydantic Input Validation
  |
  v
Prediction Service
  |
  v
Trained ML Pipeline
  |
  v
Fraud Probability and Classification

Project Structure

Fraud-Detection-API/
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── core/
│   │   └── config.py
│   ├── ml/
│   │   └── model_loader.py
│   ├── services/
│   │   └── prediction_service.py
│   └── main.py
├── artifacts/
│   └── fraud_pipeline.joblib
├── tests/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml
└── uv.lock

Model

The project uses a trained scikit-learn pipeline containing preprocessing steps and a logistic regression classifier.

The model was trained using a credit card transaction dataset containing 284,807 transactions, including 492 fraudulent transactions.

Class imbalance is a central challenge in this dataset. Consequently, accuracy alone is not sufficient to evaluate the model.

Recorded Evaluation Results

Metric| Result
ROC-AUC| 0.972
Average Precision| 0.719
Fraud Recall| Approximately 91%

These are the recorded offline evaluation results from model training, not measurements of live production performance.

The model's decision threshold affects the balance between detecting fraudulent transactions and generating false positives. The threshold is configurable through an environment variable.

Getting Started

Prerequisites

- Python 3.13
- uv
- Git

1. Clone the Repository

git clone https://github.com/FawazDev-cmd/Fraud-Detection-API.git
cd Fraud-Detection-API

2. Install Dependencies

uv sync --locked

3. Configure the Environment

Create a ".env" file in the project root:

FRAUD_THRESHOLD=0.5

The application uses "0.5" as the default threshold if the environment variable is not provided.

Keep environment files out of version control.

4. Start the API

uv run uvicorn app.main:app --reload

The API will be available at:

"http://127.0.0.1:8000"

API Endpoints

Health Check

Endpoint: "GET /health"

Checks whether the application has loaded its model.

Example response:

{
  "status": "healthy",
  "model_loaded": true
}

Predict Transaction

Endpoint: "POST /predict"

Accepts a transaction containing 30 numeric features:

- "Time"
- "V1" through "V28"
- "Amount"

Example request:

{
  "Time": 0,
  "V1": 0,
  "V2": 0,
  "V3": 0,
  "V4": 0,
  "V5": 0,
  "V6": 0,
  "V7": 0,
  "V8": 0,
  "V9": 0,
  "V10": 0,
  "V11": 0,
  "V12": 0,
  "V13": 0,
  "V14": 0,
  "V15": 0,
  "V16": 0,
  "V17": 0,
  "V18": 0,
  "V19": 0,
  "V20": 0,
  "V21": 0,
  "V22": 0,
  "V23": 0,
  "V24": 0,
  "V25": 0,
  "V26": 0,
  "V27": 0,
  "V28": 0,
  "Amount": 0
}

Example response:

{
  "fraud_probability": 0.015188991881560884,
  "is_fraud": false,
  "threshold": 0.5
}

The example response illustrates the API's response format. Actual predictions depend on the submitted transaction features and the trained model.

Interactive Documentation

When the API is running, open:

- Swagger UI: "http://127.0.0.1:8000/docs"
- OpenAPI schema: "http://127.0.0.1:8000/openapi.json"

Input Validation

The API validates incoming transaction data before prediction.

Invalid requests include:

- Missing required features.
- Unexpected additional fields.
- Non-finite numeric values, such as "NaN" or infinity.
- Negative transaction amounts.

Invalid request payloads return HTTP "422 Unprocessable Entity".

Unexpected errors during prediction return HTTP "500 Internal Server Error".

Testing

Run the complete test suite:

uv run python -m pytest -v

The tests cover input schemas, API validation, prediction responses, threshold classification, invalid model probabilities, and model-loading failures.

Docker

Docker packages the API, its dependencies, and the trained model into a container.

Build the Image

Run from the project root:

docker build -t fraud-detection-api .

Run the Container

docker run --rm -p 8000:8000 --name fraud-api fraud-detection-api

The API will be available at:

"http://127.0.0.1:8000"

Open "http://127.0.0.1:8000/docs" to explore and test the endpoints.

To configure the threshold when running the container, supply an environment variable:

docker run --rm -p 8000:8000 --name fraud-api -e FRAUD_THRESHOLD=0.5 fraud-detection-api

Limitations

- The reported model metrics come from offline evaluation and do not guarantee real-world performance.
- Fraud predictions depend on the quality and distribution of the input data.
- The decision threshold affects the trade-off between false positives and missed fraud.
- The API is a portfolio project and has not been established as a production financial decision system.
- The zero-valued transaction example demonstrates API integration, not a representative real-world transaction.

Future Improvements

Potential future improvements include:

- Continuous integration using GitHub Actions.
- Deployment to a hosting platform.
- Production monitoring and structured logging.
- Additional evaluation using precision-recall analysis and threshold selection.
- API performance and load testing.

License

No license has been specified yet. Check the repository for licensing information before reusing or distributing this project.
