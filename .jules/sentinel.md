## 2024-05-23 - [Path Traversal Protection in ArchiveScanner]
**Vulnerability:** The `ArchiveScanner` module previously allowed scanning any directory, including the filesystem root (`/` or `C:\`) and critical system directories (`/etc`, `/var`, `C:\Windows`). This could lead to information disclosure or Denial of Service by traversing the entire filesystem.
**Learning:** Even internal tools need boundaries. Users (even self-users) can make mistakes like running a scan on `/` by accident. Input validation for file paths is crucial for any tool interacting with the file system.
**Prevention:** Implemented `is_unsafe_path` check in `ArchiveScanner` using a blocklist of critical system paths and root anchors. This check is applied before scanning begins.
