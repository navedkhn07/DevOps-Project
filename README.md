## DevOps Portfolio: Multi-Cloud IaC, Kubernetes, CI/CD, DevSecOps & AIOps

### Project Overview
This portfolio demonstrates a realistic, production-grade DevOps implementation across IaC (Terraform for AWS & Azure), Kubernetes orchestration, CI/CD with zero-downtime deployments, integrated DevSecOps scanning, and AIOps-style anomaly detection with monitoring (Prometheus + Grafana).

### Tools Used
- Terraform, AWS, Azure
- Docker, GitHub Actions
- Kubernetes, Kustomize, NGINX Ingress, cert-manager
- SonarQube, Trivy, Snyk
- Prometheus, Grafana
- Python (AIOps anomaly simulation)

### Architecture Diagram (ASCII)
```
 dev -> PR -> GitHub Actions -> build/test -> scan (Sonar/Trivy/Snyk)
                                 |
                                 v
                         push container to GHCR
                                 |
                                 v
                      kustomize deploy -> Kubernetes
                               /                 \
                       staging cluster       prod cluster
                            |                      |
                        sample-app           sample-app
                      (Deployment/Service)  (Deployment/Service)
                            |                      |
                        NGINX Ingress <---- TLS via cert-manager
                            |
                         Users/Traffic

 Terraform (AWS/Azure):
  - AWS: VPC, Subnets, SG, EC2 (nginx), S3 (encrypted)
  - Azure: RG, VNet/Subnet, NSG, Public IP, NIC, Linux VM (nginx), Blob

 Monitoring & AIOps:
  - Prometheus scrapes metrics, Grafana dashboards
  - Python script simulates log anomalies for predictive/thresholding demo
```

### Setup Instructions

#### 1) Terraform IaC
- AWS
  - Configure credentials (profile or env). Edit `terraform/aws/variables.tf` as needed.
  - Provide a unique `s3_bucket_name`.
  - Commands:
    ```bash
    cd terraform/aws
    terraform init
    terraform apply -auto-approve
    ```
- Azure
  - Export `ARM_*` or set `subscription_id`, `tenant_id` in `terraform/azure/variables.tf` via TFVARS.
  - Provide a globally unique `storage_account_name` and your `ssh_public_key`.
  - Commands:
    ```bash
    cd terraform/azure
    terraform init
    terraform apply -auto-approve
    ```

#### 2) Kubernetes Manifests
- Base manifests in `k8s/base` with `Deployment`, `Service`, `Ingress`, `ConfigMap`, `Secret`, `HPA`.
- Overlays for staging and prod using Kustomize.
- Apply:
  ```bash
  # staging
  kustomize build k8s/overlays/staging | kubectl apply -f -
  kubectl -n staging rollout status deployment/stg-sample-app

  # production
  kustomize build k8s/overlays/production | kubectl apply -f -
  kubectl -n production rollout status deployment/prod-sample-app
  ```

#### 3) CI/CD Pipeline
- GitHub Actions workflow in `.github/workflows/cicd.yaml`:
  - Builds container, runs pytest, pushes to GHCR
  - Runs SonarQube scan (`SONAR_TOKEN`, `SONAR_HOST_URL` secrets)
  - Trivy image scan (fails on HIGH/CRITICAL)
  - Snyk container scan (fails on high severity)
  - Deploys to Kubernetes with rolling updates via Kustomize (staging then prod)
- Required GitHub secrets:
  - `SONAR_TOKEN`, `SONAR_HOST_URL`
  - `SNYK_TOKEN`
  - `KUBE_CONFIG_STAGING_B64`, `KUBE_CONFIG_PROD_B64` (base64 kubeconfigs)

#### 4) Monitoring & Dashboards
- Prometheus config in `monitoring/prometheus/prometheus.yml` (includes rules hook)
- Grafana configs in `monitoring/grafana/*` with Prometheus data source
- Deploy your Prometheus/Grafana stack (Helm or manifests) and import dashboards

#### 5) AIOps Anomaly Detection (Demo)
- Script `scripts/anomaly_detector.py` simulates a stream of log events and flags anomalies using a rolling z-score.
- Run locally:
  ```bash
  python scripts/anomaly_detector.py
  ```

### Key Learnings
- Multi-cloud IaC patterns with Terraform, secure defaults, and outputs for ops.
- Kubernetes rolling updates, readiness/liveness, and HPA for elastic scaling.
- CI/CD with environment promotion, image metadata, and zero-downtime deploys.
- DevSecOps integration that gates releases on code quality and vulnerability scans.
- Observability and AIOps foundations with metrics, dashboards, and anomaly signals.

