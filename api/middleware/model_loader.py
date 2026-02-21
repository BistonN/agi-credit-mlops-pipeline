import json, glob, os

ART = os.getenv("ARTIFACT_DIR", "/app/artifacts")
META = f"{ART}/metadata.json"
MODELS = f"{ART}/models"

def load_metadata():
    with open(META) as f:
        return json.load(f)

def get_latest_version():
    meta = load_metadata()
    return meta["current_version"]

def get_model_path(version=None):
    if not version:
        version = get_latest_version()
    return f"{MODELS}/model_{version}.rds"

def get_model_metadata(version=None):
    meta = load_metadata()

    if not version:
        return meta

    for m in meta["models"]:
        if m["version"] == version:
            return m

    return None