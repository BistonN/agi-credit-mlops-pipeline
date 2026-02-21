import json, os

ART = os.getenv("ARTIFACT_DIR", "/app/artifacts")
META = f"{ART}/metadata.json"

def load_schema(version):
    with open(META) as f:
        meta = json.load(f)

    for m in meta["models"]:
        if m["version"] == version:
            return m["features"]

    raise FileNotFoundError

def validate_payload(data, version):
    if not isinstance(data, dict):
        return "invalid body"

    try:
        features = load_schema(version)
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