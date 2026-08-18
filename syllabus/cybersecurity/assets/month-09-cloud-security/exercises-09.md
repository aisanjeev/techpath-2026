# Month 9 — Practice Exercises: Cloud Security

**25 exercises with worked answers.**

---

## Section A: AWS IAM and Shared Responsibility (Questions 1-8)

**Q1.** What is the AWS Shared Responsibility Model? Give 3 specific examples for each side (AWS's responsibility and customer's responsibility) for an EC2 instance running a web application.

**Answer:**

**AWS's Responsibility ("Security OF the Cloud"):**
1. **Physical data centre security:** Physical access controls, environmental controls (power, cooling), hardware destruction at end of life for the EC2 host server
2. **Hypervisor isolation:** Ensuring one customer's EC2 instance cannot access another customer's memory or CPU; the virtualisation layer that makes EC2 work
3. **Underlying network infrastructure:** The global AWS network, backbone routing, DDoS protection at the infrastructure level (AWS Shield Standard — free)

**Customer's Responsibility ("Security IN the Cloud"):**
1. **Operating system patching:** The OS on your EC2 instance (Ubuntu, Amazon Linux, Windows Server) — AWS doesn't patch it for you. If Log4Shell vulnerability is announced and you're running Log4j, AWS won't apply the patch.
2. **Security groups and NACLs:** Configuring which ports and IPs can connect to your EC2 instance. If you open port 22 (SSH) to `0.0.0.0/0` (entire internet), that's your misconfiguration.
3. **Data encryption and application security:** Encrypting data you store (EBS volumes, data written to S3), the application code running on EC2 (SQL injection, XSS vulnerabilities in your app), IAM roles attached to the instance.

---

**Q2.** Read the following IAM policy and explain precisely what it allows and what is missing that makes it a security risk.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "ec2:List*"
      ],
      "Resource": "*"
    }
  ]
}
```

**Answer:**
**What it allows:**
- `s3:*` on `*`: Complete, unrestricted access to ALL S3 actions on ALL buckets and ALL objects in the entire AWS account. This includes: creating buckets, reading objects, writing objects, deleting objects, changing bucket policies (including making them public), deleting entire buckets.
- `ec2:Describe*` and `ec2:List*`: Read-only enumeration of all EC2 resources — can list instances, VPCs, security groups, key pairs, AMIs, etc. No write access to EC2.

**Security risks:**
1. **Overprivileged S3 access:** A Lambda function, application, or user with this policy can access EVERY S3 bucket in the account — including backups, logs, encrypted secrets, and other teams' data. If the application is compromised, the attacker has full S3 access.
2. **Should be scoped to specific resources:** `"Resource": "arn:aws:s3:::my-specific-bucket"` and `"Resource": "arn:aws:s3:::my-specific-bucket/*"` — not `*`
3. **S3:DeleteObject and S3:DeleteBucket should not be granted to applications:** Only human admins should have delete permissions.
4. **Missing conditions:** No IP restrictions, no MFA requirement, no time-based restrictions.

**Corrected least-privilege version:**
```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-app-bucket",
        "arn:aws:s3:::my-app-bucket/*"
      ]
    }
  ]
}
```

---

**Q3.** Explain the difference between an IAM Role and an IAM User. When would you use each?

**Answer:**
**IAM User:**
- A permanent identity tied to a specific human or application
- Has permanent credentials: password (for console) + access keys (for API/CLI)
- Access keys are static — same key works until rotated or deleted
- Best for: human users who need long-term AWS access

**IAM Role:**
- A temporary identity — no permanent credentials attached
- Granted temporary credentials via STS (Security Token Service) — expire in 15 minutes to 12 hours
- Can be ASSUMED by: EC2 instances, Lambda functions, ECS tasks, other AWS services, federated users, cross-account access
- Best for: AWS services, applications running on AWS, federated access

**When to use each:**

| Scenario | Use |
|----------|-----|
| Human developer needs to deploy to AWS from their laptop | IAM User with access keys (or better: SSO with Role assumption) |
| Lambda function needs to read from S3 | IAM Role (execution role attached to Lambda) |
| EC2 web server needs to put files in S3 | IAM Role (instance profile attached to EC2) |
| Cross-account access: Team A's account → Team B's S3 bucket | IAM Role in Team B's account that Team A can assume |
| CI/CD pipeline (GitHub Actions) deploying to AWS | IAM Role with OIDC trust (temporary credentials via federation) |
| Service account for a monitoring tool (non-human) | IAM User with access keys if it can't use roles; prefer roles where possible |

**Key security principle:** Never use IAM Users for services running on AWS infrastructure. Always use IAM Roles — no static credentials that can be stolen if the instance is compromised.

---

**Q4.** A developer accidentally committed an AWS access key to a public GitHub repository. What are the immediate steps to take?

**Answer:**
**Immediate actions (within the next 10 minutes):**

1. **Disable the key NOW — don't delete yet:**
   ```bash
   aws iam update-access-key --access-key-id AKIAIOSFODNN7EXAMPLE --status Inactive
   # Disabling (not deleting) preserves the key ID for investigation
   ```

2. **Determine the exposure window:** When was the key committed? `git log --format="%H %ai" -- config.py`. How long has it been public?

3. **Investigate what happened with the key:**
   ```bash
   # CloudTrail: what did this key do?
   aws cloudtrail lookup-events \
     --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIAIOSFODNN7EXAMPLE \
     --max-results 50 \
     --output json
   
   # Check for unusual activity: new users created? New policies? S3 data exfil?
   aws cloudtrail lookup-events \
     --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIAIOSFODNN7EXAMPLE \
     --start-time "2024-01-01" \
     --query 'Events[*].{Time:EventTime,Event:EventName,IP:CloudTrailEvent}' \
     --output table
   ```

4. **Rotate the key (create a new one, update all applications that used it):**
   ```bash
   aws iam create-access-key --user-name service-account  # Create new key
   # Update application configuration with new key
   aws iam delete-access-key --access-key-id AKIAIOSFODNN7EXAMPLE  # Delete old
   ```

5. **Remove from git history:**
   ```bash
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch config.py' \
     --prune-empty --tag-name-filter cat -- --all
   git push origin --force --all
   ```
   Note: Force-pushing to main/master requires coordination. The key is ALREADY exposed even after history rewrite — rotation is the only effective fix.

6. **Enable AWS GuardDuty finding alert:** GuardDuty may have already detected unusual API activity from an unexpected geography.

7. **Check AWS Health:** Are there any AWS security notices about this key from their automated detection?

---

**Q5.** What is an S3 bucket policy and how does it differ from an IAM policy? Write an S3 bucket policy that:
- Allows public GET access to objects in a `public/` prefix
- Requires HTTPS (denies HTTP)
- Denies access from outside the `ap-south-1` (Mumbai) region

**Answer:**
**Difference:**
- **IAM policy:** Attached to an identity (user/role) — defines what THAT IDENTITY can do to resources
- **S3 bucket policy:** Attached to the bucket (resource policy) — defines who can access THIS BUCKET

Both are evaluated and must both allow for access to be granted (except when one explicitly denies — explicit deny always wins).

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicReadForPublicPrefix",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-bucket/public/*"
    },
    {
      "Sid": "DenyHTTP",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    },
    {
      "Sid": "DenyNonMumbaiRegion",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": "ap-south-1"
        }
      }
    }
  ]
}
```

