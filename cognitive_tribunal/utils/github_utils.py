"""
GitHub utilities for the Cognitive Tribunal project.
Provides GitHub API wrapper and repository analysis functions.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import os

try:
    from github import Github, Repository, GithubException
    from github.Repository import Repository as RepoType
except ImportError:
    # Graceful degradation if PyGithub not installed
    Github = None
    Repository = None
    GithubException = Exception
    RepoType = Any


class GitHubClient:
    """Wrapper for GitHub API operations."""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub personal access token (optional, uses env var if not provided)
        """
        if Github is None:
            raise ImportError("PyGithub is required. Install with: pip install PyGithub")
        
        token = token or os.environ.get('GITHUB_TOKEN')
        self.client = Github(token) if token else Github()
        self.user = self.client.get_user() if token else None
    
    def get_user_repos(self, username: Optional[str] = None) -> List[RepoType]:
        """
        Get all repositories for a user.
        
        Args:
            username: GitHub username (uses authenticated user if not provided)
            
        Returns:
            List of repository objects
        """
        try:
            if username:
                user = self.client.get_user(username)
            else:
                user = self.user or self.client.get_user()
            
            return list(user.get_repos())
        except GithubException as e:
            print(f"Error fetching user repos: {e}")
            return []
    
    def get_org_repos(self, org_name: str) -> List[RepoType]:
        """
        Get all repositories for an organization.
        
        Args:
            org_name: Organization name
            
        Returns:
            List of repository objects
        """
        try:
            org = self.client.get_organization(org_name)
            return list(org.get_repos())
        except GithubException as e:
            print(f"Error fetching org repos: {e}")
            return []
    
    def get_repo_details(self, repo: RepoType) -> Dict:
        """
        Extract detailed information from a repository.
        
        Args:
            repo: GitHub repository object
            
        Returns:
            Dictionary containing repository details
        """
        try:
            return {
                'name': repo.name,
                'full_name': repo.full_name,
                'description': repo.description,
                'url': repo.html_url,
                'clone_url': repo.clone_url,
                'is_fork': repo.fork,
                'is_private': repo.private,
                'is_archived': repo.archived,
                'is_template': repo.is_template,
                'default_branch': repo.default_branch,
                'language': repo.language,
                'languages': repo.get_languages(),
                'size': repo.size,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'watchers': repo.watchers_count,
                'open_issues': repo.open_issues_count,
                'created_at': repo.created_at.isoformat() if repo.created_at else None,
                'updated_at': repo.updated_at.isoformat() if repo.updated_at else None,
                'pushed_at': repo.pushed_at.isoformat() if repo.pushed_at else None,
                'topics': repo.get_topics(),
                'has_wiki': repo.has_wiki,
                'has_issues': repo.has_issues,
                'has_projects': repo.has_projects,
                'license': repo.license.name if repo.license else None,
            }
        except Exception as e:
            return {
                'name': repo.name,
                'full_name': repo.full_name,
                'error': str(e),
            }
    
    def get_parent_repo(self, repo: RepoType) -> Optional[Dict]:
        """
        Get parent repository if this is a fork.
        
        Args:
            repo: GitHub repository object
            
        Returns:
            Parent repository details or None
        """
        if not repo.fork:
            return None
        
        try:
            parent = repo.parent
            return {
                'name': parent.name,
                'full_name': parent.full_name,
                'url': parent.html_url,
                'owner': parent.owner.login,
            }
        except Exception:
            return None
    
    def get_repo_commits(self, repo: RepoType, since: Optional[datetime] = None, max_count: int = 100) -> List[Dict]:
        """
        Get recent commits from a repository.
        
        Args:
            repo: GitHub repository object
            since: Only get commits after this date
            max_count: Maximum number of commits to fetch
            
        Returns:
            List of commit information
        """
        try:
            commits = repo.get_commits(since=since)
            commit_list = []
            
            for i, commit in enumerate(commits):
                if i >= max_count:
                    break
                
                commit_list.append({
                    'sha': commit.sha,
                    'message': commit.commit.message,
                    'author': commit.commit.author.name if commit.commit.author else 'Unknown',
                    'date': commit.commit.author.date.isoformat() if commit.commit.author else None,
                    'url': commit.html_url,
                })
            
            return commit_list
        except Exception as e:
            print(f"Error fetching commits: {e}")
            return []
    
    def get_repo_dependencies(self, repo: RepoType) -> Dict[str, List[str]]:
        """
        Attempt to extract dependencies from common package files.
        
        Args:
            repo: GitHub repository object
            
        Returns:
            Dictionary mapping dependency file to list of dependencies
        """
        dependencies = {}
        
        # Common dependency files
        dep_files = [
            'requirements.txt',
            'package.json',
            'Pipfile',
            'Gemfile',
            'go.mod',
            'Cargo.toml',
            'pom.xml',
            'build.gradle',
        ]
        
        for dep_file in dep_files:
            try:
                content = repo.get_contents(dep_file)
                dependencies[dep_file] = content.decoded_content.decode('utf-8').split('\n')
            except:
                # File doesn't exist, skip
                continue
        
        return dependencies
    
    def analyze_repo_activity(self, repo: RepoType) -> Dict:
        """
        Analyze repository activity and health.
        
        Args:
            repo: GitHub repository object
            
        Returns:
            Activity metrics
        """
        try:
            recent_commits = self.get_repo_commits(repo, max_count=10)
            
            return {
                'recent_commits_count': len(recent_commits),
                'last_commit_date': recent_commits[0]['date'] if recent_commits else None,
                'is_active': len(recent_commits) > 0,
                'open_issues': repo.open_issues_count,
                'is_archived': repo.archived,
            }
        except Exception as e:
            return {
                'error': str(e),
            }


def classify_repo_type(repo_details: Dict) -> str:
    """
    Classify repository type based on its characteristics.
    
    Args:
        repo_details: Repository details dictionary
        
    Returns:
        Repository type classification
    """
    if repo_details.get('is_fork'):
        return 'fork'
    elif repo_details.get('is_template'):
        return 'template'
    elif repo_details.get('is_archived'):
        return 'archived'
    elif repo_details.get('is_private'):
        return 'private-original'
    else:
        return 'public-original'


def detect_modifications(repo_details: Dict, commits: List[Dict]) -> Dict:
    """
    Detect if a forked repository has been modified.
    
    Args:
        repo_details: Repository details
        commits: List of commits
        
    Returns:
        Modification analysis
    """
    if not repo_details.get('is_fork'):
        return {'is_fork': False, 'has_modifications': False}
    
    # Simple heuristic: if there are commits and the repo was updated after creation
    created_at = repo_details.get('created_at')
    updated_at = repo_details.get('updated_at')
    pushed_at = repo_details.get('pushed_at')
    
    has_own_commits = len(commits) > 0
    has_updates = pushed_at and created_at and pushed_at > created_at
    
    return {
        'is_fork': True,
        'has_modifications': has_own_commits or has_updates,
        'commit_count': len(commits),
        'appears_active': has_own_commits,
    }
