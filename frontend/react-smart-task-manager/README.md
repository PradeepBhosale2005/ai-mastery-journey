# React Assignment: Smart Task Manager

This folder contains a complete React solution for the Smart Task Manager assignment from `backend/AssignmentPrompt.txt`.

## Assignment Requirement

Build a practical mini productivity app using React hooks.

The app must support:

1. Add a task with a title and priority.
2. Display all tasks with title, priority, and status.
3. Toggle task status between Completed and Pending.
4. Delete a task permanently.
5. Search tasks by title.
6. Filter tasks by All, Completed, and Pending.
7. Toggle the UI between light and dark themes.

## Implemented Features

- React functional components
- `useState` for tasks, form input, filters, search, and theme
- `useEffect` for localStorage persistence and theme updates
- `useMemo` for filtered tasks and dashboard statistics
- `useCallback` for task actions
- Add task form with title and priority
- Task list with checkbox status toggle
- Delete button for each task
- Search bar
- All / Completed / Pending filters
- Light and dark theme toggle
- Responsive dashboard cards
- Local storage persistence
- Utility tests with Vitest

## Project Structure

```text
frontend/react-smart-task-manager/
├── README.md
├── package.json
├── index.html
├── vite.config.js
├── .gitignore
└── src/
    ├── App.jsx
    ├── main.jsx
    ├── index.css
    ├── components/
    │   ├── Dashboard.jsx
    │   ├── FilterBar.jsx
    │   ├── TaskForm.jsx
    │   ├── TaskList.jsx
    │   └── ThemeToggle.jsx
    ├── test/
    │   └── setup.js
    ├── utils/
    │   └── taskUtils.js
    └── __tests__/
        └── taskUtils.test.js
```

## Setup

From the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
git pull
cd .\frontend\react-smart-task-manager
npm install
```

## Run the App

```powershell
npm run dev
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:5173/
```

## Build the App

```powershell
npm run build
```

## Run Tests

```powershell
npm test
```

## Demo Checklist

Use this while submitting or presenting:

```text
1. Add a task with title and priority.
2. Confirm the task appears with Pending status.
3. Click the checkbox to mark it Completed.
4. Use the search bar to search by title.
5. Use All / Completed / Pending filters.
6. Delete a task.
7. Toggle between Light Theme and Dark Theme.
8. Refresh the page and confirm tasks/theme remain saved.
```

## Safe ZIP for LMS Upload

Create the ZIP from the repository root:

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey

$src = ".\frontend\react-smart-task-manager"
$tmp = ".\frontend\react-smart-task-manager-submit"
$zip = ".\frontend\react-smart-task-manager.zip"

Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $zip -Force -ErrorAction SilentlyContinue
Copy-Item $src $tmp -Recurse

Remove-Item "$tmp\node_modules" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\coverage" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$tmp\.env" -Force -ErrorAction SilentlyContinue
Get-ChildItem $tmp -Recurse -Directory -Filter ".vite" | Remove-Item -Recurse -Force

Compress-Archive -Path $tmp -DestinationPath $zip -Force
Remove-Item $tmp -Recurse -Force
```

Verify runtime folders are not included:

```powershell
tar -tf .\frontend\react-smart-task-manager.zip | Select-String "node_modules|dist|coverage|.env|.vite"
```

No output means it is safe.

Upload this file:

```text
C:\Users\pradeep.bhosale_jade\ai-mastery-journey\frontend\react-smart-task-manager.zip
```
