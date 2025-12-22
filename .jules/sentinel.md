## 2025-12-22 - Path Traversal Prevention in ArchiveScanner
**Vulnerability:** The `ArchiveScanner` previously allowed scanning of any directory, including sensitive system paths like `/etc`, `/proc`, and `/sys`. This could lead to information disclosure if run with elevated privileges or on sensitive mounts.
**Learning:** Security checks like path validation must be centralized (e.g., in `should_exclude`) rather than ad-hoc in entry points to ensure they apply recursively and consistently. `Path.resolve()` is crucial for preventing bypasses using symlinks or relative paths (`..`).
**Prevention:** Always sanitize and validate file paths against a blocklist of sensitive directories before processing, resolving paths to their absolute canonical form first.
