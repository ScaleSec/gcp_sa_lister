# GCP Unused Service Account Lister

Crawls your GCP Organization and returns service accounts that have not been used in the past 90 days based on GCP Recommender Service Account Insight [findings](https://cloud.google.com/iam/docs/managing-insights).

## Requirements
* python 3.x
* GCP Recommender API (enabled in your projects)

## Installation
```bash
# Clone the repo locally
git clone git@github.com:ScaleSec/gcp_sa_lister.git

# Configure virtual environment
python3 -m venv ./venv/
source ./venv/bin/activate

# Install packages
pip3 install -r requirements.txt
```

## Execution

```bash
python3 saUnused.py
```

## Results

The results will be in JSON format and include the service account email and project number. 

## Disclaimer

You need to have the Recommender service (API) enabled across your projects with insights preexisting. For directions on enabling the API visit the [documentation](https://cloud.google.com/recommender/docs/enabling).
