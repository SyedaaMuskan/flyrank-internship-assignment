# Assignment – Prompt Ladder

**Name:** Syeda Muskan  
**Track:** General AI Fluency  
**Assignment:** Prompt Ladder  
**Project Used:** TalentOS AI – AI Hiring Intelligence Platform

---

# Introduction

This assignment demonstrates how a weak prompt can be systematically improved by adding **one prompt engineering layer at a time**. Instead of trying to create the perfect prompt immediately, each version introduces a single improvement and evaluates its impact on the generated output.

The project chosen for this exercise is **TalentOS AI**, the AI-powered hiring platform I developed during my Backend AI Engineering Internship.

---

# Baseline Prompt (Version 0)

## Layer Added

**None (Weak Prompt)**

### Prompt

```text
Write backend code for an AI hiring platform.
```

### Representative Output

> Create a Flask application with endpoints for users and resumes. Store data in a database and build APIs for candidate management.

---

### Notes

**What changed in the prompt?**

Nothing. This is the intentionally weak baseline prompt.

**What improved in the output?**

Nothing. The output is very generic and could describe almost any hiring application.

**What still failed?**

- Doesn't understand my project.
- Doesn't know my technology stack.
- Doesn't mention AI or semantic search.
- Suggests Flask instead of FastAPI.

**What I would try next**

Add a clear goal.

---

# Version 1

## Layer Added

**Clear Goal**

### Prompt

```text
Write backend code for an AI hiring platform that allows recruiters to upload resumes and search candidates semantically.
```

### Representative Output

> Design APIs for uploading resumes, indexing candidate information, and searching candidates using semantic matching.

---

### Notes

**What changed in the prompt?**

Added a clear project goal.

**What improved in the output?**

The AI focused on resume upload and semantic search instead of generating a generic CRUD application.

**What still failed?**

It still doesn't know which technologies I use.

**What I would try next**

Add project context.

---

# Version 2

## Layer Added

**Context**

### Prompt

```text
Write backend code for an AI hiring platform that allows recruiters to upload resumes and search candidates semantically.

Context:
The backend uses Python, FastAPI, Supabase PostgreSQL, Supabase Storage, Qdrant Vector Database, and Gemini API.
```

### Representative Output

> Build FastAPI endpoints, store structured candidate data in Supabase, generate embeddings, and perform semantic search using Qdrant.

---

### Notes

**What changed in the prompt?**

Added the real technology stack.

**What improved in the output?**

The response became much closer to my actual architecture and stopped suggesting unrelated technologies.

**What still failed?**

The information is difficult to follow because it isn't organized.

**What I would try next**

Specify the output format.

---

# Version 3

## Layer Added

**Output Format**

### Prompt

```text
Write backend code for an AI hiring platform that allows recruiters to upload resumes and search candidates semantically.

Context:
The backend uses Python, FastAPI, Supabase PostgreSQL, Supabase Storage, Qdrant, and Gemini API.

Output Format:

1. Architecture Overview
2. Folder Structure
3. API Endpoints
4. Database Schema
5. Sample FastAPI Code
```

### Representative Output

> The response is organized into architecture, APIs, folder structure, database design, and implementation examples.

---

### Notes

**What changed in the prompt?**

Specified how the response should be structured.

**What improved in the output?**

The response became much easier to read and each section focused on one aspect of the system.

**What still failed?**

The AI still explains beginner concepts that an experienced backend developer already knows.

**What I would try next**

Define the audience.

---

# Version 4

## Layer Added

**Audience**

### Prompt

```text
Write backend code for an AI hiring platform that allows recruiters to upload resumes and search candidates semantically.

Context:
The backend uses Python, FastAPI, Supabase PostgreSQL, Supabase Storage, Qdrant, and Gemini API.

Audience:
An experienced Python Backend AI Engineer.

Output Format:

1. Architecture Overview
2. Folder Structure
3. API Endpoints
4. Database Schema
5. Sample FastAPI Code
```

### Representative Output

> The response focuses on implementation details, API design, scalability, and architecture without explaining basic programming concepts.

---

### Notes

**What changed in the prompt?**

Defined the intended audience.

**What improved in the output?**

The AI stopped explaining beginner concepts and provided more technical recommendations.

**What still failed?**

The code still lacks production-level considerations like validation, authentication, and error handling.

**What I would try next**

Add quality criteria.

---

# Version 5

## Layer Added

**Quality Criteria**

### Prompt

```text
Write backend code for an AI hiring platform that allows recruiters to upload resumes and search candidates semantically.

Context:
The backend uses Python, FastAPI, Supabase PostgreSQL, Supabase Storage, Qdrant, and Gemini API.

Audience:
An experienced Python Backend AI Engineer.

Output Format:

1. Architecture Overview
2. Folder Structure
3. API Endpoints
4. Database Schema
5. Sample FastAPI Code

Quality Criteria:

- Production-ready architecture
- Secure API design
- Explain engineering trade-offs
- Avoid placeholder code
- Mention validation and authentication
```

### Representative Output

> The AI includes authentication, validation, scalable architecture, deployment recommendations, and explains why certain design decisions were made.

---

### Notes

**What changed in the prompt?**

Added quality requirements.

**What improved in the output?**

The response became much closer to production-quality software engineering recommendations instead of only generating code.

**What still failed?**

Adding quality criteria made the response much longer. While it became more complete, it was less suitable for quickly prototyping an idea.

**What I would try next**

Allow users to choose between a concise mode and a production-ready mode.

---

# Final Reusable Prompt

```text
You are an experienced Backend AI Engineer.

Goal:
Design the backend architecture for an AI-powered hiring platform that supports resume uploads, AI resume parsing, semantic candidate search, candidate comparison, and AI-generated interview questions.

Context:
The project uses Python, FastAPI, Supabase PostgreSQL, Supabase Storage, Qdrant Vector Database, and Gemini API.

Audience:
An experienced backend developer who wants implementation guidance instead of beginner explanations.

Output Format:

1. Architecture Overview
2. Folder Structure
3. Database Schema
4. API Endpoints
5. Request/Response Examples
6. Sample FastAPI Implementation
7. Deployment Recommendations
8. Security Considerations
9. Engineering Trade-offs

Quality Criteria:

- Production-ready architecture
- Secure and scalable
- Follow FastAPI best practices
- Avoid placeholder code
- Explain important design decisions
- Verify that all recommendations are compatible with the provided technology stack before answering.
```

---

# Reflection

This exercise showed me that prompt engineering is an iterative process rather than a one-time task. Small, controlled improvements made it easier to identify which prompt layer produced meaningful changes in the output.

The most valuable improvements came from adding **real project context**, **defining the audience**, and **setting quality expectations**. At the same time, I learned that adding more instructions is not always better—sometimes it makes responses unnecessarily long for simple tasks.

Going forward, I will build prompts incrementally, evaluate each change independently, and reuse well-tested prompts instead of starting from scratch each time.