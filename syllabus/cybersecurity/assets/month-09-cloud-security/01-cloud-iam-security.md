# Cloud IAM Security — Identity is the New Perimeter

## Why Identity is the #1 Cloud Breach Cause

In traditional on-premises networks, the perimeter was the firewall. In the cloud, **identity is the perimeter**. The most common cloud breaches — Capital One, Uber, LastPass — exploited overly permissive IAM roles, exposed credentials, or misconfigured trust policies.

In cloud environments:
- A single over-permissive IAM role can grant access to millions of records
- Credentials in source code are scraped by bots within minutes of being pushed
- Every cloud action leaves an API call — meaning IAM controls determine what damage is possible

---

## AWS IAM Deep Dive

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Principal** | Who is making the request: IAM user, role, service, or federated identity |
| **Policy** | JSON document defining what actions are allowed/denied on which resources |
| **Role** | An identity with a policy, assumed temporarily (no long-term credentials) |
| **Permission Boundary** | Max permissions a principal can ever have — even if their policy grants more |
| **Service Control Policy (SCP)** | Org-level guardrails applied to entire AWS accounts |

### IAM Policy Anatomy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3ReadOnly",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-secure-bucket",
        "arn:aws:s3:::my-secure-bucket/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:RequestedRegion": "ap-south-1"
        }
      }
    }
  ]
}
```

**Dangerous patterns to identify:**
```json
// Wildcard action — grants ALL S3 permissions
"Action": "s3:*"

// Wildcard resource — applies to ALL resources
"Resource": "*"

// Both wildcards = admin-equivalent for this service
"Action": "*",
"Resource": "*"
```

### IAM Privilege Escalation Paths

Common ways attackers escalate from a limited IAM identity to full admin:

| Technique | Dangerous Permission Required |
|-----------|------------------------------|
| Attach admin policy to self | `iam:AttachUserPolicy` |
| Create new admin user | `iam:CreateUser` + `iam:AttachUserPolicy` |
| Add self to admin group | `iam:AddUserToGroup` |
| Assume high-privilege role | `sts:AssumeRole` (without conditions) |
| Update existing policy to add `*` | `iam:CreatePolicyVersion` |
| Pass a privileged role to EC2 | `iam:PassRole` + `ec2:RunInstances` |

**Tool for discovering escalation paths:** Cloudsplaining and PMapper can visualise these paths automatically.

### Roles vs Users — Always Prefer Roles

**IAM Users** have long-term access keys — these are static credentials that:
- Get committed to code, Dockerfiles, CI/CD configs
- Don't expire automatically
- Are the #1 cause of cloud credential leaks

**IAM Roles** are temporary — assumed for sessions of minutes to hours:
```bash
# EC2 instance role — no keys needed in code
aws s3 ls s3://bucket  # Works automatically via instance metadata

# Cross-account role assumption
aws sts assume-role \
  --role-arn arn:aws:iam::123456789:role/ReadOnlyRole \
  --role-session-name audit-session

# Lambda execution role — set in function config, not code
```

### AWS Security Best Practices Checklist

- [ ] Root account: MFA enabled, access keys deleted, never used for daily tasks
- [ ] All IAM users have MFA enforced via SCP
- [ ] No `*/*` policies on any principal that doesn't need admin
- [ ] Access keys rotated every 90 days (or replaced with roles)
- [ ] CloudTrail enabled in ALL regions (including global services)
- [ ] GuardDuty enabled in all regions
- [ ] AWS Config with security rules active
- [ ] Permission boundaries on developer accounts
- [ ] SCPs at Organisation level blocking dangerous actions

---

## Azure RBAC and Entra ID (formerly Azure AD)

### Azure Role-Based Access Control

```
Management Group (top-level)
  └── Subscription
        └── Resource Group
              └── Resource (VM, Storage, KeyVault)

RBAC roles are assigned at any level — lower levels inherit from above
```

**Built-in roles:**
| Role | Can do |
|------|--------|
| **Owner** | Full control + assign roles to others |
| **Contributor** | Create/manage resources, cannot assign roles |
| **Reader** | View only |
| **User Access Administrator** | Manage role assignments only |

### Managed Identities (Azure's answer to IAM roles)

```bash
# System-assigned managed identity — tied to the resource lifecycle
az vm identity assign --name myVM --resource-group myRG

# Use the identity from inside the VM (no credentials in code)
curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/' \
  -H 'Metadata: true'
```

**Dangerous Azure RBAC issues:**
- Service principals with **Owner** role (overly permissive)
- Application registrations with `Directory.ReadWrite.All` (can read entire Active Directory)
- Conditional access policies with too many bypasses
- Guest accounts with excessive permissions

---

## GCP IAM

GCP uses a similar model: **Principals** (users, service accounts, groups) are bound to **roles** on **resources** via **IAM policies**.

```bash
# Grant viewer role on a project
gcloud projects add-iam-policy-binding my-project \
  --member="serviceAccount:my-sa@my-project.iam.gserviceaccount.com" \
  --role="roles/viewer"

# List all IAM bindings (look for overly permissive)
gcloud projects get-iam-policy my-project --format=json
```

**GCP-specific risks:**
- Service account keys downloaded and stored insecurely (prefer Workload Identity Federation)
- `roles/editor` is too permissive for most use cases
- Default service accounts with editor role on Compute Engine instances

---

## Zero Trust in Cloud Environments

Traditional security: trust everything inside the network.
Zero Trust: **never trust, always verify** — regardless of network location.

**Zero Trust principles in cloud:**
1. **Verify explicitly** — authenticate and authorise every request with full context (identity, location, device health, time)
2. **Least privilege** — JIT (Just-In-Time) access, minimum required permissions, short-lived credentials
3. **Assume breach** — design for when, not if. Segment data, encrypt everything, monitor all access

**Practical implementation:**
- Replace VPN with Identity-Aware Proxy (GCP BeyondCorp, Azure AD Application Proxy, Cloudflare Access)
- Use FIDO2/hardware keys for all admin access
- Every service-to-service call uses a service identity with minimal scope
- All traffic encrypted in transit (even internal)
- Continuous monitoring with anomaly detection on access patterns
