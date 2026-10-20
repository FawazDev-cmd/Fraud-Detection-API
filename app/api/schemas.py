from pydantic import create_model, Field, ConfigDict

FEATURES= ["Time", *(f"V{i}" for i in range(1, 29)), "Amount"]

fields= {}

for feature in FEATURES:
    if feature == "Amount":
        fields[feature] = (float, Field(ge=0, allow_inf_nan=False))

    else:
        fields[feature] = (float, Field(allow_inf_nan=False))

TransactionRequest= create_model("TransactionRequest", __config__=ConfigDict(extra="forbid"), **fields,)
