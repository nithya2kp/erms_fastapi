# Engineering Resource Management SYstem
**This is a FastAPI-based backend application that provides full-stack application designed to help managers assign engineers to projects efficiently, track their workload, and plan future allocations.**

##Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: OAuth2 with JWT
- **Validation**: Pydantic
- **Containerization**: Docker

### Frontend
- **Framework**: React (Basic setup for login page)
- **Styling**: CSS

### DevOps
- **Version Control**: Git + GitHub
- **Environment**: Docker Compose (local development)

## AI Tools Used

- **ChatGPT**: Assisted in designing the backend structure, writing SQLAlchemy models, and writing documentation.

## Project Approach

This project was developed following an API-first approach using FastAPI for backend development. Authentication, user roles, and resource assignment were prioritized. While the frontend implementation is currently minimal (basic login page), it provides a foundation for full-featured dashboards to be built on top of the API.
Due to limited hands-on experience with React, only the login functionality was implemented at this stage.

## Core Features

### 1. Authentication & User Roles
- Login system with two roles: **Manager** and **Engineer**
- Engineers can view their assignments
- Managers can assign engineers to projects

### 2. Engineer Management
- **Profile**: Name, skills (React, Node.js, Python, etc.), seniority level
- **Employment Type**: Full-time (100%) or Part-time (50%)
- **Current Status**: Displays current allocation (e.g., 60% allocated, 40% available)

### 3. Project Management
- Basic Info: Project name, description, start/end dates, required team size
- Required Skills: Tech stack needed for each project
- Project Status: Active, Planning, or Completed

### 4. Assignment System
- Assign engineers to projects with a specific allocation percentage
- View current assignments (who is working on what)
- Capacity tracking with workload indicators

---