---

**Q6.** What is CloudTrail and what events does it capture? Write a CloudTrail query (using AWS CLI) to find all EC2 instances that were terminated in the last 7 days.

**Answer:**
**CloudTrail** records AWS API calls made in your account — who made the call, when, from where, and what the parameters were. Essential for: security investigation, compliance auditing, operational troubleshooting.

**What it captures:**
- Management events (default): Control plane operations — creating, modifying, deleting AWS resources (EC2 start/stop/terminate, IAM changes, S3 bucket creation, etc.)
- Data events (optional, additional cost): Object-level S3 operations (GetObject, PutObject per object), Lambda function invocations
- Insight events (optional): Unusual API activity patterns (sudden spike in API calls)

```bash
# Find all EC2 TerminateInstances events in last 7 days
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=TerminateInstances \
  --start-time $(date -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --output json | python3 -c "
import json, sys

events = json.load(sys.stdin)['Events']
print(f'Found {len(events)} termination events')
print('-' * 70)
for e in events:
    ct = json.loads(e['CloudTrailEvent'])
    print(f'Time: {e[\"EventTime\"]}')
    print(f'User: {ct[\"userIdentity\"].get(\"arn\", \"Unknown\")}')
    print(f'Source IP: {ct.get(\"sourceIPAddress\", \"Unknown\")}')
    instances = ct.get('requestParameters', {}).get('instancesSet', {}).get('items', [])
    for inst in instances:
        print(f'  Instance: {inst[\"instanceId\"]}')
    print()
"
```

---

**Q7.** What is AWS GuardDuty? Describe 5 types of threats it can detect and how it works technically.

**Answer:**
**GuardDuty:** AWS threat detection service that continuously monitors for malicious activity using ML on three data sources: CloudTrail (API calls), VPC Flow Logs (network traffic), and DNS logs (DNS queries).

**How it works:** GuardDuty ingests the data sources, applies ML models and threat intelligence (known bad IPs, domains, patterns) to identify anomalous or malicious activity. You don't configure log collection — GuardDuty handles it separately from your existing CloudTrail setup.

**5 threat types it detects:**

1. **Crypto mining:** EC2 instance querying known cryptocurrency mining pool domains or connecting to known mining pool IPs → `CryptoCurrency:EC2/BitcoinTool.B!DNS`

2. **Compromised IAM credentials used from unusual location:** Your access key is typically used from `ap-south-1`; suddenly appears from a Russian IP → `UnauthorizedAccess:IAMUser/TorIPCaller` or anomalous behavior finding

3. **Data exfiltration:** Unusual large data transfer from S3 bucket detected in VPC Flow Logs → `Exfiltration:S3/ObjectRead.Unusual`

4. **Port scanning from EC2 instance:** Your EC2 instance starts scanning other IP addresses → `Recon:EC2/PortProbeUnprotectedPort` or `Recon:EC2/Portscan` — indicates your instance may be compromised

5. **DNS-based C2 communication:** EC2 instance making DNS queries to known malware C2 domains → `Trojan:EC2/DNSDataExfiltration` — malware often uses DNS tunneling

---

**Q8.** Write a Python script that uses Boto3 to audit an AWS account for common security misconfigurations. Include checks for: public S3 buckets, EC2 instances with ports 22/3389 open to internet, and IAM users with no MFA.

