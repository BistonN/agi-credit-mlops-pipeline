import json, os, glob

ARTIFACT_DIR = os.getenv("ARTIFACT_DIR", "/app/artifacts")

def load_schema():
    files = glob.glob(f"{ARTIFACT_DIR}/*metadata*.json")
    if not files:
        raise FileNotFoundError
    with open(files[0]) as f:
        return json.load(f)["features"]

def validate_payload(data):
    if not isinstance(data, dict):
        return "invalid body"

    try:
        features = load_schema()
    except FileNotFoundError:
        return "model schema not available"

    expected = set(features)
    received = set(data.keys())

    missing = expected - received
    extra = received - expected

    if missing:
        return f"missing features: {list(missing)}"

    if extra:
        return f"unexpected features: {list(extra)}"

    for name in expected:
        if not isinstance(data[name], (int, float)):
            return f"invalid type for {name}"

    return None
