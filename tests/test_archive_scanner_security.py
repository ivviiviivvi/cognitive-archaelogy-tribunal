
import unittest
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner

class TestArchiveScannerSecurity(unittest.TestCase):

    def test_unsafe_path_detection_posix(self):
        """Test detection of unsafe POSIX paths."""
        scanner = ArchiveScanner()

        # Mocking os.name to simulate POSIX
        with patch('os.name', 'posix'):
            # Using patch for Path.resolve to avoid actual filesystem interaction/errors
            with patch('pathlib.Path.resolve') as mock_resolve:
                # Test root
                mock_resolve.return_value = Path('/')
                self.assertTrue(scanner.is_unsafe_path(Path('/')))

                # Test /etc
                mock_resolve.return_value = Path('/etc')
                self.assertTrue(scanner.is_unsafe_path(Path('/etc')))

                # Test safe path
                mock_resolve.return_value = Path('/home/user/documents')
                self.assertFalse(scanner.is_unsafe_path(Path('/home/user/documents')))

    def test_unsafe_path_detection_nt(self):
        """Test detection of unsafe Windows paths."""
        scanner = ArchiveScanner()

        # Mocking os.name to simulate Windows
        with patch('os.name', 'nt'):
            with patch('pathlib.Path.resolve') as mock_resolve:
                # Test C:\
                mock_resolve.return_value = Path('C:\\')
                self.assertTrue(scanner.is_unsafe_path(Path('C:\\')))

                # Test C:\Windows
                mock_resolve.return_value = Path('C:\\Windows')
                self.assertTrue(scanner.is_unsafe_path(Path('C:\\Windows')))

                # Test safe path
                mock_resolve.return_value = Path('D:\\Archives')
                self.assertFalse(scanner.is_unsafe_path(Path('D:\\Archives')))

    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner.is_unsafe_path')
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.resolve')
    def test_scan_directory_blocks_unsafe(self, mock_resolve, mock_is_dir, mock_exists, mock_is_unsafe):
        """Test that scan_directory blocks unsafe paths."""
        scanner = ArchiveScanner()
        mock_resolve.return_value = Path('/etc')
        mock_is_unsafe.return_value = True

        result = scanner.scan_directory('/etc')

        self.assertIn('error', result)
        self.assertIn('Security risk', result['error'])
        self.assertTrue(mock_is_unsafe.called)

    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner.is_unsafe_path')
    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.is_dir', return_value=True)
    @patch('pathlib.Path.resolve')
    @patch('cognitive_tribunal.modules.archive_scanner.ArchiveScanner._scan_recursive')
    def test_scan_directory_allows_safe(self, mock_scan_rec, mock_resolve, mock_is_dir, mock_exists, mock_is_unsafe):
        """Test that scan_directory allows safe paths."""
        scanner = ArchiveScanner()
        mock_resolve.return_value = Path('/home/user/safe')
        mock_is_unsafe.return_value = False

        result = scanner.scan_directory('/home/user/safe')

        # Should not return error about security
        if 'error' in result:
            self.assertNotIn('Security risk', result['error'])

        self.assertTrue(mock_scan_rec.called)

if __name__ == '__main__':
    unittest.main()