**Answer:**
```python
import boto3
import json

def audit_aws_account():
    """Audit AWS account for common security misconfigurations."""
    report = {"findings": [], "summary": {}}
    
    # ─────────────────────────────────────────
    # Check 1: Public S3 Buckets
    # ─────────────────────────────────────────
    print("[*] Checking S3 buckets for public access...")
    s3_client = boto3.client('s3')
    s3_control = boto3.client('s3control', region_name='us-east-1')
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()['Account']
    
    public_buckets = []
    try:
        buckets = s3_client.list_buckets()['Buckets']
        for bucket in buckets:
            name = bucket['Name']
            try:
                # Check account-level public access block
                pab = s3_client.get_public_access_block(Bucket=name)['PublicAccessBlockConfiguration']
                is_blocked = all([
                    pab.get('BlockPublicAcls'), pab.get('IgnorePublicAcls'),
                    pab.get('BlockPublicPolicy'), pab.get('RestrictPublicBuckets')
                ])
                if not is_blocked:
                    public_buckets.append(name)
                    report['findings'].append({
                        'severity': 'HIGH',
                        'resource': f's3://{name}',
                        'issue': 'S3 bucket public access block not fully enabled',
                        'recommendation': 'Enable all 4 public access block settings'
                    })
            except s3_client.exceptions.NoSuchPublicAccessBlockConfiguration:
                public_buckets.append(name)
                report['findings'].append({
                    'severity': 'HIGH',
                    'resource': f's3://{name}',
                    'issue': 'S3 bucket has no public access block configured',
                    'recommendation': 'Enable S3 public access block'
                })
    except Exception as e:
        print(f"  [!] S3 check error: {e}")
    
    # ─────────────────────────────────────────
    # Check 2: EC2 Security Groups — Open SSH/RDP
    # ─────────────────────────────────────────
    print("[*] Checking EC2 security groups for open SSH/RDP...")
    ec2 = boto3.client('ec2')
    
    dangerous_sgs = []
    try:
        sgs = ec2.describe_security_groups()['SecurityGroups']
        for sg in sgs:
            for permission in sg.get('IpPermissions', []):
                from_port = permission.get('FromPort', 0)
                to_port = permission.get('ToPort', 65535)
                
                for ip_range in permission.get('IpRanges', []):
                    if ip_range.get('CidrIp') in ('0.0.0.0/0',):
                        for port in [22, 3389]:
                            if from_port <= port <= to_port:
                                service = 'SSH' if port == 22 else 'RDP'
                                dangerous_sgs.append(sg['GroupId'])
                                report['findings'].append({
                                    'severity': 'HIGH',
                                    'resource': f"sg/{sg['GroupId']} ({sg['GroupName']})",
                                    'issue': f'{service} (port {port}) open to 0.0.0.0/0',
                                    'recommendation': f'Restrict {service} to specific IP ranges or use VPN/SSM Session Manager'
                                })
    except Exception as e:
        print(f"  [!] EC2 SG check error: {e}")
    
    # ─────────────────────────────────────────
    # Check 3: IAM Users Without MFA
    # ─────────────────────────────────────────
    print("[*] Checking IAM users for MFA...")
    iam = boto3.client('iam')
    
    no_mfa_users = []
    try:
        users = iam.list_users()['Users']
        for user in users:
            username = user['UserName']
            mfa_devices = iam.list_mfa_devices(UserName=username)['MFADevices']
            
            # Check if user has console access
            try:
                iam.get_login_profile(UserName=username)
                has_console = True
            except iam.exceptions.NoSuchEntityException:
                has_console = False
            
            if has_console and not mfa_devices:
                no_mfa_users.append(username)
                report['findings'].append({
                    'severity': 'HIGH',
                    'resource': f'iam/user/{username}',
                    'issue': 'IAM user with console access has no MFA device',
                    'recommendation': 'Enable MFA for all console users'
                })
    except Exception as e:
        print(f"  [!] IAM MFA check error: {e}")
    
    # Summary
    critical_count = sum(1 for f in report['findings'] if f['severity'] == 'CRITICAL')
    high_count = sum(1 for f in report['findings'] if f['severity'] == 'HIGH')
    
    report['summary'] = {
        'total_findings': len(report['findings']),
        'critical': critical_count,
        'high': high_count,
        'public_buckets': len(public_buckets),
        'open_security_groups': len(set(dangerous_sgs)),
        'users_without_mfa': len(no_mfa_users)
    }
    
    print("\n" + "=" * 50)
    print("AUDIT RESULTS")
    print("=" * 50)
    print(json.dumps(report['summary'], indent=2))
    print("\nDetailed findings:")
    for finding in report['findings']:
        print(f"\n[{finding['severity']}] {finding['resource']}")
        print(f"  Issue: {finding['issue']}")
        print(f"  Fix: {finding['recommendation']}")
    
    return report

if __name__ == '__main__':
    audit_aws_account()
```

---

## Section B: Azure and GCP Security (Questions 9-13)

**Q9.** What is Azure Entra ID (formerly Azure Active Directory) and how does Conditional Access improve security compared to simple MFA?

**Answer:**
**Azure Entra ID:** Microsoft's cloud identity platform. It provides: user authentication (single sign-on across Microsoft 365, Azure, and thousands of SaaS apps), role-based access control for Azure resources, device management, and security policies.

**Simple MFA:** User enters password → prompted for MFA → access granted. Binary: authenticated or not.

**Conditional Access:** A policy engine that evaluates MULTIPLE signals BEFORE granting access. Access is granted, blocked, or restricted based on conditions:

```
Signals evaluated:
- User identity (who is this?)
- Device (is this a managed/compliant device?)
- Application (which app is being accessed?)
- Location (IP address, named location, country)
- Risk level (Microsoft's real-time risk assessment)

Example policies:
1. "Require MFA for all access from outside the office network"
   → Office IP range: no MFA needed
   → External IP: MFA required
   
2. "Block access from high-risk sign-in locations (Tor, known bad IPs)"
   → Even with correct password+MFA
   
3. "Require compliant device for Microsoft 365 access"
   → Personal laptop (not MDM enrolled): blocked
   → Corporate managed laptop (MDM enrolled): allowed

4. "Admin roles require FIDO2 hardware key (no SMS MFA)"
   → Privileged users get stronger authentication requirement
```

**Why it's better than simple MFA:**
- Adapts to context — more friction for higher-risk access, less friction for routine office access (improves usability)
- Can block access even with valid MFA if device/location is suspicious
- Risk-based policies use ML to detect impossible travel, known bad IPs, leaked credentials

---

**Q10.** Explain the Google Cloud IAM permission model. What are predefined roles, custom roles, and basic roles? Which should you use in production?

**Answer:**

**Basic roles (Primitive roles — avoid in production):**
- `roles/viewer`: Read access to all GCP resources in the project
- `roles/editor`: Read + write access to most resources
- `roles/owner`: Full admin access including billing and IAM changes

**Why avoid basic roles:** They're extremely broad — `roles/editor` grants write access to EVERY service in the project. A compromised service account with `roles/editor` can modify any resource. Violates least privilege severely.

**Predefined roles:** Google-maintained roles with specific, named sets of permissions for individual services:
- `roles/compute.instanceAdmin.v1`: Full control of Compute Engine instances
- `roles/compute.viewer`: Read-only access to Compute Engine
- `roles/storage.objectViewer`: Read objects in Cloud Storage
- `roles/bigquery.dataViewer`: Read BigQuery datasets and tables
- `roles/container.developer`: Deploy to GKE, no cluster admin access

