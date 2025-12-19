## 2024-05-23 - Path Traversal Protection
**Vulnerability:** The `ArchiveScanner` module previously allowed scanning of any directory, including sensitive system paths like `/etc` or `/proc`.
**Learning:** Even in CLI tools where the user is "trusted", preventing accidental or malicious scanning of system critical paths is essential for "Defense in Depth". Path resolution (`resolve()`) is critical before checking against blocklists to prevent relative path bypasses (`../etc`).
**Prevention:** Always normalize paths using `Path.resolve()` before performing security checks. Use `startswith` with a trailing separator (e.g., `os.path.join(path, '')`) to prevent partial prefix matches (e.g., preventing `/bin` from blocking `/binary`).
