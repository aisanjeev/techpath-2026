# Month 9 — Week-by-Week Study Plan
## Cloud Security: AWS, Azure, GCP, and Zero Trust

**Total study time: ~80 hours over 4 weeks**

---

## Week 1 — Cloud Architecture and AWS Security Fundamentals

**Goal:** Understand the shared responsibility model and master AWS IAM, the most critical cloud security control.

### Day 1 — The Cloud Security Mindset
- **Read:** `01-cloud-security-aws.md` — cloud fundamentals section
- **The Shared Responsibility Model — this is foundational:**
  
  | What AWS/Azure/GCP manages | What YOU manage |
  |---------------------------|----------------|
  | Physical data centres | Data encryption in transit + at rest |
  | Hypervisor and host OS | IAM policies and access controls |
  | Network infrastructure | Application security |
  | Underlying services | Patching OS on EC2/VMs you create |
  | DDoS protection of infrastructure | Firewall rules (Security Groups) |

  **Key insight:** The cloud provider secures the INFRASTRUCTURE. You secure everything you BUILD and CONFIGURE on top of it. Most cloud breaches are misconfigurations — IAM errors, public S3 buckets, open security groups.

- **The 6 pillars of AWS Well-Architected Framework (Security pillar):**
  1. Implement a strong identity foundation
  2. Enable traceability (logging, monitoring)
  3. Apply security at all layers
  4. Automate security best practices
  5. Protect data in transit and at rest
  6. Keep people away from data (use automation, not humans with direct access)

### Day 2 — AWS IAM: Identity and Access Management
- **Core IAM concepts:**
  ```
  Principal → makes a request
  Action    → what they want to do (s3:GetObject, ec2:DescribeInstances)
  Resource  → what they want to do it to (arn:aws:s3:::bucket-name/*)
  Effect    → Allow or Deny
  ```
- **IAM policy types:**
  - **Identity-based:** Attached to users/groups/roles — what can THIS identity do?
  - **Resource-based:** Attached to resources (S3 bucket policies) — who can access THIS resource?
  - **Permission boundaries:** Maximum permissions an identity can ever have
  - **SCPs (Service Control Policies):** Org-level guardrails that apply even to admins