**Custom roles:** You define exactly which permissions are included. Most granular, most effort to maintain.

**What to use in production:**
1. **Predefined roles first:** Usually cover 80% of use cases. Check the GCP documentation for the right service-specific predefined role.
2. **Custom roles** when a predefined role is still too broad or you need specific permission combinations not covered by any predefined role.
3. **NEVER basic roles** in production (except for initial setup; remove as soon as proper roles are configured).

---

**Q11.** What is a Cloud Security Posture Management (CSPM) tool? Compare Prowler, ScoutSuite, and AWS Security Hub.

**Answer:**
**CSPM:** A category of security tools that continuously assess cloud configurations against security best practices and compliance frameworks. They don't protect in real-time — they identify misconfigurations that could be exploited.

| Feature | Prowler | ScoutSuite | AWS Security Hub |
|---------|---------|------------|-----------------|
| **Type** | Open-source CLI | Open-source CLI | AWS managed service |
| **Cost** | Free | Free | AWS pricing (varies) |
| **Clouds** | AWS, Azure, GCP | AWS, Azure, GCP, Alibaba | AWS-native (partners for others) |
| **Running** | Manual/CI pipeline | Manual | Continuous |
| **Output** | JSON, CSV, HTML | HTML report | AWS console, API |
| **Compliance** | CIS, GDPR, HIPAA, PCI, SOC 2 | CIS, custom | CIS, PCI, NIST, custom |
| **Integration** | GitHub Actions, AWS Security Hub | Standalone | Native AWS (GuardDuty, Inspector, etc.) |
| **Best for** | CI/CD pipeline security checks | Quick snapshot audit | Ongoing operational security monitoring |

**Prowler example:**
```bash
prowler aws --compliance cis_level2_aws
# Generates findings for each CIS benchmark control
```

**ScoutSuite example:**
```bash
scout aws
# Generates interactive HTML report showing resource risk levels across all services
```

**AWS Security Hub:** Always-on in your AWS account. Aggregates findings from GuardDuty, Inspector, Macie, and third-party tools into one dashboard. Scores your account against CIS benchmarks continuously.

---

**Q12.** A startup's cloud architect says "We don't need to worry about IAM permissions — we use VPC security groups and private subnets to keep everything locked down." What are the flaws in this reasoning?

**Answer:**
**The architect is confusing network-level security with identity-level security.** These are separate, complementary layers — not substitutes for each other.

**Why VPC/network controls are insufficient:**

1. **Insider threats bypass network controls:** A legitimate employee with developer-level access can already reach internal resources. Without proper IAM, they can access ALL resources — databases, secrets, prod data — not just what their role requires.

2. **Compromised IAM credentials bypass network controls:** If an attacker steals a developer's access keys, they can call AWS APIs from ANYWHERE — from their own laptop, from a coffee shop, from another country. AWS API calls go through the internet to AWS endpoints, not through your VPC. Your VPC security groups don't protect the API plane.

3. **Instance compromise → lateral movement via over-privileged instance roles:** If your EC2 web server has `AdministratorAccess` IAM role (common in "we just need it to work" setups), an attacker who exploits your web app gets admin access to your entire AWS account via the metadata endpoint — regardless of your security groups.

4. **Private subnets ≠ IAM control:** Resources in private subnets can still be accessed by IAM principals with the right permissions from within AWS. Private subnets prevent PUBLIC INTERNET access; they don't prevent authenticated IAM access from other services.

**The correct model:** Defence-in-depth with BOTH:
- Network layer: VPC, security groups, NACLs, private subnets
- Identity layer: IAM least privilege, service roles, no wildcard permissions

---

**Q13.** What is the Kubernetes attack surface? Describe the attack path from a compromised container to full cloud account access.

**Answer:**
**Kubernetes introduces a large attack surface:**
- API server (control plane): Unauthenticated or weak auth access to cluster admin
- ETCD: The cluster's key-value store — contains all secrets if accessible
- Kubelet: Node-level API — can be exploited to access other containers on the node
- Container escape: Privileged containers can break out to the host OS
- Cloud metadata: Containers can reach `169.254.169.254` unless blocked

**Attack path: Compromised container → Full cloud account access:**
```
Step 1: Initial access
Attacker exploits web vulnerability in containerised app → RCE in a container
(e.g., Log4Shell in a Java microservice)

Step 2: Container enumeration
- Check if in Kubernetes: env | grep KUBERNETES
- Check service account: cat /var/run/secrets/kubernetes.io/serviceaccount/token
- Enumerate cluster: use the token with kubectl/curl to list pods, secrets, configmaps

Step 3: Kubernetes privilege escalation
Option A: Service account with excessive RBAC → get secrets from other namespaces
   kubectl get secrets --all-namespaces → find DB passwords, API keys
Option B: Pod with hostPath mount → read host OS files
   cat /host/etc/shadow, read /host/root/.aws/credentials
Option C: Privileged container → escape to host OS
   nsenter --target 1 --mount --uts --ipc --net --pid -- bash

Step 4: Cloud metadata from the host
- Once on host OS: curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
- Returns IAM role credentials for the EC2 instance (worker node)
- Worker node IAM roles often have broad permissions: ECR pull, S3 read, CloudWatch

Step 5: Lateral movement to cloud
- Use stolen IAM credentials from your attacker machine
- Access S3, RDS, Secrets Manager, SSM Parameter Store
- Create new IAM users for persistence
- Full account compromise
```

---

## Section C: Incident Response and Compliance (Questions 14-20)

**Q14.** What is VPC Flow Logs and how would you use them to investigate a suspected data exfiltration incident from an EC2 instance?

**Answer:**
**VPC Flow Logs** capture metadata about network traffic in your VPC: source IP, destination IP, port, protocol, packet count, byte count, action (ACCEPT/REJECT), and timestamp. NOT the content — just the headers.

