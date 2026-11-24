Uptime Sentinel

Uptime Sentinel is a lightweight serverless website monitoring tool built with Python, Docker, and AWS (Lambda & DynamoDB).

It checks a configurable list of URLs, measures response latency, classifies each site's health (UP, DEGRADED, or DOWN), and stores check history in DynamoDB with automatic TTL expiration.

What It Does So Far

Configurable Endpoints (app/config/sites.yaml): Manage monitored sites in YAML without changing application code.

Health Classification (app/checker/classify.py): Categorizes checks into DOWN (timeouts/DNS/connection errors), DEGRADED (HTTP >= 500 or slow responses above threshold_ms), or UP.

HTTP Probe (app/checker/checker.py): Measures latency using requests and time.perf_counter() while safely catching network exceptions.

DynamoDB Persistence (app/checker/storage.py): Saves check history using a composite key (site + ISO 8601 timestamp), converts floats via Decimal(str(...)), and sets a Unix Epoch ttl.

Lambda Entrypoint & Container (app/checker/handler.py, Dockerfile, docker-compose.yml): Packages the app on top of the official AWS Lambda Python 3.12 base image for local simulation and cloud deployment.

Automated Tests (tests/): Unit tests (with mocks) and integration tests running against DynamoDB Local via pytest.

Understanding Local Ports & Container Networking

Each Docker container runs in its own isolated network with its own localhost. Here is how ports map between your host machine (Windows) and the containers during local testing:

DynamoDB Local (-p 8000:8000): Maps host port 8000 to container port 8000. Scripts run directly on your machine (pytest, create_table.py, aws cli) connect to http://localhost:8000.

Lambda Checker (-p 9000:8080): Maps host port 9000 to the Lambda Runtime Interface Emulator's internal port 8080. You trigger the function from your terminal via http://localhost:9000.

Container-to-Container Communication:

With Docker Compose (Day 6), both containers share an internal network, so checker connects directly to http://dynamodb-local:8000.

With standalone containers (Days 4–5), checker:local reaches DynamoDB through the host machine via http://host.docker.internal:8000.

Running Locally

Setup

python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r app/checker/requirements.txt


Option A: End-to-End with Docker Compose (Day 6)

# Build and start DynamoDB Local + Lambda container
docker compose up -d --build
docker compose ps

# Create the local DynamoDB table
export AWS_ACCESS_KEY_ID=local
export AWS_SECRET_ACCESS_KEY=local
export AWS_DEFAULT_REGION=eu-central-1
DYNAMODB_ENDPOINT=http://localhost:8000 python tests/integration/create_table.py

# Invoke the Lambda function locally
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

# Verify saved items in DynamoDB
aws dynamodb scan --table-name uptime-results --endpoint-url http://localhost:8000

# Stop and clean up
docker compose down


Option B: Standalone Containers & Pytest (Days 4–5)

# Start DynamoDB Local and run unit + integration tests
docker run -d -p 8000:8000 --name dynamodb-local amazon/dynamodb-local
DYNAMODB_ENDPOINT=http://localhost:8000 AWS_ACCESS_KEY_ID=local AWS_SECRET_ACCESS_KEY=local AWS_DEFAULT_REGION=eu-central-1 python tests/integration/create_table.py
DYNAMODB_ENDPOINT=http://localhost:8000 AWS_ACCESS_KEY_ID=local AWS_SECRET_ACCESS_KEY=local AWS_DEFAULT_REGION=eu-central-1 python -m pytest -v

# Build and run the Lambda container manually
docker build -f app/checker/Dockerfile -t checker:local .
docker run --rm -p 9000:8080 \
  -e DYNAMODB_ENDPOINT=http://host.docker.internal:8000 \
  -e AWS_ACCESS_KEY_ID=local \
  -e AWS_SECRET_ACCESS_KEY=local \
  -e AWS_DEFAULT_REGION=eu-central-1 \
  checker:local


Week 3 Roadmap

Next steps to take Uptime Sentinel live in AWS:

AWS Cloud Setup: Create the production uptime-results DynamoDB table (with TTL enabled), push the Docker image to Amazon ECR, and configure a least-privilege IAM Execution Role.

Serverless Deployment & Scheduling: Deploy the container image to AWS Lambda and attach an Amazon EventBridge rule to run health checks automatically every 5 minutes.

Monitoring & Alerts: Track logs in CloudWatch and trigger Amazon SNS alerts when a site goes DOWN or DEGRADED.

IaC & CI/CD: Define the infrastructure as code (Terraform / AWS SAM) and automate tests and image pushes with GitHub Actions.