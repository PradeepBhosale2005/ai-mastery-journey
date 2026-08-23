function TaskList({ tasks, onToggleTask, onDeleteTask }) {
  if (tasks.length === 0) {
    return (
      <section className="empty-state" aria-label="No tasks found">
        <h2>No tasks found</h2>
        <p>Add a task or change your search/filter selection.</p>
      </section>
    );
  }

  return (
    <section className="task-list" aria-label="Task list">
      {tasks.map((task) => (
        <article className={task.completed ? 'task-item completed' : 'task-item'} key={task.id}>
          <label className="task-checkbox">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggleTask(task.id)}
            />
            <span className="visually-hidden">
              Mark {task.title} as {task.completed ? 'pending' : 'completed'}
            </span>
          </label>

          <div className="task-content">
            <h3>{task.title}</h3>
            <div className="task-meta">
              <span className={`priority-badge ${task.priority.toLowerCase()}`}>{task.priority}</span>
              <span className={task.completed ? 'status completed-status' : 'status pending-status'}>
                {task.completed ? 'Completed' : 'Pending'}
              </span>
            </div>
          </div>

          <button className="delete-button" type="button" onClick={() => onDeleteTask(task.id)}>
            Delete
          </button>
        </article>
      ))}
    </section>
  );
}

export default TaskList;
