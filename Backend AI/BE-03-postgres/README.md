# BE-03 — FastAPI + PostgreSQL + Docker

## Overview

This assignment upgrades the Task Manager API from SQLite to PostgreSQL and runs the application and database together using Docker Compose.

The main goal was to replace local SQLite storage with a real PostgreSQL database while keeping the existing CRUD API working and making the data persistent across container restarts.

## Architecture

```text
Client
  ↓
FastAPI
  ↓
PostgreSQL
  ↓
Docker Volume