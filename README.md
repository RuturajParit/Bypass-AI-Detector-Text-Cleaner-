# CCA2: CI/CD Pipeline Using Jenkins, Docker and Kubernetes

## 1. Project Overview

This project demonstrates an automated CI/CD pipeline for a Python-based text-cleaning application. Jenkins automates source-code checkout, validation, Docker image creation, image publishing, Kubernetes execution, and output artifact archiving.

## 2. Technologies Used

- Git and GitHub — source-code management
- Jenkins — CI/CD automation
- Docker — application containerization
- Docker Hub — container image registry
- Kubernetes — container orchestration
- Python — text-cleaning application
- AWS EC2 — cloud-hosted environment (if applicable to the actual deployment)

## 3. Project Structure

```text
.
├── Jenkinsfile
├── Dockerfile
├── src/
│   └── cleaner.py
├── examples/
│   └── assignment.txt
├── k8s/
│   └── job.yaml
└── output/
    └── clean_assignment.txt
```

## 4. Deployment Process

1. The source code is stored in GitHub.
2. Jenkins checks out the repository.
3. The pipeline validates the Python source files.
4. Docker builds the application image.
5. Jenkins authenticates with Docker Hub and pushes the versioned image.
6. Kubernetes runs the application using the image created for that build.
7. The cleaned output is retrieved and archived as a Jenkins build artifact.

## 5. Output

The application processes the input text and generates `output/clean_assignment.txt`. Jenkins archives this file after successful execution.

## 6. Result

The project demonstrates an automated CI/CD workflow integrating GitHub, Jenkins, Docker, Docker Hub, and Kubernetes. Attach screenshots of the actual pipeline execution and deployment results as evidence.

## 7. Repository

https://github.com/RuturajParit/Bypass-AI-Detector-Text-Cleaner-
