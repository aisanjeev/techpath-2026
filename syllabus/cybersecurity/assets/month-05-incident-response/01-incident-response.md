# Incident Response: NIST Lifecycle, Playbooks & Team Roles

## What Is Incident Response?

Incident Response (IR) is the organised process of detecting, containing, and recovering from security incidents. The goal is not just to stop the immediate attack — it is to:

1. **Minimise damage** — contain quickly before the attacker achieves their objective
2. **Preserve evidence** — maintain integrity for forensics and potential legal action
3. **Understand the root cause** — so you can close the door the attacker used
4. **Prevent recurrence** — improve detection and hardening based on what happened

IR is both a technical discipline and a people/process challenge. The best-equipped technical team will fail without clear communication, documented playbooks, and practiced tabletop exercises.

---

## NIST SP 800-61 IR Lifecycle

NIST Special Publication 800-61 is the most widely adopted IR framework. It defines six phases:

### Phase 1: Prepare

Prevention is better than cure. Preparation happens before any incident and determines how effectively you respond.

**Activities:**
- Write and maintain an Incident Response Plan (IRP) — who does what, contact trees, escalation paths
- Develop playbooks for common incident types: ransomware, phishing, account compromise, insider threat
- Deploy and configure detection tools: SIEM, EDR, Sysmon, network sensors
- Conduct regular tabletop exercises to practice response without a real incident
- Establish relationships with legal, HR, PR, and executive stakeholders
- Prepare jump bags: pre-built forensic toolkits on USB drives with write-blockers, memory capture tools, network cables
- Train staff on how to recognise and report suspicious activity

**Key artefacts produced:** IR plan document, playbooks, contact list, asset inventory, tool inventory

### Phase 2: Identify (Detection & Analysis)

The incident begins when it is detected — either by automated alert, user report, or external notification.

**Detection sources:**
- SIEM alerts (log correlation)
- EDR/XDR alerts (behavioural detection on endpoints)
- Threat intelligence feeds (known IOC match)
- User reports ("my computer is acting strange")
- External notification (law enforcement, partner organisation, bug bounty)

**Analysis activities:**
- Validate the alert: true positive or false positive?
- Determine severity and scope: single endpoint, or multiple systems?
- Declare an incident and open a formal incident ticket
- Notify stakeholders per the IRP escalation path
- Preserve initial evidence before starting containment

**Key questions to answer:**
- What is the nature of the incident (ransomware, data breach, insider, APT)?
- When did it start? (Check logs backward from detection point)
- What systems are confirmed affected?
- What systems might be affected but are unconfirmed?

### Phase 3: Contain

Stop the bleeding. Containment prevents further damage while preserving forensic evidence.

**Short-term containment (immediate):**
- Network isolation: disconnect affected hosts from the network at the switch level (VLAN change) or endpoint firewall
- Block C2 IP/domain at perimeter firewall and DNS sinkholes
- Disable compromised accounts (not reset — attacker may have a backdoor account)
- Preserve memory before isolation if malware may clear on restart

**Long-term containment (while eradication is planned):**
- Deploy additional monitoring to detect if the attacker pivots to other systems
- Maintain network segmentation
- Continue collecting evidence from all affected systems

**Critical rule:** Contain without destroying evidence. Pulling a network cable is better than powering off a machine (which loses volatile memory data).

### Phase 4: Eradicate

Remove the threat root-to-tip — not just the surface malware.

**Eradication checklist:**
- Remove all malware, backdoors, and persistence mechanisms
- Patch or mitigate the initial access vector (the CVE or misconfiguration exploited)
- Rotate all potentially compromised credentials (especially privileged accounts)
- Remove attacker-created accounts, scheduled tasks, and services
- Re-image rather than trying to "clean" heavily compromised systems
- Verify eradication on all affected systems — not just patient zero

**Common mistakes:**
- Cleaning only the initially detected host while the attacker has lateral-moved to 5 others
- Resetting passwords but missing that the attacker also has a second-factor bypass
- Not patching the entry point, allowing re-compromise within days

### Phase 5: Recover

Restore normal operations safely — not just restoring systems, but restoring confidence.

**Recovery steps:**
- Restore systems from clean backups (verified pre-incident) or rebuild from image
- Gradually reconnect systems with enhanced monitoring
- Monitor the restored environment closely for re-compromise indicators
- Validate that business operations are fully functional
- Communicate status to stakeholders: users, management, customers if affected
- Document the recovery process for the lessons-learned review

### Phase 6: Learn (Post-Incident Activity)

The most skipped phase — and the most valuable for long-term improvement.

**Post-Incident Review (PIR) should happen within 2 weeks:**
- What happened, and why? (Timeline of the incident)
- Was detection fast enough? What caused any delay?
- Did containment work? What slowed it down?
- Were playbooks followed? Were they helpful?
- What detection rules need to be created or tuned?
- What hardening would have prevented or reduced the impact?
- What process improvements are needed?

**Output:** Updated IR plan, new/updated playbooks, improved detection rules, hardening backlog tickets

---

## IR Team Roles and Responsibilities

| Role | Responsibilities |
|------|-----------------|
| **Incident Commander** | Overall coordination, decision authority, stakeholder communications |
| **Lead Analyst** | Technical investigation, forensics, evidence collection |
| **SOC Analysts (L1/L2)** | Log analysis, alert correlation, scope identification |
| **IT Operations** | System isolation, firewall changes, account management |
| **Legal / Compliance** | Evidence preservation guidance, regulatory notification decisions |
| **HR** | Involved in insider threat incidents; employee communication |
| **PR / Communications** | External communication if customer data is involved |
| **CISO / Executive** | Executive decisions (pay ransom? notify authorities?) |

---

## IR Playbook: Ransomware Response

A playbook is a pre-written step-by-step procedure for a specific incident type.

```
RANSOMWARE RESPONSE PLAYBOOK
Phase 1 (DETECT): SIEM alert fires for mass file encryption or
                   multiple .locked extensions created rapidly
Phase 2 (VALIDATE): Confirm on at least 2 systems. Check:
  - File extensions changed?
  - Ransom note present?
  - EDR alert on shadow copy deletion (vssadmin)?
Phase 3 (CONTAIN):
  1. Isolate affected systems immediately (VLAN, firewall rule)
  2. Disable compromised accounts
  3. Block C2 IPs/domains at perimeter
  4. Alert backup team: do NOT run backups (risk of encrypting backups)
Phase 4 (ERADICATE):
  1. Identify patient zero and entry point
  2. Determine lateral movement scope
  3. Re-image all confirmed affected systems
  4. Patch entry point CVE or misconfig
Phase 5 (RECOVER):
  1. Restore from last clean backup (verify backup integrity first)
  2. Change ALL privileged passwords
  3. Re-enable systems with enhanced monitoring
Phase 6 (LEARN):
  1. PIR within 72 hours
  2. Update backup strategy if backups were affected
  3. Document TTPs and create new detection rules
```

---

## IR Communication Template

**Initial Incident Notification (to management):**
```
TO:    CISO, Legal, IT Director
FROM:  SOC Lead / Incident Commander
RE:    Security Incident — INC-2026-001

We have confirmed a security incident on [DATE] at [TIME].

SEVERITY: High
AFFECTED SYSTEMS: [N] hosts in [NETWORK SEGMENT]
NATURE: [Ransomware / Data breach / Credential theft / etc.]
STATUS: Containment in progress

IMMEDIATE ACTIONS TAKEN:
- [List of containment actions]

NEXT UPDATE: [Time]
INCIDENT COMMANDER: [Name, phone]
```
