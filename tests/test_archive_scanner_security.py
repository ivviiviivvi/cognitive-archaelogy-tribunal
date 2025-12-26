
import unittest
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):
    """Security tests for ArchiveScanner."""

    def setUp(self):
        self.scanner = ArchiveScanner()
        self.test_dir = Path("test_security_env")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_block_unsafe_paths(self):
        """Test that scanning unsafe paths is blocked."""
        # Mocking Path.resolve to return an unsafe path without actually needing it to exist
        with patch('pathlib.Path.resolve') as mock_resolve:
            # Test a few unsafe paths
            unsafe_paths = ['/etc', '/proc', '/sys']

            for path in unsafe_paths:
                mock_resolve.return_value = Path(path)
                # We need to mock exists and is_dir to pass the initial checks
                with patch('pathlib.Path.exists', return_value=True), \
                     patch('pathlib.Path.is_dir', return_value=True):

                    result = self.scanner.scan_directory(path)

                    self.assertIn('error', result, f"Should return error for unsafe path: {path}")
                    self.assertIn('unsafe', result.get('error', '').lower(), f"Error message should mention unsafe/blocked path for: {path}")

    def test_symlink_traversal_prevention(self):
        """Test that the scanner does not follow symlinks."""
        # Create a directory structure with a symlink
        safe_dir = self.test_dir / "safe"
        safe_dir.mkdir()
        (safe_dir / "file.txt").write_text("content")

        target_dir = self.test_dir / "target"
        target_dir.mkdir()
        (target_dir / "secret.txt").write_text("secret")

        # Create symlink in safe_dir pointing to target_dir
        symlink = safe_dir / "link_to_target"
        try:
            symlink.symlink_to(target_dir.resolve())
        except OSError:
            self.skipTest("Symlinks not supported on this OS")

        # Scan safe_dir
        results = self.scanner.scan_directory(str(safe_dir))

        # Check files found
        found_files = [f['name'] for f in results.get('files', [])]

        self.assertIn('file.txt', found_files)
        self.assertNotIn('secret.txt', found_files, "Scanner followed symlink to secret file")

if __name__ == '__main__':
    unittest.main()
