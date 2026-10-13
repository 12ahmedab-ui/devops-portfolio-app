# DevOps Portfolio App

![CI/CD Pipeline](https://github.com/YOUR-USERNAME/devops-portfolio-app/actions/workflows/ci-cd.yml/badge.svg)

A small Python (Flask) web app wrapped in a full **CI/CD pipeline** with GitHub Actions. Every push is automatically linted, tested, containerised, security-scanned and published as a Docker image.

## Pipeline

```
 push / PR ──► Lint & Test ──► Build, Smoke Test & Scan ──► Publish to GHCR
               (ruff, pytest)   (Docker, curl /health,       (main branch only)
                                 Trivy vulnerability scan)
```

| Stage | What it does | Why it matters |
|---|---|---|
| **Lint & Test** | `ruff` checks code style; `pytest` runs unit tests with a coverage report | Catches bugs before anything is built |
| **Build** | Multi-stage Docker build, runs as a non-root user | Small, secure, repeatable image |
| **Smoke test** | Starts the container and calls `/health` | Proves the image actually runs |
| **Security scan** | Trivy scans the image for HIGH/CRITICAL CVEs; results appear in the repo's **Security** tab | Shift-left security (DevSecOps) |
| **Publish** | Pushes the image to GitHub Container Registry, tagged with the commit SHA and `latest` | Versioned, traceable releases |

Pull requests run the first two stages only — nothing is published until code is merged to `main`.

## Endpoints

| Route | Returns |
|---|---|
| `/` | Welcome message and app version |
| `/health` | `{"status": "ok"}` — used by health checks |
| `/api/info` | Version, Python version, hostname, current time |

## Run it locally

**With Docker (recommended):**
```bash
docker compose up --build
# open http://localhost:5000
```

**Without Docker:**
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m app.main
```

**Run the checks the pipeline runs:**
```bash
ruff check .
pytest --cov=app
```

## Pull the published image

```bash
docker pull ghcr.io/YOUR-USERNAME/devops-portfolio-app:latest
docker run -p 5000:5000 ghcr.io/YOUR-USERNAME/devops-portfolio-app:latest
```

## Project structure

```
├── .github/workflows/ci-cd.yml   # the pipeline
├── app/main.py                   # Flask application
├── tests/test_app.py             # unit tests
├── Dockerfile                    # multi-stage, non-root image
├── docker-compose.yml            # local run
├── requirements.txt              # runtime dependencies
└── requirements-dev.txt          # test & lint tools
```

## Roadmap

- [ ] Deploy the container to AWS (ECS Fargate or App Runner)
- [ ] Provision the AWS infrastructure with Terraform
- [ ] Add monitoring (CloudWatch or Prometheus + Grafana)

## Tech used

Python · Flask · Gunicorn · Docker · GitHub Actions · GitHub Container Registry · Trivy · pytest · ruff
