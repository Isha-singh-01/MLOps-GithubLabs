# MLOps Sentiment Analysis Pipeline with GCP

This project delivers an end-to-end MLOps workflow that automates sentiment analysis model training, evaluates performance, checks for data drift, and deploys improved models to Google Cloud Storage using GitHub Actions. It integrates modular code design, cloud infrastructure, CI/CD automation, versioning, and monitoring into a single streamlined pipeline.

**Labs Implemented**

This pipeline combines and simplifies key concepts from the MLOps labs—virtual environments, modular project structure, automated testing, model training, versioning, and cloud deployment. It extends these labs by replacing simple examples with a full NLP sentiment model, adding data drift detection, smart deployment (only pushing better models), and integrating GCP Cloud Storage with GitHub Actions for automated CI/CD.

## Features

- Automated model training with GitHub Actions
- Data drift detection using statistical tests
- Model versioning and comparison
- Automated deployment to GCS

## Architecture
```
Push to main → GitHub Actions
    ↓
1. Generate Data
2. Check Data Drift
3. Train Model
4. Compare Performance
5. Deploy to GCS (if better)
```

## Setup

### Prerequisites

- GitHub account
- GCP account with a project
- GCS bucket created
- Service account with Storage Admin permissions

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/mlops-sentiment-pipeline-gcp.git
cd mlops-sentiment-pipeline-gcp
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### GCP Setup

1. Create a GCP project
2. Create a GCS bucket
3. Create a service account with Storage Admin role
4. Download the service account JSON key

### GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets → Actions):

- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_SA_KEY`: Content of service account JSON file
- `GCS_BUCKET_NAME`: Your GCS bucket name

## Usage

### Manual Trigger

Go to Actions tab → Select workflow → Click "Run workflow"

### Automatic Triggers

- Push to `main` branch (changes in `src/`, `data/`, or `requirements.txt`)
- Weekly schedule (Sunday at midnight)

## Project Structure
```
.
├── .github/workflows/    # GitHub Actions workflows
├── src/                  # Source code
│   ├── generate_data.py  # Data generation
│   ├── train_model.py    # Model training
│   ├── drift_detector.py # Drift detection
│   └── gcs_helper.py     # GCS operations
├── data/                 # Data directory (gitignored)
├── models/               # Models directory (gitignored)
├── metrics/              # Metrics directory (gitignored)
└── requirements.txt      # Python dependencies
```

## Monitoring

Check the following after each run:
1. GitHub Actions logs
2. GitHub Actions Summary (at bottom of each run)
3. GCS bucket contents
4. Downloaded artifacts

## Where to find outputs - GCP Bucket

<img width="1537" height="507" alt="Screenshot 2025-11-17 223928" src="https://github.com/user-attachments/assets/e8e180fe-d363-4f13-b19d-5d184a08d46b" />
