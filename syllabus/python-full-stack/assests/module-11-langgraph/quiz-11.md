# Quiz: LangGraph -- AI Agents & Agentic Workflows

**Module 11 | 15 Questions | Pass Mark: 60%**

---

## Q1. What is an AI agent?
- A) A simple chatbot that answers questions
- B) An LLM that can decide, use tools, and loop until done ✅
- C) A database management system
- D) A web scraping tool

> **Explanation:** An AI agent is an LLM with the ability to decide what to do next, use tools, and loop through think-act-observe cycles until the task is complete.

---

## Q2. What does ReAct stand for?
- A) React JavaScript Framework
- B) Reasoning + Acting ✅
- C) Read and Compute
- D) Retrieve and Cache

> **Explanation:** ReAct = Reasoning + Acting. The agent reasons, acts (uses a tool), observes the result, and repeats until done.

---

## Q3. What is LangGraph used for?
- A) Building static websites
- B) Creating charts and graphs
- C) Building stateful, multi-step AI workflows ✅
- D) Managing databases

> **Explanation:** LangGraph is for building stateful, multi-step AI workflows with loops, conditions, and state management.

---

## Q4. In LangGraph, what is a 'node'?
- A) A database record
- B) A function that processes the graph's state ✅
- C) A type of LLM model
- D) A CSS styling element

> **Explanation:** A node is a Python function that takes state, processes it, and returns updated state.

---

## Q5. What does the add_messages annotation do?
- A) Deletes old messages
- B) Replaces the message list entirely
- C) Appends new messages to the existing list ✅
- D) Converts messages to embeddings

> **Explanation:** add_messages appends new messages instead of replacing the list, preserving conversation history.

---

## Q6. What is the purpose of a conditional edge?
- A) To always go to the same next node
- B) To choose the next node based on the current state ✅
- C) To delete a node from the graph
- D) To create a new LLM instance

> **Explanation:** A conditional edge uses a routing function to decide which node to go to next based on the current state.

---

## Q7. Why is a clear docstring important for tools?
- A) It makes the code look professional
- B) The LLM reads it to decide when and how to use the tool ✅
- C) It is required by Python syntax
- D) It speeds up execution

> **Explanation:** The LLM reads the tool's docstring to understand when to use it and what arguments to pass.

---

## Q8. What is a checkpoint in LangGraph?
- A) A debugging breakpoint in code
- B) A saved snapshot of the graph's state that can be resumed ✅
- C) A type of unit test
- D) A code review step

> **Explanation:** A checkpoint saves the graph's state, allowing you to resume conversations or implement human-in-the-loop approval.

---

## Q9. What is the Supervisor pattern?
- A) One agent does everything alone
- B) A central agent that routes tasks to specialized agents ✅
- C) Agents compete to answer first
- D) Users manually pick which agent to use

> **Explanation:** The Supervisor pattern has a central agent that routes tasks to specialized agents and coordinates the workflow.

---

## Q10. When should you use human-in-the-loop?
- A) For every single agent action
- B) Only for answering FAQ questions
- C) For irreversible actions or those involving money and people ✅
- D) Never -- agents should be fully autonomous

> **Explanation:** Use HITL for irreversible actions (emails), financial actions (refunds), or changes affecting people (enrollment).

---

## Q11. What does interrupt_before do?
- A) Cancels the graph execution
- B) Pauses the graph before a specific node runs ✅
- C) Speeds up execution
- D) Deletes the node from the graph

> **Explanation:** interrupt_before pauses execution before the specified node, allowing human review before the action happens.

---

## Q12. What is LangSmith used for?
- A) Writing Python code
- B) Monitoring, debugging, and testing AI agents ✅
- C) Creating vector databases
- D) Building web frontends

> **Explanation:** LangSmith monitors every step, helps debug errors, and runs automated evaluations on AI agents.

---

## Q13. What makes Agentic RAG different from regular RAG?
- A) There is no difference
- B) Agentic RAG can rewrite queries, grade documents, and verify answers ✅
- C) Regular RAG is more accurate
- D) Agentic RAG does not use a vector store

> **Explanation:** Agentic RAG adds search-grade-rewrite-verify intelligence to the RAG pipeline for higher quality answers.

---

## Q14. What type of memory stores facts across sessions?
- A) Short-term memory
- B) Long-term memory (vector store) ✅
- C) Episodic memory
- D) Buffer memory

> **Explanation:** Long-term memory uses a vector store to persist user facts across sessions.

---

## Q15. Why set a recursion_limit or max retries?
- A) To make the agent run faster
- B) To prevent infinite loops where the agent keeps retrying forever ✅
- C) To reduce memory usage
- D) To improve answer quality

> **Explanation:** Without limits, agents can get stuck in loops. A recursion_limit or max retries prevents this.
