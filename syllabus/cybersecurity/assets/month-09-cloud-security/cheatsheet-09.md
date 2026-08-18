# Month 9 — Cloud Security Cheat Sheet

## AWS IAM Policy Structure

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "StatementID",
      "Effect": "Allow | Deny",
      "Principal": {"AWS": "arn:aws:iam::ACCOUNT:root"},
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": ["arn:aws:s3:::bucket-name/*"],
      "Condition": {
        "StringEquals": {"aws:RequestedRegion": "eu-west-1"},
        "Bool": {"aws:MultiFactorAuthPresent": "true"}
      }
    }
  ]
}
```

## AWS CLI Security Commands

| Command | Purpose |
|---|---|
| `aws iam get-account-authorization-details` | Full IAM snapshot |
| `aws iam simulate-principal-policy` | Test what a principal can do |
| `aws iam list-attached-user-policies --user-name X` | Policies on a user |
| `aws iam generate-credential-report` | Download credential report CSV |
| `aws s3api get-bucket-policy --bucket NAME` | View bucket policy |
| `aws s3api get-public-access-block --bucket NAME` | Check public access block |
| `aws iam list-roles` | List all IAM roles |
| `aws sts get-caller-identity` | Who am I? (current credentials) |
| `aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=ConsoleLogin` | Find console logins |
| `aws guardduty list-findings --detector-id ID` | List GuardDuty findings |

## Azure RBAC Quick Reference

| Built-in Role | Scope | Access Level |
|---|---|---|
| Owner | Subscription/RG/Resource | Full access + can assign roles |
| Contributor | Subscription/RG/Resource | Full access, cannot assign roles |
| Reader | Any | Read-only |
| User Access Administrator | Any | Manage access, no resource access |
| Storage Blob Data Owner | Storage Account | Full blob access |

```bash
# Azure CLI — assign RBAC role
az role assignment create \
  --assignee "user@domain.com" \
  --role "Reader" \
  --scope "/subscriptions/SUB_ID/resourceGroups/my-rg"

# List role assignments
az role assignment list --all --output table

# Check effective permissions on a resource
az resource show --ids /subscriptions/.../resourceGroups/rg/providers/...
```

## Dangerous IAM Permission Combinations

| Permissions | Risk |
|---|---|
| `iam:*` | Full IAM control → create admin user |
| `iam:PassRole` + `ec2:RunInstances` | Attach privileged role to new instance |
| `iam:CreatePolicyVersion` | Add admin policy to existing policy |
| `iam:AttachUserPolicy` + `iam:CreateUser` | Create admin user |
| `lambda:CreateFunction` + `iam:PassRole` | Deploy function with privileged role |
| `sts:AssumeRole` (wildcard resource) | Assume any role in account |
| `s3:GetObject` on `*` | Read all S3 data in account |

## Network Security Groups (AWS Security Groups)

```bash
# Dangerous: allow all inbound
"IpRanges": [{"CidrIp": "0.0.0.0/0"}]   # Never for SSH/RDP/DB

# Find publicly open SSH (port 22) in AWS
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?FromPort==`22` && IpRanges[?CidrIp==`0.0.0.0/0`]]]'

# Remediation — restrict to VPN/bastion CIDR
"CidrIp": "10.0.0.0/8"   # Private network only
```

## Kubernetes RBAC Cheat Sheet

```yaml
# Least-privilege ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]   # No create/delete/exec

---
# Dangerous: never grant this to applications
kind: ClusterRoleBinding
roleRef:
  name: cluster-admin   # Full cluster access
subjects:
- kind: ServiceAccount
  name: my-app  # Application should NOT have cluster-admin
```

## Cloud Security Monitoring — Key Events to Alert On

| Event | Service | Why |
|---|---|---|
| ConsoleLogin without MFA | CloudTrail | Account compromise risk |
| IAM policy change | CloudTrail | Privilege escalation |
| Root account usage | CloudTrail | Always alert — should never be used |
| S3 public access enabled | CloudTrail | Data exposure |
| Security group 0.0.0.0/0 added | CloudTrail | Network exposure |
| GuardDuty: CryptoCurrency:EC2/BitcoinTool.B | GuardDuty | Cryptomining |
| GuardDuty: UnauthorizedAccess:IAMUser | GuardDuty | Credential compromise |
| Unusual region activity | CloudTrail | Lateral movement / exfiltration |

## Zero-Trust Principles

```
Never trust, always verify:
1. Verify identity explicitly (MFA, device health, location)
2. Use least-privilege access (JIT/JEA — just-in-time, just-enough)
3. Assume breach (segment everything, log everything, detect fast)

Practical controls:
- No implicit trust based on network location (VPN ≠ secure)
- Strong identity for every workload (managed identities, SPIFFE/SPIRE)
- Microsegmentation: each service talks only to what it needs
- Continuous validation: re-check trust at each access decision
```
