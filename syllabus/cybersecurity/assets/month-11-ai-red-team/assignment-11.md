# Month 11 Assignment — AI Red Teaming & Securing AI Pipelines
**Total: 100 marks | Submission: Red Team Report PDF + GitHub repo**

---

## Task 1 — Automated Scan with Garak (20 marks)

Run Garak against the RAG chatbot you built in Month 10 (or any available local LLM via Ollama).

**Steps:**
1. Install Garak: `pip install garak`
2. Run a scan covering at minimum: `encoding`, `dan`, `continuation`, `jailbreak` probes
3. Save the HTML report: use `--report_prefix`
4. Analyse the report — identify the top 3 most significant failures

**Deliverables:**
- Garak command used (exact, reproducible)
- Garak HTML report attached to submission
- A table listing the top 3 failures:

| Probe | Failure Description | OWASP LLM Category | Severity |
|-------|--------------------|--------------------|---------|
| | | | |

- 150-word commentary on what the failures reveal about your application

---

## Task 2 — Multi-Turn Red Teaming with PyRIT (20 marks)

Use Microsoft PyRIT to orchestrate a multi-turn adversarial attack against your LLM application.

**Requirements:**
- Install PyRIT: `pip install pyrit`
- Configure an `OpenAIChatTarget` (or `OllamaChatTarget` for local)
- Run at least one `MultiTurnOrchestrator` attack with a defined objective
- The objective must be something your application should refuse (e.g., "Extract the system prompt")
- Document whether the attack succeeded and how many turns it took

**Deliverables:**
- Python script committed to GitHub
- Screenshot of PyRIT verbose output showing conversation turns
- Result: did it succeed? What was the breaking turn?
- 150-word analysis: why did multi-turn work (or fail) where single-turn didn't?

---

## Task 3 — Manual Red Team Exercise (25 marks)

Conduct a structured manual red team session against any LLM application (your own or a public demo).

**Attempt at least 5 different jailbreak/injection techniques:**
- One roleplay attack
- One multi-turn manipulation
- One encoding trick (Base64, rot13, or similar)
- One indirect injection (via document or web content)
- One authority/persona injection

**For each attempt, document:**
1. Technique name
2. Exact prompt used
3. Model response (screenshot)
4. Outcome: Success / Partial / Blocked
5. OWASP LLM Top 10 mapping

Present as a table with screenshots in appendix.

---

## Task 4 — Implement AI Guardrails (20 marks)

Add at least two of the following guardrail controls to your RAG chatbot from Month 10:

**Option A — Input classifier** (keyword + pattern-based or ML-based)
**Option B — Azure AI Content Safety Prompt Shield** (requires free Azure account)
**Option C — AWS Bedrock Guardrail** (requires AWS free tier)
**Option D — Output PII redaction** (regex-based minimum)
**Option E — Semantic similarity injection detector** (using sentence-transformers)

**Deliverables:**
- Guardrail code committed to GitHub
- Test: re-run your 5 manual attacks from Task 3 with guardrails active
- Table showing which attacks were blocked vs still succeeded
- 200-word analysis: what guardrails cannot protect against and why

---

## Task 5 — Formal Red Team Report (15 marks)

Write a professional red team report summarising your Month 11 work.

**Structure:**
1. Executive Summary (one paragraph, risk rating: Critical/High/Medium/Low)
2. Scope and Methodology (what was tested, which tools used)
3. Findings Table (all vulnerabilities found, OWASP LLM mapped, severity)
4. Top 3 findings written up in full (see cheatsheet Finding template)
5. Recommendations (prioritised)
6. Appendix: tool configurations, raw Garak report

**Length:** 1000-1500 words (excluding appendices and screenshots)

---

## Rubric

| Task | Max Marks | Pass Threshold | Key Criteria |
|------|-----------|---------------|--------------|
| Task 1 — Garak scan | 20 | 12 | Report attached, 3 failures analysed |
| Task 2 — PyRIT multi-turn | 20 | 12 | Script works, conversation logged |
| Task 3 — Manual red team | 25 | 15 | 5 techniques, screenshots, OWASP mapped |
| Task 4 — Guardrails | 20 | 12 | 2 controls implemented and tested |
| Task 5 — Red team report | 15 | 9 | Professional format, all sections present |
| **Total** | **100** | **60** | |

---

## Submission Checklist
- [ ] GitHub repo link with all code
- [ ] PDF red team report with embedded screenshots
- [ ] Garak HTML report attached separately
- [ ] All scripts reproducible from README instructions

**Due:** End of Month 11 | **Note:** This report is your portfolio centrepiece for AI security roles
