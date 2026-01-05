## 2024-05-23 - CLI Empty State Pattern
**Learning:** Users perceive CLI tools as "broken" or "confusing" when running them without arguments produces a raw error trace or dry usage text. A "Welcome Panel" (Empty State) dramatically improves the first-run experience and guides the user to the correct syntax.
**Action:** Always implement a dedicated "No Arguments" handler that displays a styled Welcome Panel with 2-3 common usage examples.
