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
      const response = await res.json();
      // Extract tasks from response wrapper
      const tasks = response.data || response || [];
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
    // prevent duplicate submissions by disabling the submit button while request is inflight
    const submitBtn = form.querySelector('button[type="submit"]');
    if (form.dataset.submitting === '1') return;
    form.dataset.submitting = '1';
    if (submitBtn) submitBtn.disabled = true;
    try {
      const res = await fetch(apiBase, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(`Failed to create task: ${res.status}`);
      titleInput.value = '';
      descriptionInput.value = '';
      await loadTasks();
    } catch (err) { showError(err.message); }
    finally {
      form.dataset.submitting = '0';
      if (submitBtn) submitBtn.disabled = false;
    }
  });

  // Initial load
  loadTasks();
});
// End: Single front-end implementation retained to avoid duplicate handlers