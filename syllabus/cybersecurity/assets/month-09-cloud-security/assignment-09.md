# Month 9 — Cloud Security: Assignment

**Total Marks: 100**
**Submission:** PDF report with AWS CLI command outputs + screenshots. Due end of Month 9 Week 4.

---

## Setup Requirements

You need an AWS free-tier account (or Azure subscription) for this assignment.

```bash
# Configure AWS CLI
aws configure
# Enter: Access Key, Secret Key, Region (eu-west-1 or us-east-1), Output (json)

# Install Prowler
pip install prowler

# Install Checkov
pip install checkov
```

---

## Task 1 — IAM Security Audit (30 marks)

Using the AWS Console and CLI against your own AWS account:

1. Generate and download the IAM Credential Report:
   ```bash
   aws iam generate-credential-report
   aws iam get-credential-report --query 'Content' --output text | base64 -d > credential-report.csv
   ```
   Analyse the report and document: any users with passwords older than 90 days, any users with unused access keys, any users without MFA enabled.

2. Simulate the IAM principal policy to test what permissions your current IAM user has:
   ```bash
   aws iam simulate-principal-policy \
     --policy-source-arn arn:aws:iam::YOUR_ACCOUNT:user/YOUR_USER \
     --action-names s3:GetObject ec2:DescribeInstances iam:CreateUser
   ```
   Document which actions are allowed vs denied.

3. Create a **least-privilege IAM policy** that allows an application to:
   - Read from a specific S3 bucket (`my-app-data`)
   - Write logs to a specific CloudWatch log group
   - No other permissions

   Write the JSON policy and attach it to a test IAM role.

**Deliverables:** Credential report analysis table, simulate-policy output screenshot, policy JSON in the report.

---

## Task 2 — S3 Security Misconfiguration & Remediation (25 marks)

1. Create an S3 bucket with deliberately insecure settings (for testing only):
   ```bash
   aws s3api create-bucket --bucket your-test-bucket-UNIQUE --region eu-west-1 \
     --create-bucket-configuration LocationConstraint=eu-west-1
   
   # Intentionally disable the public access block
   aws s3api delete-public-access-block --bucket your-test-bucket-UNIQUE
   ```

2. Run Prowler's S3 checks against the bucket:
   ```bash
   prowler aws --service s3 --output-formats json
   ```

3. Document each finding Prowler reports (severity, description, resource).

4. Remediate all findings:
   ```bash
   # Block public access
   aws s3api put-public-access-block --bucket your-test-bucket-UNIQUE \
     --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
   
   # Enable default encryption
   aws s3api put-bucket-encryption --bucket your-test-bucket-UNIQUE \
     --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms"}}]}'
   
   # Enable versioning
   aws s3api put-bucket-versioning --bucket your-test-bucket-UNIQUE \
     --versioning-configuration Status=Enabled
   ```

5. Re-run Prowler and confirm the findings are resolved.

**Deliverables:** Before/after Prowler finding counts, remediation commands used, final Prowler output.

---

## Task 3 — Terraform IaC Security Scanning (25 marks)

Write a Terraform configuration that intentionally contains security misconfigurations, then scan and fix them.

**Insecure Terraform file (`main.tf`):**
```hcl
resource "aws_security_group" "insecure" {
  name = "insecure-sg"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "company-data-bucket"
  acl    = "public-read"
}
```

1. Run Checkov and tfsec against the file:
   ```bash
   checkov -f main.tf
   tfsec main.tf
   ```

2. Document every finding (check ID, severity, description).

3. Write a remediated `main_secure.tf` that passes all checks.

**Deliverables:** Checkov output screenshot, finding list table, remediated Terraform code in report.

---

## Task 4 — Cloud Security Posture Report (20 marks)

Write a Cloud Security Posture Assessment report for your test AWS account covering findings from Tasks 1-3.

**Structure:**
- Executive Summary (4-6 sentences including overall risk rating)
- Findings Table:

| Finding | Service | Severity | CIS Control | Remediated? |
|---------|---------|----------|-------------|-------------|
| ... | ... | ... | ... | ... |

- Architecture Recommendation: Draw or describe a secure 3-tier AWS architecture (VPC + public/private subnets + security groups + least-privilege IAM roles)
- Roadmap: 3 short-term (immediate), 3 medium-term (1 month) actions

---

## Marking Rubric

| Task | Criteria | Marks |
|---|---|---|
| Task 1 | Credential report analysed with specific findings | 10 |
| Task 1 | Simulate-policy output documented | 8 |
| Task 1 | Least-privilege policy JSON correct and attached | 12 |
| Task 2 | Prowler findings documented before remediation | 10 |
| Task 2 | All findings remediated + re-run shows clean | 10 |
| Task 2 | Remediation commands included in report | 5 |
| Task 3 | Checkov/tfsec findings list complete | 10 |
| Task 3 | Remediated Terraform passes all checks | 15 |
| Task 4 | Executive summary with risk rating | 5 |
| Task 4 | Findings table with CIS controls | 5 |
| Task 4 | Architecture diagram/description | 5 |
| Task 4 | Prioritised roadmap | 5 |
| **Total** | | **100** |

---

> **Cleanup:** After completing this assignment, delete all AWS resources created (S3 bucket, IAM roles/policies, security groups) to avoid ongoing charges.