**Enabling VPC Flow Logs:**
```bash
# Enable flow logs to CloudWatch Logs
aws ec2 create-flow-logs \
  --resource-ids vpc-12345678 \
  --resource-type VPC \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /vpc/flowlogs \
  --deliver-logs-permission-arn arn:aws:iam::123:role/FlowLogsRole
```

**Investigation for suspected exfiltration from `10.0.1.50`:**
```python
import boto3
from datetime import datetime, timedelta

def analyse_flow_logs_for_exfiltration(instance_ip: str, hours_back: int = 24):
    logs = boto3.client('logs')
    
    query = f"""
    fields @timestamp, srcAddr, dstAddr, dstPort, bytes, packets
    | filter srcAddr = "{instance_ip}"
    | filter bytes > 1000000  # > 1MB transfers
    | filter not (dstAddr like /10\\./ or dstAddr like /172\.16/)  # Exclude internal IPs
    | sort bytes desc
    | limit 50
    """
    
    start = int((datetime.now() - timedelta(hours=hours_back)).timestamp())
    end = int(datetime.now().timestamp())
    
    response = logs.start_query(
        logGroupName='/vpc/flowlogs',
        startTime=start,
        endTime=end,
        queryString=query
    )
    query_id = response['queryId']
    
    # Wait for and fetch results
    import time
    while True:
        result = logs.get_query_results(queryId=query_id)
        if result['status'] == 'Complete':
            break
        time.sleep(1)
    
    print(f"Large outbound transfers from {instance_ip}:")
    total_bytes = 0
    destinations = set()
    for row in result['results']:
        data = {f['field']: f['value'] for f in row}
        bytes_transferred = int(data.get('bytes', 0))
        dst = data.get('dstAddr')
        total_bytes += bytes_transferred
        destinations.add(dst)
        print(f"  → {dst}:{data.get('dstPort')} | {bytes_transferred/1024/1024:.1f} MB")
    
    print(f"\nTotal: {total_bytes/1024/1024:.1f} MB to {len(destinations)} unique destinations")
    return result['results']

analyse_flow_logs_for_exfiltration("10.0.1.50", hours_back=72)
```

---

**Q15.** Explain the concept of "lateral movement" in a cloud environment. How does it differ from traditional network lateral movement?

**Answer:**
**Traditional lateral movement:** Move between hosts using network access — SSH, SMB, WMI. Limited by firewalls and network segmentation. You're moving between IP addresses.

**Cloud lateral movement:** Move between cloud resources using IAM credentials and cloud API calls. Different vectors:

**1. IAM credential chaining:**
```
Compromise EC2 instance → steal instance role credentials
→ The instance role has AssumeRole permission for another role
→ Assume that role: aws sts assume-role --role-arn arn:aws:iam::123:role/database-admin
→ Now have database admin access without touching the database server network
```

**2. Secrets Manager / Parameter Store escalation:**
```
Compromise Lambda function with secrets:read permission
→ Read ALL secrets: aws secretsmanager list-secrets
→ Find database_admin_password secret
→ Now can authenticate to RDS databases directly
```

**3. Cross-account movement:**
```
IAM role in Account A has permissions to assume a role in Account B
→ Lateral movement across AWS accounts
→ Common in hub-spoke architectures where one account manages others
```

**4. Service role abuse:**
```
Compromise ECS task → task's IAM role has ECR:GetAuthorizationToken + ECR:PutImage
→ Push malicious Docker image to ECR
→ Next time any service pulls that image → persistence and lateral movement to all services using that image
```

**Key difference:** Cloud lateral movement often doesn't require network access at all — it happens through API calls. Traditional network segmentation doesn't prevent IAM-based lateral movement. Monitoring needs to focus on API call patterns, not just network flow logs.

---

**Q16.** What is "defence in depth" in a cloud context? Design a 5-layer security architecture for a web application on AWS.

**Answer:**

```
Layer 1: EDGE (AWS Shield + CloudFront + WAF)
┌─────────────────────────────────────────────────────┐
│ CloudFront CDN with WAF rules (OWASP managed rules) │
│ AWS Shield Advanced (DDoS protection)               │
│ Geographic blocking for high-risk countries         │
└─────────────────────────────────────────────────────┘
                    ↓
Layer 2: LOAD BALANCER (Application Load Balancer)
┌─────────────────────────────────────────────────────┐
│ ALB in public subnet                                │
│ Only accepts HTTPS (443) from CloudFront            │
│ SSL termination + certificate management            │
│ Target health checks                                │
└─────────────────────────────────────────────────────┘
                    ↓
Layer 3: APPLICATION (EC2/ECS in private subnets)
┌─────────────────────────────────────────────────────┐
│ No public IP addresses                              │
│ Security group: only accept from ALB security group │
│ IAM instance role: least privilege (read S3 only)  │
│ IMDSv2 enforced (prevents metadata SSRF)           │
│ OS-level: CrowdStrike/GuardDuty for runtime        │
└─────────────────────────────────────────────────────┘
                    ↓
Layer 4: DATA (RDS in isolated subnets)
┌─────────────────────────────────────────────────────┐
│ RDS in private isolated subnet (no route to internet│
│ Security group: only accept from app security group │
│ Encryption at rest (KMS) + in transit (SSL)        │
│ Credentials in Secrets Manager (auto-rotation)     │
│ Automated backups + point-in-time recovery         │
└─────────────────────────────────────────────────────┘
                    ↓
Layer 5: MONITORING & RESPONSE (Continuous)
┌─────────────────────────────────────────────────────┐
│ GuardDuty: threat detection (ML on API+DNS+Flow)   │
│ CloudTrail: all API calls logged to S3             │
│ VPC Flow Logs: network traffic metadata            │
│ CloudWatch Alarms: anomaly detection               │
│ AWS Config: configuration compliance monitoring    │
│ Security Hub: centralised finding management       │
└─────────────────────────────────────────────────────┘
```

---

**Q17.** What is the CIS AWS Foundations Benchmark? List 5 critical Level 1 controls and how to verify each.

**Answer:** The CIS AWS Foundations Benchmark is a set of security configuration recommendations for AWS accounts, developed by the Center for Internet Security with community consensus. Level 1 are basic controls appropriate for all environments; Level 2 are for higher-security environments.

