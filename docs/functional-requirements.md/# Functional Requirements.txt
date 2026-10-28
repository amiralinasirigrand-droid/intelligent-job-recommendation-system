# Functional Requirements

## 1. User Account Management

### FR-01 — User Registration
The system shall allow a new user to create an account.

### FR-02 — User Login
The system shall allow registered users to authenticate and access their personal profile.

### FR-03 — User Profile Management
The system shall allow users to create, view, and update their personal profile.

---

## 2. Education Management

### FR-04 — Education Information
The system shall allow users to add, view, update, and remove their education information.

Education information may include
- Degree
- Field of study
- Institution
- Start date
- End date

---

## 3. Work Experience Management

### FR-05 — Work Experience
The system shall allow users to add, view, update, and remove their work experience.

Work experience information may include
- Job title
- Company
- Description
- Start date
- End date

---

## 4. Skill Management

### FR-06 — User Skills
The system shall allow users to add, view, update, and remove skills associated with their profile.

### FR-07 — Skill Information
The system shall store relevant information about skills used by the system for job matching.

---

## 5. Job Management

### FR-08 — Job Storage
The system shall store job opportunities in the database.

### FR-09 — Job Information
Each job opportunity shall contain relevant information such as
- Job title
- Company
- Description
- Required skills
- Required experience
- Other relevant requirements

### FR-10 — Job Browsing
The system shall allow users to browse available job opportunities.

### FR-11 — Job Search
The system shall allow users to search for relevant job opportunities.

### FR-12 — Job Details
The system shall allow users to view detailed information about a selected job opportunity.

---

## 6. Job Matching

### FR-13 — Profile and Job Comparison
The system shall compare the user's profile with the requirements of available job opportunities.

The comparison shall consider relevant user information including
- Education
- Work experience
- Technical skills

### FR-14 — Compatibility Score
The system shall calculate a compatibility score representing the degree of match between a user's profile and a job opportunity.

### FR-15 — Skill Matching
The system shall identify skills possessed by the user that correspond to the skills required by a job.

---

## 7. Skill-Gap Analysis

### FR-16 — Missing Skill Identification
The system shall identify skills required by a job that are not present in the user's profile.

### FR-17 — Skill-Gap Presentation
The system shall present identified skill gaps to the user in an understandable format.

---

## 8. Job Recommendation

### FR-18 — Job Recommendations
The system shall generate job recommendations based on the compatibility between the user's profile and available job opportunities.

### FR-19 — Recommendation Ranking
The system shall rank recommended job opportunities according to their calculated compatibility.

---

## 9. System Administration

### FR-20 — Job Data Management
The system shall provide an appropriate mechanism for managing job opportunities and their requirements.

### FR-21 — Skill Data Management
The system shall provide an appropriate mechanism for maintaining the skills used by the recommendation system.