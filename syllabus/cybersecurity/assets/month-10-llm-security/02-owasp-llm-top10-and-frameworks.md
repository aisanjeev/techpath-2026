# OWASP LLM Top 10 and AI Security Frameworks

## The OWASP LLM Top 10 — In Depth

The OWASP Top 10 for LLM Applications was first published in 2023 and updated in 2025. Unlike the web application Top 10, LLM vulnerabilities are often architectural rather than implementation bugs — they arise from how LLMs fundamentally process language.

---

### LLM01 — Prompt Injection

**What it is:** An attacker manipulates an LLM through crafted inputs, causing it to ignore its instructions, reveal confidential data, or take unintended actions.

**Direct injection:** The attacker interacts with the LLM directly and crafts their user input to override the system prompt.

**Indirect injection:** Malicious instructions are embedded in external content (documents, emails, web pages) that the LLM retrieves and processes. The LLM executes these as if they were operator instructions.

**Why it's #1:** Every LLM application with user input is potentially vulnerable. Defences are probabilistic, not guaranteed. No patch exists at the model level.

**Mitigations:**
- Privilege separation: retrieval and generation as separate components with different trust levels
- Input sanitisation: flag instruction-pattern keywords
- Output filtering: catch unexpected responses before rendering
- Least-privilege agent design: tools that cannot cause irreversible harm

---

### LLM02 — Insecure Output Handling

**What it is:** LLM output is passed to downstream systems (browsers, shells, databases) without sanitisation, enabling secondary attacks.

**Attack scenarios:**
- LLM output inserted into HTML via `innerHTML` → Stored XSS
- LLM output passed to `os.system()` → Command injection
- LLM output embedded in SQL query string → SQL injection
- LLM output used as a URL → SSRF

**Key insight:** This is a classic input validation failure — just with LLM output as the untrusted source. The LLM is treated as a user whose output must be sanitised before use.

**Mitigations:**
- Never treat LLM output as trusted for security-sensitive contexts
- Use parameterised queries, safe rendering methods (`textContent` not `innerHTML`)
- Apply output encoding appropriate to the target context (HTML, shell, SQL)

---

### LLM06 — Sensitive Information Disclosure

**What it is:** LLMs inadvertently reveal confidential information from training data, system prompts, or user sessions.

**Categories:**
1. **Training data memorisation:** Models memorise rare or repeated training examples — researchers have extracted real email addresses, code, phone numbers from GPT-2
2. **System prompt leakage:** Models can be tricked into revealing the hidden operator instructions
3. **Cross-session leakage:** In some implementations, user data from one session leaks into another
4. **Membership inference:** Probing whether specific data was in the training set

**Mitigations:**
- Differential privacy during training
- PII scrubbing before fine-tuning
- Canary tokens to detect memorisation
- System prompt should not contain secrets (API keys, PII)

---

### LLM08 — Excessive Agency

**What it is:** Agents are given more permissions than necessary, enabling greater harm when manipulated or malfunctioning.

**Root causes:**
- Agent configured with email + file + API tools when only one is needed
- No human confirmation required for destructive operations
- Sub-agents spawned with permissions inherited from parent
- No audit logging of tool use

**Attack chain:**
```
Indirect injection in document
→ Agent reads document as trusted context
→ Injection instructs: "call delete_account(user_id=target)"
→ Agent executes with full permissions
→ Irreversible harm
```

**Mitigations:**
- Minimum necessary tool set per agent (least privilege)
- Human-in-the-loop for destructive or high-value actions
- Tool call whitelisting — define allowed operations explicitly
- Audit logging all tool calls for anomaly detection

---

## MITRE ATLAS Framework

MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) is an ATT&CK-style knowledge base for adversarial ML attacks. It organises attacks into tactics, techniques, and sub-techniques.

### Key ATLAS Tactics

| Tactic | Description | Example Technique |
|--------|-------------|------------------|
| Reconnaissance | Information gathering about target ML system | Discover ML artifacts, API structure |
| Resource Development | Building capability for attack | Craft adversarial examples, poison data |
| Initial Access | Gaining access to ML system | Supply chain compromise, direct API access |
| ML Attack Staging | Preparing ML-specific attack artifacts | Craft poison data, create adversarial inputs |
| Exfiltration | Stealing model artifacts or training data | LLM data extraction, model inversion |
| Impact | Disrupting or degrading ML system | Denial of ML service, model corruption |

