"""
Module 3: Personal Repo Analyzer
Analyzes personal GitHub repositories, classifying forks vs originals and tracking modifications.
"""

from typing import Dict, List, Optional
from datetime import datetime

from ..utils.github_utils import (
    GitHubClient, classify_repo_type, detect_modifications
)


class PersonalRepoAnalyzer:
    """
    Analyzes personal GitHub repositories.
    Identifies forks, originals, and tracks modifications.
    """
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the personal repo analyzer.
        
        Args:
            github_token: GitHub personal access token
        """
        self.github_client = GitHubClient(github_token)
        self.repositories: List[Dict] = []
        self.stats = {
            'total_repos': 0,
            'by_type': {},
            'by_language': {},
            'total_stars': 0,
            'total_forks': 0,
        }
    
    def analyze_user_repos(self, username: Optional[str] = None) -> Dict:
        """
        Analyze all repositories for a user.
        
        Args:
            username: GitHub username (uses authenticated user if not provided)
            
        Returns:
            Analysis results
        """
        print(f"Fetching repositories for user: {username or 'authenticated user'}...")
        
        repos = self.github_client.get_user_repos(username)
        
        if not repos:
            return {'error': 'No repositories found or authentication failed'}
        
        print(f"Found {len(repos)} repositories. Analyzing...")
        
        self.repositories = []
        
        for repo in repos:
            print(f"  Analyzing: {repo.full_name}")
            repo_info = self._analyze_repository(repo)
            self.repositories.append(repo_info)
        
        self._update_stats()
        
        return self.get_results()
    
    def _analyze_repository(self, repo) -> Dict:
        """Analyze a single repository."""
        # Get basic details
        repo_details = self.github_client.get_repo_details(repo)
        
        # Classify type
        repo_type = classify_repo_type(repo_details)
        repo_details['repo_type'] = repo_type
        
        # Get commits for modification detection
        commits = self.github_client.get_repo_commits(repo, max_count=50)
        repo_details['recent_commits'] = commits[:5]  # Store only 5 most recent
        repo_details['commit_count'] = len(commits)
        
        # For forks, get parent info and detect modifications
        if repo_details.get('is_fork'):
            parent = self.github_client.get_parent_repo(repo)
            repo_details['parent'] = parent
            
            modifications = detect_modifications(repo_details, commits)
            repo_details['modifications'] = modifications
        
        # Get dependencies
        dependencies = self.github_client.get_repo_dependencies(repo)
        if dependencies:
            repo_details['dependencies'] = dependencies
        
        # Activity analysis
        activity = self.github_client.analyze_repo_activity(repo)
        repo_details['activity'] = activity
        
        return repo_details
    
    def _update_stats(self):
        """Update statistics after analysis."""
        self.stats['total_repos'] = len(self.repositories)
        
        # Count by type
        self.stats['by_type'] = {}
        for repo in self.repositories:
            repo_type = repo.get('repo_type', 'unknown')
            self.stats['by_type'][repo_type] = self.stats['by_type'].get(repo_type, 0) + 1
        
        # Count by language
        self.stats['by_language'] = {}
        for repo in self.repositories:
            language = repo.get('language') or 'Unknown'
            self.stats['by_language'][language] = self.stats['by_language'].get(language, 0) + 1
        
        # Aggregate stars and forks
        self.stats['total_stars'] = sum(repo.get('stars', 0) for repo in self.repositories)
        self.stats['total_forks'] = sum(repo.get('forks', 0) for repo in self.repositories)
    
    def get_results(self) -> Dict:
        """Get comprehensive analysis results."""
        return {
            'stats': self.stats,
            'repositories': self.repositories,
            'analysis_timestamp': datetime.now().isoformat(),
        }
    
    def get_forks(self) -> List[Dict]:
        """Get all forked repositories."""
        return [repo for repo in self.repositories if repo.get('is_fork')]
    
    def get_originals(self) -> List[Dict]:
        """Get all original (non-fork) repositories."""
        return [repo for repo in self.repositories if not repo.get('is_fork')]
    
    def get_modified_forks(self) -> List[Dict]:
        """Get forks that have been modified."""
        modified = []
        for repo in self.repositories:
            if repo.get('is_fork'):
                modifications = repo.get('modifications', {})
                if modifications.get('has_modifications'):
                    modified.append(repo)
        return modified
    
    def get_unmodified_forks(self) -> List[Dict]:
        """Get forks that haven't been modified."""
        unmodified = []
        for repo in self.repositories:
            if repo.get('is_fork'):
                modifications = repo.get('modifications', {})
                if not modifications.get('has_modifications'):
                    unmodified.append(repo)
        return unmodified
    
    def get_archived_repos(self) -> List[Dict]:
        """Get archived repositories."""
        return [repo for repo in self.repositories if repo.get('is_archived')]
    
    def get_active_repos(self) -> List[Dict]:
        """Get recently active repositories."""
        active = []
        for repo in self.repositories:
            activity = repo.get('activity', {})
            if activity.get('is_active') and not repo.get('is_archived'):
                active.append(repo)
        return active
    
    def get_repos_by_language(self, language: str) -> List[Dict]:
        """Get repositories by programming language."""
        return [repo for repo in self.repositories if repo.get('language') == language]
    
    def generate_triage_report(self) -> Dict:
        """
        Generate a triage report for personal repositories.
        
        Returns:
            Triage recommendations
        """
        forks = self.get_forks()
        modified_forks = self.get_modified_forks()
        unmodified_forks = self.get_unmodified_forks()
        archived = self.get_archived_repos()
        
        return {
            'summary': {
                'total_repos': len(self.repositories),
                'forks': len(forks),
                'modified_forks': len(modified_forks),
                'unmodified_forks': len(unmodified_forks),
                'archived': len(archived),
            },
            'recommendations': {
                'consider_deleting': [
                    {
                        'name': repo['name'],
                        'reason': 'Unmodified fork - can be re-forked if needed',
                        'url': repo['url'],
                    }
                    for repo in unmodified_forks[:10]  # Top 10
                ],
                'consider_archiving': [
                    {
                        'name': repo['name'],
                        'reason': 'No recent activity',
                        'url': repo['url'],
                        'last_update': repo.get('updated_at'),
                    }
                    for repo in self.repositories
                    if not repo.get('is_archived') 
                    and not repo.get('activity', {}).get('is_active')
                ][:10],  # Top 10
                'active_projects': [
                    {
                        'name': repo['name'],
                        'language': repo.get('language'),
                        'stars': repo.get('stars', 0),
                        'url': repo['url'],
                    }
                    for repo in self.get_active_repos()
                ],
            },
            'timestamp': datetime.now().isoformat(),
        }
