#!/usr/bin/env python3
"""
Example: Archive Scanner Usage
Demonstrates how to use the Archive Scanner module programmatically.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner


def main():
    print("Archive Scanner Example")
    print("=" * 70)
    
    # Create scanner instance
    scanner = ArchiveScanner(exclude_patterns=[
        '__pycache__',
        '.git',
        'node_modules',
        '*.tmp',
    ])
    
    # Scan a directory (use current directory as example)
    scan_path = Path.cwd()
    print(f"\nScanning: {scan_path}")
    
    results = scanner.scan_directory(str(scan_path), recursive=True, max_depth=2)
    
    # Display results
    print("\n" + "=" * 70)
    print("SCAN RESULTS")
    print("=" * 70)
    
    stats = results.get('stats', {})
    print(f"\nTotal files: {stats.get('total_files', 0)}")
    print(f"Total size: {stats.get('total_size', 0):,} bytes")
    
    print("\nFiles by category:")
    for category, count in stats.get('by_category', {}).items():
        print(f"  {category}: {count}")
    
    # Deduplication info
    dedup = results.get('deduplication', {})
    dedup_stats = dedup.get('stats', {})
    
    print(f"\nDeduplication:")
    print(f"  Total files: {dedup_stats.get('total_files', 0)}")
    print(f"  Duplicate groups: {dedup_stats.get('duplicate_groups', 0)}")
    print(f"  Duplicate files: {dedup_stats.get('duplicate_files', 0)}")
    print(f"  Potential space savings: {dedup.get('potential_space_savings', 0):,} bytes")
    
    # Show some large files
    large_files = scanner.get_large_files(min_size_mb=0.1)  # Files > 0.1 MB
    if large_files:
        print(f"\nLarge files (> 0.1 MB): {len(large_files)}")
        for file in large_files[:5]:
            print(f"  - {file['name']}: {file['size']:,} bytes")
    
    # Show files by category
    code_files = scanner.get_files_by_category('code')
    if code_files:
        print(f"\nCode files: {len(code_files)}")
        for file in code_files[:5]:
            print(f"  - {file['name']}")
    
    # Errors
    errors = stats.get('errors', [])
    if errors:
        print(f"\nErrors encountered: {len(errors)}")
        for error in errors[:5]:
            print(f"  - {error}")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
