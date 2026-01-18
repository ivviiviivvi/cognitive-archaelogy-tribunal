# Sentinel Journal - Critical Security Learnings

## 2024-05-23 - Path Traversal Prevention in File Scanners
**Vulnerability:** The `ArchiveScanner` module allowed scanning of the filesystem root (`/` or `C:\`) and sensitive system directories without restriction. This could lead to traversing the entire filesystem, accessing sensitive system files, or causing denial of service via resource exhaustion.
**Learning:** Even in local CLI tools, path validation is crucial. Relying solely on user discretion is insufficient. `pathlib.Path.resolve()` is essential for normalization but must be paired with explicit checks against unsafe anchors and prefixes.
**Prevention:** Implemented a robust `is_unsafe_path` check that:
1. Resolves paths to absolute form.
2. Blocks the filesystem anchor (root).
3. Blocks platform-specific system directories (e.g., `/etc`, `C:\Windows`) by checking exact matches and directory prefixes using `os.sep` to avoid partial string matching false positives.
