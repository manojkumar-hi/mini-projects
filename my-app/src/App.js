import React, { useState } from 'react';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([
    'Learn React',
    'Write Code',
    'Take a break'
  ]);
  const [newTask, setNewTask] = useState('');

  const handleAddTask = () => {
    if (newTask.trim() === '') return; // ignore empty input
    setTasks([...tasks, newTask.trim()]);
    setNewTask(''); // clear input box
  };

  return (
    <div className="container">
      <h1>My Todo App</h1>
      <p>Tasks for today:</p>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>{task}</li>
        ))}
      </ul>

      <input
        type="text"
        placeholder="Enter new task"
        value={newTask}
        onChange={(e) => setNewTask(e.target.value)}
      />
      <button onClick={handleAddTask}>Add Task</button>
    </div>
  );
}

export default App;
