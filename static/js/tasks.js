// Frontend JS for Task Manager — moved out of template
document.addEventListener('DOMContentLoaded', () => {
  const apiBase = '/api/v1/tasks';
  const taskList = document.getElementById('task-list');
  const form = document.getElementById('task-form');
  const titleInput = document.getElementById('title');
  const descriptionInput = document.getElementById('description');
  const errorContainer = document.getElementById('error-container');

  function showError(msg) {
    if (!errorContainer) return;
    errorContainer.textContent = msg;
    errorContainer.style.display = 'block';
    setTimeout(() => { errorContainer.style.display = 'none'; }, 4000);
  }

  async function loadTasks() {
    try {
      const res = await fetch(apiBase);
      if (!res.ok) throw new Error(`Failed to load tasks: ${res.status}`);
      const tasks = await res.json();
      renderTasks(tasks);
    } catch (err) {
      showError(err.message);
    }
  }

  function renderTasks(tasks) {
    taskList.innerHTML = '';
    tasks.forEach(task => {
      const li = document.createElement('li');
      li.className = 'task-item' + (task.completed ? ' completed' : '');

      const content = document.createElement('div');
      content.className = 'task-content';

      const title = document.createElement('div');
      title.className = 'task-title';
      title.textContent = task.title;

      const desc = document.createElement('div');
      desc.className = 'task-description';
      desc.textContent = task.description || '';

      const meta = document.createElement('div');
      meta.className = 'task-meta';
      meta.textContent = `Created: ${new Date(task.created_at).toLocaleString()}`;

      content.appendChild(title);
      content.appendChild(desc);
      content.appendChild(meta);

      const actions = document.createElement('div');
      actions.className = 'task-actions';

      const completeBtn = document.createElement('button');
      completeBtn.className = 'btn btn-complete';
      completeBtn.textContent = task.completed ? 'Uncomplete' : 'Complete';
      completeBtn.onclick = async () => {
        try {
          await fetch(`${apiBase}/${task.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completed: !task.completed })
          });
          loadTasks();
        } catch (err) { showError(err.message); }
      };

      const editBtn = document.createElement('button');
      editBtn.className = 'btn btn-edit';
      editBtn.textContent = 'Edit';
      editBtn.onclick = async () => {
        const newTitle = prompt('Edit task title', task.title);
        if (!newTitle) return;
        try {
          await fetch(`${apiBase}/${task.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: newTitle })
          });
          loadTasks();
        } catch (err) { showError(err.message); }
      };

      const delBtn = document.createElement('button');
      delBtn.className = 'btn btn-delete';
      delBtn.textContent = 'Delete';
      delBtn.onclick = async () => {
        if (!confirm('Delete this task?')) return;
        try {
          await fetch(`${apiBase}/${task.id}`, { method: 'DELETE' });
          loadTasks();
        } catch (err) { showError(err.message); }
      };

      actions.appendChild(completeBtn);
      actions.appendChild(editBtn);
      actions.appendChild(delBtn);

      li.appendChild(content);
      li.appendChild(actions);
      taskList.appendChild(li);
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      title: titleInput.value.trim(),
      description: descriptionInput.value.trim() || null
    };
    if (!payload.title) { showError('Title is required'); return; }
    try {
      const res = await fetch(apiBase, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(`Failed to create task: ${res.status}`);
      titleInput.value = '';
      descriptionInput.value = '';
      loadTasks();
    } catch (err) { showError(err.message); }
  });

  // Initial load
  loadTasks();
});
// Task management functionality
class TaskManager {
    constructor() {
        this.taskList = document.getElementById('task-list');
        this.taskForm = document.getElementById('task-form');
        this.errorContainer = document.getElementById('error-container');
        
        this.setupEventListeners();
        this.loadTasks();
    }
    
    setupEventListeners() {
        this.taskForm.addEventListener('submit', (e) => this.handleSubmit(e));
    }
    
    async loadTasks() {
        try {
            const response = await fetch('/api/v1/tasks');
            const tasks = await response.json();
            
            this.taskList.innerHTML = '';
            tasks.forEach(task => this.renderTask(task));
        } catch (error) {
            this.showError('Failed to load tasks');
        }
    }
    
    async handleSubmit(event) {
        event.preventDefault();
        
        const formData = new FormData(this.taskForm);
        const taskData = {
            title: formData.get('title'),
            description: formData.get('description')
        };
        
        try {
            const response = await fetch('/api/v1/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(taskData)
            });
            
            if (!response.ok) {
                throw new Error('Failed to create task');
            }
            
            const task = await response.json();
            this.renderTask(task);
            this.taskForm.reset();
        } catch (error) {
            this.showError('Failed to create task');
        }
    }
    
    async handleDelete(taskId) {
        try {
            const response = await fetch(`/api/v1/tasks/${taskId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Failed to delete task');
            }
            
            document.getElementById(`task-${taskId}`).remove();
        } catch (error) {
            this.showError('Failed to delete task');
        }
    }
    
    async handleComplete(taskId, completed) {
        try {
            const response = await fetch(`/api/v1/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ completed: !completed })
            });
            
            if (!response.ok) {
                throw new Error('Failed to update task');
            }
            
            const task = await response.json();
            const taskElement = document.getElementById(`task-${taskId}`);
            taskElement.outerHTML = this.createTaskHTML(task);
        } catch (error) {
            this.showError('Failed to update task');
        }
    }
    
    renderTask(task) {
        const taskHTML = this.createTaskHTML(task);
        this.taskList.insertAdjacentHTML('beforeend', taskHTML);
    }
    
    createTaskHTML(task) {
        return `
            <li id="task-${task.id}" class="task-item ${task.completed ? 'completed' : ''}">
                <div class="task-content">
                    <div class="task-title">${this.escapeHtml(task.title)}</div>
                    ${task.description ? `<div class="task-description">${this.escapeHtml(task.description)}</div>` : ''}
                    <div class="task-meta">Created: ${new Date(task.created_at).toLocaleString()}</div>
                </div>
                <div class="task-actions">
                    <button class="btn btn-complete" onclick="taskManager.handleComplete(${task.id}, ${task.completed})">
                        ${task.completed ? 'Uncomplete' : 'Complete'}
                    </button>
                    <button class="btn btn-delete" onclick="taskManager.handleDelete(${task.id})">Delete</button>
                </div>
            </li>
        `;
    }
    
    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
    
    showError(message) {
        this.errorContainer.textContent = message;
        this.errorContainer.style.display = 'block';
        setTimeout(() => {
            this.errorContainer.style.display = 'none';
        }, 3000);
    }
}

// Initialize task manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.taskManager = new TaskManager();
});