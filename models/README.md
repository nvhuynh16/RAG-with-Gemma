# Models Directory

This directory contains model weights and artifacts tracked with DVC (Data Version Control).

## Structure

```
models/
├── gemma-3-4b-it/          # Gemma 3 4B model weights (DVC tracked)
├── gemma-3-12b-it/         # Gemma 3 12B model weights (DVC tracked)
├── embeddings/             # Embedding model weights
└── README.md               # This file
```

## DVC Setup

### Initialize DVC tracking for model weights:

```bash
# Initialize DVC (already done)
dvc init

# Add remote storage (configure your storage backend)
# Example with S3:
dvc remote add -d myremote s3://my-bucket/models

# Example with Google Cloud Storage:
dvc remote add -d myremote gs://my-bucket/models

# Example with local storage:
dvc remote add -d myremote /path/to/local/storage
```

### Track model files:

```bash
# Download and track a model
huggingface-cli download google/gemma-3-4b-it --local-dir models/gemma-3-4b-it
dvc add models/gemma-3-4b-it
git add models/gemma-3-4b-it.dvc .gitignore
git commit -m "Track Gemma 3-4B model with DVC"

# Push to DVC remote
dvc push
```

### Pull models from DVC:

```bash
# Pull all tracked models
dvc pull

# Pull specific model
dvc pull models/gemma-3-4b-it.dvc
```

## Model Versioning Strategy

1. **Version Control**: All model metadata and references tracked in Git via `.dvc` files
2. **Binary Storage**: Large model binaries stored in DVC remote (S3, GCS, etc.)
3. **Reproducibility**: Exact model versions pinned for each experiment
4. **Collaboration**: Team members can pull exact model versions using DVC

## Adding New Models

```bash
# 1. Download model locally
huggingface-cli download <model-name> --local-dir models/<model-name>

# 2. Track with DVC
dvc add models/<model-name>

# 3. Commit to git
git add models/<model-name>.dvc .gitignore
git commit -m "Add <model-name> model"

# 4. Push to DVC remote
dvc push
```

## CI/CD Integration

DVC is integrated in the CI/CD pipeline:
- Models are automatically pulled during deployment
- Model checksums verified for integrity
- Failed pulls trigger pipeline failure

See `.github/workflows/ci.yml` for implementation details.