- **Write and read IAM policies:**
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        "Resource": [
          "arn:aws:s3:::my-app-bucket",
          "arn:aws:s3:::my-app-bucket/*"
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
- **Principle of Least Privilege for AWS:** Start with no permissions. Grant only what's needed, using specific actions and specific resources — never `*:*`.

### Day 3 — AWS CLI and Hands-on IAM
- **Set up AWS Free Tier account** (if not already done): aws.amazon.com/free
- **AWS CLI configuration:**
  ```bash
  pip install awscli
  aws configure
  # AWS Access Key ID: [your key]
  # AWS Secret Access Key: [your secret]
  # Default region: ap-south-1  (Mumbai for India)
  # Default output format: json
  ```
- **IAM hands-on:**
  ```bash
  # List IAM users
  aws iam list-users
  
  # Create a user with least privilege
  aws iam create-user --user-name lambda-deployer
  aws iam create-policy --policy-name LambdaDeployOnly \
    --policy-document file://lambda-deploy-policy.json
  aws iam attach-user-policy --user-name lambda-deployer \
    --policy-arn arn:aws:iam::123456789012:policy/LambdaDeployOnly
  
  # Simulate policy — will this action be allowed?
  aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::123456789012:user/lambda-deployer \
    --action-names s3:DeleteObject \
    --resource-arns arn:aws:s3:::my-bucket/*
  # Output: Decision = "explicitDeny" or "allowed"
  
  # Find over-privileged users
  aws iam list-users --output json | python3 -c "
  import json, sys
  users = json.load(sys.stdin)['Users']
  for u in users: print(u['UserName'], u.get('PasswordLastUsed', 'NEVER'))"
  
  # List all access keys and when last used
  aws iam list-access-keys --user-name lambda-deployer
  aws iam get-access-key-last-used --access-key-id AKIAIOSFODNN7EXAMPLE
  ```

### Day 4 — S3 Security: The Most Common Cloud Breach Vector
- **Why S3 security matters:** Hundreds of major breaches have resulted from public S3 buckets. In 2017-2020, hundreds of millions of records were exposed due to misconfigured S3 bucket policies.
- **S3 security checklist:**
  ```bash
  # 1. Block all public access at account level (the #1 protection)
  aws s3api put-public-access-block \
    --bucket my-bucket \
    --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
  
  # 2. Enable server-side encryption
  aws s3api put-bucket-encryption --bucket my-bucket \
    --server-side-encryption-configuration \
    '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms"}}]}'
  
  # 3. Enable versioning and MFA delete
  aws s3api put-bucket-versioning --bucket my-bucket \
    --versioning-configuration "Status=Enabled,MFADelete=Enabled"
  
  # 4. Enable access logging
  aws s3api put-bucket-logging --bucket my-bucket \
    --bucket-logging-status '{"LoggingEnabled":{"TargetBucket":"my-logs-bucket","TargetPrefix":"s3/"}}'
  
  # 5. Check for public buckets in your account
  aws s3api list-buckets --output json | python3 -c "
  import json, sys, boto3
  s3 = boto3.client('s3')
  buckets = json.load(sys.stdin)['Buckets']
  for b in buckets:
      acl = s3.get_bucket_acl(Bucket=b['Name'])
      for grant in acl['Grants']:
          if 'AllUsers' in str(grant) or 'AuthenticatedUsers' in str(grant):
              print(f'PUBLIC: {b[\"Name\"]}')"
  ```

### Day 5 — AWS CloudTrail and Security Logging
- **CloudTrail:** Records all API calls in your AWS account. Essential for security, compliance, and incident response.
  ```bash
  # Enable CloudTrail in all regions with log file validation
  aws cloudtrail create-trail \
    --name my-security-trail \
    --s3-bucket-name my-cloudtrail-logs \
    --is-multi-region-trail \
    --enable-log-file-validation
  
  # Search CloudTrail for suspicious activity
  aws cloudtrail lookup-events \
    --lookup-attributes AttributeKey=EventName,AttributeValue=DeleteBucket \
    --start-time 2024-01-01 \
    --output json | python3 -c "
  import json, sys
  events = json.load(sys.stdin)['Events']
  for e in events:
      print(f'{e[\"EventTime\"]} | {e[\"Username\"]} | {e[\"EventName\"]}')"
  
  # CloudWatch alert for root account usage
  aws cloudwatch put-metric-alarm \
    --alarm-name RootAccountLogin \
    --metric-name RootLoginCount \
    --namespace CloudTrailMetrics \
    --statistic Sum \
    --threshold 1 \
    --comparison-operator GreaterThanOrEqualToThreshold \
    --evaluation-periods 1 \
    --alarm-actions arn:aws:sns:...:SecurityAlerts
  ```
- **AWS Security Hub:** Centralised security findings across all AWS services, including automated CIS benchmark checks
- **AWS GuardDuty:** Threat detection using ML on CloudTrail, DNS, VPC Flow logs
- **Complete quiz questions 1-7 from `quiz-09.json`**

---

## Week 2 — Azure, GCP, and Cloud Attack Techniques

**Goal:** Understand multi-cloud security and common attack patterns.

### Day 6 — Azure Security Fundamentals
- **Read:** `02-azure-gcp-zero-trust.md` — Azure section
- **Azure Active Directory (Entra ID):** Microsoft's identity platform — used for SSO across Microsoft 365, Azure, and third-party apps
  ```bash
  # Azure CLI
  az login
  
  # List users
  az ad user list --output table
  
  # List role assignments (who has what access?)
  az role assignment list --all --output table
  
  # Check for stale service principals
  az ad sp list --all --query "[?passwordCredentials[?endDateTime < '2024-01-01']]" --output table
  ```
- **Azure-specific security services:**
  - **Microsoft Defender for Cloud:** Multi-cloud security posture (replaces Azure Security Center)
  - **Azure Sentinel (Microsoft Sentinel):** Cloud-native SIEM with built-in connectors
  - **Azure Key Vault:** Secrets, keys, and certificates management
  - **Conditional Access:** MFA, device compliance, and location-based access policies
  - **Azure Policy:** Automated compliance (deny creating public storage accounts, etc.)

### Day 7 — GCP Security Fundamentals
- **GCP IAM:** Similar to AWS but with key differences
  ```bash
  # gcloud CLI
  gcloud auth login
  gcloud config set project my-project-id
  
  # List IAM policy bindings for a project
  gcloud projects get-iam-policy my-project-id
  
  # Find who has Owner role (most dangerous)
  gcloud projects get-iam-policy my-project-id --format=json | python3 -c "
  import json, sys
  policy = json.load(sys.stdin)
  for binding in policy['bindings']:
      if binding['role'] == 'roles/owner':
          for member in binding['members']:
              print(f'OWNER: {member}')"
  ```
- **GCP Security Command Center:** Similar to AWS Security Hub, centralises findings
- **VPC Service Controls:** Restrict access to GCP services within a security perimeter (prevents data exfiltration)
- **Binary Authorization:** Only deploy containers signed by your CI/CD pipeline

### Day 8 — Cloud Attack Techniques
- **Complete `lab-09-a.json`** — all 5 steps
- **Common cloud attack vectors:**
  
  **1. Metadata API attacks:**
  ```bash
  # If you have SSRF or code execution on a cloud VM, the metadata API gives you:
  curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
  # Returns: access key, secret key, session token for the instance's IAM role
  # → Use these credentials from your attacker's machine
  ```
  
  **2. Overprivileged IAM roles:**
  ```bash
  # If a Lambda function has AdministratorAccess policy → attacker compromising the function
  # gets full AWS account access
  # Enumerate what a role can do:
  aws sts assume-role --role-arn arn:aws:iam::123:role/my-role --role-session-name test
  # Use returned credentials to test permissions
  ```
  
  **3. EC2 user data abuse:**
  ```bash
  # EC2 instances can run a startup script (user data)
  # If attacker can modify this → code execution on next restart
  aws ec2 describe-instance-attribute --instance-id i-xxxx --attribute userData
  ```

### Day 9 — Kubernetes Security
- **K8s security is increasingly important as everything moves to containers:**
  ```bash
  # Check pod security — what privileges does each pod have?
  kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.securityContext}{"\n"}{end}'
  
  # Find pods running as root
  kubectl get pods -o json | python3 -c "
  import json, sys
  pods = json.load(sys.stdin)
  for pod in pods['items']:
      for container in pod['spec']['containers']:
          sc = container.get('securityContext', {})
          if sc.get('runAsUser', 0) == 0:
              print(f'ROOT: {pod[\"metadata\"][\"name\"]} / {container[\"name\"]}')"
  
  # Check for privileged containers (can escape to host)
  kubectl get pods -o json | grep '"privileged": true'
  
  # Kubernetes RBAC — who can do what?
  kubectl auth can-i --list --as system:serviceaccount:default:my-sa
  ```
- **K8s attack paths:** Compromised container → escape to host (privileged container) → lateral movement to cloud IAM (IMDS access from host) → full account compromise

### Day 10 — CSPM and Cloud Security Posture Management
- **Complete `lab-09-b.json`** — all 5 steps
- **CSPM tools:** Continuously check your cloud configuration against security best practices
  ```bash
  # Prowler — open-source CSPM for AWS (also Azure/GCP)
  pip install prowler
  prowler aws                         # Run all AWS checks
  prowler aws -c iam_disable_90_days_credentials  # Specific check
  prowler aws --compliance cis_level2_aws          # CIS benchmark
  
  # ScoutSuite — multi-cloud security auditing
  pip install scoutsuite
  scout aws                           # Audit AWS account
  # Generates an HTML report with findings
  ```
- **Cloud Security Alliance (CSA) Cloud Controls Matrix:** cloudsecurityalliance.org — industry standard framework for cloud security controls

---

## Week 3 — Zero Trust and Advanced Topics

### Day 11 — Zero Trust Architecture
- **Read:** `02-azure-gcp-zero-trust.md` — Zero Trust section
- **Zero Trust core principle:** "Never trust, always verify." No implicit trust based on network location. Even internal network traffic is untrusted.
- **Zero Trust vs VPN:**
  - **VPN:** You connect, you get network access to everything on that network segment. Flat network = lateral movement is easy.
  - **Zero Trust:** Every request is authenticated AND authorised individually. Even if you're on the internal network, you still need to prove identity and have explicit permission for each resource.

- **Zero Trust pillars (CISA Zero Trust Maturity Model):**
  1. **Identity:** Strong auth (MFA), SSO, privileged access management
  2. **Devices:** Device health/compliance check before access
  3. **Networks:** Micro-segmentation, encrypted internal traffic
  4. **Applications:** Application-level access control (not network-level)
  5. **Data:** Classify data, encrypt at rest and in transit, DLP

- **Zero Trust implementation example:**
  ```
  Traditional: Internal user → VPN → Internal DB server (trusted because on VPN)
  Zero Trust:  User → Identity verification (MFA) → Device check (MDM) →
               → Application check (do they have permission for THIS DB?) →
               → Access granted for THIS session only → All actions logged
  ```

### Day 12 — Cloud Incident Response
- **Cloud IR is different from on-premise:**
  - Evidence is ephemeral: instances terminate, log retention defaults to 90 days
  - More log sources available (CloudTrail, VPC Flow Logs, GuardDuty)
  - Containment is faster: isolate with IAM deny policy
  - Recovery is often faster: destroy and redeploy from Infrastructure as Code

- **AWS incident response playbook:**
  ```bash
  # 1. Revoke all active sessions for a compromised user/role
  aws iam create-policy --policy-name EmergencyDeny \
    --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Deny","Action":"*","Resource":"*"}]}'
  aws iam attach-user-policy --user-name compromised-user --policy-arn arn:...
  
  # 2. Disable compromised access key
  aws iam update-access-key --access-key-id AKIAIOSFODNN7EXAMPLE --status Inactive
  
  # 3. Create forensic snapshot of EC2 instance
  aws ec2 create-snapshot --volume-id vol-1234567890abcdef0 \
    --description "ForensicSnapshot-Incident2024-01-15"
  
  # 4. Isolate the EC2 instance (security group with no allow rules)
  aws ec2 modify-instance-attribute --instance-id i-1234567890abcdef0 \
    --groups sg-quarantine-group
  
  # 5. Preserve evidence: download CloudTrail logs for the period
  aws s3 sync s3://my-cloudtrail-bucket/AWSLogs/ ./ir-evidence/
  ```

### Day 13 — Cloud Compliance: CIS Benchmarks
- **CIS (Center for Internet Security) Benchmarks** are detailed security configuration guides for cloud platforms. CIS AWS Foundations Benchmark has 50+ controls.
- **Key CIS AWS controls (level 1 — must implement):**
  - Avoid using root account for day-to-day tasks
  - Enable MFA on root account
  - Ensure no root account access keys exist
  - Enable CloudTrail in all regions
  - Ensure CloudTrail log file validation is enabled
  - Enable GuardDuty
  - Ensure S3 buckets are not publicly accessible
  - Ensure security groups don't allow 0.0.0.0/0 to port 22 (SSH) or 3389 (RDP)
  - Enable VPC Flow Logs
  - Ensure no IAM user has both console access and access keys (use one method)

### Day 14 — Cloud Security Architecture Review
- **Practice:** Review a fictional cloud architecture for security issues
  ```
  Architecture: Web app on EC2 (public subnet) → RDS MySQL (private subnet)
  
  Security review questions:
  □ Are security groups least-privilege? (EC2 SG: only 443 from 0.0.0.0/0)
  □ Is RDS encrypted at rest? (KMS)
  □ Is database accessible from anywhere except the app server? (Should be NO)
  □ Are database credentials stored in Secrets Manager or hardcoded?
  □ Is EC2 instance role least-privilege? (Only the app's required actions)
  □ Are CloudTrail, VPC Flow Logs, GuardDuty enabled?
  □ Is S3 public access blocked at account level?
  □ Are all services in correct regions (data residency)?
  ```

### Day 15 — Review and Exercises
- **Complete:** `exercises-09.md` questions 1-15
- **AWS Skill Builder (free tier):** skillbuilder.aws — take the "Security Fundamentals" digital course (free)
- **AWS Security Workshop labs:** workshops.aws/categories/Security — hands-on labs using real AWS services

---

## Week 4 — Mastery, Certifications, and Portfolio

### Day 16-17 — Assignment Tasks 1-2
- Complete `assignment-09.md` Tasks 1 and 2

### Day 18-19 — Assignment Tasks 3-4
- Complete `assignment-09.md` Tasks 3 and 4
- **Prepare for AWS Security Specialty or AWS Solutions Architect certification:**
  - Review all services: IAM, S3, EC2, VPC, KMS, CloudTrail, GuardDuty, Security Hub, WAF, Shield, Config
  - Practice exam questions: whizlabs.com, tutorials dojo (free sample tests)

### Day 20 — Final Assessment
- **Complete:** `exercises-09.md` questions 16-25
- **Quiz:** `quiz-09.json` — all 15 questions
- **Competency checklist:**
  - [ ] Explain the AWS Shared Responsibility Model with examples for EC2 vs S3 vs Lambda
  - [ ] Write an IAM policy that grants read-only access to a specific S3 bucket
  - [ ] Identify 3 security misconfigurations in a given IAM policy
  - [ ] Configure S3 bucket to block public access via CLI
  - [ ] Search CloudTrail for all root account logins in the last 7 days
  - [ ] Explain what GuardDuty detects and how to respond to a finding
  - [ ] Describe Zero Trust architecture and how it differs from VPN
  - [ ] Run Prowler and interpret a finding from the CIS benchmark output
  - [ ] Write a cloud incident response procedure for a compromised access key
  - [ ] Explain the difference between IAM roles, users, and groups with when to use each
