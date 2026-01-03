## 2026-01-03 - [Information Leakage in Error Handling]
**Vulnerability:** Raw exception messages containing potential secrets (e.g., API tokens in URLs) or internal paths were being printed directly to stdout.
**Learning:** Python's `print(e)` is not secure for production apps dealing with sensitive data, as exception messages often contain the context of the error (including secrets).
**Prevention:** Implement "Fail Securely" by catching exceptions, logging the full details (including stack traces) to a secure log file, and displaying only a generic error message to the user.
