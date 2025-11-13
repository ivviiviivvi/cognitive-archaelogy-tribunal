"""
Triage report generator.
Generates actionable triage reports from audit results.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class TriageReportGenerator:
    """
    Generates triage reports with actionable recommendations.
    """
    
    def __init__(self):
        """Initialize triage report generator."""
        self.report: Dict[str, Any] = {
            'metadata': {
                'generated_at': None,
                'version': '1.0',
            },
            'archives': {},
            'ai_conversations': {},
            'personal_repos': {},
            'org_repos': {},
            'web_bookmarks': {},
            'priorities': {
                'high': [],
                'medium': [],
                'low': [],
            },
        }
    
    def add_archive_triage(self, archive_data: Dict):
        """Add archive triage information."""
        if not archive_data:
            return
        
        triage = {
            'duplicates_found': 0,
            'space_wasted': 0,
            'recommendations': [],
        }
        
        # Extract deduplication info
        dedup = archive_data.get('deduplication', {})
        if dedup:
            stats = dedup.get('stats', {})
            triage['duplicates_found'] = stats.get('duplicate_files', 0)
            triage['space_wasted'] = dedup.get('potential_space_savings', 0)
            
            if triage['duplicates_found'] > 0:
                triage['recommendations'].append({
                    'priority': 'high',
                    'action': 'Remove duplicate files',
                    'impact': f"Save {self._format_bytes(triage['space_wasted'])}",
                    'count': triage['duplicates_found'],
                })
                
                self.report['priorities']['high'].append({
                    'category': 'archives',
                    'item': 'Duplicate files',
                    'action': 'Review and remove duplicates',
                    'impact': f"{triage['duplicates_found']} duplicates, {self._format_bytes(triage['space_wasted'])} wasted",
                })
        
        self.report['archives'] = triage
    
    def add_ai_context_triage(self, ai_data: Dict):
        """Add AI context triage information."""
        if not ai_data:
            return
        
        stats = ai_data.get('stats', {})
        
        triage = {
            'total_conversations': stats.get('total_conversations', 0),
            'total_messages': stats.get('total_messages', 0),
            'recommendations': [],
        }
        
        # Recommendations based on conversation count
        if triage['total_conversations'] > 100:
            triage['recommendations'].append({
                'priority': 'medium',
                'action': 'Organize conversations by topic',
                'impact': 'Improve searchability and context retrieval',
            })
            
            self.report['priorities']['medium'].append({
                'category': 'ai_conversations',
                'item': 'Large conversation archive',
                'action': 'Organize and categorize conversations',
                'impact': f"{triage['total_conversations']} conversations to organize",
            })
        
        self.report['ai_conversations'] = triage
    
    def add_personal_repo_triage(self, repo_data: Dict):
        """Add personal repository triage information."""
        if not repo_data:
            return
        
        repos = repo_data.get('repositories', [])
        
        # Count different types
        unmodified_forks = [r for r in repos if r.get('is_fork') and not r.get('modifications', {}).get('has_modifications')]
        archived = [r for r in repos if r.get('is_archived')]
        inactive = [r for r in repos if not r.get('activity', {}).get('is_active') and not r.get('is_archived')]
        
        triage = {
            'total_repos': len(repos),
            'unmodified_forks': len(unmodified_forks),
            'archived': len(archived),
            'inactive': len(inactive),
            'recommendations': [],
        }
        
        # Add recommendations
        if unmodified_forks:
            triage['recommendations'].append({
                'priority': 'medium',
                'action': 'Consider deleting unmodified forks',
                'impact': f"Clean up {len(unmodified_forks)} unused forks",
                'repos': [r['name'] for r in unmodified_forks[:5]],
            })
            
            self.report['priorities']['medium'].append({
                'category': 'personal_repos',
                'item': 'Unmodified forks',
                'action': 'Delete unnecessary forks',
                'impact': f"{len(unmodified_forks)} repos can be removed",
            })
        
        if inactive:
            triage['recommendations'].append({
                'priority': 'low',
                'action': 'Archive inactive repositories',
                'impact': f"Archive {len(inactive)} inactive projects",
                'repos': [r['name'] for r in inactive[:5]],
            })
            
            self.report['priorities']['low'].append({
                'category': 'personal_repos',
                'item': 'Inactive repositories',
                'action': 'Archive or revive inactive projects',
                'impact': f"{len(inactive)} inactive repos",
            })
        
        self.report['personal_repos'] = triage
    
    def add_org_repo_triage(self, org_data: Dict):
        """Add organization repository triage information."""
        if not org_data:
            return
        
        stats = org_data.get('stats', {})
        by_status = stats.get('by_status', {})
        
        triage = {
            'total_repos': stats.get('total_repos', 0),
            'by_status': by_status,
            'total_open_issues': stats.get('total_open_issues', 0),
            'recommendations': [],
        }
        
        # Add recommendations based on status
        abandoned_count = by_status.get('abandoned', 0)
        if abandoned_count > 0:
            triage['recommendations'].append({
                'priority': 'high',
                'action': 'Address abandoned repositories',
                'impact': f"Archive or revive {abandoned_count} abandoned repos",
            })
            
            self.report['priorities']['high'].append({
                'category': 'org_repos',
                'item': 'Abandoned repositories',
                'action': 'Archive or assign owners',
                'impact': f"{abandoned_count} repos need attention",
            })
        
        stale_count = by_status.get('stale', 0)
        if stale_count > 0:
            triage['recommendations'].append({
                'priority': 'medium',
                'action': 'Review stale repositories',
                'impact': f"Update or archive {stale_count} stale repos",
            })
            
            self.report['priorities']['medium'].append({
                'category': 'org_repos',
                'item': 'Stale repositories',
                'action': 'Review and update',
                'impact': f"{stale_count} repos need review",
            })
        
        if triage['total_open_issues'] > 50:
            triage['recommendations'].append({
                'priority': 'medium',
                'action': 'Address open issues',
                'impact': f"Review {triage['total_open_issues']} open issues",
            })
        
        self.report['org_repos'] = triage

    def add_web_bookmark_triage(self, bookmark_data: Dict):
        """Add web bookmark triage information."""
        if not bookmark_data:
            return

        stats = bookmark_data.get('stats', {})
        total_bookmarks = stats.get('total_bookmarks', 0)

        triage = {
            'total_bookmarks': total_bookmarks,
            'recommendations': [],
        }

        if total_bookmarks > 200:
            triage['recommendations'].append({
                'priority': 'low',
                'action': 'Review and organize bookmarks',
                'impact': f'Improve usability of {total_bookmarks} bookmarks',
            })

            self.report['priorities']['low'].append({
                'category': 'web_bookmarks',
                'item': 'Large bookmark collection',
                'action': 'Organize bookmarks into folders or tags',
                'impact': f'{total_bookmarks} bookmarks to organize',
            })

        self.report['web_bookmarks'] = triage
    
    def generate(self) -> Dict:
        """
        Generate the complete triage report.
        
        Returns:
            Triage report dictionary
        """
        self.report['metadata']['generated_at'] = datetime.now().isoformat()
        
        # Add summary
        self.report['summary'] = {
            'total_high_priority': len(self.report['priorities']['high']),
            'total_medium_priority': len(self.report['priorities']['medium']),
            'total_low_priority': len(self.report['priorities']['low']),
        }
        
        return self.report
    
    def save_to_file(self, output_path: str, pretty: bool = True) -> bool:
        """
        Save triage report to JSON file.
        
        Args:
            output_path: Path to output file
            pretty: Whether to pretty-print JSON
            
        Returns:
            Success status
        """
        try:
            report = self.generate()
            
            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(report, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(report, f, ensure_ascii=False)
            
            print(f"Triage report saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving triage report: {e}")
            return False
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    def generate_text_report(self) -> str:
        """
        Generate a human-readable text report.
        
        Returns:
            Formatted text report
        """
        report = self.generate()
        lines = []
        
        lines.append("=" * 70)
        lines.append("COGNITIVE ARCHAEOLOGY TRIBUNAL - TRIAGE REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {report['metadata']['generated_at']}")
        lines.append("")
        
        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 70)
        summary = report['summary']
        lines.append(f"  High Priority Items:   {summary['total_high_priority']}")
        lines.append(f"  Medium Priority Items: {summary['total_medium_priority']}")
        lines.append(f"  Low Priority Items:    {summary['total_low_priority']}")
        lines.append("")
        
        # High priority
        if report['priorities']['high']:
            lines.append("HIGH PRIORITY ACTIONS")
            lines.append("-" * 70)
            for item in report['priorities']['high']:
                lines.append(f"  [{item['category'].upper()}] {item['item']}")
                lines.append(f"    Action: {item['action']}")
                lines.append(f"    Impact: {item['impact']}")
                lines.append("")
        
        # Medium priority
        if report['priorities']['medium']:
            lines.append("MEDIUM PRIORITY ACTIONS")
            lines.append("-" * 70)
            for item in report['priorities']['medium']:
                lines.append(f"  [{item['category'].upper()}] {item['item']}")
                lines.append(f"    Action: {item['action']}")
                lines.append(f"    Impact: {item['impact']}")
                lines.append("")
        
        # Low priority
        if report['priorities']['low']:
            lines.append("LOW PRIORITY ACTIONS")
            lines.append("-" * 70)
            for item in report['priorities']['low']:
                lines.append(f"  [{item['category'].upper()}] {item['item']}")
                lines.append(f"    Action: {item['action']}")
                lines.append(f"    Impact: {item['impact']}")
                lines.append("")
        
        lines.append("=" * 70)
        
        return "\n".join(lines)
