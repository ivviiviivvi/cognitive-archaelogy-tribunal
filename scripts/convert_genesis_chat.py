#!/usr/bin/env python3
"""
Genesis Chat Preservation Converter

Converts genesis-chat-preservation.md to AI Context Aggregator JSON format.
This enables Phase 3 baseline completion by processing existing curated conversations.

Input: context/history/genesis-chat-preservation.md (3,466 lines)
Output: data/genesis-conversations.json (AI Context Aggregator format)

Format:
- Parses prompt/response pairs from markdown
- Creates conversation objects with messages
- Compatible with cognitive_tribunal.modules.ai_context_aggregator

Author: Cognitive Archaeology Tribunal
Date: 2025-11-17
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple


class GenesisChatConverter:
    """Convert genesis chat markdown to AI conversation JSON format."""

    def __init__(self):
        """Initialize the converter."""
        self.conversations = []
        self.current_section = None

    def parse_markdown(self, file_path: str) -> List[Dict]:
        """
        Parse the genesis chat markdown file.

        Args:
            file_path: Path to genesis-chat-preservation.md

        Returns:
            List of conversation dictionaries
        """
        print(f"📖 Reading: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into table of contents and full transcript
        # The full transcript starts after the first "---" section
        parts = content.split('---', 1)

        if len(parts) < 2:
            print("⚠️  Warning: Could not find transcript section")
            full_transcript = content
        else:
            full_transcript = parts[1]

        # Parse prompt-response pairs
        conversations = self._extract_conversations(full_transcript)

        print(f"✅ Extracted {len(conversations)} conversations")

        return conversations

    def _extract_conversations(self, text: str) -> List[Dict]:
        """
        Extract prompt-response pairs from transcript text.

        Strategy:
        - Look for patterns like "1prompt", "1response", "2prompt", etc.
        - Extract content between these markers
        - Group prompts and responses into conversations
        """
        conversations = []

        # Pattern to match: number + "prompt" or number + "response"
        # Examples: "1prompt", "2response", "3prompt"
        pattern = r'^(\d+)(prompt|response)\s*$'

        lines = text.split('\n')
        current_exchange = []
        current_content = []
        current_type = None
        current_number = None

        for i, line in enumerate(lines):
            match = re.match(pattern, line.strip())

            if match:
                # Save previous content if exists
                if current_type and current_content:
                    current_exchange.append({
                        'type': current_type,
                        'number': current_number,
                        'content': '\n'.join(current_content).strip()
                    })
                    current_content = []

                # Check if we should create a new conversation
                # (when we hit a new prompt after having a response)
                if current_type == 'response' and match.group(2) == 'prompt':
                    if current_exchange:
                        conversations.append(self._create_conversation(current_exchange))
                        current_exchange = []

                current_number = match.group(1)
                current_type = match.group(2)

            else:
                # Accumulate content lines
                if current_type and line.strip():
                    current_content.append(line)

        # Don't forget the last exchange
        if current_type and current_content:
            current_exchange.append({
                'type': current_type,
                'number': current_number,
                'content': '\n'.join(current_content).strip()
            })

        if current_exchange:
            conversations.append(self._create_conversation(current_exchange))

        return conversations

    def _create_conversation(self, exchange: List[Dict]) -> Dict:
        """
        Create a conversation object from prompt-response exchange.

        Args:
            exchange: List of dicts with 'type', 'number', and 'content'

        Returns:
            Conversation dict in AI Context Aggregator format
        """
        # Extract title from first prompt
        title = "Cognitive OS Architecture"
        if exchange and exchange[0]['type'] == 'prompt':
            first_line = exchange[0]['content'].split('\n')[0][:100]
            title = first_line or f"Conversation {exchange[0]['number']}"

        # Build messages array
        messages = []
        for item in exchange:
            author = 'user' if item['type'] == 'prompt' else 'assistant'
            messages.append({
                'id': f"{item['number']}_{item['type']}",
                'author': author,
                'create_time': None,  # No timestamps in markdown
                'content': item['content']
            })

        # Create conversation object
        conversation = {
            'title': title,
            'source': 'genesis-chat',
            'source_file': 'context/history/genesis-chat-preservation.md',
            'create_time': None,
            'update_time': None,
            'messages': messages,
            'metadata': {
                'exchange_count': len(exchange),
                'conversation_number': exchange[0]['number'] if exchange else 'unknown'
            }
        }

        return conversation

    def save_json(self, conversations: List[Dict], output_path: str):
        """
        Save conversations to JSON files.

        Creates individual JSON files per conversation in ChatGPT-compatible format.

        Args:
            conversations: List of conversation dicts
            output_path: Path to output directory
        """
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save each conversation as individual file (ChatGPT format)
        for i, conv in enumerate(conversations, 1):
            conv_file = output_dir / f"conversation_{i:03d}.json"

            # Convert to ChatGPT-compatible format
            chatgpt_format = {
                'title': conv['title'],
                'create_time': conv.get('create_time'),
                'update_time': conv.get('update_time'),
                'messages': conv['messages']
            }

            with open(conv_file, 'w', encoding='utf-8') as f:
                json.dump(chatgpt_format, f, indent=2, ensure_ascii=False)

        # Also save master index
        index_file = output_dir / '_index.json'
        index_data = {
            'source': 'genesis-chat-preservation',
            'generated_at': datetime.now().isoformat(),
            'conversation_count': len(conversations),
            'files': [f"conversation_{i:03d}.json" for i in range(1, len(conversations) + 1)],
            'metadata': {
                'original_file': 'context/history/genesis-chat-preservation.md',
                'conversion_tool': 'convert_genesis_chat.py',
                'description': 'Curated AI conversations from cognitive OS architecture planning'
            }
        }

        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved: {output_path}/")
        print(f"   {len(conversations)} conversation files")
        print(f"   {sum(len(c['messages']) for c in conversations)} total messages")
        print(f"   1 index file (_index.json)")

        return output_path


def main():
    """Main execution function."""
    print("=" * 60)
    print("Genesis Chat Preservation Converter")
    print("=" * 60)
    print()

    # Paths
    input_file = "context/history/genesis-chat-preservation.md"
    output_dir = "data/genesis-conversations"

    # Convert
    converter = GenesisChatConverter()
    conversations = converter.parse_markdown(input_file)

    if conversations:
        converter.save_json(conversations, output_dir)
        print()
        print("✅ Conversion complete!")
        print(f"   Input:  {input_file}")
        print(f"   Output: {output_dir}/")
        print()
        print("📋 Next step:")
        print(f"   python main.py --ai-conversations {output_dir} --output-dir ./output/phase3-genesis")
    else:
        print("❌ No conversations extracted")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
