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