# 🧠 Real-Time Collaborative Workspace Backend

A production-grade backend service for a real-time collaborative developer workspace, built using **Django**, **Django REST Framework**, **Django Channels**, **Redis**, **Celery**, and **JWT-based authentication**.

The system supports:
- Secure authentication
- Project & workspace management
- Real-time collaboration using WebSockets
- Asynchronous background job processing
- Cloud-ready, scalable architecture

---

## 📐 Architecture Diagram

```mermaid
graph TD
    Client["Client (Browser / Postman)"]

    Client -->|"REST APIs (HTTP)"| DRF["Django REST Framework"]
    DRF --> Auth["JWT Authentication"]
    DRF --> Projects["Projects & Workspaces"]
    DRF --> Jobs["Job Submission APIs"]

    Client -->|"WebSocket (ASGI)"| Daphne["Daphne ASGI Server"]
    Daphne --> Channels["Django Channels"]
    Channels --> Consumers["Workspace Consumers"]
    Consumers --> WSAuth["JWT WebSocket Authentication"]

    Channels -->|"Pub / Sub"| Redis["Redis"]
    Redis --> ChannelLayer["Channels Layer"]
    Redis --> Broker["Celery Broker & Results"]

    Broker --> Celery["Celery Workers"]
    Celery --> Retry["Retry Logic"]
    Celery --> Background["Background Processing"]

```
---

## 🧰 Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **WebSockets**: Django Channels + Daphne
- **Message Broker / Cache**: Redis
- **Async Jobs**: Celery
- **Database**: SQLite (development), PostgreSQL recommended for production
- **API Docs**: Swagger (drf-yasg)
- **Deployment Ready**: Docker-compatible services

---

## 🚀 Setup & Run Instructions

### 1️⃣ Prerequisites

- Python **3.10+**
- Redis (Docker recommended)
- Virtual environment support

---

### 2️⃣ Clone Repository & Setup Environment

```bash
git clone <your-repository-url>
cd collab_backend

python -m venv my_env
my_env\Scripts\activate   # Windows
# source my_env/bin/activate  # Linux / macOS

pip install -r requirements.txt

```

### 3️⃣ Start Redis

Using Docker:
```bash

docker run -d -p 6379:6379 redis

```
Verify Redis:
```bash
redis-cli ping
# PONG
```
### 4️⃣ Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
### 5️⃣ Start Django (ASGI via Daphne)
```bash
daphne -b 127.0.0.1 -p 8000 collab_backend.asgi:application
```

Note: Daphne is required for reliable WebSocket support.

### 6️⃣ Start Celery Worker

Open a new terminal (activate virtualenv first):
```bash
celery -A collab_backend worker --loglevel=info
```
## 🔐 Authentication (JWT)
Login Endpoint
```bash
POST /api/auth/login/

```

Request Body:
```bash
{
  "email": "user@example.com",
  "password": "password"
}

```
Response:
```bash
{
  "access": "<JWT_ACCESS_TOKEN>",
  "refresh": "<JWT_REFRESH_TOKEN>"
}

```
Use the access token for all authenticated APIs.

## 📁 Project & Workspace APIs

- Create, update, delete projects

- Manage workspaces

- Assign roles (Owner / Collaborator / Viewer)

- Protected using JWT & role-based permissions

## 📘 API Documentation

This project uses **Swagger UI (drf-yasg)** to provide interactive, self-documenting REST APIs.

Swagger allows you to:
- Explore all available endpoints
- Authenticate using JWT Bearer tokens
- Execute API requests directly from the browser
- Validate request/response schemas

Swagger UI:
Once the server is running, open:
```bash

http://127.0.0.1:8000/swagger/
```

---

## 🔐 Authentication in Swagger (JWT Bearer)

### Step 1: Generate JWT Token

Use the **Login API**:

**Endpoint**
```bash

POST /api/auth/login/
```

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "password"
}
```
Response
```json
{
  "access": "<JWT_ACCESS_TOKEN>",
  "refresh": "<JWT_REFRESH_TOKEN>"
}
```
Step 2: Authorize in Swagger UI

-Click the Authorize 🔓 button (top-right)

-In the Bearer field, enter:
```json
Bearer <JWT_ACCESS_TOKEN>
```
-Click Authorize

-Close the popup

All protected APIs are now authenticated.

## 📁 Project & Workspace APIs (Swagger)
- Create Project

- Swagger Path
```bash
POST /api/projects/projects/
```

- Request Body
```bash
{
  "name": "My Project",
  "description": "Demo project"
}
```

- Expected Response
```bash
{
  "id": 1,
  "name": "My Project",
  "description": "Demo project",
  "created_at": "2025-12-26T17:23:38Z",
  "owner": 2
}
```
#### List Projects

Swagger Path
```bash
GET /api/projects/projects/

```
Returns all projects owned or accessible by the authenticated user.

#### Update Project

Swagger Path
```bash
PUT /api/projects/projects/{project_id}/

