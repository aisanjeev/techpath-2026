# Month 9 — Cloud Security: Quick Revision Notes

## Shared Responsibility Model

| Layer | AWS manages | Customer manages |
|---|---|---|
| Physical | Data centre, hardware, networking | Nothing |
| Virtualisation | Hypervisor, host OS | Nothing |
| Platform (IaaS) | Compute, storage, networking services | OS, runtime, data, applications |
| Platform (PaaS) | OS, runtime, middleware | Application code, data |
| SaaS | Everything except user config | Access controls, data, configuration |

**Key principle**: AWS secures *of* the cloud; you secure *in* the cloud.

## AWS IAM Core Concepts

| Concept | Description |
|---|---|
| Principal | Who makes the request: user, role, service, account |
| Policy | JSON document defining Allow/Deny on actions + resources |
| Role | Identity assumed by a service or user (no long-term credentials) |
| Permission boundary | Maximum permissions a role or user can have |
| SCP | Service Control Policy — org-wide guardrails (AWS Organizations) |
| ABAC | Attribute-Based Access Control — tags drive permissions |
| RBAC | Role-Based Access Control — group-based access |

```json
// Minimal least-privilege IAM policy example
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadSpecificBucket",
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::my-bucket/*"
    }
  ]
}
```

## Azure Identity Concepts

| Concept | AWS Equivalent | Description |
|---|---|---|
| Entra ID (AAD) | IAM + Cognito | Identity provider for Azure and M365 |
| Service Principal | IAM Role | App identity in Entra ID |
| Managed Identity | IAM Instance Profile | Credential-free identity for Azure services |
| Azure RBAC | IAM Role + Policy | Role assignments on resources/resource groups |
| Conditional Access | IAM Condition / SCP | Policy engine for adaptive auth (MFA, location) |

## Cloud Privilege Escalation Patterns

```bash
# Over-permissive role — IAM pass-role abuse
# Attacker has: iam:PassRole + ec2:RunInstances
# They launch an EC2 with a privileged role attached
aws ec2 run-instances --image-id ami-xxxxx \
  --iam-instance-profile Name=AdminRole \
  --instance-type t2.micro

# Wildcard policy abuse
"Action": ["*"]   # Full admin — never do this
"Resource": ["*"] # All resources — combine with overly broad Action = very dangerous

# Assume role chain
aws sts assume-role --role-arn arn:aws:iam::123456789:role/PrivilegedRole \
  --role-session-name pwned
```

## Storage Security

| Service | Risk | Fix |
|---|---|---|
| S3 | Public ACLs, no encryption, wide bucket policy | Block Public Access, SSE-S3/KMS, restrict to VPC endpoint |
| Azure Blob | Public anonymous access, SAS token leakage | Disable public access, use private endpoints, expire SAS |
| GCS | allUsers ACL | Remove allUsers, use Uniform bucket-level access |

```bash
# Block all S3 public access at account level
aws s3control put-public-access-block \
  --account-id 123456789012 \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

## Network Security Layers

| Concept | AWS | Azure | Purpose |
|---|---|---|---|
| Virtual Network | VPC | VNet | Isolated network for resources |
| Subnet isolation | Public/Private subnets | Subnet tiers | Separate internet-facing from internal |
| Firewall (instance) | Security Group | NSG | Stateful port/IP rules |
| Firewall (subnet) | NACL | NSG (subnet) | Stateless rules |
| Private connectivity | PrivateLink / VPC Endpoint | Private Endpoint | Access services without internet |
| WAF | AWS WAF | Azure WAF | Layer 7 protection |

## Container & Kubernetes Security

```yaml
# Pod Security — never run as root
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop: ["ALL"]
```

- Image scanning: Trivy, ECR image scanning, Azure Defender for Containers
- Secrets: Kubernetes Secrets (base64, not encrypted at rest by default) → use Vault or AWS Secrets Manager
- RBAC: Least-privilege ServiceAccount per workload; never use `cluster-admin` for apps
- Pod-to-pod: Network policies to restrict lateral movement

## IaC Security Tools

| Tool | What it scans | Install |
|---|---|---|
| Checkov | Terraform, CloudFormation, Kubernetes | `pip install checkov` |
| tfsec | Terraform | `brew install tfsec` |
| Terrascan | Terraform, Kubernetes, Helm | GitHub: accurics/terrascan |
| KICS | IaC across all formats | https://kics.io |

```bash
# Scan Terraform code with Checkov
checkov -d ./terraform --framework terraform

# Scan with tfsec
tfsec ./terraform
```

## Multi-Cloud Posture Assessment

- **Prowler** — AWS/Azure/GCP — 300+ checks based on CIS benchmarks
- **ScoutSuite** — multi-cloud audit tool — generates HTML report with findings
- **CloudSploit** — continuous cloud misconfiguration detection

```bash
# Run Prowler against AWS
prowler aws --service s3 iam cloudtrail

# Run ScoutSuite against AWS
python scout.py aws --profile default
```
