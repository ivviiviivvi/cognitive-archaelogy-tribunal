#!/usr/bin/env python3
"""
Cognitive Archaeology Tribunal - Main CLI
Command-line interface for running the complete audit suite.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from cognitive_tribunal.modules.archive_scanner import ArchiveScanner
from cognitive_tribunal.modules.ai_context_aggregator import AIContextAggregator
from cognitive_tribunal.modules.personal_repo_analyzer import PersonalRepoAnalyzer
from cognitive_tribunal.modules.org_repo_analyzer import OrgRepoAnalyzer
from cognitive_tribunal.modules.web_bookmark_analyzer import WebBookmarkAnalyzer
from cognitive_tribunal.outputs.inventory import InventoryGenerator
from cognitive_tribunal.outputs.knowledge_graph import KnowledgeGraphGenerator
from cognitive_tribunal.outputs.triage_report import TriageReportGenerator

console = Console()

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Cognitive Archaeology Tribunal - Comprehensive digital archaeology tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all modules
  python main.py --all --output-dir ./output
  
  # Scan archives only
  python main.py --scan-archives /path/to/archives --output-dir ./output
  
  # Analyze personal repos
  python main.py --personal-repos username --output-dir ./output
  
  # Analyze org repos
  python main.py --org-repos orgname --output-dir ./output
  
  # Load AI conversations
  python main.py --ai-conversations /path/to/chatgpt/export --output-dir ./output
        """
    )
    
    # Module selection
    parser.add_argument('--all', action='store_true', help='Run all modules (requires other arguments)')
    parser.add_argument('--scan-archives', metavar='PATH', help='Scan archive directories (comma-separated paths)')
    parser.add_argument('--ai-conversations', metavar='PATH', help='Load AI conversations from path')
    parser.add_argument('--personal-repos', metavar='USERNAME', help='Analyze personal GitHub repos')
    parser.add_argument('--org-repos', metavar='ORGNAME', help='Analyze organization GitHub repos')
    parser.add_argument('--web-bookmarks', metavar='PATH', help='Analyze web bookmarks from an export file')
    
    # Configuration
    parser.add_argument('--github-token', help='GitHub personal access token (or use GITHUB_TOKEN env var)')
    parser.add_argument('--output-dir', default='./output', help='Output directory (default: ./output)')
    parser.add_argument('--no-inventory', action='store_true', help='Skip inventory generation')
    parser.add_argument('--no-graph', action='store_true', help='Skip knowledge graph generation')
    parser.add_argument('--no-triage', action='store_true', help='Skip triage report generation')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not (args.all or args.scan_archives or args.ai_conversations or args.personal_repos or args.org_repos or args.web_bookmarks):
        parser.error('At least one module must be specified')
    
    console.print(Panel.fit(
        "[bold blue]COGNITIVE ARCHAEOLOGY TRIBUNAL[/bold blue]\n[italic]Comprehensive Archaeological Dig Tool[/italic]",
        border_style="blue",
        padding=(1, 2)
    ))
    console.print()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize results storage
    results = {}
    
    # Module 1: Archive Scanner
    if args.scan_archives:
        with console.status("[bold cyan]Running Archive Scanner...", spinner="dots"):
            scanner = ArchiveScanner()
            paths = [p.strip() for p in args.scan_archives.split(',')]

            if len(paths) == 1:
                archive_results = scanner.scan_directory(paths[0])
            else:
                archive_results = scanner.scan_multiple_locations(paths)

            results['archives'] = archive_results

            # Save module results
            import json
            with open(output_dir / 'archives.json', 'w') as f:
                json.dump(archive_results, f, indent=2)

        console.print(f"[green]✓ Archive scan complete.[/green] Found {archive_results.get('stats', {}).get('total_files', 0)} files")
    
    # Module 2: AI Context Aggregator
    if args.ai_conversations:
        with console.status("[bold cyan]Running AI Context Aggregator...", spinner="dots"):
            aggregator = AIContextAggregator()
            ai_results = aggregator.load_chatgpt_export(args.ai_conversations)
            results['ai_conversations'] = aggregator.get_results()

            # Save module results
            import json
            with open(output_dir / 'ai_conversations.json', 'w') as f:
                json.dump(results['ai_conversations'], f, indent=2)
        
        console.print(f"[green]✓ AI context aggregation complete.[/green] Loaded {ai_results.get('loaded_count', 0)} conversations")
    
    # Module 3: Personal Repo Analyzer
    if args.personal_repos:
        with console.status("[bold cyan]Running Personal Repo Analyzer...", spinner="dots"):
            try:
                analyzer = PersonalRepoAnalyzer(args.github_token)
                repo_results = analyzer.analyze_user_repos(args.personal_repos)
                results['personal_repos'] = repo_results

                # Save module results
                import json
                with open(output_dir / 'personal_repos.json', 'w') as f:
                    json.dump(repo_results, f, indent=2)

                console.print(f"[green]✓ Personal repo analysis complete.[/green] Analyzed {repo_results.get('stats', {}).get('total_repos', 0)} repositories")
            except Exception as e:
                console.print(f"[red]✗ Error analyzing personal repos: {e}[/red]")
    
    # Module 4: Org Repo Analyzer
    if args.org_repos:
        with console.status("[bold cyan]Running Org Repo Analyzer...", spinner="dots"):
            try:
                analyzer = OrgRepoAnalyzer(args.github_token)
                org_results = analyzer.analyze_org_repos(args.org_repos)
                results['org_repos'] = org_results

                # Save module results
                import json
                with open(output_dir / 'org_repos.json', 'w') as f:
                    json.dump(org_results, f, indent=2)

                console.print(f"[green]✓ Org repo analysis complete.[/green] Analyzed {org_results.get('stats', {}).get('total_repos', 0)} repositories")
            except Exception as e:
                console.print(f"[red]✗ Error analyzing org repos: {e}[/red]")
    
    # Module 5: Web Bookmark Analyzer
    if args.web_bookmarks:
        with console.status("[bold cyan]Running Web Bookmark Analyzer...", spinner="dots"):
            analyzer = WebBookmarkAnalyzer()
            bookmark_results = analyzer.analyze_bookmarks(args.web_bookmarks)
            results['web_bookmarks'] = bookmark_results

            # Save module results
            import json
            with open(output_dir / 'web_bookmarks.json', 'w') as f:
                json.dump(bookmark_results, f, indent=2)

        console.print(f"[green]✓ Web bookmark analysis complete.[/green] Found {bookmark_results.get('stats', {}).get('total_bookmarks', 0)} bookmarks")

    # Generate unified outputs
    console.print()
    console.rule("[bold]GENERATING OUTPUTS[/bold]")
    console.print()
    
    # Unified Inventory
    if not args.no_inventory:
        with console.status("[bold cyan]Generating unified inventory...", spinner="dots"):
            inventory = InventoryGenerator()

            if 'archives' in results:
                inventory.add_archive_results(results['archives'])
            if 'ai_conversations' in results:
                inventory.add_ai_context_results(results['ai_conversations'])
            if 'personal_repos' in results:
                inventory.add_personal_repo_results(results['personal_repos'])
            if 'org_repos' in results:
                inventory.add_org_repo_results(results['org_repos'])

            inventory.save_to_file(str(output_dir / 'inventory.json'))
        console.print("[green]✓ Inventory saved[/green]")
    
    # Knowledge Graph
    if not args.no_graph:
        with console.status("[bold cyan]Generating knowledge graph...", spinner="dots"):
            graph = KnowledgeGraphGenerator()

            if not args.no_inventory:
                graph.build_from_inventory(inventory.get_inventory())
                graph.save_to_file(str(output_dir / 'knowledge_graph.json'))
                graph.export_to_cytoscape(str(output_dir / 'knowledge_graph_cytoscape.json'))
        console.print("[green]✓ Knowledge graph saved[/green]")
    
    # Triage Report
    if not args.no_triage:
        with console.status("[bold cyan]Generating triage report...", spinner="dots"):
            triage = TriageReportGenerator()

            if 'archives' in results:
                triage.add_archive_triage(results['archives'])
            if 'ai_conversations' in results:
                triage.add_ai_context_triage(results['ai_conversations'])
            if 'personal_repos' in results:
                triage.add_personal_repo_triage(results['personal_repos'])
            if 'org_repos' in results:
                triage.add_org_repo_triage(results['org_repos'])

            triage.save_to_file(str(output_dir / 'triage_report.json'))

            # Also save as text
            with open(output_dir / 'triage_report.txt', 'w') as f:
                f.write(triage.generate_text_report())

        console.print("[green]✓ Triage report saved[/green]")
    
    # Final summary
    console.print()
    console.print(Panel("[bold green]COMPLETE![/bold green]", border_style="green"))
    console.print(f"\nAll outputs saved to: [bold]{output_dir.absolute()}[/bold]")

    tree = Tree("[bold]Generated files[/bold]")
    for file in sorted(output_dir.glob('*')):
        tree.add(file.name)
    console.print(tree)
    console.print()


if __name__ == '__main__':
    main()