```
Modify project name or description.

#### Delete Project

Swagger Path
```bash
DELETE /api/projects/projects/{project_id}/
```

Deletes a project (Owner only).

### ⚙️ Job APIs (Swagger + Celery)
#### Submit Background Job

Swagger Path
```bash
POST /api/jobs/submit/
```

Request Body
```bash
{
  "code": "print('Hello World')",
  "language": "python"
}
```

Response
```
{
  "message": "Job queued",
  "job_id": "job_123"
}
```
### 🔴 Real-Time Collaboration (WebSockets)
WebSocket Endpoint
```bash
ws://127.0.0.1:8000/ws/workspaces/<workspace_id>/?token=<JWT_ACCESS_TOKEN>
```
### Authentication

- JWT is passed during WebSocket handshake

- Custom middleware validates token and attaches user to scope

### 🧪 WebSocket Testing (Browser Console)

Open Chrome DevTools → Console and run:
```bash
const token = "YOUR_JWT_ACCESS_TOKEN";

const socket = new WebSocket(
  `ws://127.0.0.1:8000/ws/workspaces/1/?token=${token}`
);

socket.onopen = () => {
    console.log("✅ CONNECTED");

    socket.send(JSON.stringify({
        event: "file_change",
        payload: {
            file: "test.js",
            content: "console.log('hello world')"
        }
    }));
};

socket.onmessage = (e) => {
    console.log("📩 MESSAGE RECEIVED:", JSON.parse(e.data));
};

socket.onerror = (e) => {
    console.error("❌ ERROR:", e);
};
```
Expected Output
```bash
✅ CONNECTED
📩 MESSAGE RECEIVED: {
  event: "file_change",
  payload: {...},
  user: "user@example.com"
}
```
## ⚙️ Asynchronous Job Processing (Celery)
Job Submission API
```bash
POST /api/jobs/submit/
Authorization: Bearer <JWT_ACCESS_TOKEN>
```

Request Body:
```bash
{
  "code": "print('Hello World')",
  "language": "python"
}
```
Background Processing Flow

- API accepts job request

- Job is queued to Celery

- Worker processes task asynchronously

- Retry logic handles transient failures

- Job result is logged / persisted

Retry Logic
```bash
@shared_task(bind=True, max_retries=3)
```

- Retries up to 3 times

- Delay between retries

- Idempotent job execution

## 🧪 Testing Summary

| Feature         | How to Test                  |
| --------------- | ---------------------------- |
| Authentication  | Postman → `/api/auth/login/` |
| REST APIs       | Swagger UI / Postman         |
| WebSockets      | Browser Console              |
| Background Jobs | Postman + Celery logs        |
| Retries         | Simulated task failures      |
| Rate Limiting   | Exceed request thresholds    |


## 🚀 Deployment Instructions

This project is designed to be cloud-ready and horizontally scalable.

### 🔧 Local Development Deployment

#### Required Services:

- Django (ASGI)

- Redis

- Celery Worker

#### Run Order:

- Start Redis

- Start Django via Daphne

- Start Celery worker
```bash
docker run -d -p 6379:6379 redis
daphne -b 0.0.0.0 -p 8000 collab_backend.asgi:application
celery -A collab_backend worker --loglevel=info

```
### ☁️ Production Deployment (Recommended)

#### Suggested Stack:

- ASGI Server: Daphne / Uvicorn

- Reverse Proxy: Nginx

- Database: PostgreSQL

- Cache & Broker: Redis

- Workers: Multiple Celery workers

#### Production Notes:

- Replace SQLite with PostgreSQL

- Store secrets using environment variables

- Enable HTTPS (WSS for WebSockets)

- Use process manager (systemd / supervisor)

- Scale Daphne & Celery independently

### 🐳 Docker Deployment (Optional)

#### Services can be containerized using:

- Django + Daphne container

- Redis container

- Celery worker container

#### This enables:

- Horizontal scaling

- CI/CD integration

- Cloud deployment (AWS / GCP / Azure)


## ⚖️ Design Decisions & Trade-offs
### Django + Channels

-Unified backend ecosystem

- Native ASGI support

- Clean WebSocket integration

### Daphne

- Reliable ASGI server

- Stable WebSocket handling on Windows

- Production-ready

### Redis

- Channel layer pub/sub

- Celery broker & result backend

- Enables horizontal scaling

### SQLite

- Fast local development

#### PostgreSQL recommended for production environments

## 📈 Scalability Considerations

- Horizontal scaling via Redis channel layers

- Stateless WebSocket consumers

- Multiple Daphne instances behind load balancer

- Independent Celery worker scaling

- JWT-based auth (no session stickiness)

- Database can be upgraded to PostgreSQL/MySQL

## 🔍 Security & Observability

- JWT expiration & refresh flow

- Input validation via serializers

- ORM-based SQL injection protection

- API rate limiting (DRF throttles)

- Environment-based secrets

- Structured logging

## 🏁 Conclusion

This backend demonstrates a production-grade architecture with real-time communication, async processing, and secure APIs.
All major features were tested locally using Daphne, Redis, Celery workers, Swagger, Postman, and browser-based WebSocket clients.
