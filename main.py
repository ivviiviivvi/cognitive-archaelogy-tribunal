#!/usr/bin/env python3
"""
Cognitive Archaeology Tribunal - Main CLI
Command-line interface for running the complete audit suite.
"""

import os
import sys
import argparse
from pathlib import Path

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

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.tree import Tree
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

def print_banner():
    if RICH_AVAILABLE:
        Console().print(Panel.fit(
            "[bold blue]COGNITIVE ARCHAEOLOGY TRIBUNAL[/bold blue]\n[italic]Comprehensive Archaeological Dig Tool[/italic]",
            border_style="blue", padding=(1, 2)
        ))
    else:
        print("=" * 70 + "\nCOGNITIVE ARCHAEOLOGY TRIBUNAL\nComprehensive Archaeological Dig Tool\n" + "=" * 70 + "\n")

def run_step(title, func, success_msg_fn):
    """Executes a step with rich status or standard print."""
    if RICH_AVAILABLE:
        console = Console()
        with console.status(f"[bold green]{title}...[/bold green]", spinner="dots"):
            try:
                res = func()
                console.print(f"[green]✓[/green] {success_msg_fn(res)}")
                return res
            except Exception as e:
                console.print(f"[bold red]✗ Error: {e}[/bold red]")
                return None
    else:
        print(f"\nRunning {title}...")
        print("-" * 70)
        try:
            res = func()
            msg = success_msg_fn(res).replace("[bold]", "").replace("[/bold]", "")
            print(f"✓ {msg}")
            return res
        except Exception as e:
            print(f"✗ Error: {e}")
            return None

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
    
    parser.add_argument('--all', action='store_true', help='Run all modules (requires other arguments)')
    parser.add_argument('--scan-archives', metavar='PATH', help='Scan archive directories (comma-separated paths)')
    parser.add_argument('--ai-conversations', metavar='PATH', help='Load AI conversations from path')
    parser.add_argument('--personal-repos', metavar='USERNAME', help='Analyze personal GitHub repos')
    parser.add_argument('--org-repos', metavar='ORGNAME', help='Analyze organization GitHub repos')
    parser.add_argument('--web-bookmarks', metavar='PATH', help='Analyze web bookmarks from an export file')
    parser.add_argument('--github-token', help='GitHub personal access token (or use GITHUB_TOKEN env var)')
    parser.add_argument('--output-dir', default='./output', help='Output directory (default: ./output)')
    parser.add_argument('--no-inventory', action='store_true', help='Skip inventory generation')
    parser.add_argument('--no-graph', action='store_true', help='Skip knowledge graph generation')
    parser.add_argument('--no-triage', action='store_true', help='Skip triage report generation')
    
    args = parser.parse_args()
    
    if not (args.all or args.scan_archives or args.ai_conversations or args.personal_repos or args.org_repos or args.web_bookmarks):
        parser.error('At least one module must be specified')
    
    print_banner()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    
    # 1. Archive Scanner
    if args.scan_archives:
        def step():
            scanner = ArchiveScanner()
            paths = [p.strip() for p in args.scan_archives.split(',')]
            res = scanner.scan_directory(paths[0]) if len(paths) == 1 else scanner.scan_multiple_locations(paths)
            import json
            with open(output_dir / 'archives.json', 'w') as f: json.dump(res, f, indent=2)
            return res
        
        msg_fn = lambda r: f"Archive scan complete. Found [bold]{r.get('stats', {}).get('total_files', 0)}[/bold] files"
        res = run_step("Archive Scanner", step, msg_fn)
        if res: results['archives'] = res

    # 2. AI Context
    if args.ai_conversations:
        def step():
            agg = AIContextAggregator()
            agg.load_chatgpt_export(args.ai_conversations)
            res = agg.get_results()
            import json
            with open(output_dir / 'ai_conversations.json', 'w') as f: json.dump(res, f, indent=2)
            return res

        msg_fn = lambda r: f"AI context loaded. [bold]{r.get('loaded_count', 0)}[/bold] conversations"
        res = run_step("AI Context Aggregator", step, msg_fn)
        if res: results['ai_conversations'] = res

    # 3. Personal Repos
    if args.personal_repos:
        def step():
            analyzer = PersonalRepoAnalyzer(args.github_token)
            res = analyzer.analyze_user_repos(args.personal_repos)
            import json
            with open(output_dir / 'personal_repos.json', 'w') as f: json.dump(res, f, indent=2)
            return res
            
        msg_fn = lambda r: f"Personal repos analyzed: [bold]{r.get('stats', {}).get('total_repos', 0)}[/bold]"
        res = run_step("Personal Repo Analyzer", step, msg_fn)
        if res: results['personal_repos'] = res

    # 4. Org Repos
    if args.org_repos:
        def step():
            analyzer = OrgRepoAnalyzer(args.github_token)
            res = analyzer.analyze_org_repos(args.org_repos)
            import json
            with open(output_dir / 'org_repos.json', 'w') as f: json.dump(res, f, indent=2)
            return res
            
        msg_fn = lambda r: f"Org repos analyzed: [bold]{r.get('stats', {}).get('total_repos', 0)}[/bold]"
        res = run_step("Org Repo Analyzer", step, msg_fn)
        if res: results['org_repos'] = res

    # 5. Web Bookmarks
    if args.web_bookmarks:
        def step():
            analyzer = WebBookmarkAnalyzer()
            res = analyzer.analyze_bookmarks(args.web_bookmarks)
            import json
            with open(output_dir / 'web_bookmarks.json', 'w') as f: json.dump(res, f, indent=2)
            return res

        msg_fn = lambda r: f"Web bookmarks found: [bold]{r.get('stats', {}).get('total_bookmarks', 0)}[/bold]"
        res = run_step("Web Bookmark Analyzer", step, msg_fn)
        if res: results['web_bookmarks'] = res

    if RICH_AVAILABLE: Console().print(Panel("GENERATING OUTPUTS", style="bold cyan"))
    else: print("\n" + "=" * 70 + "\nGENERATING OUTPUTS\n" + "=" * 70)

    # Unified Inventory
    inventory = InventoryGenerator()
    if 'archives' in results: inventory.add_archive_results(results['archives'])
    if 'ai_conversations' in results: inventory.add_ai_context_results(results['ai_conversations'])
    if 'personal_repos' in results: inventory.add_personal_repo_results(results['personal_repos'])
    if 'org_repos' in results: inventory.add_org_repo_results(results['org_repos'])

    if not args.no_inventory:
        run_step("Unified Inventory", lambda: inventory.save_to_file(str(output_dir / 'inventory.json')), lambda _: "Inventory saved")
    
    if not args.no_graph:
        def step():
            graph = KnowledgeGraphGenerator()
            graph.build_from_inventory(inventory.get_inventory())
            graph.save_to_file(str(output_dir / 'knowledge_graph.json'))
            graph.export_to_cytoscape(str(output_dir / 'knowledge_graph_cytoscape.json'))
        run_step("Knowledge Graph", step, lambda _: "Knowledge graph saved")
        
    if not args.no_triage:
        def step():
            triage = TriageReportGenerator()
            if 'archives' in results: triage.add_archive_triage(results['archives'])
            if 'ai_conversations' in results: triage.add_ai_context_triage(results['ai_conversations'])
            if 'personal_repos' in results: triage.add_personal_repo_triage(results['personal_repos'])
            if 'org_repos' in results: triage.add_org_repo_triage(results['org_repos'])
            triage.save_to_file(str(output_dir / 'triage_report.json'))
            with open(output_dir / 'triage_report.txt', 'w') as f: f.write(triage.generate_text_report())
        run_step("Triage Report", step, lambda _: "Triage report saved")

    if RICH_AVAILABLE:
        c = Console()
        c.print(Panel("COMPLETE!", style="bold green"))
        c.print(f"\nAll outputs saved to: [underline]{output_dir.absolute()}[/underline]")
        tree = Tree("[bold]Generated files[/bold]")
        for file in sorted(output_dir.glob('*')): tree.add(file.name)
        c.print(tree)
        c.print()
    else:
        print("\n" + "=" * 70 + "\nCOMPLETE!\n" + "=" * 70)
        print(f"\nAll outputs saved to: {output_dir.absolute()}\n\nGenerated files:")
        for file in sorted(output_dir.glob('*')): print(f"  - {file.name}")
        print()

if __name__ == '__main__':
    main()