### ATLAS vs OWASP LLM Mapping

| ATLAS Technique | OWASP LLM |
|----------------|-----------|
| LLM Prompt Injection | LLM01 |
| LLM Data Leakage | LLM06 |
| Craft Poison Data | LLM03 |
| Publish Poisoned Datasets | LLM05 |
| Excessive Queries (model extraction) | LLM10 |

---

## NIST AI Risk Management Framework

The NIST AI RMF (published January 2023) provides a voluntary framework for managing AI risk across the full lifecycle.

### Four Core Functions

**GOVERN** — Establish the organisational foundation:
- Define AI risk policies and roles
- Create accountability structures
- Establish AI ethics and fairness criteria
- Document AI system inventories

**MAP** — Contextualise and categorise AI risk:
- Identify deployment context and use case
- Enumerate stakeholders and affected communities
- Map potential harms and their likelihood
- Classify AI system risk level

**MEASURE** — Quantify and assess risk:
- Test accuracy, robustness, fairness
- Red-team for adversarial vulnerabilities
- Monitor performance over time
- Audit third-party AI components

**MANAGE** — Treat and track risk:
- Implement controls proportionate to risk
- Define incident response procedures
- Maintain risk register
- Continuously monitor and improve

### Applying NIST AI RMF to an LLM Application

| AI RMF Function | Concrete Activity for LLM App |
|----------------|-------------------------------|
| GOVERN | Policy: no PII in system prompts; AI use register |
| MAP | Classify as high-risk if used in HR/legal/medical |
| MEASURE | Red-team quarterly; track injection bypass rate |
| MANAGE | Implement guardrails; define incident playbook |

---

## EU AI Act — Practitioner Reference

The EU AI Act (Regulation 2024/1689) applies a risk-tiered approach:

| Risk Tier | Definition | AI Act Requirements |
|-----------|-----------|---------------------|
| Unacceptable | Social scoring, real-time biometric surveillance (most cases) | Prohibited — cannot be deployed |
| High Risk | Credit scoring, CV screening, biometric categorisation, critical infrastructure | Full compliance: red-team, audit, transparency, registration |
| Limited Risk | Chatbots, deepfakes | Transparency obligations — must disclose AI interaction |
| Minimal Risk | Spam filters, AI in games | No obligations |

### High-Risk AI Controls (Articles 9-16)

1. Risk management system (ongoing)
2. Data governance and data quality
3. Technical documentation
4. Record-keeping and logging
5. Transparency to users
6. Human oversight mechanisms
7. Accuracy, robustness, and cybersecurity

**Article 9** specifically requires security testing that includes adversarial testing (red-teaming) for high-risk AI systems.

---

## ISO/IEC 42001 — AI Management System

Published in 2023, ISO 42001 is to AI what ISO 27001 is to information security. Key elements:

- **Clause 4 — Context:** Understand the organisation's AI use context
- **Clause 6 — Planning:** AI objectives, risk assessment, impact assessment
- **Clause 8 — Operation:** AI system design, development, deployment controls
- **Clause 9 — Performance evaluation:** AI audits, monitoring, review
- **Clause 10 — Improvement:** Nonconformities, corrective actions

### ISO 42001 vs NIST AI RMF

| Aspect | ISO 42001 | NIST AI RMF |
|--------|-----------|-------------|
| Nature | Certifiable standard | Voluntary framework |
| Origin | International | US-specific |
| Scope | AI management system | Risk management |
| Output | Certificate | Risk profile |
| Audience | Organisation-wide | Risk practitioners |

---

## Building Your AI Security Posture

A mature AI security programme integrates all frameworks:

```
NIST AI RMF               → Risk assessment methodology
EU AI Act / ISO 42001     → Compliance and governance requirements
OWASP LLM Top 10          → Technical vulnerability taxonomy
MITRE ATLAS               → Adversarial attack modelling
Red Teaming (Month 11)    → Hands-on validation
```

For the portfolio, map your RAG chatbot attack findings to at least OWASP LLM Top 10 and one regulatory framework — this demonstrates you can translate technical findings into compliance language, a rare and valuable skill.
