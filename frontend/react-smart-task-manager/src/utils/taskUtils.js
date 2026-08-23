export const PRIORITIES = ['High', 'Medium', 'Low'];

export const FILTERS = {
  ALL: 'All',
  COMPLETED: 'Completed',
  PENDING: 'Pending',
};

export function createTask(title, priority) {
  const cleanTitle = String(title || '').trim();

  if (!cleanTitle) {
    throw new Error('Task title is required.');
  }

  if (!PRIORITIES.includes(priority)) {
    throw new Error('Priority must be High, Medium, or Low.');
  }

  return {
    id: crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`,
    title: cleanTitle,
    priority,
    completed: false,
    createdAt: new Date().toISOString(),
  };
}

export function filterTasks(tasks, searchTerm, statusFilter) {
  const normalizedSearch = String(searchTerm || '').toLowerCase().trim();

  return tasks.filter((task) => {
    const matchesSearch = task.title.toLowerCase().includes(normalizedSearch);
    const matchesStatus =
      statusFilter === FILTERS.ALL ||
      (statusFilter === FILTERS.COMPLETED && task.completed) ||
      (statusFilter === FILTERS.PENDING && !task.completed);

    return matchesSearch && matchesStatus;
  });
}

export function getTaskStats(tasks) {
  const total = tasks.length;
  const completed = tasks.filter((task) => task.completed).length;
  const pending = total - completed;
  const highPriority = tasks.filter((task) => task.priority === 'High').length;

  return {
    total,
    completed,
    pending,
    highPriority,
  };
}
