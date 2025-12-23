## 2025-12-23 - [Deduplication Performance]
**Learning:** Eagerly hashing files on size collision in Deduplicator was inefficient because find_duplicates (which is called anyway) did not utilize the results, leading to redundant IO. Caching hashes in Deduplicator and removing eager hashing improved performance significantly.
**Action:** Always check if computed results are actually used before computing them eagerly, or ensure they are cached and reused.
