📝 To-Do List App

A minimal full-stack To-Do List application built with Flask (Python).

This project demonstrates:

CRUD functionality (Create, Read, Update, Delete)

Persistent storage using tasks.json

RESTful API endpoints at /tasks

A clean frontend UI at /ui (the homepage / redirects here)

It was developed as part of an academic assignment to illustrate how a minimal application can later be adapted into a DevOps pipeline.

🚀 Setup Instructions
1. Clone this repository
git clone https://github.com/mmerino90/to-do-list-app.git
cd to-do-list-app

2. Create and activate a virtual environment (Windows PowerShell)
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the application
python app.py

5. Open in browser

Frontend UI: http://127.0.0.1:5000/

API (raw JSON): http://127.0.0.1:5000/tasks

🧭 Usage
✅ Using the Frontend (UI)

Add a task with the input field and Add button.

Update a task with the Edit button.

Remove a task with the Delete button.

Tasks are stored in tasks.json and persist between sessions.

✅ Using the API (PowerShell examples)

Add a task

curl -Method POST -Uri "http://127.0.0.1:5000/tasks" `
     -Body '{"title":"Buy milk"}' -ContentType "application/json"


Get all tasks

curl http://127.0.0.1:5000/tasks


Update task #1

curl -Method PUT -Uri "http://127.0.0.1:5000/tasks/1" `
     -Body '{"title":"Buy almond milk"}' -ContentType "application/json"


Delete task #1

curl -Method DELETE -Uri "http://127.0.0.1:5000/tasks/1"


👉 On macOS/Linux or Git Bash, use the curl -X format instead:

curl -X POST -H "Content-Type: application/json" \
     -d '{"title":"Buy milk"}' http://127.0.0.1:5000/tasks

📂 Project Structure
to-do-list-app/
│── app.py               # Flask backend (API + routes + redirect to UI)
│── tasks.json           # Persistent storage file
│── requirements.txt     # Python dependencies
│── README.md            # Documentation
│── templates/
│    └── index.html      # Frontend (HTML + CSS + JS)
│── docs/
     └── architecture.png   # Architecture diagram (for the report)

🔌 API Endpoints

GET /tasks → Retrieve all tasks

POST /tasks → Create a new task (JSON body: {"title": "..."})

PUT /tasks/<id> → Update a task by ID

DELETE /tasks/<id> → Delete a task by ID

Task format:

{ "id": 1, "title": "Buy milk" }

🛠 Troubleshooting

ModuleNotFoundError: No module named 'flask'
Make sure the venv is activated and run:

pip install -r requirements.txt


tasks.json JSON decode error (empty or corrupted file)
Reset the file content to:

[]


Port already in use
Run Flask on a different port:

$env:FLASK_RUN_PORT=5001
python app.py

📌 Notes for Scaling (DevOps Context)

Replace tasks.json with a proper database (PostgreSQL, MySQL, or MongoDB).

Containerize with Docker for consistent deployment.

Add CI/CD pipelines (GitHub Actions, Jenkins) for automated testing and deployment.

Use monitoring and logging (Prometheus, Grafana, ELK stack) in production.

Implement authentication & authorization for multi-user support.