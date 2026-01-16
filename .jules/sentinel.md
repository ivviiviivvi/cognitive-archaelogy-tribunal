## 2025-05-22 - Path Traversal in ArchiveScanner
**Vulnerability:** `ArchiveScanner` allowed scanning the entire filesystem root (`/`) and critical system directories (`/etc`, `/var`, etc.) via `scan_directory`.
**Learning:** `pathlib.Path.resolve()` handles `..` traversal but does not inherently block access to system paths. Explicit checks against a blocklist or allowed scope are necessary.
**Prevention:** Implement `is_unsafe_path` checks that validate resolved paths against a list of known unsafe system directories and the filesystem root anchor before proceeding with operations.
