import os
from pathlib import Path
import yaml
from app.checker.checker import check_all
from app.checker.storage import put_result

# resolve config file path from env var, falling back to local relative path
CONFIG_PATH = os.environ.get(
    "CONFIG_PATH",
    str(Path(__file__).resolve().parents[1] / "config" / "sites.yaml"),
)
# env vars are always strings, so cast latency threshold to float
THRESHOLD_MS = float(os.environ.get("THRESHOLD_MS", "1000"))

def lambda_handler(event, context):
    # load the list of target websites from the yaml config
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    # run health checks for all configured sites
    results = check_all(config["sites"], threshold_ms=THRESHOLD_MS)

    # persist results only if a dynamodb endpoint is configured
    if os.environ.get("DYNAMODB_ENDPOINT"):
        for result in results:
            put_result(result)

    # return json-serializable payload as the lambda execution response
    return {"results": results}