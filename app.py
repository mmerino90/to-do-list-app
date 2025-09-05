from flask import Flask, request, jsonify, render_template, redirect, url_for
import json, os

app = Flask(__name__)
DATA_FILE = "tasks.json"

# --- Helper functions ---
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# --- Routes ---
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    tasks = load_tasks()
    new_task = request.json
    new_task["id"] = len(tasks) + 1
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return {"error": "Task not found"}, 404
    task.update(request.json)
    save_tasks(tasks)
    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return {"error": "Task not found"}, 404
    tasks.remove(task)
    save_tasks(tasks)
    return jsonify(task)

@app.route("/")
def home():
    # Redirect to frontend by default
    return redirect(url_for("ui"))

@app.route("/ui")
def ui():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
