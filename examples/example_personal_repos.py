#!/usr/bin/env python3
"""
Example: Personal Repo Analyzer Usage
Demonstrates how to use the Personal Repo Analyzer module programmatically.
"""

import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cognitive_tribunal.modules.personal_repo_analyzer import PersonalRepoAnalyzer


def main():
    print("Personal Repo Analyzer Example")
    print("=" * 70)
    
    # Get GitHub token from environment
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("\nNote: No GITHUB_TOKEN found. Using unauthenticated API (lower rate limits)")
        print("Set GITHUB_TOKEN environment variable for better performance.\n")
    
    # Create analyzer instance
    analyzer = PersonalRepoAnalyzer(github_token=github_token)
    
    # Analyze repos (will use authenticated user if token is provided)
    print("\nFetching and analyzing repositories...")
    
    try:
        results = analyzer.analyze_user_repos()  # No username = use authenticated user
        
        # Display results
        print("\n" + "=" * 70)
        print("ANALYSIS RESULTS")
        print("=" * 70)
        
        stats = results.get('stats', {})
        print(f"\nTotal repositories: {stats.get('total_repos', 0)}")
        print(f"Total stars: {stats.get('total_stars', 0)}")
        print(f"Total forks: {stats.get('total_forks', 0)}")
        
        print("\nRepositories by type:")
        for repo_type, count in stats.get('by_type', {}).items():
            print(f"  {repo_type}: {count}")
        
        print("\nRepositories by language:")
        for language, count in sorted(stats.get('by_language', {}).items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {language}: {count}")
        
        # Show forks info
        forks = analyzer.get_forks()
        modified_forks = analyzer.get_modified_forks()
        unmodified_forks = analyzer.get_unmodified_forks()
        
        print(f"\nForks analysis:")
        print(f"  Total forks: {len(forks)}")
        print(f"  Modified forks: {len(modified_forks)}")
        print(f"  Unmodified forks: {len(unmodified_forks)}")
        
        # Show triage report
        print("\n" + "=" * 70)
        print("TRIAGE RECOMMENDATIONS")
        print("=" * 70)
        
        triage = analyzer.generate_triage_report()
        summary = triage.get('summary', {})
        
        print(f"\nTotal repos: {summary.get('total_repos', 0)}")
        print(f"Forks: {summary.get('forks', 0)}")
        print(f"Modified forks: {summary.get('modified_forks', 0)}")
        print(f"Unmodified forks: {summary.get('unmodified_forks', 0)}")
        print(f"Archived: {summary.get('archived', 0)}")
        
        # Show recommendations
        recommendations = triage.get('recommendations', {})
        
        consider_deleting = recommendations.get('consider_deleting', [])
        if consider_deleting:
            print(f"\nConsider deleting ({len(consider_deleting)} repos):")
            for repo in consider_deleting[:3]:
                print(f"  - {repo['name']}: {repo['reason']}")
        
        consider_archiving = recommendations.get('consider_archiving', [])
        if consider_archiving:
            print(f"\nConsider archiving ({len(consider_archiving)} repos):")
            for repo in consider_archiving[:3]:
                print(f"  - {repo['name']}: {repo['reason']}")
        
        active_projects = recommendations.get('active_projects', [])
        if active_projects:
            print(f"\nActive projects ({len(active_projects)} repos):")
            for repo in active_projects[:3]:
                print(f"  - {repo['name']} ({repo.get('language', 'Unknown')}): ⭐ {repo.get('stars', 0)}")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you have a valid GitHub token set in GITHUB_TOKEN environment variable")
        return
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
