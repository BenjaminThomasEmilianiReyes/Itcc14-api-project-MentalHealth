# ITCC14 API Project — MindEase: Mental Health Support Platform

## 👥 Members
> All team members with GitHub profile links. (Must use full name or surname for grading)

- [Reyes, Benjamin Thomas Emiliani](https://github.com/BenjaminThomasEmilianiReyes)
- [Realisan, James Marco G.](https://github.com/jamesrealisan)

---

## 🧠 Project Title: MindEase – Mental Health Support Platform

### 📖 Context
MindEase is a web-based platform designed to promote student mental well-being through **self-assessment tools**, **relaxation resources**, and **confidential support channels**.  
While most mental health platforms focus on front-end design, MindEase emphasizes a **robust backend architecture** to ensure security, data consistency, and seamless integration across all modules.

---

### ⚙️ Problems / Needs Analysis
Current student mental health support systems rely on **manual counseling records** and **disconnected communication tools**, resulting in fragmented data and privacy risks.  
Without a **centralized backend**, schools cannot track trends in student well-being or securely manage counselor–student interactions.  
MindEase solves this by providing a **Flask-based RESTful API** with a **MySQL database** backend that enables integration with future apps or institutional dashboards.

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

### 🗓 Milestone 1 (Nov Week 1): Project Proposal & API Draft
**What we'll do:**  
Finalize our project topic "MindEase," write the problem statement, define data models, and create an initial API documentation outline.

**Deliverables:**  
- Updated `README.md` with Problem Statement and Data Models  
- ITCC14 Project Document (Chapters 1 & 2)  
- Initial `api.yaml` file listing endpoints  

**Checklist:**  
- [ ] Hold team meeting to finalize topic  
- [ ] Write Problem Statement & Data Models  
- [ ] Create `api.yaml` (initial API endpoints)  
- [ ] Complete Chapters 1–2 of Project Doc  
- [ ] Commit and push all files  

---

### 🗓 Milestone 2 (Nov Week 2): Backend Setup & Initial Endpoints
**What we'll do:**  
Set up Flask and MySQL. Implement basic `register` and `login` endpoints. Begin OpenAPI documentation and start Chapter 3 of the project document.

**Deliverables:**  
- Flask backend initialized  
- Working `/register` and `/login` endpoints  
- Updated API documentation (Swagger or YAML)  
- Chapter 3 (System Design)  

**Checklist:**  
- [ ] Initialize repo and virtualenv  
- [ ] Install Flask and dependencies  
- [ ] Implement register/login endpoints  
- [ ] Document endpoints with SwaggerUI  
- [ ] Push updates to GitHub  

---

### 🗓 Milestone 3 (Nov Week 3): Complete Backend API
**What we'll do:**  
Implement all CRUD operations and finalize API routes for `moods`, `assessments`, and `forum`. Add validation and error handling.

**Deliverables:**  
- Fully functional CRUD API  
- Error handling and validation  
- Seed data for demo  
- Validated OpenAPI spec  

**Checklist:**  
- [ ] All endpoints completed  
- [ ] Input validation added  
- [ ] Seed data created  
- [ ] OpenAPI validated  
- [ ] Push to GitHub  

---

### 🗓 Milestone 4 (Nov Week 4): Frontend Integration
**What we'll do:**  
Create a simple web interface that interacts with the API to log moods and view results. Prepare for presentation.

**Deliverables:**  
- Frontend connected to backend  
- Demo-ready interface for mood tracking  
- Instructions for running app  

**Checklist:**  
- [ ] Frontend lists and creates moods  
- [ ] Handles loading/errors  
- [ ] Document run steps in README  

---

### 🗓 Milestone 5 (Optional, Dec Week 1): Docker Containerization
**What we'll do:**  
Containerize the backend for consistency and easier deployment.

**Deliverables:**  
- Working Dockerfile  
- README instructions for Docker setup  

**Checklist:**  
- [ ] Dockerfile builds successfully  
- [ ] App runs in container  
- [ ] Document Docker commands  

---

### 🏁 Final (Dec Week 2): Presentation & Demo
**What we'll do:**  
Present the full MindEase project—showing the live API, frontend, and database integration. Explain system purpose and flow.

**Deliverables:**  
- Final slides  
- Live demo / backup video  
- Complete GitHub repo  

**Checklist:**  
- [ ] Slides ready  
- [ ] Demo environment prepared  
- [ ] Repository finalized  

---

## 📎 Repository Link
> *(To be added after pushing to GitHub)*  
Example: [https://github.com/BenjaminReyes/itcc14-api-project-mindease](https://github.com/BenjaminReyes/itcc14-api-project-mindease)

