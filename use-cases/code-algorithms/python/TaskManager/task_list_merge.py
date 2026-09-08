"""
Task List Synchronization and Conflict Resolution Module.

This module implements a bidirectional state synchronization algorithm between local
(offline) and remote (cloud) task stores. It uses Last-Write-Wins (LWW) timestamp logic,
status precedence rules (completion wins), and set-union tag merging to achieve eventual
consistency across distributed storage layers.
"""

import copy
from typing import Dict, Tuple, Set, Optional

from models import TaskStatus, TaskPriority, Task


def merge_task_lists(
    local_tasks: Dict[str, Task],
    remote_tasks: Dict[str, Task]
) -> Tuple[
    Dict[str, Task],  # Merged result mapping task_id -> Task
    Dict[str, Task],  # Tasks to create on remote
    Dict[str, Task],  # Tasks to update on remote
    Dict[str, Task],  # Tasks to create on local
    Dict[str, Task]   # Tasks to update on local
]:
    """
    Synchronize local and remote task dictionaries and calculate state delta operations.

    Iterates over the union of task IDs from both local and remote dictionaries. It routes
    tasks into sync categories: missing remotely (create remote), missing locally (create local),
    or present in both (resolve field conflict).

    Args:
        local_tasks (Dict[str, Task]): Dictionary mapping task IDs to local Task objects.
        remote_tasks (Dict[str, Task]): Dictionary mapping task IDs to remote Task objects.

    Returns:
        Tuple[Dict[str, Task], Dict[str, Task], Dict[str, Task], Dict[str, Task], Dict[str, Task]]:
            A 5-tuple containing delta change sets:
            - merged_tasks: Comprehensive dictionary of all synchronized tasks.
            - to_create_remote: Tasks that exist locally and must be created on remote.
            - to_update_remote: Tasks modified locally that must be updated on remote.
            - to_create_local: Tasks that exist remotely and must be created locally.
            - to_update_local: Tasks modified remotely that must be updated locally.

    Raises:
        AttributeError: If any task object lacks required fields (`updated_at`, `status`, `tags`).
        TypeError: If input parameters are not dictionary instances.

    Example:
        >>> local = {'t1': Task('Task 1')}
        >>> remote = {'t1': Task('Task 1 Updated'), 't2': Task('Task 2')}
        >>> merged, cr_rem, up_rem, cr_loc, up_loc = merge_task_lists(local, remote)
        >>> set(merged.keys()) == {'t1', 't2'}
        True
        >>> 't2' in cr_loc
        True

    Notes:
        - Hard Deletions: This function does not handle tombstones. If a task is missing from
          one side, it is assumed to be a newly created task on the other side.
    """
    merged_tasks: Dict[str, Task] = {}
    to_create_remote: Dict[str, Task] = {}
    to_update_remote: Dict[str, Task] = {}
    to_create_local: Dict[str, Task] = {}
    to_update_local: Dict[str, Task] = {}

    # Step 1: Discover all unique task IDs across local and remote sources
    all_task_ids: Set[str] = set(local_tasks.keys()) | set(remote_tasks.keys())

    # Step 2: Process each task ID based on source presence
    for task_id in all_task_ids:
        local_task: Optional[Task] = local_tasks.get(task_id)
        remote_task: Optional[Task] = remote_tasks.get(task_id)

        # Case 1: Exists locally only -> Queue for creation on remote server
        if local_task and not remote_task:
            merged_tasks[task_id] = local_task
            to_create_remote[task_id] = local_task

        # Case 2: Exists remotely only -> Queue for creation in local database
        elif not local_task and remote_task:
            merged_tasks[task_id] = remote_task
            to_create_local[task_id] = remote_task

        # Case 3: Exists in both stores -> Perform field-level conflict resolution
        else:
            assert local_task is not None and remote_task is not None

            merged_task, should_update_local, should_update_remote = resolve_task_conflict(
                local_task, remote_task
            )

            merged_tasks[task_id] = merged_task

            if should_update_local:
                to_update_local[task_id] = merged_task

            if should_update_remote:
                to_update_remote[task_id] = merged_task

    return (
        merged_tasks,
        to_create_remote,
        to_update_remote,
        to_create_local,
        to_update_local
    )


