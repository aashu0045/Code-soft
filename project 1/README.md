# Beginner-Friendly Python To-Do List (Tkinter GUI)

A simple to-do list desktop app built with Python's standard Tkinter GUI toolkit. No extra packages required.

## Features
- Add, edit, delete tasks
- Mark tasks complete/incomplete
- Clear completed tasks
- Auto-saves to `tasks.json` in the same folder
- Manual Save and Load buttons
- Shortcuts: Enter=Add, Delete=Remove, Double-click=Toggle, F2=Edit

## Requirements
- Python 3.10+ (earlier 3.x should also work)

## Run
On Windows, double-click the file or run from terminal:

```bash
python "To Do list.py"
```

Tasks persist in `tasks.json` in this folder. You can delete that file to reset.

## Files
- `To Do list.py`: App source code
- `tasks.json`: Saved data (auto-created)

## Notes for Beginners
- The app uses a `Listbox` widget to display tasks.
- Tasks are stored as a list of dictionaries: `{ "text": str, "completed": bool }`.
- The code is organized into small methods to make it easy to follow.




