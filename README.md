# ITCC14 API Project — MindEase: Mental Health Support Platform

## 👥 Members
> All team members with GitHub profile links. (Must use full name or surname for grading)

- [Reyes, Benjamin Thomas Emiliani](https://github.com/BenjaminThomasEmilianiReyes)
- [Realisan, James Marco G.](https://github.com/jamesrealisan)
- [Mocsana, Mohammad Yusuf T.](https://github.com/MoyMocsana)
- [paulagwynzellelabadan](https://github.com/paulagwynzellelabadan)
---

## 🧠 Project Title: MindEase – Mental Health Support Platform

### 📖 Context
MindEase is a web-based platform designed to promote student mental well-being through **self-assessment tools**, **relaxation resources**, and **confidential support channels**.  
While most mental health platforms focus on front-end design, MindEase emphasizes a **robust backend architecture** to ensure security, data consistency, and seamless integration across all modules.

---

### ⚙️ Problems / Needs Analysis
Current student mental health support systems rely on **manual counseling records** and **disconnected communication tools**, resulting in fragmented data and privacy risks.  
Without a **centralized backend**, schools cannot track trends in student well-being or securely manage counselor–student interactions.  
MindEase solves this by providing a **Flask-based REST API** with a **MySQL database** backend that enables integration with future apps or institutional dashboards.

---

### 💡 Solution Overview
MindEase’s backend architecture provides scalable and secure data management to support multiple front-end clients (web and mobile).

**Key Technical Features:**
- **Framework:** Flask (Python)
- **Authentication:** Token-based user access control
- **API Endpoints:**
  - `POST /api/register` – Register new users with validation & password hashing  
  - `POST /api/login` – Authenticate and generate access token  
  - `GET /api/selfcheck` – Retrieve self-assessment questions  
  - `POST /api/results` – Submit self-assessment results  
  - `GET /api/moods`, `POST /api/moods` – Log and view mood entries  
  - `POST /api/forum` – Counselor-student forum endpoint  

**Database Design:**
| Table | Fields |
|--------|--------|
| users | user_id, name, role, email, password_hash |
| mood_entries | entry_id, user_id, mood, date_logged |
| assessments | assessment_id, user_id, score, feedback, date_taken |
| forum | forum_id, sender_id, forum_role, content, timestamp |

All tables are linked using **foreign keys** to maintain data integrity.

---

## ## My Project Milestones

### 🗓 *Milestone 1 (Nov Week 1): Project Proposal & Introduction*

*What we'll do:*  
Finalize the “MindEase” project topic, define the problem statement and data models, and create the initial API documentation using Postman.

*Deliverables:*  
- Updated README.md with Problem Statement and Data Models  
- ITCC14 Project Document (Chapters 1 & 2)  
- Initial **Postman collection (MindEase_API.postman_collection.json)** listing all planned endpoints  

*Checklist:*  
- [x] Hold team meeting to finalize topic  
- [x] Write Problem Statement & Data Models  
- [x] Create Postman API collection (initial endpoints)  
- [x] Complete Chapters 1–2 of Project Doc  
- [x] Commit and push all files  

---

### 🗓 *Milestone 2 (Nov Week 2): Backend Setup & Initial Endpoints*

*What we'll do:*  
Set up the Flask backend with virtual environment and dependencies.  
Implement register and login endpoints, connect to a database, and document working endpoints in Postman.

*Deliverables:*  
- Flask server running locally  
- Working */register* and */login* endpoints  
- Updated Postman API collection with working examples  
- Chapter 3 (System Design) of ITCC14 Project Document  

*Checklist:*  
- [x] Initialize repository and virtual environment  
- [x] Install Flask, SQLAlchemy, Bcrypt, JWT  
- [x] Implement /register and /login  
- [x] Update Postman documentation  
- [x] Write Chapter 3  
- [x] Push commits to GitHub  

---

### 🗓 *Milestone 3 (Nov Week 3): Full Backend API Implementation*

*What we'll do:*  
Complete all CRUD endpoints (moods, assessments, forum).  
Add input validation, error handling, and seed sample data for demo.  
Update and validate the Postman collection to match actual responses.

*Deliverables:*  
- Full CRUD API completed  
- Consistent error handling and validation  
- Seed data for testing  
- Updated Postman collection validated against working API  

*Checklist:*  
- [x] Implement CRUD endpoints for all resources  
- [x] Add error handling (400/404)  
- [x] Create seed script for sample data  
- [x] Validate Postman API responses  
- [x] Push all backend updates  

---

### 🗓 *Milestone 4 (Nov Week 4): Frontend Integration*

*What we'll do:*  
Develop a simple frontend (HTML, JS, or React) that interacts with the API to display and create mood entries.  
Handle loading, errors, and prepare demo instructions.

*Deliverables:*  
- Frontend integrated with backend  
- User interface for mood logging and viewing  
- Instructions in README for running frontend and backend  

*Checklist:*  
- [ ] Frontend lists mood entries  
- [ ] Frontend can create new moods  
- [ ] Frontend handles loading/errors  
- [ ] Document run instructions in README  

---

### 🗓 *Milestone 5 (Optional, Dec Week 1): Docker Containerization*

*What we'll do:*  
Containerize the backend for easier setup using Docker.  

*Deliverables:*  
- Working Dockerfile  
- Documentation for building and running container  

*Checklist:*  
- [ ] Dockerfile builds successfully  
- [ ] App runs in container  
- [ ] Docker instructions in README  

---

### 🏁 *Final (Dec Week 2): Presentation & Demo*

*What we'll do:*  
Present the full MindEase system—backend API, frontend integration, and project documentation.  

*Deliverables:*  
- Presentation slides  
- Live API + frontend demo  
- Seed data for testing  

*Checklist:*  
- [ ] Slides completed  
- [ ] Demo setup ready  
- [ ] Repository finalized  

---

## 📎 Repository Link
*(To be added after pushing to GitHub)*  

Example: [https://github.com/BenjaminReyes/itcc14-api-project-mindease](https://github.com/BenjaminThomasEmilianiReyes/itcc14-api-project-mindease)

