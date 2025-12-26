## 2025-10-27 - [Path Traversal in Archive Scanner]
**Vulnerability:** The `ArchiveScanner` followed symbolic links recursively and did not validate the root path against sensitive system directories. This could allow reading arbitrary files (e.g., `/etc/passwd`) or causing infinite loops if a user (or a malicious archive) created a symlink to a sensitive location.
**Learning:** `pathlib.Path.iterdir()` combined with `is_dir()` implicitly allows traversing symlinks to directories. Explicit checks for `is_symlink()` are required to prevent escaping the intended scan scope.
**Prevention:**
1. Always resolve paths (`path.resolve()`) before validation.
2. Explicitly check `is_symlink()` and skip or validate target before recursing.
3. Implement a blocklist of known unsafe system paths (`/proc`, `/etc`, etc.) for any tool that accepts a root scan path.
