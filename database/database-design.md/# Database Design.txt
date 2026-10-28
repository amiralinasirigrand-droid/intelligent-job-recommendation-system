# Database Design

## 1. Database Overview

The system will use PostgreSQL as its relational database management system.

The database will store user information, education, work experience, skills, job opportunities, and the relationships required for job matching and recommendation.

The initial database design consists of the following main tables

- User
- Education
- Experience
- Skill
- UserSkill
- Job
- JobSkill

A separate Profile table will not be used in the initial design. A user's profile will be represented through the user's account information together with their education, work experience, and skills.

---

## 2. User

Stores user account and basic personal information.

 Attribute  Description 
------
 id  Primary key 
 email  User email address 
 password_hash  Securely stored password hash 
 first_name  User first name 
 last_name  User last name 
 created_at  Account creation timestamp 
 updated_at  Last update timestamp 

---

## 3. Education

Stores education records associated with users.

 Attribute  Description 
------
 id  Primary key 
 user_id  Foreign key referencing User 
 degree  Degree or qualification 
 field_of_study  Field of study 
 institution  Educational institution 
 start_date  Start date 
 end_date  End date 

Relationship

User 1N Education

---

## 4. Experience

Stores work experience records associated with users.

 Attribute  Description 
------
 id  Primary key 
 user_id  Foreign key referencing User 
 job_title  Position or job title 
 company  Company name 
 description  Description of the experience 
 start_date  Start date 
 end_date  End date 

Relationship

User 1N Experience

---

## 5. Skill

Stores the skills used by the system.

 Attribute  Description 
------
 id  Primary key 
 name  Skill name 
 description  Skill description 

---

## 6. UserSkill

Associates users with their skills.

 Attribute  Description 
------
 user_id  Foreign key referencing User 
 skill_id  Foreign key referencing Skill 
 proficiency  User's proficiency level 

Relationship

User NM Skill through UserSkill.

---

## 7. Job

Stores job opportunities.

 Attribute  Description 
------
 id  Primary key 
 title  Job title 
 company  Company name 
 description  Job description 
 location  Job location 
 employment_type  Type of employment 
 created_at  Creation timestamp 
 updated_at  Last update timestamp 

---

## 8. JobSkill

Associates jobs with their required skills.

 Attribute  Description 
------
 job_id  Foreign key referencing Job 
 skill_id  Foreign key referencing Skill 
 required_level  Required proficiency level 
 is_required  Indicates whether the skill is mandatory 

Relationship

Job NM Skill through JobSkill.

---

## 9. Main Relationships

The main database relationships are

User 1N Education

User 1N Experience

User NM Skill through UserSkill

Job NM Skill through JobSkill

---

## 10. Recommendation Data

Compatibility scores and recommendation results will initially be calculated dynamically by the matching and recommendation components rather than being stored as permanent database records.

This decision may be revisited during implementation and performance evaluation if required.
## 11. Primary Key Constraints

The UserSkill table will use a composite primary key consisting of:

(user_id, skill_id)

This prevents duplicate associations between the same user and skill.

The JobSkill table will use a composite primary key consisting of:

(job_id, skill_id)

This prevents duplicate associations between the same job and skill.