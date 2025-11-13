"""
Unified inventory generator.
Combines results from all modules into a single JSON inventory.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class InventoryGenerator:
    """
    Generates unified inventory from all audit modules.
    """
    
    def __init__(self):
        """Initialize inventory generator."""
        self.inventory: Dict[str, Any] = {
            'metadata': {
                'generated_at': None,
                'version': '1.0',
            },
            'archives': {},
            'ai_conversations': {},
            'personal_repos': {},
            'org_repos': {},
            'web_bookmarks': {},
        }
    
    def add_web_bookmark_results(self, results: Dict):
        """Add web bookmark analyzer results to inventory."""
        self.inventory['web_bookmarks'] = results

    def add_archive_results(self, results: Dict):
        """Add archive scanner results to inventory."""
        self.inventory['archives'] = results
    
    def add_ai_context_results(self, results: Dict):
        """Add AI context aggregator results to inventory."""
        self.inventory['ai_conversations'] = results
    
    def add_personal_repo_results(self, results: Dict):
        """Add personal repo analyzer results to inventory."""
        self.inventory['personal_repos'] = results
    
    def add_org_repo_results(self, results: Dict):
        """Add org repo analyzer results to inventory."""
        self.inventory['org_repos'] = results
    
    def generate(self) -> Dict:
        """
        Generate the unified inventory.
        
        Returns:
            Complete inventory dictionary
        """
        self.inventory['metadata']['generated_at'] = datetime.now().isoformat()
        
        # Add summary statistics
        self.inventory['summary'] = self._generate_summary()
        
        return self.inventory
    
    def _generate_summary(self) -> Dict:
        """Generate summary statistics across all modules."""
        summary = {}
        
        # Archive summary
        if self.inventory['archives']:
            archive_stats = self.inventory['archives'].get('stats', {})
            summary['archives'] = {
                'total_files': archive_stats.get('total_files', 0),
                'total_size_bytes': archive_stats.get('total_size', 0),
                'categories': len(archive_stats.get('by_category', {})),
            }
        
        # AI conversations summary
        if self.inventory['ai_conversations']:
            ai_stats = self.inventory['ai_conversations'].get('stats', {})
            summary['ai_conversations'] = {
                'total_conversations': ai_stats.get('total_conversations', 0),
                'total_messages': ai_stats.get('total_messages', 0),
                'sources': len(ai_stats.get('by_source', {})),
            }
        
        # Personal repos summary
        if self.inventory['personal_repos']:
            personal_stats = self.inventory['personal_repos'].get('stats', {})
            summary['personal_repos'] = {
                'total_repos': personal_stats.get('total_repos', 0),
                'types': personal_stats.get('by_type', {}),
            }
        
        # Org repos summary
        if self.inventory['org_repos']:
            org_stats = self.inventory['org_repos'].get('stats', {})
            summary['org_repos'] = {
                'total_repos': org_stats.get('total_repos', 0),
                'by_status': org_stats.get('by_status', {}),
            }

        # Web bookmarks summary
        if self.inventory['web_bookmarks']:
            bookmark_stats = self.inventory['web_bookmarks'].get('stats', {})
            summary['web_bookmarks'] = {
                'total_bookmarks': bookmark_stats.get('total_bookmarks', 0),
            }
        
        return summary
    
    def save_to_file(self, output_path: str, pretty: bool = True) -> bool:
        """
        Save inventory to JSON file.
        
        Args:
            output_path: Path to output file
            pretty: Whether to pretty-print JSON
            
        Returns:
            Success status
        """
        try:
            inventory = self.generate()
            
            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(inventory, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(inventory, f, ensure_ascii=False)
            
            print(f"Inventory saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving inventory: {e}")
            return False
    
    def get_inventory(self) -> Dict:
        """Get the current inventory."""
        return self.generate()
