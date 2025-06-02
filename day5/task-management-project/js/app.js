// This file contains the JavaScript code that implements the functionality of the task management system.

document.addEventListener('DOMContentLoaded', function() {
    const taskInput = document.getElementById('taskInput');
    const addTaskButton = document.getElementById('addTaskButton');
    const taskList = document.getElementById('taskList');
    const filterTasks = document.getElementById('filterTasks');
    const searchBar = document.getElementById('searchBar');
    const clearCompletedButton = document.getElementById('clearCompletedButton');

    // --- Local Storage Helpers ---
    function getTasks() {
        return JSON.parse(localStorage.getItem('tasks') || '[]');
    }
    function saveTasks(tasks) {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }

    // --- Render Tasks ---
    function renderTasks(tasks) {
        taskList.innerHTML = '';
        tasks.forEach((task, idx) => {
            const li = document.createElement('li');
            li.className = task.completed ? 'completed' : 'pending';

            // Checkbox
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.className = 'task-checkbox';
            checkbox.checked = task.completed;
            checkbox.onchange = function() {
                tasks[idx].completed = checkbox.checked;
                saveTasks(tasks);
                renderTasks(tasks);
            };

            // Task text
            const span = document.createElement('span');
            span.textContent = task.text;

            // Remove button
            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'Remove';
            removeBtn.className = 'remove-btn';
            removeBtn.onclick = function(e) {
                e.stopPropagation();
                tasks.splice(idx, 1);
                saveTasks(tasks);
                renderTasks(tasks);
            };

            li.appendChild(checkbox);
            li.appendChild(span);
            li.appendChild(removeBtn);
            taskList.appendChild(li);
        });
    }

    // --- Initial Load ---
    let tasks = getTasks();
    renderTasks(tasks);

    // --- Add Task ---
    addTaskButton.onclick = function() {
        const taskText = taskInput.value.trim();
        if (taskText) {
            tasks.push({ text: taskText, completed: false });
            saveTasks(tasks);
            renderTasks(tasks);
            taskInput.value = '';
        }
    };

    // --- Filter Tasks ---
    filterTasks.onchange = function() {
        let filtered = tasks;
        if (filterTasks.value === 'pending') {
            filtered = tasks.filter(t => !t.completed);
        } else if (filterTasks.value === 'completed') {
            filtered = tasks.filter(t => t.completed);
        }
        renderTasks(filtered);
    };

    // --- Search Tasks ---
    searchBar.oninput = function() {
        const query = searchBar.value.toLowerCase();
        const filtered = tasks.filter(t => t.text.toLowerCase().includes(query));
        renderTasks(filtered);
    };

    // --- Clear Completed Tasks ---
    clearCompletedButton.onclick = function() {
        const completedCount = tasks.filter(t => t.completed).length;
        if (completedCount === 0) {
            alert("There are no completed tasks to clear.");
            return;
        }
        tasks = tasks.filter(t => !t.completed);
        saveTasks(tasks);
        renderTasks(tasks);
    };
});