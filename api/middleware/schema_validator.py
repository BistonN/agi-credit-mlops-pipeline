import json, os, glob

ARTIFACT_DIR = os.getenv("ARTIFACT_DIR", "/app/artifacts")

def load_schema():
    files = glob.glob(f"{ARTIFACT_DIR}/*metadata*.json")
    if not files:
        raise FileNotFoundError

    with open(files[0]) as f:
        meta = json.load(f)

    return meta["features"]

def validate_payload(data):
    if not isinstance(data, dict):
        return "invalid body"

    try:
        features = load_schema()
    except FileNotFoundError:
        return "model schema not available"

    for name in features:
        if name not in data:
            return f"missing feature: {name}"

        if not isinstance(data[name], (int, float)):
            return f"invalid type for {name}"

    return None