# User Guide: TaskManager System

## Introduction
Welcome to the TaskManager System User Guide. This step-by-step guide will walk you through setting up TaskManager, creating tasks using natural language parsing, understanding the priority triage engine, and synchronizing task stores.

---

## Prerequisites
- **Python 3.11+** installed (`python --version`).
- A command terminal (Terminal on macOS/Linux, PowerShell or Command Prompt on Windows).

---

## Step 1: Navigating to the Project Directory
Open your terminal and navigate to the `TaskManager` directory:

```bash
cd use-cases/code-algorithms/python/TaskManager
```

Verify that the CLI executable is ready:

```bash
python cli.py --help
```

---

## Step 2: Creating Tasks

### Method A: Explicit Command Parameters
To create a task with detailed explicit fields:

```bash
python cli.py create "Deploy Production Release" \
  --description "Ship version 2.0 to cloud server" \
  --priority 4 \
  --due "2026-09-15" \
  --tags "deploy,critical"
```

### Method B: Natural Language Text Parsing
You can quickly create tasks using syntax shortcuts:
- `!1` to `!4` or `!urgent`, `!high`, `!medium`, `!low` for priority.
- `@tagname` to attach tags.
- `#today`, `#tomorrow`, `#friday`, or `#YYYY-MM-DD` for due dates.

```bash
python cli.py parse "Review security audit report !urgent @security @audit #friday"
```

---

## Step 3: Viewing and Sorting Tasks

### Listing Tasks by Priority Score
TaskManager automatically calculates an importance score for each task based on priority tier, due date urgency, tag boosts, and recency.

To view tasks sorted by priority (highest importance score first):

```bash
python cli.py list
```

### Filtering Tasks
- **By Status**:
  ```bash
  python cli.py list --status todo
  ```
- **By Priority**:
  ```bash
  python cli.py list --priority 4
  ```
- **Overdue Tasks Only**:
  ```bash
  python cli.py list --overdue
  ```

---

## Step 4: Updating Task Status and Managing Tags

### Changing Status
Move tasks through the lifecycle (`todo` -> `in_progress` -> `review` -> `done`):

```bash
# Start working on a task
python cli.py update-status <TASK_ID> in_progress

# Mark task as completed (applies a -50 score penalty so it drops out of emergency view)
python cli.py update-status <TASK_ID> done
```

### Managing Tags
```bash
# Add a tag to boost score or organize
python cli.py add-tag <TASK_ID> blocker

# Remove a tag
python cli.py remove-tag <TASK_ID> finance
```

---

## Step 5: Data Synchronization (Advanced)
If you operate in an offline/local environment and need to merge tasks with a remote server, use the `task_list_merge` module in Python:

```python
from storage import load_tasks
from task_list_merge import merge_task_lists

local_tasks = load_tasks("tasks.json")
remote_tasks = load_tasks("remote_tasks.json")

merged, to_cr_remote, to_up_remote, to_cr_local, to_up_local = merge_task_lists(
    local_tasks, remote_tasks
)

print(f"Sync complete. {len(merged)} total tasks reconciled.")
```

---

## Common Mistakes & Pitfalls

1. **Incorrect Date Formatting**: Using `15/09/2026` or `Sept 15` will fail date validation. Always use `YYYY-MM-DD` (e.g. `2026-09-15`).
2. **Missing Spaces in Parsing Strings**: When using `cli.py parse`, ensure spaces precede syntax markers (`!urgent @tag #date`). For example, `"Buy milk!urgent"` will not parse priority because space is missing.
3. **Invalid Task IDs**: When updating or tagging tasks, pass the full UUID or ID string displayed in `cli.py list`.

---

## Troubleshooting Checklist

| Symptom | Cause | Resolution |
|---|---|---|
| `cli.py: error: invalid choice` | Misspelled subcommand | Check available subcommands via `python cli.py --help` |
| `ValueError: Invalid priority level` | Priority passed outside 1-4 | Use integer 1 (LOW), 2 (MEDIUM), 3 (HIGH), or 4 (URGENT) |
| `tasks.json` not updating | Permission denied | Ensure your terminal user has write permissions in the workspace directory |
