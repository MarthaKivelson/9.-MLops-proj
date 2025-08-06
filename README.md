🚗 End-to-End Vehicle Price Prediction (MLOps Project)
This repository contains the source code for an end-to-end Machine Learning Operations (MLOps) project focused on predicting vehicle prices. The project covers the entire ML lifecycle, from data ingestion and validation to model training, deployment as a web service, and automation via a CI/CD pipeline.

🌟 Features
Modular Pipeline Architecture: A structured and scalable ML pipeline with distinct components for data ingestion, validation, transformation, model training, evaluation, and pushing.

MongoDB Integration: Uses MongoDB Atlas as a NoSQL database for storing and retrieving the raw dataset.

Cloud Storage for Models: Leverages AWS S3 for robust and versioned model storage and registry.

Automated CI/CD: A complete CI/CD pipeline using GitHub Actions to automatically build, test, and deploy the application.

Containerization with Docker: The entire application is containerized using Docker for consistent environments and scalable deployments.

Cloud Deployment: Deployed on an AWS EC2 instance with models served from an ECR (Elastic Container Registry) image.

Web Application: A user-friendly web interface built with FastAPI/Flask for real-time predictions.

Robust Error Handling: Integrated logging and exception handling for maintainability.

⚙️ Technology Stack
Language: Python 3.10

ML Frameworks: Scikit-learn, Pandas, NumPy

Database: MongoDB Atlas

Cloud Services: AWS (EC2, ECR, S3, IAM)

CI/CD: GitHub Actions

Containerization: Docker

Web Framework: FastAPI / Flask

🚀 Project Workflow
The project follows a standard MLOps workflow:

Data Ingestion: Data is fetched from MongoDB Atlas.

Data Validation: The ingested data is validated against a predefined schema (schema.yaml).

Data Transformation: Feature engineering and preprocessing are applied to the data.

Model Training: A machine learning model is trained on the transformed data.

Model Evaluation: The trained model is evaluated against a baseline. If it performs better, it's pushed to the next stage.

Model Pusher: The validated model is pushed to an AWS S3 bucket for storage.

Deployment: A Docker image is built, pushed to AWS ECR, and deployed on an AWS EC2 instance, serving a prediction API.

🔧 Setup and Installation Guide
Follow these steps to set up the project locally and deploy it.

Prerequisites
Git

Conda or a Python virtual environment manager

An AWS Account with IAM user credentials

A MongoDB Atlas Account

1. Local Environment Setup
First, clone the repository and set up your Python environment.

Bash

# Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# Create a Conda virtual environment
conda create -n vehicle python=3.10 -y
conda activate vehicle

# Install project requirements
pip install -r requirements.txt

# Install the local package for src access
pip install -e .
2. MongoDB Atlas Setup
This project uses MongoDB to store the initial dataset.

Sign up for a free account on MongoDB Atlas.

Create a new project.

Create a free M0 cluster.

In Database Access, create a new database user with a secure password.

In Network Access, add 0.0.0.0/0 to the IP access list to allow connections from anywhere.

Go to your cluster's Connect tab, select Drivers, and copy the Python connection string.

Set the connection string as an environment variable. Replace <password> with your database user's password.

Bash

# For Bash/Zsh (Linux/macOS)
export MONGODB_URL="mongodb+srv://user:<password>@cluster-url..."

# For PowerShell (Windows)
$env:MONGODB_URL = "mongodb+srv://user:<password>@cluster-url..."
Run the provided Jupyter notebook in the notebooks folder to push your dataset to the database.

3. AWS Setup for Model Storage and Deployment
The project requires an IAM user, an S3 bucket for models, and an ECR repository for Docker images.

Create an IAM User:

In the AWS IAM console, create a new user.

Attach the AdministratorAccess policy (for simplicity in this project).

Generate an access key (select Command Line Interface (CLI)) and download the CSV file.

Configure AWS CLI credentials: Set the credentials from the downloaded CSV file as environment variables.

Bash

# For Bash/Zsh (Linux/macOS)
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"

# For PowerShell (Windows) - update with your credentials
$env:AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
$env:AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_KEY"
Create an S3 Bucket:

In the AWS S3 console, create a new bucket (e.g., your-name-vehicle-models).

Keep the region as us-east-1.

Uncheck "Block all public access" and acknowledge the warning.

Create an ECR Repository:

In the AWS ECR console, create a new private repository (e.g., vehicleproj).

🛠️ How to Run the Project
Running the Training Pipeline
After setting up the environment variables, you can trigger the entire training pipeline.

Bash

python demo.py
This will execute all the steps from Data Ingestion to Model Pusher, storing the final model artifact in your S3 bucket.

🚀 CI/CD and Deployment
The deployment is fully automated using GitHub Actions.

Workflow
Trigger: A git push to the main branch triggers the GitHub Actions workflow defined in .github/workflows/aws.yaml.

Build: A Docker image is built based on the Dockerfile.

Push: The Docker image is tagged and pushed to the AWS ECR repository.

Deploy: The workflow connects to a pre-configured EC2 instance, pulls the new image from ECR, and starts the container.

Deployment Setup Steps
These steps are handled by the CI/CD pipeline but require a one-time setup.

Launch an EC2 Instance:

Use an Ubuntu Server AMI (e.g., 24.04 LTS).

Choose an instance type (e.g., t2.medium).

Create and download a key pair.

In the security group, allow HTTP (port 80) and HTTPS (port 443) traffic.

Also, add a Custom TCP rule to allow traffic on port 5000 from source 0.0.0.0/0.

Install Docker on EC2:

Connect to your EC2 instance via SSH or EC2 Instance Connect.

Run the following commands:

Bash

sudo apt-get update -y && sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
Configure GitHub Secrets:

In your GitHub repository, go to Settings > Secrets and variables > Actions.

Add the following repository secrets:

AWS_ACCESS_KEY_ID: Your IAM user's access key.

AWS_SECRET_ACCESS_KEY: Your IAM user's secret key.

AWS_DEFAULT_REGION: e.g., us-east-1.

ECR_REPO: The name of your ECR repository (e.g., vehicleproj).

MONGODB_URL: Your MongoDB connection string.

After pushing a change to main, the application will be automatically deployed. You can access it via: http://<your-ec2-public-ip>:5000.

📂 Project Structure
.
├── .github/workflows/         # GitHub Actions CI/CD pipeline
│   └── aws.yaml
├── notebooks/                 # Jupyter notebooks for EDA and experiments
├── src/                       # Source code for the project
│   ├── components/            # ML pipeline components
│   ├── config/                # Configuration files (schema)
│   ├── constant/              # Project constants
│   ├── data_access/           # Scripts for accessing data
│   ├── entity/                # Project entities (configs, artifacts)
│   ├── exception/             # Custom exception handling
│   ├── logger/                # Logging setup
│   ├── pipeline/              # ML pipeline definitions
│   └── utils/                 # Utility functions
├── static/                    # Static files for the web app (CSS, JS)
├── templates/                 # HTML templates for the web app
├── app.py                     # Main application file (Flask/FastAPI)
├── demo.py                    # Script to run the training pipeline
├── Dockerfile                 # Docker configuration for the application
├── requirements.txt           # Python package requirements
├── setup.py                   # Setup script for installing local packages
└── template.py                # Script to create the initial project structure