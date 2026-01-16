
import sys
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestUnsafeScan(unittest.TestCase):
    def test_scan_root_blocked_real_path(self):
        """Test with real Path objects (safe because we mock _scan_recursive)."""
        scanner = ArchiveScanner()
        scanner._scan_recursive = MagicMock()

        # "/" is definitely unsafe and exists
        result = scanner.scan_directory("/")

        # Verification
        if scanner._scan_recursive.called:
             self.fail("Security FAIL: Root directory scan was allowed!")

        self.assertIn('error', result)
        self.assertIn('Security risk', result['error'])
        print("\n[SUCCESS] Root scan blocked correctly.")

if __name__ == '__main__':
    unittest.main()
