import { FILTERS } from '../utils/taskUtils.js';

function FilterBar({ searchTerm, statusFilter, onSearchChange, onStatusFilterChange }) {
  return (
    <section className="filter-card" aria-label="Search and filter tasks">
      <div className="form-group form-group-grow">
        <label htmlFor="task-search">Search Tasks</label>
        <input
          id="task-search"
          type="search"
          value={searchTerm}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Search by task title"
        />
      </div>

      <div className="filter-buttons" role="group" aria-label="Task status filters">
        {Object.values(FILTERS).map((filter) => (
          <button
            key={filter}
            type="button"
            className={filter === statusFilter ? 'filter-button active' : 'filter-button'}
            onClick={() => onStatusFilterChange(filter)}
          >
            {filter}
          </button>
        ))}
      </div>
    </section>
  );
}

export default FilterBar;
