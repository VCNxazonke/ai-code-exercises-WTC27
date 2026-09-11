# Exercise 6: Part 4 - Reflection Answers

## Reflection Question 1: How does implementing this feature help you understand the overall architecture?
Implementing the audit log system required using the exact same generic `Repository[T]` base pattern and dependency injection providers (`get_audit_repo`) present in the initial codebase. Adding an entity without changing existing route code proved how layered, decoupled architectures prevent regression errors when extending applications.

## Reflection Question 2: Which design patterns did you find most useful in the original code?
The developer found the **Repository Pattern** combined with **Dependency Injection** (`Depends`) most useful. It cleanly isolated data storage operations from route controllers, making audit logging seamless to insert into login and admin endpoints.

## Reflection Question 3: How would you explain the repository pattern and dependency injection to a colleague?
- **Repository Pattern:** It acts like a librarian. Instead of going directly into the warehouse stacks (writing raw SQL/ORM code everywhere), you ask the librarian (`UserRepository.get_by_id()`) for the item, hiding warehouse storage details.
- **Dependency Injection:** It acts like a catering service. Instead of an endpoint function making its own database connection from scratch, the framework creates and provides the database connection directly into the function parameter.

## Reflection Question 4: How did tracing the execution flow help you understand where to add your code?
Tracing the execution flow revealed the exact execution sequence: Middleware -> Dependencies -> Handler -> Repository. This made it clear that user action auditing should occur inside service/repository calls during endpoint execution, ensuring events are logged only after security dependencies successfully validate credentials.
