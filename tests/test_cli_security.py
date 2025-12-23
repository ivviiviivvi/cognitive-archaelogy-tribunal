import unittest
import subprocess
import sys
from pathlib import Path

class TestCLISecurity(unittest.TestCase):
    def test_github_token_arg_not_exposed(self):
        """Test that the --github-token argument is not exposed in the CLI."""
        # Run main.py with --help
        result = subprocess.run(
            [sys.executable, 'main.py', '--help'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )

        # Check that --github-token is NOT in the output
        self.assertNotIn('--github-token', result.stdout, "Security risk: --github-token argument exposed in CLI")

if __name__ == '__main__':
    unittest.main()
