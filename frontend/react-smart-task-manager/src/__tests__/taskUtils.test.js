import { describe, expect, it, vi } from 'vitest';
import { FILTERS, createTask, filterTasks, getTaskStats } from '../utils/taskUtils.js';

describe('task utilities', () => {
  it('creates a pending task with title and priority', () => {
    vi.stubGlobal('crypto', { randomUUID: () => 'test-id-1' });

    const task = createTask('  Finish assignment  ', 'High');

    expect(task).toMatchObject({
      id: 'test-id-1',
      title: 'Finish assignment',
      priority: 'High',
      completed: false,
    });

    vi.unstubAllGlobals();
  });

  it('filters tasks by search term and pending status', () => {
    const tasks = [
      { id: '1', title: 'Prepare React demo', priority: 'High', completed: false },
      { id: '2', title: 'Submit project', priority: 'Medium', completed: true },
    ];

    const result = filterTasks(tasks, 'react', FILTERS.PENDING);

    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Prepare React demo');
  });

  it('calculates task dashboard stats', () => {
    const tasks = [
      { id: '1', title: 'Task 1', priority: 'High', completed: false },
      { id: '2', title: 'Task 2', priority: 'High', completed: true },
      { id: '3', title: 'Task 3', priority: 'Low', completed: false },
    ];

    expect(getTaskStats(tasks)).toEqual({
      total: 3,
      completed: 1,
      pending: 2,
      highPriority: 2,
    });
  });
});
