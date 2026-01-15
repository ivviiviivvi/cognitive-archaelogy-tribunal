## 2025-05-18 - [File Hashing Performance]
**Learning:** `hashlib.file_digest` (Python 3.11+) provides ~10% speedup over manual chunk reading and releases GIL. 8KB buffer size is suboptimal for modern I/O; 64KB+ is preferred.
**Action:** Always check for `hashlib.file_digest` availability when hashing files. Use at least 64KB buffer for fallbacks.
