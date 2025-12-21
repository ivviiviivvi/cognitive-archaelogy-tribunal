
import unittest
import os
import shutil
import tempfile
from pathlib import Path
from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):
    def test_unsafe_directory_scan_prevention(self):
        """Test that scanning unsafe system directories is prevented."""
        scanner = ArchiveScanner()

        # Determine which system directories actually exist in this environment
        existing_unsafe_paths = []
        possible_unsafe_paths = ['/etc', '/proc', '/sys', '/var', '/usr', '/bin', '/sbin']

        for path in possible_unsafe_paths:
            if os.path.exists(path) and os.path.isdir(path):
                existing_unsafe_paths.append(path)

        # Test existing system directories are blocked
        for path in existing_unsafe_paths:
             result = scanner.scan_directory(path, recursive=False)
             self.assertIn('error', result)
             self.assertIn("Unsafe directory", result['error'], f"Failed to block unsafe path: {path}")

    def test_root_directory_scan_prevention(self):
        """Test that scanning root directory is prevented."""
        scanner = ArchiveScanner()
        if os.path.exists('/'):
             result = scanner.scan_directory('/', recursive=False)
             self.assertIn('error', result)
             self.assertIn("Unsafe directory", result['error'])

    def test_safe_directory_scan_allowed(self):
        """Test that scanning a safe directory is still allowed."""
        scanner = ArchiveScanner()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = scanner.scan_directory(temp_dir)
            self.assertNotIn('error', result)
            self.assertIn('stats', result)

if __name__ == '__main__':
    unittest.main()
