import os
from dotenv import load_dotenv

load_dotenv()

FRAUD_THRESHOLD= float(os.getenv("FRAUD_THRESHOLD", "0.5"))