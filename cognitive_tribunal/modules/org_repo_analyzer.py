"""
Module 4: Org Repo Analyzer
Analyzes organization repositories for status and dependencies.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta

from ..utils.github_utils import GitHubClient, classify_repo_type


class OrgRepoAnalyzer:
    """
    Analyzes organization GitHub repositories.
    Focuses on status, dependencies, and organizational health.
    """
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the org repo analyzer.
        
        Args:
            github_token: GitHub personal access token
        """
        self.github_client = GitHubClient(github_token)
        self.repositories: List[Dict] = []
        self.stats = {
            'total_repos': 0,
            'by_type': {},
            'by_language': {},
            'by_status': {},
            'total_open_issues': 0,
        }
    
    def analyze_org_repos(self, org_name: str) -> Dict:
        """
        Analyze all repositories for an organization.
        
        Args:
            org_name: GitHub organization name
            
        Returns:
            Analysis results
        """
        print(f"Fetching repositories for organization: {org_name}...")
        
        repos = self.github_client.get_org_repos(org_name)
        
        if not repos:
            return {'error': f'No repositories found for organization: {org_name}'}
        
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
        
        # Determine status
        status = self._determine_repo_status(repo_details)
        repo_details['status'] = status
        
        # Get recent commits
        commits = self.github_client.get_repo_commits(repo, max_count=10)
        repo_details['recent_commits'] = commits[:3]  # Store only 3 most recent
        repo_details['commit_count'] = len(commits)
        
        # Get dependencies
        dependencies = self.github_client.get_repo_dependencies(repo)
        if dependencies:
            repo_details['dependencies'] = dependencies
            repo_details['dependency_files'] = list(dependencies.keys())
        
        # Activity analysis
        activity = self.github_client.analyze_repo_activity(repo)
        repo_details['activity'] = activity
        
        return repo_details
    
    def _determine_repo_status(self, repo_details: Dict) -> str:
        """
        Determine the status of a repository.
        
        Returns: active, stale, archived, or abandoned
        """
        if repo_details.get('is_archived'):
            return 'archived'
        
        # Check last update time
        updated_at = repo_details.get('updated_at')
        if updated_at:
            try:
                update_time = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
                days_since_update = (datetime.now(update_time.tzinfo) - update_time).days
                
                if days_since_update < 30:
                    return 'active'
                elif days_since_update < 180:
                    return 'stale'
                else:
                    return 'abandoned'
            except:
                pass
        
        return 'unknown'
    
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
        
        # Count by status
        self.stats['by_status'] = {}
        for repo in self.repositories:
            status = repo.get('status', 'unknown')
            self.stats['by_status'][status] = self.stats['by_status'].get(status, 0) + 1
        
        # Count open issues
        self.stats['total_open_issues'] = sum(repo.get('open_issues', 0) for repo in self.repositories)
    
    def get_results(self) -> Dict:
        """Get comprehensive analysis results."""
        return {
            'stats': self.stats,
            'repositories': self.repositories,
            'analysis_timestamp': datetime.now().isoformat(),
        }
    
    def get_repos_by_status(self, status: str) -> List[Dict]:
        """Get repositories by status."""
        return [repo for repo in self.repositories if repo.get('status') == status]
    
    def get_active_repos(self) -> List[Dict]:
        """Get active repositories."""
        return self.get_repos_by_status('active')
    
    def get_stale_repos(self) -> List[Dict]:
        """Get stale repositories."""
        return self.get_repos_by_status('stale')
    
    def get_archived_repos(self) -> List[Dict]:
        """Get archived repositories."""
        return self.get_repos_by_status('archived')
    
    def get_abandoned_repos(self) -> List[Dict]:
        """Get abandoned repositories."""
        return self.get_repos_by_status('abandoned')
    
    def get_repos_with_issues(self) -> List[Dict]:
        """Get repositories with open issues."""
        return [repo for repo in self.repositories if repo.get('open_issues', 0) > 0]
    
    def get_dependency_summary(self) -> Dict[str, List[str]]:
        """
        Get summary of all dependencies across repositories.
        
        Returns:
            Dictionary mapping dependency type to list of repos using it
        """
        dep_summary = {}
        
        for repo in self.repositories:
            dependencies = repo.get('dependencies', {})
            for dep_file, deps in dependencies.items():
                if dep_file not in dep_summary:
                    dep_summary[dep_file] = []
                dep_summary[dep_file].append(repo['name'])
        
        return dep_summary
    
    def generate_health_report(self) -> Dict:
        """
        Generate a health report for the organization.
        
        Returns:
            Organization health metrics and recommendations
        """
        active = self.get_active_repos()
        stale = self.get_stale_repos()
        abandoned = self.get_abandoned_repos()
        archived = self.get_archived_repos()
        with_issues = self.get_repos_with_issues()
        
        # Calculate health score (0-100)
        total = len(self.repositories)
        if total == 0:
            health_score = 0
        else:
            active_score = (len(active) / total) * 50
            stale_penalty = (len(stale) / total) * 20
            abandoned_penalty = (len(abandoned) / total) * 30
            health_score = max(0, min(100, active_score - stale_penalty - abandoned_penalty))
        
        return {
            'health_score': round(health_score, 2),
            'summary': {
                'total_repos': total,
                'active': len(active),
                'stale': len(stale),
                'abandoned': len(abandoned),
                'archived': len(archived),
                'with_open_issues': len(with_issues),
                'total_open_issues': self.stats['total_open_issues'],
            },
            'recommendations': {
                'needs_attention': [
                    {
                        'name': repo['name'],
                        'reason': f"Stale: No updates in {self._days_since_update(repo)} days",
                        'url': repo['url'],
                        'open_issues': repo.get('open_issues', 0),
                    }
                    for repo in stale[:10]
                ],
                'consider_archiving': [
                    {
                        'name': repo['name'],
                        'reason': f"Abandoned: No updates in {self._days_since_update(repo)} days",
                        'url': repo['url'],
                    }
                    for repo in abandoned[:10]
                ],
                'active_projects': [
                    {
                        'name': repo['name'],
                        'language': repo.get('language'),
                        'stars': repo.get('stars', 0),
                        'url': repo['url'],
                        'open_issues': repo.get('open_issues', 0),
                    }
                    for repo in active[:10]
                ],
            },
            'dependency_summary': self.get_dependency_summary(),
            'timestamp': datetime.now().isoformat(),
        }
    
    def _days_since_update(self, repo: Dict) -> int:
        """Calculate days since last update."""
        updated_at = repo.get('updated_at')
        if not updated_at:
            return -1
        
        try:
            update_time = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            return (datetime.now(update_time.tzinfo) - update_time).days
        except:
            return -1
    
    def generate_migration_plan(self) -> Dict:
        """
        Generate a migration plan for repositories.
        
        Returns:
            Migration recommendations and priorities
        """
        abandoned = self.get_abandoned_repos()
        stale = self.get_stale_repos()
        
        plan = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'no_action_needed': [],
        }
        
        # High priority: abandoned with dependencies or issues
        for repo in abandoned:
            if repo.get('open_issues', 0) > 0 or repo.get('dependencies'):
                plan['high_priority'].append({
                    'name': repo['name'],
                    'action': 'Archive or revive',
                    'reason': 'Abandoned with dependencies or open issues',
                    'url': repo['url'],
                })
        
        # Medium priority: stale repos
        for repo in stale:
            plan['medium_priority'].append({
                'name': repo['name'],
                'action': 'Review and update',
                'reason': 'Stale - needs attention',
                'url': repo['url'],
            })
        
        # Active repos need no action
        for repo in self.get_active_repos():
            plan['no_action_needed'].append({
                'name': repo['name'],
                'status': 'Active and healthy',
                'url': repo['url'],
            })
        
        return {
            'plan': plan,
            'summary': {
                'high_priority': len(plan['high_priority']),
                'medium_priority': len(plan['medium_priority']),
                'low_priority': len(plan['low_priority']),
                'no_action_needed': len(plan['no_action_needed']),
            },
            'timestamp': datetime.now().isoformat(),
        }
