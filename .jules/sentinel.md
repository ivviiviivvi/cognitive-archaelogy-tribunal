## 2025-12-21 - Block Sensitive Directory Scanning
**Vulnerability:** The `ArchiveScanner` allowed scanning of sensitive system directories (e.g., `/etc`, `/proc`, `/`) if the user had read permissions. This could lead to information disclosure or resource exhaustion (when scanning virtual filesystems like `/proc`).
**Learning:** File scanning tools must explicitly validate input paths against a blocklist of known system directories. Simply resolving paths is not enough; we must check if the resolved path is a parent of or equal to a sensitive directory.
**Prevention:** Implemented `is_unsafe_path` method in `ArchiveScanner` which checks resolved paths against `UNSAFE_SYSTEM_DIRS` before proceeding with a scan.
