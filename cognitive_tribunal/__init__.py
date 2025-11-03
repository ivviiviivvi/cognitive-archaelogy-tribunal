"""
Cognitive Archaeology Tribunal
A comprehensive archaeological dig tool for multi-layer cognitive ecosystems.
"""

__version__ = "0.1.0"
__author__ = "Cognitive Tribunal Team"

from .modules.archive_scanner import ArchiveScanner
from .modules.ai_context_aggregator import AIContextAggregator
from .modules.personal_repo_analyzer import PersonalRepoAnalyzer
from .modules.org_repo_analyzer import OrgRepoAnalyzer

__all__ = [
    "ArchiveScanner",
    "AIContextAggregator", 
    "PersonalRepoAnalyzer",
    "OrgRepoAnalyzer",
]
