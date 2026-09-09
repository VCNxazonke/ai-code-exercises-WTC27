# Frequently Asked Questions (FAQ): TaskManager System

## 1. Getting Started

### Q: What are the minimum requirements to run TaskManager?
**A**: TaskManager requires Python 3.11 or higher. It relies exclusively on the Python standard library, so no external `pip` packages or virtual environment installations are necessary.

### Q: How do I install and launch TaskManager?
**A**: Simply clone or navigate to the repository folder (`use-cases/code-algorithms/python/TaskManager`) and run commands via `python cli.py <subcommand>`.

---

## 2. Features & Functionality

### Q: How does the priority scoring algorithm calculate task importance?
**A**: The score is calculated mathematically by evaluating 5 factors:
1. **Base Priority Tier**: Low = 10 pts, Medium = 20 pts, High = 40 pts, Urgent = 60 pts.
2. **Due Date Urgency**: Overdue (+35 pts), Due today (+20 pts), Due in <=2 days (+15 pts), Due in <=7 days (+10 pts).
3. **Status Penalty**: Completed (`DONE`) tasks receive a -50 pt penalty (sinking them to the bottom), while `REVIEW` tasks receive a -15 pt adjustment.
4. **Hot-Tag Boost**: Tasks with tags like `blocker`, `critical`, or `urgent` gain a +8 pt boost.
5. **Recency**: Tasks modified in the last 24 hours receive a +5 pt boost.

### Q: How does natural language parsing work in `cli.py parse`?
**A**: The parser scans input text using regular expressions to extract tags (`@tag`), priority markers (`!1` to `!4` or `!urgent`), and date keywords (`#today`, `#tomorrow`, `#friday`, `#YYYY-MM-DD`). Cleaned text becomes the task title.

---

## 3. Data Persistence & Synchronization

### Q: Where are tasks saved?
**A**: Tasks are serialized into a standard JSON file (`tasks.json`) in the application root. Python `UUID` objects, `TaskStatus`/`TaskPriority` Enums, and `datetime` objects are converted to flat JSON strings using `TaskEncoder`.

### Q: How does TaskManager handle sync conflicts between offline local data and a remote server?
**A**: The `task_list_merge` module uses **Last-Write-Wins (LWW)** based on `updated_at` timestamps for scalar properties (title, description, priority, due date). However, **completion status takes absolute precedence** (if either local or remote marks a task `DONE`, `DONE` wins), and **tags are merged via set union** so no tags are discarded.

---

## 4. Troubleshooting

### Q: What happens if `tasks.json` is missing or corrupted?
**A**: If `tasks.json` does not exist, `TaskManager` initializes a fresh, empty task dictionary. If the file contains invalid JSON, `TaskDecoder` catches parsing errors gracefully and prompts for file re-initialization.

### Q: Why isn't my due date tag (`#friday`) setting the correct date?
**A**: Ensure there is a space before the `#` symbol (e.g. `"Submit report #friday"`). Dates are computed relative to current local time (`datetime.now()`).
