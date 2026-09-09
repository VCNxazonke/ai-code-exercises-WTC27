# Task Manager System

A robust, offline-first Python Task Management application featuring an automated priority triage scoring engine, natural language task string parsing, tag set management, JSON persistence, and bidirectional eventual-consistency synchronization.

---

## Key Features

- **Natural Language Parsing**: Automatically extract titles, tags (`@tag`), priority levels (`!1`-`!4` or `!urgent`), and due dates (`#today`, `#tomorrow`, `#friday`, `#YYYY-MM-DD`) from free-form text.
- **Priority Triage Algorithm**: Multi-factor scoring engine evaluating base priority weights, due date urgency, completion status degradation, hot-tag boosts (`blocker`, `critical`), and recency.
- **CLI Interface**: Powerful command-line tool for creating, updating, filtering, tagging, and visualizing task metrics.
- **JSON Storage & Serialization**: Custom JSON encoder/decoder handling Python Enums, `datetime` ISO strings, and `UUID` identifiers with atomic file operations.
- **Bidirectional Sync Engine**: Differential synchronization protocol for resolving conflicts between local offline caches and remote task stores using Last-Write-Wins (LWW) and status precedence.

---

## Technologies Used

- **Language**: Python 3.11+
- **Standard Library Modules**: `argparse`, `json`, `re`, `datetime`, `uuid`, `enum`, `copy`, `unittest`
- **External Dependencies**: None (Zero external third-party dependencies)

---

## Installation & Requirements

### Prerequisites
- Python 3.11 or higher installed on your system.

### Quick Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd use-cases/code-algorithms/python/TaskManager
   ```
2. Verify Python environment:
   ```bash
   python --version
   ```

---

## Basic Usage Examples

### 1. Create Tasks via CLI
```bash
# Standard task creation with explicit flags
python cli.py create "Prepare Quarterly Report" --description "Financial breakdown" --priority 3 --due "2026-09-30" --tags "work,finance"

# Quick task creation via natural language parsing
python cli.py parse "Submit tax return !urgent @finance #friday"
```

### 2. List & Filter Tasks
```bash
# List all tasks sorted by priority score (highest first)
python cli.py list

# Filter by status (todo, in_progress, review, done)
python cli.py list --status todo

# Filter by priority (1=LOW, 2=MEDIUM, 3=HIGH, 4=URGENT)
python cli.py list --priority 4

# View overdue tasks
python cli.py list --overdue
```

### 3. Update Task Properties
```bash
# Change task status
python cli.py update-status <task_id> in_progress

# Change task priority
python cli.py update-priority <task_id> 4

# Update due date
python cli.py update-due-date <task_id> "2026-10-15"
```

### 4. Tag Management & Statistics
```bash
# Add and remove tags
python cli.py add-tag <task_id> "blocker"
python cli.py remove-tag <task_id> "finance"

# Display overall task statistics
python cli.py stats
```

---

## Code Structure Overview

```
TaskManager/
├── cli.py               # Command Line Interface (argument parsing, subcommands)
├── models.py            # Core domain models (Task, TaskStatus, TaskPriority)
├── storage.py           # Storage engine (save_tasks, load_tasks, TaskEncoder, TaskDecoder)
├── task_manager.py      # Core TaskManager controller (CRUD, filtering, stats)
├── task_priority.py     # Priority scoring algorithm & sorting functions
├── task_parser.py       # Natural language text parsing engine (regex, date calculation)
├── task_list_merge.py   # Differential sync & conflict resolution engine
├── README.md            # Project documentation overview
├── USER_GUIDE.md       # Step-by-step user guide
├── FAQ.md               # Frequently Asked Questions
└── tests/               # Unit test suite (55 automated tests)
    ├── test_cli.py
    ├── test_models.py
    ├── test_storage.py
    ├── test_task_list_merge.py
    ├── test_task_manager.py
    ├── test_task_parser.py
    └── test_task_priority.py
```

---

## Running Unit Tests

Run the full automated test suite using Python's built-in `unittest` runner:

```bash
python -m unittest discover tests
```

---

## Configuration & Storage Options

Tasks are automatically persisted to a local `tasks.json` file in the working directory. The storage path can be overridden programmatically when initializing `TaskManager`:

```python
from task_manager import TaskManager

manager = TaskManager(storage_path="custom_tasks.json")
```

---

## Troubleshooting

- **Invalid Date Format**: Ensure all date inputs use `YYYY-MM-DD` format (e.g. `2026-09-15`).
- **Corrupted `tasks.json`**: If `tasks.json` becomes malformed due to manual editing, delete or backup the file; `TaskManager` will re-initialize an empty task store automatically.

---

## License

This project is open-source and available under the [MIT License](LICENSE).
