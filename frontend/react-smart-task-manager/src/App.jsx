import { useCallback, useEffect, useMemo, useState } from 'react';
import Dashboard from './components/Dashboard.jsx';
import FilterBar from './components/FilterBar.jsx';
import TaskForm from './components/TaskForm.jsx';
import TaskList from './components/TaskList.jsx';
import ThemeToggle from './components/ThemeToggle.jsx';
import { FILTERS, createTask, filterTasks, getTaskStats } from './utils/taskUtils.js';

const TASK_STORAGE_KEY = 'smart-task-manager.tasks';
const THEME_STORAGE_KEY = 'smart-task-manager.theme';

const sampleTasks = [
  {
    id: 'sample-1',
    title: 'Review React hooks assignment',
    priority: 'High',
    completed: false,
    createdAt: new Date().toISOString(),
  },
  {
    id: 'sample-2',
    title: 'Prepare task manager demo',
    priority: 'Medium',
    completed: true,
    createdAt: new Date().toISOString(),
  },
];

function loadInitialTasks() {
  try {
    const savedTasks = localStorage.getItem(TASK_STORAGE_KEY);
    return savedTasks ? JSON.parse(savedTasks) : sampleTasks;
  } catch {
    return sampleTasks;
  }
}

function loadInitialTheme() {
  try {
    return localStorage.getItem(THEME_STORAGE_KEY) || 'light';
  } catch {
    return 'light';
  }
}

function App() {
  const [tasks, setTasks] = useState(loadInitialTasks);
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState('Medium');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState(FILTERS.ALL);
  const [theme, setTheme] = useState(loadInitialTheme);
  const [error, setError] = useState('');

  useEffect(() => {
    localStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(tasks));
  }, [tasks]);

  useEffect(() => {
    document.body.dataset.theme = theme;
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }, [theme]);

  const stats = useMemo(() => getTaskStats(tasks), [tasks]);

  const visibleTasks = useMemo(
    () => filterTasks(tasks, searchTerm, statusFilter),
    [tasks, searchTerm, statusFilter],
  );

  const handleAddTask = useCallback(
    (event) => {
      event.preventDefault();

      try {
        const nextTask = createTask(title, priority);
        setTasks((currentTasks) => [nextTask, ...currentTasks]);
        setTitle('');
        setPriority('Medium');
        setError('');
      } catch (validationError) {
        setError(validationError.message);
      }
    },
    [title, priority],
  );

  const handleToggleTask = useCallback((taskId) => {
    setTasks((currentTasks) =>
      currentTasks.map((task) =>
        task.id === taskId ? { ...task, completed: !task.completed } : task,
      ),
    );
  }, []);

  const handleDeleteTask = useCallback((taskId) => {
    setTasks((currentTasks) => currentTasks.filter((task) => task.id !== taskId));
  }, []);

  const handleToggleTheme = useCallback(() => {
    setTheme((currentTheme) => (currentTheme === 'light' ? 'dark' : 'light'));
  }, []);

  return (
    <main className="app-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">React Hooks Assignment</p>
          <h1>Smart Task Manager</h1>
          <p className="hero-copy">
            Add tasks, assign priority, track completion, search your work, filter by status,
            and switch between light and dark themes.
          </p>
        </div>
        <ThemeToggle theme={theme} onToggleTheme={handleToggleTheme} />
      </section>

      <Dashboard stats={stats} />

      <section className="panel">
        <TaskForm
          title={title}
          priority={priority}
          onTitleChange={setTitle}
          onPriorityChange={setPriority}
          onAddTask={handleAddTask}
        />
        {error && <p className="error-message">{error}</p>}
      </section>

      <FilterBar
        searchTerm={searchTerm}
        statusFilter={statusFilter}
        onSearchChange={setSearchTerm}
        onStatusFilterChange={setStatusFilter}
      />

      <TaskList tasks={visibleTasks} onToggleTask={handleToggleTask} onDeleteTask={handleDeleteTask} />
    </main>
  );
}

export default App;