**5 Critical Level 1 Controls:**

**1. Ensure MFA is enabled for the root account (1.5):**
```bash
aws iam get-account-summary | python3 -c "
import json, sys
summary = json.load(sys.stdin)['SummaryMap']
print('Root MFA enabled:', 'YES' if summary.get('AccountMFAEnabled') else 'NO ← FAIL')
"
```

**2. Ensure no root account access keys exist (1.4):**
```bash
aws iam list-access-keys --user-name "" 2>&1
# or
aws iam get-account-summary | python3 -c "
import json,sys; s=json.load(sys.stdin)['SummaryMap']
print('Root access keys:', s.get('AccountAccessKeysPresent', 0), '← should be 0')
"
```

**3. Ensure CloudTrail is enabled in all regions (3.1):**
```bash
aws cloudtrail describe-trails --include-shadow-trails --output json | python3 -c "
import json, sys
trails = json.load(sys.stdin)['trailList']
multi_region = [t for t in trails if t.get('IsMultiRegionTrail')]
print(f'Multi-region trails: {len(multi_region)}  ← should be >= 1')
for t in multi_region:
    print(f'  {t[\"Name\"]}: logging={t.get(\"HasCustomEventSelectors\")}')
"
```

**4. Ensure Security Groups don't allow SSH from 0.0.0.0/0 (5.2):**
```bash
aws ec2 describe-security-groups --output json | python3 -c "
import json, sys
sgs = json.load(sys.stdin)['SecurityGroups']
for sg in sgs:
    for perm in sg.get('IpPermissions', []):
        if perm.get('FromPort', 0) <= 22 <= perm.get('ToPort', 65535):
            for r in perm.get('IpRanges', []):
                if r.get('CidrIp') == '0.0.0.0/0':
                    print(f'FAIL: {sg[\"GroupId\"]} ({sg[\"GroupName\"]}) allows SSH from 0.0.0.0/0')
"
```

**5. Ensure AWS Config is enabled in all regions (3.5):**
```bash
aws configservice describe-configuration-recorders --output json | python3 -c "
import json, sys
recorders = json.load(sys.stdin)['ConfigurationRecorders']
print(f'Config recorders: {len(recorders)} ← should be >= 1')
"
```

---

**Q18.** What is cloud IAM privilege escalation? Give 3 specific IAM misconfiguration examples that allow escalation to full admin.

**Answer:** Cloud IAM privilege escalation means using granted permissions to gain additional (higher) privileges than were intended — analogous to local privilege escalation but via cloud API calls.

**3 Escalation paths:**

**1. `iam:CreateAccessKey` → Full account access:**
```bash
# Permission: iam:CreateAccessKey (create access keys for OTHER users)
# Attack: Create an access key for the existing admin user
aws iam create-access-key --user-name admin-user
# Returns: AccessKeyId + SecretAccessKey for admin-user
# Now you have admin access
```

**2. `iam:AttachUserPolicy` → Full admin:**
```bash
# Permission: iam:AttachUserPolicy (attach policies to users)
# Attack: Attach AdministratorAccess to yourself
aws iam attach-user-policy \
  --user-name current-user \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
# Now current-user has full admin
```

**3. `lambda:UpdateFunctionCode` + execution role with admin permissions:**
```bash
# Scenario: Lambda function has AdministratorAccess execution role
# Your permission: lambda:UpdateFunctionCode (update the function code)

# Attack: Replace the Lambda function code with code that exfiltrates credentials
aws lambda update-function-code \
  --function-name target-function \
  --zip-file fileb://evil_function.zip

# Next time the Lambda runs, it runs with AdministratorAccess
# → full account access
```

**Detection:** Monitor CloudTrail for these specific API calls by non-admin users. AWS IAM Access Analyzer can also identify these risky permission combinations.

---

**Q19.** What is Terraform/Infrastructure as Code (IaC) security? What can go wrong with insecure Terraform code?

**Answer:**
**IaC security** = securing the code that defines cloud infrastructure. Terraform, CloudFormation, Pulumi define resources as code — security misconfigurations in this code become security issues at deployment time.

**What goes wrong:**

**1. Hardcoded secrets:**
```hcl
resource "aws_db_instance" "main" {
  password = "MyPassword123!"  # ← Stored in git history forever
}
```
Fix: `password = var.db_password` + store in AWS Secrets Manager

**2. Publicly accessible resources:**
```hcl
resource "aws_security_group_rule" "ssh" {
  type        = "ingress"
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]  # ← Open to entire internet
}
```

**3. No encryption:**
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "my-sensitive-data"
  # No encryption configuration
  # No versioning
  # No public access block
}
```

**4. Overprivileged IAM:**
```hcl
resource "aws_iam_policy" "app_policy" {
  policy = jsonencode({
    Statement = [{
      Action   = "*"      # ← Wildcard action
      Resource = "*"      # ← Wildcard resource
      Effect   = "Allow"
    }]
  })
}
```

**IaC security scanning:**
```bash
# Checkov — scan Terraform before apply
pip install checkov
checkov -d ./terraform/ --compact

# tfsec
tfsec ./terraform/

# Common findings will include: open security groups, missing encryption,
# no MFA delete on S3, public RDS snapshots, over-privileged IAM
```

---

**Q20.** You receive a GuardDuty finding: `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`. Explain what this means and write a complete incident response procedure.

**Answer:**
**What the finding means:**
AWS IAM credentials that were issued for an EC2 instance (via the instance metadata service) are being used from an IP address OUTSIDE AWS. This should never happen in normal operations — instance credentials are designed to be used only from the instance itself. This almost always indicates:
1. SSRF vulnerability exploited — attacker retrieved instance credentials via `http://169.254.169.254/` from a vulnerability
2. Malware on the instance exfiltrating credentials
3. Compromised developer who grabbed instance credentials and is using them externally

**Incident Response Procedure:**

