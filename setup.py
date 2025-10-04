"""Setup configuration for RAG-with-Gemma package"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rag-with-gemma",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Offline RAG system using Google's Gemma LLM with MLOps best practices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/RAG-with-Gemma",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.3.4",
            "pytest-cov>=6.0.0",
            "black>=24.10.0",
            "flake8>=7.1.1",
            "mypy>=1.13.0",
        ],
        "mlops": [
            "mlflow>=2.19.0",
            "dvc>=3.59.1",
            "prometheus-client>=0.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rag-api=run_api:main",
            "rag-benchmark=benchmark:main",
            "rag-mlflow=mlflow_experiment:main",
        ],
    },
)
