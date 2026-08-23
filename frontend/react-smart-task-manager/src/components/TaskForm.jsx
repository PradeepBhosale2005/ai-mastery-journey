import { PRIORITIES } from '../utils/taskUtils.js';

function TaskForm({ title, priority, onTitleChange, onPriorityChange, onAddTask }) {
  return (
    <form className="task-form" onSubmit={onAddTask} aria-label="Add new task form">
      <div className="form-group form-group-grow">
        <label htmlFor="task-title">Task Title</label>
        <input
          id="task-title"
          type="text"
          value={title}
          onChange={(event) => onTitleChange(event.target.value)}
          placeholder="Example: Prepare weekly report"
        />
      </div>

      <div className="form-group">
        <label htmlFor="task-priority">Priority</label>
        <select
          id="task-priority"
          value={priority}
          onChange={(event) => onPriorityChange(event.target.value)}
        >
          {PRIORITIES.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      <button className="primary-button" type="submit">
        Add Task
      </button>
    </form>
  );
}

export default TaskForm;
