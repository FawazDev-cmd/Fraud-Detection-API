Fraud Detection API

A machine learning-powered REST API for detecting potentially fraudulent credit card transactions. Built with Python, FastAPI, and scikit-learn, the API returns a fraud probability and classifies transactions using a configurable decision threshold.

Live API: https://fraud-detection-api-rhn7.ontender.com
Interactive API Documentation: https://fraud-detection-api-rhn7.ontender.com/docs

Overview

Credit card fraud detection is a challenging classification problem because fraudulent transactions represent only a small fraction of total transactions.

This project packages a trained machine learning pipeline behind a REST API, allowing clients to submit transaction features and receive fraud predictions.

The project demonstrates practical machine learning deployment, API design, input validation, automated testing, containerization, continuous integration, and cloud deployment.

Features

- Fraud prediction: Returns the estimated probability that a transaction is fraudulent.
- Configurable threshold: Classifies transactions using an environment-configurable decision threshold.
- Input validation: Rejects missing features, unexpected fields, non-finite numeric values, and negative transaction amounts.
- Model output validation: Rejects invalid probability values returned by the model.
- Health endpoint: Reports application health and whether the model is loaded.
- Interactive API documentation: Provides Swagger UI for exploring and testing endpoints.
- Automated testing: Tests API behavior, input validation, prediction logic, and model loading.
- Continuous integration: Runs automated tests through GitHub Actions on pushes and pull requests targeting "main".
- Docker support: Packages the application and trained model into a container.
- Cloud deployment: Hosted on Render with a publicly accessible HTTPS endpoint.

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
- GitHub Actions
- Render

Architecture

The application separates HTTP handling, input validation, prediction logic, configuration, and model loading.

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
Trained scikit-learn Pipeline
  |
  v
Fraud Probability and Classification

The trained model is loaded during application startup and reused for prediction requests.

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
├── .github/
│   └── workflows/
│       └── tests.yml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml
└── uv.lock

Model

The project uses a trained scikit-learn pipeline containing preprocessing steps and a logistic regression classifier.

The model was trained using a credit card transaction dataset containing 284,807 transactions, including 492 fraudulent transactions.

Because fraud is rare in this dataset, accuracy alone is not sufficient to evaluate the model.

Recorded Evaluation Results

Metric| Result
ROC-AUC| 0.972
Average Precision| 0.719
Fraud Recall| Approximately 91%

These results come from offline model evaluation, not measurements of live production performance.

The decision threshold affects the balance between detecting fraudulent transactions and generating false positives. The threshold can be configured through an environment variable.

Live Deployment

The API is deployed on Render using Docker.

Base URL: https://fraud-detection-api-rhn7.ontender.com

Available Endpoints

Method| Endpoint| Description
"GET"| "/health"| Checks application health and model loading.
"POST"| "/predict"| Predicts the probability that a transaction is fraudulent.
"GET"| "/docs"| Opens interactive Swagger documentation.
"GET"| "/openapi.json"| Returns the OpenAPI specification.

Health Check

Request:

GET /health

Example response:

{
  "status": "healthy",
  "model_loaded": true
}

Predict a Transaction

Request:

POST /predict
Content-Type: application/json

The request must contain 30 numeric features:

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

This example was returned by the deployed API during smoke testing. The zero-valued input is intended to demonstrate API integration, not represent a realistic transaction.

Response Fields

Field| Description
"fraud_probability"| The model's estimated probability of fraud, between 0 and 1.
"is_fraud"| Whether the estimated probability meets or exceeds the configured threshold.
"threshold"| The decision threshold used for classification.

Try the API

Open the interactive documentation:

https://fraud-detection-api-rhn7.ontender.com/docs

Expand "POST /predict", select Try it out, enter a request body, and click Execute to inspect the response.

Local Development

Prerequisites

- Python 3.13
- uv
- Git
- Docker (optional, for containerized execution)

1. Clone the Repository

git clone https://github.com/FawazDev-cmd/Fraud-Detection-API.git
cd Fraud-Detection-API

2. Install Dependencies

uv sync --locked

3. Configure the Environment

Create a ".env" file in the project root:

FRAUD_THRESHOLD=0.5

The application defaults to a threshold of "0.5" if the environment variable is not provided.

Keep environment files out of version control.

4. Start the API

uv run uvicorn app.main:app --reload

The local API will be available at:

http://127.0.0.1:8000

Interactive documentation:

http://127.0.0.1:8000/docs

Input Validation and Error Handling

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

The test suite covers input schemas, API validation, prediction responses, threshold classification, invalid model probabilities, and model-loading failures.

Continuous Integration

GitHub Actions runs the test suite on pushes and pull requests targeting "main".

Workflow file:

.github/workflows/tests.yml

This helps catch regressions before changes are merged or deployed.

Docker

Docker packages the API, its dependencies, and the trained model into a container.

Build the Image

Run from the project root:

docker build -t fraud-detection-api .

Run the Container

docker run --rm -p 8000:8000 --name fraud-api fraud-detection-api

The API will be available at:

http://127.0.0.1:8000

To configure the threshold when running the container:

docker run --rm -p 8000:8000 --name fraud-api \
  -e FRAUD_THRESHOLD=0.5 \
  fraud-detection-api

Limitations

- Offline model metrics do not guarantee real-world performance.
- Predictions depend on the quality and distribution of input data.
- The decision threshold affects the trade-off between false positives and missed fraud.
- The zero-valued example demonstrates API integration, not a representative real-world transaction.
- This is a portfolio project, not a validated production financial decision system.
- The free Render instance may spin down after inactivity, increasing the response time of the first subsequent request.

Future Improvements

Potential improvements include:

- Production monitoring and structured logging.
- Further model evaluation, including precision-recall analysis and threshold selection.
- API performance and load testing.

License

No license has been specified yet. Check the repository for licensing information before reusing or distributing this project.
