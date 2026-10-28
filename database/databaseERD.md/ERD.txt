# Entity Relationship Diagram (ERD)

## 1. Overview

The database of the Intelligent Web-Based Job and Skill Recommendation System is designed using a relational database model.

The main entities represent users, their educational background, work experience, skills, and available job opportunities.

The system uses associative entities to represent many-to-many relationships between users and skills, and between jobs and skills.

---

## 2. Entities

### User

Represents a registered user of the system.

Attributes

- id (PK)
- email
- password_hash
- first_name
- last_name
- created_at
- updated_at

---

### Education

Represents the educational background of a user.

Attributes

- id (PK)
- user_id (FK → User.id)
- degree
- field_of_study
- institution
- start_date
- end_date

---

### Experience

Represents the professional work experience of a user.

Attributes

- id (PK)
- user_id (FK → User.id)
- job_title
- company
- description
- start_date
- end_date

---

### Skill

Represents a technical or professional skill that can be associated with users and jobs.

Attributes

- id (PK)
- name
- description

---

### UserSkill

Associative entity connecting users with their skills.

Attributes

- user_id (PK, FK → User.id)
- skill_id (PK, FK → Skill.id)
- proficiency

The composite primary key is

(user_id, skill_id)

This prevents the same skill from being assigned more than once to the same user.

---

### Job

Represents a job opportunity available in the system.

Attributes

- id (PK)
- title
- company
- description
- location
- employment_type
- created_at
- updated_at

---

### JobSkill

Associative entity connecting jobs with their required skills.

Attributes

- job_id (PK, FK → Job.id)
- skill_id (PK, FK → Skill.id)
- required_level
- is_required

The composite primary key is

(job_id, skill_id)

This prevents the same skill from being added more than once to the same job.

---

## 3. Relationships

### User – Education

One User can have multiple Education records.

Cardinality

User 1  N Education

---

### User – Experience

One User can have multiple Experience records.

Cardinality

User 1  N Experience

---

### User – Skill

A User can have multiple Skills, and a Skill can belong to multiple Users.

Cardinality

User N  M Skill

This relationship is implemented through the UserSkill associative entity.

---

### Job – Skill

A Job can require multiple Skills, and a Skill can be required by multiple Jobs.

Cardinality

Job N  M Skill

This relationship is implemented through the JobSkill associative entity.

---

## 4. Relationship Summary

```text
User
 
  1N
 
 +------ Education

User
 
  1N
 
 +------ Experience

User
 
  1N
 
 +------ UserSkill ------ N1 ------ Skill

Job
 
  1N
 
 +------ JobSkill ------ N1 ------ Skill

The UserSkill and JobSkill entities transform the many-to-many relationships into relational database structures.

5. Foreign Key Constraints

The following foreign key constraints are defined

Education.user_id references User.id
Experience.user_id references User.id
UserSkill.user_id references User.id
UserSkill.skill_id references Skill.id
JobSkill.job_id references Job.id
JobSkill.skill_id references Skill.id

Foreign key constraints ensure referential integrity between related entities.

6. Primary Key Constraints

Each main entity has a unique primary key

User.id
Education.id
Experience.id
Skill.id
Job.id

The associative entities use composite primary keys

UserSkill (user_id, skill_id)
JobSkill (job_id, skill_id)
7. Recommendation Data

Recommendation results are not stored as a permanent database entity in the initial design.

Instead, compatibility scores, matched skills, missing skills, and recommendation rankings are calculated dynamically by the application based on

User profile information
User skills
Job requirements
Skill proficiency
Matching algorithms

The calculated results are returned through the recommendation API.

This approach avoids storing potentially outdated recommendation results and allows recommendations to be recalculated when user or job data changes.