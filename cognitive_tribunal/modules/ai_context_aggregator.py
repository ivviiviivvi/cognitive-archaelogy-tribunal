"""
Module 2: AI Context Aggregator
Aggregates AI conversation context from various sources.
Supports ChatGPT export formats and other AI conversation logs.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class AIContextAggregator:
    """
    Aggregates AI conversation context from various sources.
    Primary support for ChatGPT conversation exports.
    """
    
    def __init__(self):
        """Initialize the AI context aggregator."""
        self.conversations: List[Dict] = []
        self.stats = {
            'total_conversations': 0,
            'total_messages': 0,
            'by_source': {},
            'date_range': {'earliest': None, 'latest': None},
        }
    
    def load_chatgpt_export(self, export_path: str) -> Dict:
        """
        Load conversations from ChatGPT export.
        
        ChatGPT exports conversations as JSON files with structure:
        {
            "title": "...",
            "create_time": timestamp,
            "update_time": timestamp,
            "mapping": { ... message tree ... }
        }
        
        Args:
            export_path: Path to ChatGPT export directory or file
            
        Returns:
            Loading results
        """
        path = Path(export_path)
        
        if not path.exists():
            return {'error': f"Path does not exist: {export_path}"}
        
        loaded_count = 0
        errors = []
        
        # Handle both directory and single file
        if path.is_dir():
            json_files = list(path.glob('*.json')) + list(path.glob('**/*.json'))
        else:
            json_files = [path]
        
        for json_file in json_files:
            try:
                result = self._load_conversation_file(json_file, source='chatgpt')
                if result.get('success'):
                    loaded_count += 1
                else:
                    errors.append(result.get('error'))
            except Exception as e:
                errors.append(f"Error loading {json_file}: {str(e)}")
        
        self._update_stats()
        
        return {
            'loaded_count': loaded_count,
            'errors': errors,
            'total_conversations': len(self.conversations),
        }
    
    def _load_conversation_file(self, file_path: Path, source: str = 'unknown') -> Dict:
        """Load a single conversation file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract conversation metadata
            conversation = {
                'title': data.get('title', 'Untitled'),
                'source': source,
                'source_file': str(file_path),
                'create_time': data.get('create_time'),
                'update_time': data.get('update_time'),
                'messages': [],
            }
            
            # Parse message mapping (ChatGPT format)
            if 'mapping' in data:
                conversation['messages'] = self._parse_chatgpt_mapping(data['mapping'])
            # Handle simple messages array format
            elif 'messages' in data:
                conversation['messages'] = data['messages']
            
            # Add parsed conversation
            self.conversations.append(conversation)
            
            return {'success': True}
            
        except json.JSONDecodeError as e:
            return {'success': False, 'error': f"Invalid JSON in {file_path}: {str(e)}"}
        except Exception as e:
            return {'success': False, 'error': f"Error loading {file_path}: {str(e)}"}
    
    def _parse_chatgpt_mapping(self, mapping: Dict) -> List[Dict]:
        """
        Parse ChatGPT's message mapping structure.
        
        The mapping is a tree structure where each node can have messages.
        We extract messages in chronological order.
        """
        messages = []
        
        for node_id, node_data in mapping.items():
            if 'message' in node_data and node_data['message']:
                msg = node_data['message']
                
                # Extract relevant message data
                message = {
                    'id': msg.get('id'),
                    'author': msg.get('author', {}).get('role', 'unknown'),
                    'create_time': msg.get('create_time'),
                    'content': self._extract_message_content(msg.get('content', {})),
                }
                
                if message['content']:  # Only add if there's actual content
                    messages.append(message)
        
        # Sort by creation time
        messages.sort(key=lambda x: x.get('create_time', 0) or 0)
        
        return messages
    
    def _extract_message_content(self, content: Dict) -> str:
        """Extract text content from message content structure."""
        if isinstance(content, str):
            return content
        
        if isinstance(content, dict):
            # ChatGPT format
            if 'parts' in content:
                return ' '.join(str(part) for part in content['parts'] if part)
            
            # Direct text field
            if 'text' in content:
                return content['text']
        
        return ''
    
    def load_generic_json_conversations(self, directory: str) -> Dict:
        """
        Load conversations from generic JSON format.
        
        Args:
            directory: Directory containing JSON conversation files
            
        Returns:
            Loading results
        """
        path = Path(directory)
        
        if not path.exists() or not path.is_dir():
            return {'error': f"Directory does not exist: {directory}"}
        
        loaded_count = 0
        errors = []
        
        for json_file in path.glob('**/*.json'):
            try:
                result = self._load_conversation_file(json_file, source='generic')
                if result.get('success'):
                    loaded_count += 1
                else:
                    errors.append(result.get('error'))
            except Exception as e:
                errors.append(f"Error loading {json_file}: {str(e)}")
        
        self._update_stats()
        
        return {
            'loaded_count': loaded_count,
            'errors': errors,
            'total_conversations': len(self.conversations),
        }
    
    def _update_stats(self):
        """Update statistics after loading conversations."""
        self.stats['total_conversations'] = len(self.conversations)
        self.stats['total_messages'] = sum(len(conv.get('messages', [])) for conv in self.conversations)
        
        # Update source statistics
        self.stats['by_source'] = {}
        for conv in self.conversations:
            source = conv.get('source', 'unknown')
            self.stats['by_source'][source] = self.stats['by_source'].get(source, 0) + 1
        
        # Update date range
        all_times = []
        for conv in self.conversations:
            if conv.get('create_time'):
                all_times.append(conv['create_time'])
            if conv.get('update_time'):
                all_times.append(conv['update_time'])
        
        if all_times:
            self.stats['date_range']['earliest'] = min(all_times)
            self.stats['date_range']['latest'] = max(all_times)
    
    def get_results(self) -> Dict:
        """Get aggregated results."""
        return {
            'stats': self.stats,
            'conversations': self.conversations,
            'summary': {
                'total_conversations': self.stats['total_conversations'],
                'total_messages': self.stats['total_messages'],
                'sources': list(self.stats['by_source'].keys()),
                'date_range': self.stats['date_range'],
            },
            'timestamp': datetime.now().isoformat(),
        }
    
    def search_conversations(self, keyword: str) -> List[Dict]:
        """
        Search conversations for a keyword.
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List of matching conversations
        """
        keyword_lower = keyword.lower()
        matching = []
        
        for conv in self.conversations:
            # Search in title
            if keyword_lower in conv.get('title', '').lower():
                matching.append(conv)
                continue
            
            # Search in messages
            for msg in conv.get('messages', []):
                content = msg.get('content', '')
                if keyword_lower in content.lower():
                    matching.append(conv)
                    break
        
        return matching
    
    def get_conversations_by_date_range(self, start_date: Optional[datetime] = None, 
                                       end_date: Optional[datetime] = None) -> List[Dict]:
        """
        Get conversations within a date range.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            Filtered conversations
        """
        filtered = []
        
        for conv in self.conversations:
            create_time = conv.get('create_time')
            if not create_time:
                continue
            
            conv_date = datetime.fromtimestamp(create_time)
            
            if start_date and conv_date < start_date:
                continue
            if end_date and conv_date > end_date:
                continue
            
            filtered.append(conv)
        
        return filtered
    
    def extract_topics(self, min_conversations: int = 2) -> Dict[str, List[str]]:
        """
        Extract common topics from conversation titles.
        
        Args:
            min_conversations: Minimum conversations to consider a topic
            
        Returns:
            Dictionary mapping topics to conversation titles
        """
        # Simple word frequency analysis
        from collections import Counter
        
        word_counts = Counter()
        word_to_titles = {}
        
        for conv in self.conversations:
            title = conv.get('title', '').lower()
            words = title.split()
            
            for word in words:
                # Filter out common words and short words
                if len(word) > 3 and word not in ['what', 'how', 'when', 'where', 'with', 'this', 'that']:
                    word_counts[word] += 1
                    if word not in word_to_titles:
                        word_to_titles[word] = []
                    word_to_titles[word].append(title)
        
        # Return topics that appear in multiple conversations
        topics = {
            word: titles 
            for word, titles in word_to_titles.items() 
            if len(titles) >= min_conversations
        }
        
        return topics
