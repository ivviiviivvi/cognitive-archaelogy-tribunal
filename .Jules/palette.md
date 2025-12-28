## 2024-05-22 - Rich CLI Output
**Learning:** Python CLI tools can be significantly enhanced with the `rich` library, which provides built-in support for colors, panels, and styled output. This improves readability and provides a more modern feel compared to plain text.
**Action:** When working on Python CLIs, check if `rich` is available. If so, encapsulate its usage in a dedicated `ui` module to maintain a consistent theme and simplify the main logic. Use `rich.console.Console` with a custom theme to enforce brand colors.
