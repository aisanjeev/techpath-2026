# Cloud Infrastructure Security — Securing Storage, Network, and Containers

## Securing Cloud Storage

Storage misconfigurations are among the most common causes of data breaches. Misconfigured S3 buckets have exposed data from healthcare providers, government agencies, and Fortune 500 companies.

### AWS S3 Security

```bash
# Check if public access block is enabled (it should be!)
aws s3api get-public-access-block --bucket my-bucket

# Enable public access block on ALL accounts
aws s3control put-public-access-block \
  --account-id 123456789012 \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Enable server-side encryption by default
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"}}]
  }'

# Enable versioning (protection against ransomware)
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled

# Enable S3 access logging
aws s3api put-bucket-logging \
  --bucket my-bucket \
  --bucket-logging-status '{"LoggingEnabled": {"TargetBucket": "my-logs-bucket", "TargetPrefix": "s3-access/"}}'
```

**S3 Bucket Policy — Deny all non-HTTPS:**
```json
{
  "Statement": [{
    "Sid": "DenyHTTP",
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"],
    "Condition": {"Bool": {"aws:SecureTransport": "false"}}
  }]
}
```

### Azure Blob Storage Security

```bash
# Disable public access on storage account
az storage account update \
  --name mystorageaccount \
  --resource-group myRG \
  --allow-blob-public-access false

# Enable soft delete (ransomware protection)
az storage blob service-properties delete-policy update \
  --account-name mystorageaccount \
  --days-retained 30 \
  --enable true

# Generate SAS token (time-limited, scope-limited access)
az storage blob generate-sas \
  --account-name mystorageaccount \
  --container-name mycontainer \
  --name myblob \
  --permissions r \
  --expiry 2026-08-05T12:00:00Z
```

**SAS Token Security Rules:**
- Never generate tokens with Write+Delete unless absolutely necessary
- Set short expiry times (hours, not months)
- Use Service SAS over Account SAS (smaller scope)
- Rotate SAS tokens regularly

---

## Cloud Network Security

### VPC/VNet Architecture Principles

```
Internet
    ↓
Internet Gateway / Azure Application Gateway
    ↓
Public Subnet (Load Balancers, NAT Gateways only)
    ↓
Private Subnet (Application servers)
    ↓
Database Subnet (RDS, Azure SQL — no internet route)
```

**Key rules:**
- Databases NEVER in public subnets
- Application servers have no direct internet route (NAT Gateway for outbound)
- Use private endpoints for cloud services (S3, Azure Storage) — traffic stays in AWS/Azure network
- VPC Flow Logs / NSG Flow Logs enabled for forensic capability

### AWS Security Groups vs NACLs

| Feature | Security Group | NACL |
|---------|----------------|------|
| Operates at | Instance level | Subnet level |
| State | Stateful (return traffic auto-allowed) | Stateless (must allow both directions) |
| Rules | Allow only | Allow AND Deny |
| Evaluation | All rules evaluated | Rules evaluated in order (lowest number first) |

```bash
# Restrict SSH to specific IP (not 0.0.0.0/0!)
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 22 \
  --cidr 203.0.113.5/32  # Your specific IP only

# Find security groups with 0.0.0.0/0 on sensitive ports
aws ec2 describe-security-groups \
  --filters Name=ip-permission.from-port,Values=22 \
             Name=ip-permission.cidr,Values=0.0.0.0/0 \
  --query 'SecurityGroups[*].GroupId'
```

---

## Container & Kubernetes Security

### Container Image Security

```bash
# Scan an image for vulnerabilities with Trivy
trivy image nginx:latest
trivy image --severity HIGH,CRITICAL python:3.11-slim

# Dockerfile best practices
# BAD:
FROM ubuntu:latest
RUN apt-get install -y everything
USER root  # Never do this!

# GOOD:
FROM ubuntu:22.04  # Pin version
RUN apt-get install -y --no-install-recommends nginx \
    && rm -rf /var/lib/apt/lists/*  # Clean up layers
USER 1001  # Non-root user
COPY --chown=1001:1001 ./app /app  # Correct ownership
```

### Kubernetes Security — Key Controls

**RBAC (Role-Based Access Control):**
```yaml
# Good: Minimal ClusterRole for a monitoring service
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]   # Read only — NOT create/delete
```

**Bad patterns to avoid:**
```yaml
# NEVER do this in production:
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]   # Full cluster admin — enormous blast radius
```

**Pod Security:**
```yaml
# Enforce non-root, read-only filesystem, drop capabilities
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    readOnlyRootFilesystem: true
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]  # Drop all Linux capabilities
```

**Secrets management (NEVER put secrets in YAML files):**
```bash
# Use AWS Secrets Manager or HashiCorp Vault
# Mount secrets as environment variables via External Secrets Operator
# Or use AWS IRSA to give pods access to Secrets Manager via IAM role
```

---

## Cloud-Native Security Monitoring

### AWS GuardDuty

GuardDuty analyses CloudTrail, VPC Flow Logs, and DNS logs using threat intelligence and ML to detect:
- Compromised EC2 instances communicating with known malicious IPs
- IAM credential exfiltration and unusual API activity
- Cryptocurrency mining on EC2
- Exposed S3 buckets being accessed by suspicious IPs

```bash
# Enable GuardDuty
aws guardduty create-detector --enable --finding-publishing-frequency SIX_HOURS

# List high severity findings
aws guardduty list-findings \
  --detector-id $(aws guardduty list-detectors --query 'DetectorIds[0]' --output text) \
  --finding-criteria '{"Criterion": {"severity": {"Gte": 7}}}'
```

### Infrastructure as Code Security — Checkov

```bash
# Install Checkov
pip install checkov

# Scan Terraform files
checkov -d ./terraform/

# Scan a specific file
checkov -f main.tf

# Output as JSON for CI/CD integration
checkov -d . -o json > checkov_results.json
```

Common Terraform misconfigurations Checkov catches:
- S3 buckets without encryption
- Security groups allowing 0.0.0.0/0 on all ports
- Unencrypted RDS instances
- Missing CloudTrail logging
- Public ECR repositories

### Prowler — Multi-Cloud Security Assessment

```bash
# Install Prowler
pip install prowler

# Run AWS CIS Benchmark checks
prowler aws --compliance cis_aws_2.0

# Run specific checks
prowler aws --checks s3_bucket_public_access_block

# Export to CSV
prowler aws -M csv -o /tmp/prowler-results
```

---

## Cloud Security Certifications

| Cert | Provider | Focus | Difficulty |
|------|----------|-------|-----------|
| **AWS Security Specialty** | Amazon | AWS security services, IAM, compliance | Advanced |
| **Azure AZ-500** | Microsoft | Azure Security technologies | Intermediate |
| **Google PCSE** | Google | GCP security | Advanced |
| **CCSP** | (ISC)² | Vendor-neutral cloud security | Advanced |
| **AWS SAA-C03** | Amazon | Cloud fundamentals (prerequisite) | Intermediate |

**Recommended path:** AWS SAA (foundations) → AWS Security Specialty OR AZ-900 (foundations) → AZ-500