def resolve_task_conflict(
    local_task: Task,
    remote_task: Task
) -> Tuple[Task, bool, bool]:
    """
    Resolve property conflicts between two versions of the same task.

    Reconciliation Protocol:
    1. Base Properties (title, description, priority, due_date): Reconciled using Last-Write-Wins (LWW)
       based on `updated_at`.
    2. Status Property: Monotonic completion rule—if either local or remote is `TaskStatus.DONE`,
       the status resolves to `DONE`. Otherwise, LWW applies.
    3. Tags: Set union (`set(local.tags) | set(remote.tags)`) ensures tag additions from both sides persist.
    4. Updated Timestamp: Reconciled to `max(local_task.updated_at, remote_task.updated_at)`.

    Args:
        local_task (Task): Local version of the task.
        remote_task (Task): Remote version of the task.

    Returns:
        Tuple[Task, bool, bool]:
            - merged_task: Reconciled Task instance (cloned, non-mutating).
            - should_update_local: Boolean flag indicating if local storage needs persistence.
            - should_update_remote: Boolean flag indicating if remote storage needs persistence.

    Raises:
        TypeError: If `updated_at` datetimes have mismatched timezone awareness (naive vs aware).
        AttributeError: If required Task attributes are missing.

    Example:
        >>> t1 = Task("Bug fix", status=TaskStatus.TODO)
        >>> t2 = Task("Bug fix", status=TaskStatus.DONE)
        >>> reconciled, update_loc, update_rem = resolve_task_conflict(t1, t2)
        >>> reconciled.status == TaskStatus.DONE
        True

    Notes:
        - Immutability Guarantee: Operates on a deep copy of `local_task` to prevent unintended side effects.
    """
    # Create an independent copy of local_task as our reconciliation working object
    merged_task: Task = copy.deepcopy(local_task)

    # Track persistence requirements for each endpoint
    should_update_local: bool = False
    should_update_remote: bool = False

    # -------------------------------------------------------------------------
    # 1. Base Property Reconciliation (Last-Write-Wins based on updated_at)
    # -------------------------------------------------------------------------
    if remote_task.updated_at > local_task.updated_at:
        # Remote version is newer: pull remote scalar attributes into merged task
        merged_task.title = remote_task.title
        merged_task.description = remote_task.description
        merged_task.priority = remote_task.priority
        merged_task.due_date = remote_task.due_date
        should_update_local = True
    else:
        # Local version is newer or equal: push local attributes to remote
        should_update_remote = True

    # -------------------------------------------------------------------------
    # 2. Special Status Resolution (Completion Monotonicity)
    # -------------------------------------------------------------------------
    if remote_task.status == TaskStatus.DONE and local_task.status != TaskStatus.DONE:
        # Remote completed the task -> Completion wins, pull status to local
        merged_task.status = TaskStatus.DONE
        merged_task.completed_at = remote_task.completed_at
        should_update_local = True
    elif local_task.status == TaskStatus.DONE and remote_task.status != TaskStatus.DONE:
        # Local completed the task -> Completion wins, push status to remote
        should_update_remote = True
    elif remote_task.status != local_task.status:
        # Both non-completed but different -> Last-Write-Wins applies
        if remote_task.updated_at > local_task.updated_at:
            merged_task.status = remote_task.status
            should_update_local = True
        else:
            should_update_remote = True

    # -------------------------------------------------------------------------
    # 3. Tag Merging (Union of local and remote tag sets)
    # -------------------------------------------------------------------------
    all_tags: Set[str] = set(local_task.tags) | set(remote_task.tags)
    merged_task.tags = list(all_tags)

    # If tag set changed relative to local or remote, mark respective endpoint dirty
    if set(merged_task.tags) != set(local_task.tags):
        should_update_local = True
    if set(merged_task.tags) != set(remote_task.tags):
        should_update_remote = True

    # -------------------------------------------------------------------------
    # 4. Final Timestamp Synchronization
    # -------------------------------------------------------------------------
    merged_task.updated_at = max(local_task.updated_at, remote_task.updated_at)

    return merged_task, should_update_local, should_update_remote
