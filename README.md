
# CORE-KUBEAUTO-DEMO-APP

This repository contains a lightweight Flask-based demo application deployed using Helm, secured with Calico NetworkPolicy, and exposed via Istio Gateway. It is integrated into a GitOps pipeline using OCI Helm registry and ArgoCD for deployment to Azure Kubernetes Service (AKS).

## Application Overview

This project is a simple Python Flask application that exposes two REST APIs. The containerized app is deployed to an Azure Kubernetes Service (AKS) cluster using Helm charts and managed by ArgoCD.

## Flask API

### GET `/`

Returns the current message.

**Response:**
```json
{
  "message": "Hello World"
}
```

### POST `/push`

Updates the internal message.

**Request:**
```json
{
  "message": "Hello from client"
}
```

**Response:**
```json
{
  "message": "Message updated to: Hello from client"
}
```

## Technology Stack

- Python Flask microservice
- Docker for containerization
- Helm 3 for Kubernetes packaging
- Istio Gateway and VirtualService for ingress
- Calico NetworkPolicy for security
- OCI Helm Registry for chart storage
- ArgoCD for GitOps-based continuous deployment
- Azure Kubernetes Service (AKS) as the target platform

## Project Structure

```
core-kubeauto-demo-app/
├── app.py                         # Flask application
├── Dockerfile                     # Container build file
├── azure-pipeline.yml             # Azure DevOps pipeline for building and pushing
├── charts/
│   ├── Chart.yaml                 # Helm chart metadata
│   ├── values.yaml                # Configurable Helm values
│   └── template/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── demo-app-istio-gateway.yaml
│       ├── demo-app-istio-virtualservice.yaml
│       └── demo-app-network-policy.yaml
```

## Docker Build

The Dockerfile uses `python:3.9-slim` and exposes port 5000.

```bash
docker build -t demo-app:latest .
```

## Helm Chart Usage

### 1. Package the chart:

```bash
helm package charts/
```

### 2. Push to OCI registry:

```bash
helm push demo-app-0.1.0.tgz oci://<your-registry>.azurecr.io/helm
```

Authenticate using:

```bash
az acr login --name <your-registry>
```

## Deployment via ArgoCD

ArgoCD is configured to watch the OCI Helm registry and deploy the chart to the `demo-app-dev` namespace in AKS.

### Example ArgoCD Application manifest:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: demo-app
  namespace: argocd
spec:
  destination:
    namespace: demo-app-dev
    server: https://kubernetes.default.svc
  source:
    chart: demo-app
    repoURL: oci://<your-registry>.azurecr.io/helm
    targetRevision: 0.1.0
  project: default
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Network Policy

The policy in `demo-app-network-policy.yaml` allows ingress from:

- The `demo-app-dev` namespace
- The `istio-system` namespace
- The AKS cluster node subnet (e.g., `10.216.91.176/28`)

Egress is allowed with logging enabled.