**T+0 — Immediate (within 5 minutes):**
```bash
# 1. Identify the affected instance and its IAM role
aws guardduty get-findings --detector-id YOUR_DETECTOR_ID --finding-ids THE_FINDING_ID

# 2. DENY all permissions via the role (emergency brake)
# Create and attach an explicit deny policy to the role
aws iam put-role-policy --role-name affected-role \
  --policy-name EmergencyDeny \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Deny","Action":"*","Resource":"*"}]}'
```

**T+5-30 minutes — Containment:**
```bash
# 3. Identify the instance
# (Finding will contain the instance ID)

# 4. Isolate the instance — move to quarantine security group (no inbound/outbound)
aws ec2 modify-instance-attribute \
  --instance-id i-AFFECTED-INSTANCE \
  --groups sg-QUARANTINE-SG-ID

# 5. Take forensic memory snapshot (for later analysis)
aws ec2 create-snapshot \
  --volume-id vol-ATTACHED-VOLUME \
  --description "ForensicSnapshot-IR-$(date +%Y%m%d)"
```

**T+30-120 minutes — Investigation:**
```bash
# 6. Check CloudTrail for what the attacker did with the credentials
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=AccessKeyId,AttributeValue=AKIAIOSFODNN7EXAMPLE \
  --start-time "24 hours before finding" \
  --output json

# Look for: new IAM users/keys created, S3 data accessed, EC2 instances launched, 
# route changes, security group modifications

# 7. Check the instance logs for SSRF or compromise evidence
# (via Systems Manager if still accessible)
aws ssm start-session --target i-AFFECTED-INSTANCE
# Check web server access logs, application logs, auth logs
```

**T+2 hours+ — Eradication and Recovery:**
```bash
# 8. Determine root cause (SSRF? Malware? Insider?)
# 9. Fix the root cause (patch the SSRF vulnerability, remove malware)
# 10. Terminate the compromised instance, launch a clean replacement from AMI
# 11. Enable IMDSv2 on all instances (prevents SSRF from accessing metadata)
aws ec2 modify-instance-metadata-options \
  --instance-id i-ALL-INSTANCES \
  --http-tokens required  # IMDSv2 only — requires session token
```

---

## Section D: Zero Trust and Advanced Cloud (Questions 21-25)

**Q21.** Explain Zero Trust architecture. Why does "never trust, always verify" apply to traffic INSIDE your network, and how is this implemented in cloud environments?

**Answer:** Traditional security assumed: if you're inside the network perimeter, you can be trusted. VPN = trusted = access to everything.

**Zero Trust rejects this** because: the perimeter doesn't exist anymore (employees work from home, cloud services span multiple providers), attackers who gain access via phishing or VPN bypass become trusted and can move laterally freely, and even internal traffic needs to be verified because insider threats are real.

**"Never trust, always verify" means:**
Every request — even between internal services — must be:
1. **Authenticated:** Who is making this request? (identity verification)
2. **Authorised:** Are they allowed to do this specific action?
3. **Inspected:** Is this request anomalous or risky?
4. **Logged:** Record everything for forensics

**Cloud implementation:**

```
Workload-to-workload: Service mesh (Istio/Linkerd) provides mTLS between services
→ Every microservice must present a valid certificate
→ Services that aren't explicitly allowed to communicate can't

Human-to-resource: BeyondCorp / Google IAP / AWS Verified Access
→ Replace VPN with identity-aware proxy
→ User proves identity (SSO + MFA + device check) for EACH application
→ No network-level access granted — only application-level

Secrets: Nothing hardcoded; Vault / AWS Secrets Manager
→ Services authenticate to Secrets Manager to get credentials
→ No static credentials stored anywhere
→ Credentials auto-rotate

Monitoring: Log ALL access, even from "trusted" sources
→ Service A accessing Service B's admin endpoint → alert
→ Even if Service A is legitimate, this unusual pattern requires investigation
```

---

**Q22.** What is a cloud security incident from a real company that you could use as a case study? What went wrong and how could it have been prevented?

**Answer:**

**Case Study: Capital One Data Breach (2019)**

**What happened:**
- Attacker (former AWS employee) exploited a Server-Side Request Forgery (SSRF) vulnerability in Capital One's WAF running on EC2
- Used SSRF to access the EC2 instance metadata endpoint: `http://169.254.169.254/`
- Retrieved IAM role credentials for the WAF's EC2 instance
- The WAF's IAM role had excessive permissions — specifically `s3:ListBuckets` and `s3:GetObject` on too many buckets
- Used stolen credentials to access and exfiltrate 106 million customer records from S3

**What went wrong (3 layers):**
1. **SSRF vulnerability in the WAF:** The custom WAF configuration allowed server-side requests — this should have been blocked
2. **EC2 IMDSv1:** IMDSv1 doesn't require authentication — any SSRF can access it. IMDSv2 (requires a PUT request first) would have prevented this
3. **Overprivileged IAM role:** The WAF's role should only have permissions to inspect traffic, not to list/read S3 buckets across the account

**How it could have been prevented:**
```
Prevention 1: Enable IMDSv2 (require session tokens for metadata access)
aws ec2 modify-instance-metadata-options --http-tokens required

Prevention 2: Least-privilege IAM for the WAF role
# WAF doesn't need ANY S3 access — the role should have had none
# Network ACL to block 169.254.169.254 access from WAF instances

Prevention 3: AWS Macie to monitor S3 access patterns
# 106 million records accessed = massively anomalous access pattern
# Macie + CloudWatch alert on unusual S3 access volume

Prevention 4: VPC Endpoints for S3 (restrict which VPCs can access which S3 buckets)
# Even if credentials stolen, S3 access only allowed from specific VPCs
```

---

**Q23.** Write a cloud security architecture review checklist for a new AWS account being set up for a production workload.

**Answer:**

---
**AWS Account Security Baseline Checklist**

**Identity and Access Management:**
- [ ] Enable MFA on root account (hardware key strongly preferred)
- [ ] Delete all root account access keys
- [ ] Do not use root account for any regular operations
- [ ] Enable AWS Organizations with SCPs to prevent member accounts from disabling security controls
- [ ] Configure IAM Identity Center (SSO) for all human access — no individual IAM users for humans
- [ ] Enforce MFA for all IAM user console access via SCPs
- [ ] Audit: no IAM users with `AdministratorAccess` policy (use roles with limited sessions)
- [ ] Set password policy: min 14 chars, rotation every 90 days, MFA required

