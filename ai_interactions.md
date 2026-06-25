# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->
I asked the agent to take my classes and formulate the architecture for the app.

Prompt:
Using this UML diagram and these requirements:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

Do this:
1. Create class stubs (no logic).
2. Implement scheduling behavior.
3. Connect the scheduler here and display results

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->
Reviewing the starter app and repository files to wire in scheduling classes and tests.
Checking repository structure and existing files, then I’ll add scheduler module plus tests.
Adding scheduler module and matching Streamlit integration now.
I’ve added the scheduler module, now verifying its contents and fixing any corruption.
Repairing the scheduler module and wiring the Streamlit app to use it, plus adding tests.
The scheduler module was partially written; checking the current end of pawpal.py and then fixing it cleanly.
Added pawpal.py with class stubs and scheduler behavior
Updated app.py to build and display a schedule from UI inputs
Added test_pawpal.py covering priority ordering and time-limit task skipping
Verified with pytest: 2 passed

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->
The AI agent did have a couple issues with importing certain files, but they were easily fixed.
---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | GitHub Copilot | Claude |
| **Prompt** | Same multi-step scheduling task prompts | Same multi-step scheduling task prompts |
| **Response summary** | Generated scheduler classes, Streamlit integration, and test cases; produced working implementation | Generated scheduler classes, Streamlit integration, and test cases; produced working implementation |
| **What was useful** | Clear class structure and algorithm implementation; tests passed with minimal fixes | Readable docstrings, detailed explanations of patterns, and robust error handling |
| **Problems noticed** | Minor import/module path issues requiring manual fixes | None: all code worked as expected |
| **Decision** | Chose Copilot approach for final implementation | - |

**Which approach did you use in your final implementation and why?**
I went with Copilot's approach. Both agents produced similar-quality results with comparable scheduling logic and test coverage. However, Copilot's output was slightly cleaner and required fewer manual adjustments, making it the practical choice for rapid iteration. The minor import fixes were trivial and the end result was equally good.
