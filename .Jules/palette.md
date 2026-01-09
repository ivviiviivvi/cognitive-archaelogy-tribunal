## 2024-05-23 - [CLI Empty State]
**Learning:** Users running a CLI without arguments often expect guidance, not just an error.
**Action:** Detect the "no arguments" state and render a rich, helpful welcome screen with examples instead of a standard `argparse` error.
