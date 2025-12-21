## 2024-05-23 - Initial Bolt Setup
**Learning:** Initial setup of Bolt's journal.
**Action:** Always check for this file before starting work.

## 2024-05-23 - Buffer Size Optimization
**Learning:** Increasing buffer size from 8KB to 64KB for file hashing yields a ~4% performance improvement for SHA256. While small, it's a "free" optimization without dependencies.
**Action:** Default to 64KB (65536 bytes) for file I/O operations involving large files.
