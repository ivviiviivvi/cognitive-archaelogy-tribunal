import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):

    def setUp(self):
        self.scanner = ArchiveScanner()

    @patch('pathlib.Path.resolve')
    def test_unsafe_paths_blocked_mocked(self, mock_resolve):
        """Test that unsafe system directories are blocked using mocks."""
        # Common unsafe paths on Linux/Unix
        unsafe_paths = [
            '/etc',
            '/proc',
            '/sys',
            '/dev',
            '/etc/passwd',
            '/proc/cpuinfo'
        ]

        for path_str in unsafe_paths:
            with self.subTest(path=path_str):
                path = MagicMock(spec=Path)
                path.__str__.return_value = path_str

                # Mock resolve behavior to just return the path string essentially
                mock_resolved_path = MagicMock(spec=Path)
                mock_resolved_path.__str__.return_value = path_str
                mock_resolve.return_value = mock_resolved_path

                # We need to make sure when scanner calls path.resolve(), it gets our mocked resolved path
                path.resolve.return_value = mock_resolved_path

                self.assertTrue(self.scanner.is_unsafe_path(path), f"Path {path_str} should be marked as unsafe")

    @patch('pathlib.Path.resolve')
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.is_dir')
    def test_scan_directory_blocks_unsafe_path(self, mock_is_dir, mock_exists, mock_resolve):
        """Test that scan_directory returns error for unsafe paths."""
        unsafe_path = '/etc'

        # Setup mocks
        mock_path = MagicMock(spec=Path)
        mock_path.__str__.return_value = unsafe_path

        # When resolve is called, return mock_path which strings to /etc
        mock_path.resolve.return_value = mock_path

        # Also need patch for Path constructor call in scan_directory
        mock_resolve.return_value = mock_path

        mock_exists.return_value = True
        mock_is_dir.return_value = True

        result = self.scanner.scan_directory(unsafe_path)

        # Expect error regarding unsafe path
        self.assertIn('error', result)
        self.assertIn('unsafe', result['error'].lower())

    @patch('pathlib.Path.resolve')
    def test_safe_paths_allowed_mocked(self, mock_resolve):
        """Test that safe paths are allowed using mocks."""
        safe_paths = [
            '/home/user/documents',
            '/tmp/my_archive',
            './local_dir'
        ]

        for path_str in safe_paths:
            with self.subTest(path=path_str):
                path = MagicMock(spec=Path)
                path.__str__.return_value = path_str

                mock_resolved_path = MagicMock(spec=Path)
                mock_resolved_path.__str__.return_value = path_str
                mock_resolve.return_value = mock_resolved_path
                path.resolve.return_value = mock_resolved_path

                self.assertFalse(self.scanner.is_unsafe_path(path), f"Path {path_str} should be safe")
