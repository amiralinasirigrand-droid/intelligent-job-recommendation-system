# System Architecture

## 1. Architectural Overview

The proposed system will use a layered web application architecture consisting of a frontend layer, an applicationAPI layer, and a data layer.

The main technologies selected for the implementation are

- React for the frontend
- Python with FastAPI for the backend and REST API
- PostgreSQL for persistent data storage
- Git for version control
- Python-based processing and recommendation algorithms

The architecture is designed to separate presentation, application logic, recommendation processing, and data storage responsibilities.

---

## 2. High-Level Architecture

The system will consist of the following main layers

### 2.1 Presentation Layer

The presentation layer will be implemented using React.

Its responsibilities include

- User interface rendering
- User registration and login interfaces
- Profile management interfaces
- Job browsing and search
- Job detail presentation
- Compatibility score presentation
- Skill-gap presentation
- Job recommendation presentation

The frontend will communicate with the backend through REST API endpoints.

---

### 2.2 Application and API Layer

The application layer will be implemented using Python and FastAPI.

Its responsibilities include

- Authentication and authorization
- User management
- Profile management
- Education management
- Work experience management
- Skill management
- Job management
- REST API endpoints
- Business logic
- Communication with the database
- Communication with the matching and recommendation components

The backend will act as the main application layer between the frontend and the database.

---

### 2.3 Data Layer

The data layer will use PostgreSQL as the persistent relational database.

It will store information related to

- Users
- User profiles
- Skills
- Education
- Work experience
- Job opportunities
- Job requirements
- Relationships between users, skills, jobs, and requirements

The backend will be responsible for accessing and modifying persistent data.

---

## 3. Recommendation and Matching Components

The intelligent functionality of the system will be implemented as backend components.

### 3.1 Matching Component

The matching component will compare information from a user's profile with the requirements of a job opportunity.

The comparison may consider

- User skills
- Required job skills
- Education
- Work experience
- Other relevant job requirements

The component will produce a compatibility score.

The exact scoring methodology will be defined during the algorithm design stage after further analysis of relevant literature and available project data.

---

### 3.2 Skill-Gap Analysis Component

The skill-gap component will analyse the difference between the user's current skills and the skills required by a selected job.

The component will identify

- Matched skills
- Missing skills

The resulting information will be presented to the user.

---

### 3.3 Recommendation Component

The recommendation component will use the results of the matching process to rank available job opportunities.

The component will generate a list of relevant job opportunities for the user.

The initial implementation will establish a baseline recommendation approach. More advanced natural language processing or machine learning techniques may be investigated later if justified by the research and evaluation results.

---

## 4. Communication Between Components

The main communication flow will be

    React Frontend
          
           REST API
          v
    FastAPI Backend
          
          +--------------------+
                              
          v                    v
    PostgreSQL          Matching  Recommendation
                            Components

The React frontend will not communicate directly with the PostgreSQL database.

All application and business logic will be handled through the backend.

---

## 5. Main Backend Components

The backend will be logically organized into the following components

    FastAPI Backend
    
    +-- Authentication
    
    +-- User Management
    
    +-- Profile Management
         +-- Education
         +-- Experience
         +-- Skills
    
    +-- Job Management
    
    +-- Matching Component
    
    +-- Skill-Gap Analysis
    
    +-- Recommendation Component
    
    +-- Database Access

The exact project folder and module structure will be defined during implementation.

---

## 6. Main System Data Flow

A typical recommendation request will follow these steps

1. The user accesses the recommendation functionality through the React frontend.
2. The frontend sends a request to the appropriate FastAPI endpoint.
3. The backend retrieves the relevant user profile and available job information.
4. The matching component compares the user profile with job requirements.
5. Compatibility scores are calculated.
6. Skill gaps are identified.
7. Jobs are ranked according to the recommendation methodology.
8. The backend returns the recommendation results through the REST API.
9. The React frontend presents the results to the user.

---

## 7. Architectural Principles

The system architecture will follow these principles

### Separation of Concerns

Each major component will have a clearly defined responsibility.

### Modularity

The system will be divided into components that can be developed and maintained independently.

### Maintainability

The architecture should allow individual components to be modified without unnecessary changes to unrelated components.

### Extensibility

The system should allow additional recommendation methods, data-processing techniques, or functionality to be added in the future.

### Security

Sensitive operations and database access will be handled by the backend rather than directly by the frontend.

---

## 8. Architectural Scope

The architecture covers the core functionality defined for the thesis

- User management
- Profile management
- Education and experience management
- Skill management
- Job management
- Job matching
- Compatibility scoring
- Skill-gap analysis
- Job recommendation

External job-platform integrations are outside the initial architectural scope unless they are later determined to be necessary for the project.

---

## 9. Technology Selection

The selected technologies are consistent with the thesis working plan.

React will be used for the frontend, Python with FastAPI for the backend and REST API, PostgreSQL for persistent storage, and Git for version control.

Python will also be used for data processing and recommendation algorithms.

Natural language processing or machine learning techniques may be investigated as an extension to the initial implementation.