**Logging and Monitoring:**
- [ ] Enable CloudTrail in all regions with log file validation
- [ ] Enable CloudTrail log integrity validation
- [ ] Enable AWS Config in all regions with all resource types
- [ ] Enable GuardDuty in all regions
- [ ] Enable Security Hub with CIS AWS Foundations Benchmark standard
- [ ] Set up CloudWatch alarms for: root login, MFA disable, large IAM changes, billing anomalies
- [ ] VPC Flow Logs enabled for all VPCs

**Network:**
- [ ] No VPCs with internet gateways unless needed
- [ ] Bastion hosts replaced with SSM Session Manager (no public SSH)
- [ ] No security group rules with `0.0.0.0/0` inbound on SSH (22) or RDP (3389)
- [ ] VPC endpoints for S3 and DynamoDB (avoid traffic leaving AWS network)

**Data Protection:**
- [ ] S3 account-level public access block enabled
- [ ] All S3 buckets encrypted (SSE-KMS or SSE-S3)
- [ ] Enable S3 server access logging for sensitive buckets
- [ ] RDS encryption at rest enabled
- [ ] EBS volumes encrypted by default (account-level setting)
- [ ] No secrets or credentials in EC2 user data or environment variables — use Secrets Manager
- [ ] KMS key rotation enabled for all CMKs

**Compute:**
- [ ] IMDSv2 enforced on all EC2 instances
- [ ] No EC2 instances with public IPs unless required (use ALB)
- [ ] EC2 instance roles: least privilege only
- [ ] Lambda environment variables: no credentials — use KMS or Secrets Manager
- [ ] Container images: scanned for vulnerabilities (ECR scanning enabled)

---

**Q24.** What is the difference between "data sovereignty" and "data residency"? How do cloud architectures address these requirements for Indian regulations?

**Answer:**
**Data Residency:** Where the data is physically stored. "Our customer data must be stored in India." Technical requirement — data at rest is in a specific geographic location.

**Data Sovereignty:** A broader concept — which country's laws and jurisdiction apply to the data. Data stored in the US but owned by an Indian company may still be subject to US CLOUD Act (government can compel cloud providers to produce data even if stored elsewhere).

**Why it matters for India:**
- **RBI:** Payment data must be stored exclusively in India (payment data localisation — circular of April 2018). No exception for foreign cloud providers.
- **DPDP Act 2023:** The Act allows data transfer to countries approved by the Central Government. The list of approved countries is not yet published. Until it is, international data transfer is restricted.
- **SEBI:** Financial data for regulated entities must be kept in India.

**AWS Architecture for India Data Residency:**
```bash
# 1. Use AWS ap-south-1 (Mumbai) or ap-south-2 (Hyderabad) regions ONLY
# 2. Prevent accidental deployment in non-Indian regions via SCP:

{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": ["ap-south-1", "ap-south-2"]
    }
  }
}

# 3. S3 bucket policy: deny uploads from non-Mumbai region
# 4. CloudTrail: verify all logs stay in ap-south-1 S3 bucket
# 5. GuardDuty: configured to ap-south-1
# 6. Encryption keys (KMS CMKs): created in ap-south-1 only

# For RBI payment data:
# - All payment APIs on ap-south-1 only
# - No cross-region replication for payment data
# - Global Accelerator: route to Mumbai even if users are elsewhere
```

---

**Q25.** Write a cloud security incident response tabletop exercise scenario and guide a team through it.

**Answer:**

---
**TABLETOP EXERCISE: "GHOST IN THE MACHINE"**

**Duration:** 2 hours | **Participants:** Cloud Architect, Security Engineer, DevOps Lead, CISO

---

**Scenario Briefing:** Monday morning, 9:15 AM. Your AWS cost dashboard shows a $47,000 spike in compute costs over the weekend. GuardDuty fires a finding at 9:20 AM: `UnauthorizedAccess:EC2/SSHBruteForce` — an EC2 instance in your production VPC is SSH-brute-forcing 45 other IP addresses. CloudTrail shows 3 new EC2 instances launched in `us-east-1` (you normally only operate in `ap-south-1`).

---

**Inject 1 (9:25 AM):** "Who knows what was running in us-east-1?"

*Expected response:* Nobody should have deployed there. Pull CloudTrail to find which IAM principal launched those instances.
```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=RunInstances \
  --start-time 2024-01-12T00:00:00Z
```

**Inject 2 (9:35 AM):** CloudTrail shows: EC2 instances launched by IAM role `lambda-deployment-role` at 2:37 AM Saturday.

*Expected response:* Lambda deployment role shouldn't be able to launch EC2. Investigate: what permissions does this role actually have? How was it exploited?
- Check role policy: does it have `ec2:RunInstances`? → Overprivileged role
- Check what Lambda function uses this role → Was the Lambda function code modified?

**Inject 3 (9:45 AM):** CloudTrail shows the Lambda function code was updated at 2:35 AM by a developer's IAM user from an IP in Ukraine.

*Decision point:* Do you disable the developer's account immediately?
→ Yes — disable immediately, investigate later. Use emergency deny policy.

**Inject 4 (10:00 AM):** You disable the developer's account. New finding: the Lambda function was reading Secrets Manager for RDS credentials, then storing them in a newly-created public S3 bucket.

*Expected response:*
1. Close the public S3 bucket immediately
2. Rotate ALL RDS credentials
3. Audit: what data did the RDS user have access to?
4. Check Macie: was sensitive data scanned?

**Debrief Questions:**
1. How long between initial compromise (2:35 AM) and detection (9:20 AM)? Why?
2. What controls would have prevented this? (MFA for IAM user, Lambda least privilege, Secrets Manager access logging)
3. What notifications are required? (DPDP Act breach notification? Customer notification?)
4. What changes to your architecture will you make?
