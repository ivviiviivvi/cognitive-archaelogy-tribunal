# Sentinel's Journal

## 2025-05-15 - Hardcoded Secrets via CLI Arguments
**Vulnerability:** The application allowed passing the GitHub Personal Access Token via a command-line argument (`--github-token`).
**Learning:** Secrets passed as command-line arguments are visible in process listings (`ps aux`) and shell history files (`.bash_history`), making them easily accessible to other users on the system or attackers with read access.
**Prevention:** Always use environment variables or configuration files with restricted permissions for handling secrets. Remove CLI flags that accept sensitive information.
