"""
Tests for Archive Scanner module.
"""

import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner


def create_test_file(directory: Path, filename: str, content: str):
    """Helper function to create test files."""
    file_path = directory / filename
    file_path.write_text(content)
    return file_path


def test_deduplicator_reset_between_locations():
    """
    Test that the deduplicator is reset between different location scans.
    
    This test verifies that when scanning multiple locations with the same
    ArchiveScanner instance, the deduplicator statistics for each location
    are independent and don't include data from previous locations.
    """
    # Create two temporary directories with identical files
    with tempfile.TemporaryDirectory() as temp_dir1:
        with tempfile.TemporaryDirectory() as temp_dir2:
            dir1 = Path(temp_dir1)
            dir2 = Path(temp_dir2)
            
            # Create identical files in both directories
            content = "This is test content for duplicate detection"
            create_test_file(dir1, "file1.txt", content)
            create_test_file(dir2, "file1.txt", content)
            
            # Scan locations one by one
            scanner = ArchiveScanner()
            
            # Scan first location
            result1 = scanner.scan_directory(str(dir1))
            dedup_stats1 = result1['deduplication']['stats']
            
            # Scan second location - should not include duplicates from first location
            result2 = scanner.scan_directory(str(dir2))
            dedup_stats2 = result2['deduplication']['stats']
            
            # Each location should report only 1 file (no duplicates within location)
            assert dedup_stats1['total_files'] == 1, \
                f"Expected 1 file in location 1, got {dedup_stats1['total_files']}"
            assert dedup_stats1['duplicate_files'] == 0, \
                f"Expected 0 duplicates in location 1, got {dedup_stats1['duplicate_files']}"
            
            assert dedup_stats2['total_files'] == 1, \
                f"Expected 1 file in location 2, got {dedup_stats2['total_files']}"
            assert dedup_stats2['duplicate_files'] == 0, \
                f"Expected 0 duplicates in location 2, got {dedup_stats2['duplicate_files']}"
            
            # If deduplicator is not reset, location 2 would show 2 total_files
            # (1 from current location + 1 from previous location)


def test_scan_multiple_locations_independent():
    """
    Test that scan_multiple_locations produces correct per-location stats.
    
    This test verifies that each location's results are independent and
    don't get contaminated by files from other locations.
    """
    with tempfile.TemporaryDirectory() as temp_dir1:
        with tempfile.TemporaryDirectory() as temp_dir2:
            dir1 = Path(temp_dir1)
            dir2 = Path(temp_dir2)
            
            # Create different files in each directory
            create_test_file(dir1, "file1.txt", "Content for location 1")
            create_test_file(dir1, "file2.txt", "More content for location 1")
            
            create_test_file(dir2, "file3.txt", "Content for location 2")
            
            # Use scan_multiple_locations
            scanner = ArchiveScanner()
            results = scanner.scan_multiple_locations([str(dir1), str(dir2)])
            
            # Check per-location results
            loc1_results = results['locations'][str(dir1)]
            loc2_results = results['locations'][str(dir2)]
            
            # Location 1 should have 2 files
            assert loc1_results['stats']['total_files'] == 2, \
                f"Expected 2 files in location 1, got {loc1_results['stats']['total_files']}"
            
            # Location 2 should have 1 file (not 3 from accumulated state)
            assert loc2_results['stats']['total_files'] == 1, \
                f"Expected 1 file in location 2, got {loc2_results['stats']['total_files']}"
            
            # Deduplication stats for location 2 should only count its own file
            loc2_dedup = loc2_results['deduplication']['stats']
            assert loc2_dedup['total_files'] == 1, \
                f"Expected 1 file in location 2 dedup stats, got {loc2_dedup['total_files']}"


def test_duplicate_detection_within_single_location():
    """
    Test that duplicates within a single location are correctly detected.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)
        
        # Create duplicate files within the same location
        content = "Duplicate content"
        create_test_file(directory, "dup1.txt", content)
        create_test_file(directory, "dup2.txt", content)
        create_test_file(directory, "unique.txt", "Unique content")
        
        scanner = ArchiveScanner()
        result = scanner.scan_directory(str(directory))
        
        # Should have 3 total files
        assert result['stats']['total_files'] == 3
        
        # Should detect 1 duplicate group with 2 files
        dedup_stats = result['deduplication']['stats']
        assert dedup_stats['total_files'] == 3
        assert dedup_stats['duplicate_groups'] == 1
        assert dedup_stats['duplicate_files'] == 1  # 2 files - 1 = 1 duplicate


def test_security_blocks_unsafe_paths():
    """Test that unsafe paths are blocked."""
    scanner = ArchiveScanner()
    scanner._scan_recursive = MagicMock()

    # Test with real paths where possible, but safely.

    # 1. Root "/"
    # This assumes we are on a system where "/" exists.
    if os.name == 'posix':
        result = scanner.scan_directory("/")
        assert 'error' in result
        assert "Security risk" in result['error']
        assert not scanner._scan_recursive.called

    # 2. System Directory "/etc" (Posix)
    if os.name == 'posix' and Path("/etc").exists():
        result = scanner.scan_directory("/etc")
        assert 'error' in result
        assert "Security risk" in result['error']

    # 3. Subdirectory of system dir "/etc/ssh" (if exists)
    # We can fake it if it doesn't exist by mocking exists/is_dir
    with patch('pathlib.Path.exists', return_value=True):
        with patch('pathlib.Path.is_dir', return_value=True):
            if os.name == 'posix':
                result = scanner.scan_directory("/etc/fake_subdir")
                assert 'error' in result
                assert "Security risk" in result['error']


def test_security_allows_safe_paths():
    """Test that safe paths are allowed."""
    with tempfile.TemporaryDirectory() as temp_dir:
        scanner = ArchiveScanner()
        # Create a dummy file
        Path(temp_dir).joinpath("test.txt").touch()

        result = scanner.scan_directory(temp_dir)

        assert 'error' not in result
        assert result['stats']['total_files'] == 1
