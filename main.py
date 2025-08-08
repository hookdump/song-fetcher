#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel
from rich import print as rprint
from search import MusicSearcher
from downloader import MusicDownloader


console = Console()


def display_results(results):
    if not results:
        console.print("[red]No results found![/red]")
        return
    
    table = Table(title="Search Results", show_header=True, header_style="bold magenta")
    table.add_column("#", style="cyan", width=3)
    table.add_column("Title", style="green", max_width=50)
    table.add_column("Artist/Channel", style="yellow", max_width=30)
    table.add_column("Duration", style="blue", width=10)
    table.add_column("Views", style="white", width=15)
    
    for idx, result in enumerate(results, 1):
        table.add_row(
            str(idx),
            result['title'][:50] + ('...' if len(result['title']) > 50 else ''),
            result['channel'][:30] + ('...' if len(result['channel']) > 30 else ''),
            result['duration'],
            result['views']
        )
    
    console.print(table)


def main():
    parser = argparse.ArgumentParser(description='Search and download music as MP3')
    parser.add_argument('--output', '-o', type=str, default='downloads',
                        help='Output directory for downloaded songs (default: downloads)')
    parser.add_argument('search_terms', nargs='*', 
                        help='Song name to search for (optional)')
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir
    
    console.print(Panel.fit(
        "[bold cyan]Music Search & Download[/bold cyan]\n"
        f"[dim]Search for any song and download as MP3[/dim]\n"
        f"[dim]Download folder: {output_dir}[/dim]",
        border_style="cyan"
    ))
    
    searcher = MusicSearcher()
    downloader = MusicDownloader(str(output_dir))
    
    # If search terms provided via command line, search immediately
    initial_search = ' '.join(args.search_terms) if args.search_terms else None
    
    while True:
        console.print("\n" + "="*60)
        
        if initial_search:
            query = initial_search
            console.print(f"\n[bold green]Searching for:[/bold green] {query}")
            initial_search = None  # Only use it once
        else:
            query = Prompt.ask("\n[bold green]Enter song name[/bold green] (or 'quit' to exit)")
        
        if query.lower() in ['quit', 'exit', 'q']:
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        console.print(f"\n[cyan]Searching for:[/cyan] {query}")
        
        with console.status("[bold green]Searching...") as status:
            results = searcher.search(query, limit=10)
        
        if not results:
            console.print("[red]No results found. Try a different search term.[/red]")
            continue
        
        display_results(results)
        
        console.print("\n[bold]Options:[/bold]")
        console.print("  • Enter a number (1-{}) to download".format(len(results)))
        console.print("  • Enter 's' to search again")
        console.print("  • Enter 'q' to quit")
        
        choice = Prompt.ask("\n[bold yellow]Your choice[/bold yellow]")
        
        if choice.lower() == 's':
            continue
        elif choice.lower() in ['q', 'quit']:
            console.print("[yellow]Goodbye![/yellow]")
            break
        
        try:
            index = int(choice) - 1
            selected = searcher.get_by_index(index)
            
            if selected:
                console.print(f"\n[green]Selected:[/green] {selected['title']}")
                console.print(f"[green]By:[/green] {selected['channel']}")
                
                confirm = Prompt.ask("\n[bold]Download this song?[/bold] (y/n)", default="y")
                
                if confirm.lower() == 'y':
                    with console.status("[bold green]Downloading and converting to MP3...") as status:
                        filepath = downloader.download_as_mp3(selected)
                    
                    if filepath:
                        console.print(f"[bold green]✓ Download complete![/bold green]")
                        console.print(f"[cyan]File saved to:[/cyan] {filepath}")
                    else:
                        console.print("[red]Download failed. Please try again.[/red]")
            else:
                console.print("[red]Invalid selection![/red]")
        
        except ValueError:
            console.print("[red]Invalid input! Please enter a number.[/red]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user. Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        sys.exit(1)