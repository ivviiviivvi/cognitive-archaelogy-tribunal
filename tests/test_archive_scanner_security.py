"""
Security tests for Archive Scanner module.
Checks for path traversal and unsafe path scanning prevention.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):

    def setUp(self):
        self.scanner = ArchiveScanner()

    @patch('sys.platform', 'linux')
    def test_unsafe_paths_posix_mocked(self):
        """Test detection of unsafe POSIX paths using mock."""
        # Test specific unsafe paths on a POSIX-like system

        # Test root and critical directories
        self.assertTrue(self.scanner.is_unsafe_path(Path('/')))
        self.assertTrue(self.scanner.is_unsafe_path(Path('/etc')))
        self.assertTrue(self.scanner.is_unsafe_path(Path('/var')))
        self.assertTrue(self.scanner.is_unsafe_path(Path('/usr/bin')))

        # Test nested unsafe paths
        self.assertTrue(self.scanner.is_unsafe_path(Path('/etc/nginx/conf.d')))

        # Test safe paths
        self.assertFalse(self.scanner.is_unsafe_path(Path('/home/user/documents')))
        self.assertFalse(self.scanner.is_unsafe_path(Path('/mnt/data')))
        self.assertFalse(self.scanner.is_unsafe_path(Path('/tmp/safe')))

    @patch('sys.platform', 'win32')
    def test_unsafe_paths_windows_mocked(self):
        """Test detection of unsafe Windows paths using mock."""
        # Test specific unsafe paths on a Windows-like system

        # Test critical directories (case-insensitive)
        self.assertTrue(self.scanner.is_unsafe_path(Path('C:\\Windows')))
        self.assertTrue(self.scanner.is_unsafe_path(Path('c:\\windows')))
        self.assertTrue(self.scanner.is_unsafe_path(Path('C:\\Program Files')))

        # Test nested unsafe paths
        self.assertTrue(self.scanner.is_unsafe_path(Path('C:\\Windows\\System32')))

        # Test safe paths
        self.assertFalse(self.scanner.is_unsafe_path(Path('C:\\Users\\User\\Documents')))
        self.assertFalse(self.scanner.is_unsafe_path(Path('D:\\Backups')))

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_blocks_unsafe_path(self, mock_is_dir, mock_exists, mock_resolve):
        """Test that scan_directory returns error for unsafe paths."""

        # Define a path that is unsafe on the current platform
        if sys.platform == 'win32':
            unsafe_path_str = 'C:\\Windows'
        else:
            unsafe_path_str = '/etc'

        mock_resolve.return_value = Path(unsafe_path_str)
        mock_exists.return_value = True
        mock_is_dir.return_value = True

        # We need to ensure is_unsafe_path returns True for this path
        # Since is_unsafe_path relies on sys.platform, it should work naturally
        # for the chosen path on the current OS.

        result = self.scanner.scan_directory(unsafe_path_str)

        self.assertIn('error', result)
        self.assertIn('Security risk', result['error'])
        self.assertIn('blocked scanning', result['error'])

if __name__ == '__main__':
    unittest.main()
