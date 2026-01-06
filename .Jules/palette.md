## 2024-05-23 - Empty State Pattern for CLI
**Learning:** Users often run CLI tools without arguments to "test the waters" or recall how to use them. A standard argparse error message (status 2) feels like a failure.
**Action:** Detect the "no arguments" state explicitly and present a "Welcome Panel" (status 0) that guides the user, turning a potential error into a helpful onboarding moment. Use `rich` for visual polish but ensure graceful degradation.
