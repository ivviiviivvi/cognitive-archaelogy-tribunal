"""
Knowledge graph generator.
Creates a knowledge graph showing relationships between different entities.
"""

from typing import Dict, List, Any, Set, Optional
from datetime import datetime
import json
from pathlib import Path


class KnowledgeGraphGenerator:
    """
    Generates a knowledge graph from audit results.
    Represents entities and their relationships.
    """
    
    def __init__(self):
        """Initialize knowledge graph generator."""
        self.nodes: List[Dict] = []
        self.edges: List[Dict] = []
        self.node_ids: Set[str] = set()
    
    def add_node(self, node_id: str, node_type: str, properties: Dict):
        """
        Add a node to the graph.
        
        Args:
            node_id: Unique identifier for the node
            node_type: Type of node (repo, file, conversation, etc.)
            properties: Node properties
        """
        if node_id not in self.node_ids:
            self.nodes.append({
                'id': node_id,
                'type': node_type,
                'properties': properties,
            })
            self.node_ids.add(node_id)
    
    def add_edge(self, source_id: str, target_id: str, relationship: str, properties: Optional[Dict] = None):
        """
        Add an edge (relationship) to the graph.
        
        Args:
            source_id: Source node ID
            target_id: Target node ID
            relationship: Type of relationship
            properties: Optional edge properties
        """
        self.edges.append({
            'source': source_id,
            'target': target_id,
            'relationship': relationship,
            'properties': properties or {},
        })
    
    def build_from_inventory(self, inventory: Dict):
        """
        Build knowledge graph from unified inventory.
        
        Args:
            inventory: Unified inventory dictionary
        """
        # Process archives
        if 'archives' in inventory:
            self._process_archives(inventory['archives'])
        
        # Process AI conversations
        if 'ai_conversations' in inventory:
            self._process_conversations(inventory['ai_conversations'])
        
        # Process personal repos
        if 'personal_repos' in inventory:
            self._process_personal_repos(inventory['personal_repos'])
        
        # Process org repos
        if 'org_repos' in inventory:
            self._process_org_repos(inventory['org_repos'])
    
    def _process_archives(self, archive_data: Dict):
        """Process archive data into graph nodes and edges."""
        # Add archive root node
        self.add_node('archives', 'collection', {
            'name': 'File Archives',
            'total_files': archive_data.get('stats', {}).get('total_files', 0),
        })
        
        # Add category nodes
        by_category = archive_data.get('stats', {}).get('by_category', {})
        for category, count in by_category.items():
            category_id = f'category_{category}'
            self.add_node(category_id, 'file_category', {
                'name': category,
                'file_count': count,
            })
            self.add_edge('archives', category_id, 'contains')
    
    def _process_conversations(self, conv_data: Dict):
        """Process AI conversation data into graph nodes and edges."""
        # Add conversations root node
        self.add_node('ai_conversations', 'collection', {
            'name': 'AI Conversations',
            'total': conv_data.get('stats', {}).get('total_conversations', 0),
        })
        
        # Add source nodes
        by_source = conv_data.get('stats', {}).get('by_source', {})
        for source, count in by_source.items():
            source_id = f'source_{source}'
            self.add_node(source_id, 'conversation_source', {
                'name': source,
                'conversation_count': count,
            })
            self.add_edge('ai_conversations', source_id, 'contains')
    
    def _process_personal_repos(self, repo_data: Dict):
        """Process personal repository data into graph nodes and edges."""
        # Add personal repos root node
        self.add_node('personal_repos', 'collection', {
            'name': 'Personal Repositories',
            'total': repo_data.get('stats', {}).get('total_repos', 0),
        })
        
        # Process individual repositories
        repositories = repo_data.get('repositories', [])
        for repo in repositories[:50]:  # Limit to 50 for graph size
            repo_id = f"repo_{repo['name']}"
            self.add_node(repo_id, 'repository', {
                'name': repo['name'],
                'language': repo.get('language'),
                'is_fork': repo.get('is_fork', False),
                'stars': repo.get('stars', 0),
            })
            self.add_edge('personal_repos', repo_id, 'contains')
            
            # Add fork relationships
            if repo.get('is_fork') and repo.get('parent'):
                parent_id = f"parent_{repo['parent']['name']}"
                self.add_node(parent_id, 'parent_repository', {
                    'name': repo['parent']['name'],
                    'full_name': repo['parent']['full_name'],
                })
                self.add_edge(repo_id, parent_id, 'forked_from')
    
    def _process_org_repos(self, org_data: Dict):
        """Process organization repository data into graph nodes and edges."""
        # Add org repos root node
        self.add_node('org_repos', 'collection', {
            'name': 'Organization Repositories',
            'total': org_data.get('stats', {}).get('total_repos', 0),
        })
        
        # Add status nodes
        by_status = org_data.get('stats', {}).get('by_status', {})
        for status, count in by_status.items():
            status_id = f'status_{status}'
            self.add_node(status_id, 'repo_status', {
                'name': status,
                'repo_count': count,
            })
            self.add_edge('org_repos', status_id, 'has_status')
    
    def generate(self) -> Dict:
        """
        Generate the knowledge graph structure.
        
        Returns:
            Knowledge graph dictionary
        """
        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'node_count': len(self.nodes),
                'edge_count': len(self.edges),
            },
            'nodes': self.nodes,
            'edges': self.edges,
            'statistics': {
                'node_types': self._count_node_types(),
                'relationship_types': self._count_relationship_types(),
            },
        }
    
    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type."""
        counts = {}
        for node in self.nodes:
            node_type = node['type']
            counts[node_type] = counts.get(node_type, 0) + 1
        return counts
    
    def _count_relationship_types(self) -> Dict[str, int]:
        """Count edges by relationship type."""
        counts = {}
        for edge in self.edges:
            rel_type = edge['relationship']
            counts[rel_type] = counts.get(rel_type, 0) + 1
        return counts
    
    def save_to_file(self, output_path: str, pretty: bool = True) -> bool:
        """
        Save knowledge graph to JSON file.
        
        Args:
            output_path: Path to output file
            pretty: Whether to pretty-print JSON
            
        Returns:
            Success status
        """
        try:
            graph = self.generate()
            
            # Ensure output directory exists
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(graph, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(graph, f, ensure_ascii=False)
            
            print(f"Knowledge graph saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving knowledge graph: {e}")
            return False
    
    def export_to_cytoscape(self, output_path: str) -> bool:
        """
        Export graph in Cytoscape.js compatible format.
        
        Args:
            output_path: Path to output file
            
        Returns:
            Success status
        """
        try:
            graph = self.generate()
            
            # Convert to Cytoscape format
            cytoscape_format = {
                'elements': {
                    'nodes': [
                        {
                            'data': {
                                'id': node['id'],
                                'type': node['type'],
                                **node['properties']
                            }
                        }
                        for node in graph['nodes']
                    ],
                    'edges': [
                        {
                            'data': {
                                'id': f"{edge['source']}_{edge['target']}",
                                'source': edge['source'],
                                'target': edge['target'],
                                'relationship': edge['relationship'],
                                **edge['properties']
                            }
                        }
                        for edge in graph['edges']
                    ]
                }
            }
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cytoscape_format, f, indent=2, ensure_ascii=False)
            
            print(f"Cytoscape graph saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting to Cytoscape format: {e}")
            return False
