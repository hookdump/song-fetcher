#!/usr/bin/env python3

from search import MusicSearcher
from downloader import MusicDownloader
from rich.console import Console
from rich.table import Table

console = Console()

def test_search():
    searcher = MusicSearcher()
    
    test_query = "Pink Champagne"
    console.print(f"\n[bold cyan]Testing search for: '{test_query}'[/bold cyan]\n")
    
    results = searcher.search(test_query, limit=5)
    
    if results:
        table = Table(title="Search Results", show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Title", style="green", max_width=50)
        table.add_column("Artist/Channel", style="yellow", max_width=30)
        table.add_column("Duration", style="blue", width=10)
        
        for idx, result in enumerate(results, 1):
            table.add_row(
                str(idx),
                result['title'][:50] + ('...' if len(result['title']) > 50 else ''),
                result['channel'][:30] + ('...' if len(result['channel']) > 30 else ''),
                result['duration']
            )
        
        console.print(table)
        console.print(f"\n[green]Found {len(results)} results![/green]")
        
        console.print("\n[bold]First result details:[/bold]")
        first = results[0]
        console.print(f"  Title: {first['title']}")
        console.print(f"  Channel: {first['channel']}")
        console.print(f"  URL: {first['url']}")
        console.print(f"  Duration: {first['duration']}")
        console.print(f"  Views: {first['views']}")
        
    else:
        console.print("[red]No results found![/red]")

if __name__ == "__main__":
    test_search()