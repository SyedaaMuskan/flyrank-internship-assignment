# FL-02 – Prompt Iteration Log

**Name:** Syeda Muskan  
**Track:** AI Fluency – Foundations  
**Project:** TalentOS AI – AI Hiring Intelligence Platform

---

# Introduction

This assignment documents the evolution of a prompt through multiple iterations using prompt engineering techniques introduced in the Anthropic Prompt Engineering Interactive Tutorial.

Instead of optimizing the prompt all at once, I improved it incrementally by applying one technique at a time and observing how the output changed. The task is based on my real internship project, **TalentOS AI**, making the exercise directly relevant to my work.

---

# Target Task

**Design the backend architecture for TalentOS AI, an AI-powered hiring platform that supports resume uploads, semantic candidate search, and AI-generated interview questions.**

---

# Version 0 – Naive Prompt

## Technique

**None (Baseline)**

### Prompt

```text
Build the backend for an AI hiring platform.
```

### Representative Output

> Create a backend using Python and Flask with APIs for users and resumes. Store candidate data in a relational database and expose CRUD endpoints.

### Observation

The response was extremely generic. It did not understand the actual problem, ignored AI functionality, and suggested technologies that did not match my project.

---

# Version 1 – Role Assignment

## Technique

**Role Assignment**

### Prompt

```text
You are an experienced Backend AI Engineer.

Build the backend for an AI hiring platform.
```

### Representative Output

> Design a scalable backend with REST APIs, authentication, and modular architecture suitable for AI-powered applications.

### Observation

Assigning a role immediately changed the quality of the response. The AI began making engineering decisions instead of simply generating beginner-level code. However, it still lacked knowledge about my specific project.

---

# Version 2 – Context & Motivation

## Technique

**Context and Motivation**

### Prompt

```text
You are an experienced Backend AI Engineer.

I am building TalentOS AI, an AI-powered hiring platform.

Recruiters should be able to upload resumes, perform semantic candidate searches, compare applicants, and generate interview questions.

The backend uses FastAPI, Supabase PostgreSQL, Supabase Storage, Qdrant Vector Database, and Gemini API.

Help me design the backend architecture.
```

### Representative Output

> Design a FastAPI application with modules for authentication, resume processing, semantic search using Qdrant, structured candidate storage in Supabase, and AI-powered interview generation.

### Observation

Adding context produced the largest improvement so far. The response closely matched my actual internship project and recommended technologies already used in my implementation.

---

# Version 3 – Few-Shot Examples

## Technique

**Few-Shot Examples**

### Prompt

```text
You are an experienced Backend AI Engineer.

Example

Input:
Design a backend for a chatbot.

Output:
- FastAPI
- Authentication
- Conversation APIs
- PostgreSQL
- Docker Deployment

Now apply the same style.

Design the backend for TalentOS AI using FastAPI, Supabase, Qdrant, and Gemini API.
```

### Representative Output

> Architecture Overview  
> Authentication Module  
> Resume Upload Service  
> Candidate Service  
> Semantic Search Service  
> AI Interview Module  
> Deployment

### Observation

The response became more consistent and organized because the example demonstrated the expected level of detail. The AI mirrored the style without needing additional instructions.

---

# Version 4 – Output Structure

## Technique

**Output Structure**

### Prompt

```text
You are an experienced Backend AI Engineer.

Design the backend for TalentOS AI.

Use the following structure:

1. Architecture Overview
2. Folder Structure
3. Database Design
4. API Endpoints
5. AI Pipeline
6. Deployment Strategy
```

### Representative Output

The AI generated clearly separated sections for architecture, APIs, database schema, AI workflow, and deployment recommendations.

### Observation

The response became significantly easier to read. Instead of mixing ideas together, each topic appeared in its own section, making the design document much more useful.

---

# Version 5 – Step Decomposition

## Technique

**Step Decomposition**

### Prompt

```text
You are an experienced Backend AI Engineer.

Think through the solution step by step.

Step 1:
Understand the hiring workflow.

Step 2:
Identify required backend services.

Step 3:
Design database architecture.

Step 4:
Design API endpoints.

Step 5:
Design the AI pipeline.

Step 6:
Recommend deployment and scalability improvements.

Finally, summarize the complete backend architecture.
```

### Representative Output

The AI first analyzed the hiring workflow before designing services, APIs, storage, AI integration, deployment, and scalability recommendations.

### Observation

Breaking the task into steps improved logical consistency. Each recommendation built naturally on the previous one, resulting in a much more complete system design.

One downside was that the response became much longer. For quick brainstorming, this level of detail may not always be necessary.

---

# Cross-Model Comparison

## Claude

### Strengths

- More conversational and thoughtful.
- Better at explaining engineering trade-offs.
- Produced cleaner architectural reasoning.
- Followed the step-by-step workflow naturally.

### Weaknesses

- Sometimes overly verbose.
- Occasionally omitted implementation details in favor of explanations.

---

## ChatGPT

### Strengths

- More implementation-focused.
- Produced detailed API designs.
- Better folder structures and code organization.
- Generated practical FastAPI recommendations.

### Weaknesses

- Occasionally assumed missing requirements.
- Sometimes introduced additional features that were not requested.

---

# Overall Comparison

For architecture discussions, **Claude** produced more thoughtful reasoning and explained *why* design decisions were made.

For backend implementation planning, **ChatGPT** generated more actionable technical details and stronger project organization.

Rather than one model being universally better, I found them complementary. Claude excelled at system thinking, while ChatGPT was stronger at implementation planning.

---

# Final Reusable Prompt Template

```text
You are an experienced [ROLE].

Goal:
Help me complete the following task:

[TASK]

Background:

[PROJECT CONTEXT]

Motivation:

[WHY THIS TASK MATTERS]

Technology Stack:

[TECH STACK]

Follow these steps:

1. Understand the problem.
2. Identify the important components.
3. Explain your reasoning.
4. Generate the solution.
5. Review the solution for completeness.

Output Format:

- Overview
- Architecture
- Implementation
- Best Practices
- Trade-offs
- Final Recommendations

Requirements:

- Do not make unsupported assumptions.
- Use production-ready recommendations.
- Explain important design decisions.
- Keep explanations concise but technically accurate.
```

---

# Reflection

This exercise reinforced that prompt engineering is an iterative process rather than a one-time activity.

The biggest improvement came from providing **real context** about my project. Once the AI understood the problem and technology stack, its recommendations became much more relevant.

Adding **role assignment** and **output structure** further improved the quality of the responses, while **step decomposition** produced the most complete reasoning, although it also increased the response length.

Finally, comparing Claude and ChatGPT showed that different models have different strengths. Claude was better at reasoning through architectural decisions, while ChatGPT produced more implementation-focused guidance. In future projects, I would use Claude for planning and ChatGPT for implementation support, combining the strengths of both models.