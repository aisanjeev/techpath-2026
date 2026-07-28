# Module 11 -- Assignment: AI Agents with LangGraph

**Deadline:** End of Week 17
**Submission:** Python files (.py) + screenshots of agent output + a short README explaining your approach

---

## Task 1: TechPath Admission Advisor Agent -- 35 marks

Build a LangGraph ReAct agent that helps students with the TechPath Institute admission process.

**Requirements:**

1. Create at least **4 custom tools**:
   - `search_courses(query)` -- search courses by topic or keyword
   - `check_eligibility(course_name, student_background)` -- check if a student meets prerequisites
   - `calculate_fee(course_name, discount_code)` -- calculate fee with optional discount (early bird 10%, referral 5%)
   - `book_demo_class(course_name, student_name, date)` -- book a free demo class

2. Build a **state graph** with:
   - A chatbot node (LLM with tools)
   - A tool execution node
   - Conditional edges (use tool or give final answer)
   - A checkpoint for conversation memory

3. The agent must handle these sample conversations:
   - "I am Ananya from Delhi. I know basic Python. Can I join the AI Agents course?"
   - "What is the fee for Python Full Stack? I have a referral code."
   - "Book a demo class for Data Science on August 10 for Priya."

4. Add a **system prompt** that makes the agent friendly, helpful, and knowledgeable about TechPath.

5. Include at least **3 demo queries** that show the agent using multiple tools in sequence.

**Deliverables:**
- `admission_advisor.py` -- the complete agent
- Screenshots showing at least 3 different conversations
- Each tool must be called at least once across the demos

---

## Task 2: Study Plan Generator (Multi-Agent System) -- 30 marks

Build a multi-agent system using the **supervisor pattern** that creates personalized study plans.

**Agents required:**

1. **Supervisor** -- reads the student's request and routes to the right specialist
2. **Skills Assessor** -- asks questions to understand the student's current level
3. **Planner** -- creates a week-by-week study plan with topics and resources
4. **Motivator** -- adds motivational tips, study techniques, and milestone rewards

**Requirements:**

1. The supervisor must correctly route to each agent based on the task
2. Each agent must have its own system prompt with clear personality
3. The system must handle at least these scenarios:
   - A complete beginner wanting to learn Python in 3 months
   - An intermediate student wanting to switch from web dev to AI
   - A student preparing for placement interviews

4. Show the **routing flow** in your output (which agent handles each step)

**Deliverables:**
- `study_planner.py` -- the complete multi-agent system
- Output showing the supervisor routing to different agents for different requests

---

## Task 3: Human-in-the-Loop Approval Agent -- 20 marks

Build a LangGraph agent that requires **human approval** before taking certain actions.

**Scenario:** A TechPath student management agent that can:
- View student records (no approval needed)
- Update student contact info (needs approval)
- Process refund requests (needs approval)
- Send batch emails (needs approval)

**Requirements:**

1. Use `interrupt_before` to pause the agent before sensitive actions
2. Show the agent's planned action to the user and wait for approval
3. If approved, execute the action; if rejected, cancel and explain why
4. Use checkpointing so the agent can resume after the interrupt

**Deliverables:**
- `approval_agent.py` -- the agent with human-in-the-loop
- Screenshots showing: an action that gets approved AND an action that gets rejected

---

## Task 4: Agentic RAG System -- 15 marks

Build a simple **Agentic RAG** system that answers questions about TechPath Institute using a document store.

**Requirements:**

1. Create a small knowledge base (at least 10 text documents) about TechPath:
   - Course descriptions, fee structure, faculty info, admission process, campus facilities, placement stats

2. Use FAISS or ChromaDB as the vector store

3. Build a LangGraph workflow with these nodes:
   - **Router** -- decide if the question needs document search or can be answered directly
   - **Retriever** -- search the vector store
   - **Grader** -- check if retrieved documents are relevant
   - **Generator** -- create the answer from relevant documents

4. Show the agent handling:
   - A question it can answer from documents
   - A question where it needs to rewrite the query and retry
   - A question outside the knowledge base (should say "I don't know")

**Deliverables:**
- `agentic_rag.py` -- the complete system
- The knowledge base documents (can be in a list in the code)

---

## Rubric

| Criteria | Excellent (Full Marks) | Good (75%) | Needs Work (50%) |
|----------|----------------------|------------|------------------|
| **Tools & Functions** | 4+ working tools with clear docstrings, proper error handling | Tools work but missing docstrings or error handling | Fewer than required tools or tools don't work |
| **Graph Structure** | Correct state, nodes, edges, conditional routing; graph compiles and runs | Graph works but missing conditional edges or checkpointing | Graph doesn't compile or is a simple chain (not a graph) |
| **Agent Behavior** | Agent reasons through multi-step tasks, uses tools correctly, gives helpful responses | Agent works for simple queries but fails on multi-step tasks | Agent doesn't use tools or gives irrelevant responses |
| **Code Quality** | Clean code, full comments on every section, clear variable names, docstrings | Some comments, mostly readable | No comments, hard to follow |
| **Demo & Output** | 3+ demo conversations showing different scenarios, clear formatted output | 1-2 demos, basic output | No demos or agent crashes |
