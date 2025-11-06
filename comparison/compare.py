"""Comparison module for Traditional RAG vs Knowledge Graph RAG."""

import asyncio
from typing import Dict, Any, List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


async def compare_systems(
    rag_system,
    kg_system,
    question: str,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Compare Traditional RAG and Knowledge Graph RAG on a single question.

    Args:
        rag_system: TraditionalRAG instance
        kg_system: KnowledgeGraphRAG instance
        question: Question to ask both systems
        verbose: Whether to print detailed comparison

    Returns:
        Dictionary with results from both systems and comparison
    """
    console.print(f"\n[bold cyan]Comparing systems on question:[/bold cyan] {question}\n")

    # Query Traditional RAG
    console.print("[yellow]Querying Traditional RAG...[/yellow]")
    rag_result = rag_system.query(question)

    # Query Knowledge Graph RAG
    console.print("[yellow]Querying Knowledge Graph RAG...[/yellow]")
    kg_result = await kg_system.query(question)

    # Prepare comparison
    comparison = {
        "question": question,
        "rag_result": rag_result,
        "kg_result": kg_result,
        "comparison_metrics": {
            "speedup": rag_result['metrics']['query_time'] / kg_result['metrics']['query_time'],
            "rag_time": rag_result['metrics']['query_time'],
            "kg_time": kg_result['metrics']['query_time'],
            "rag_sources": rag_result['metrics']['num_source_chunks'],
            "kg_facts": kg_result['metrics']['num_facts'],
            "kg_entities": kg_result['metrics']['num_entities'],
            "kg_relationships": kg_result['metrics']['num_relationships']
        }
    }

    if verbose:
        display_comparison(comparison)

    return comparison


def display_comparison(comparison: Dict[str, Any]) -> None:
    """
    Display a rich comparison of results.

    Args:
        comparison: Comparison dictionary from compare_systems
    """
    console.print("\n" + "=" * 100)
    console.print("[bold green]COMPARISON RESULTS[/bold green]")
    console.print("=" * 100)

    # Question
    console.print(f"\n[bold]Question:[/bold] {comparison['question']}")

    # Answers comparison
    console.print("\n[bold cyan]Traditional RAG Answer:[/bold cyan]")
    console.print(Panel(comparison['rag_result']['answer'], border_style="blue"))

    console.print("\n[bold magenta]Knowledge Graph RAG Answer:[/bold magenta]")
    console.print(Panel(comparison['kg_result']['answer'], border_style="magenta"))

    # Metrics table
    table = Table(title="Performance Metrics", box=box.ROUNDED, show_header=True)
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Traditional RAG", style="blue")
    table.add_column("Knowledge Graph RAG", style="magenta")
    table.add_column("Difference", style="green")

    # Query time
    rag_time = comparison['comparison_metrics']['rag_time']
    kg_time = comparison['comparison_metrics']['kg_time']
    speedup = comparison['comparison_metrics']['speedup']
    time_diff = "RAG faster" if speedup < 1 else f"KG faster ({speedup:.2f}x)"

    table.add_row(
        "Query Time",
        f"{rag_time:.2f}s",
        f"{kg_time:.2f}s",
        time_diff
    )

    # Sources/Facts
    table.add_row(
        "Retrieved Items",
        f"{comparison['comparison_metrics']['rag_sources']} chunks",
        f"{comparison['comparison_metrics']['kg_facts']} facts",
        f"+{comparison['comparison_metrics']['kg_facts'] - comparison['comparison_metrics']['rag_sources']}"
    )

    # Entities (KG only)
    table.add_row(
        "Entities Identified",
        "N/A",
        f"{comparison['comparison_metrics']['kg_entities']}",
        "KG advantage"
    )

    # Relationships (KG only)
    table.add_row(
        "Relationships Found",
        "N/A",
        f"{comparison['comparison_metrics']['kg_relationships']}",
        "KG advantage"
    )

    console.print("\n", table)

    # Key insights
    console.print("\n[bold yellow]Key Insights:[/bold yellow]")
    insights = []

    if comparison['comparison_metrics']['kg_entities'] > 0:
        insights.append(f"✓ KG identified {comparison['comparison_metrics']['kg_entities']} entities and their relationships")

    if comparison['comparison_metrics']['kg_facts'] > comparison['comparison_metrics']['rag_sources']:
        insights.append(f"✓ KG retrieved {comparison['comparison_metrics']['kg_facts'] - comparison['comparison_metrics']['rag_sources']} more relevant facts")

    insights.append("✓ KG provides structured, relationship-aware context")
    insights.append("✓ Traditional RAG provides chunk-based context")

    for insight in insights:
        console.print(f"  {insight}")


async def run_comparison_suite(
    rag_system,
    kg_system,
    questions: List[str]
) -> List[Dict[str, Any]]:
    """
    Run a suite of comparison tests.

    Args:
        rag_system: TraditionalRAG instance
        kg_system: KnowledgeGraphRAG instance
        questions: List of questions to test

    Returns:
        List of comparison results
    """
    console.print("\n[bold green]Running Comparison Suite[/bold green]")
    console.print(f"Testing {len(questions)} questions...\n")

    results = []
    for i, question in enumerate(questions, 1):
        console.print(f"[bold]Test {i}/{len(questions)}[/bold]")
        result = await compare_systems(rag_system, kg_system, question, verbose=False)
        results.append(result)
        console.print("[green]✓ Complete[/green]\n")

    # Summary statistics
    display_summary_statistics(results)

    return results


def display_summary_statistics(results: List[Dict[str, Any]]) -> None:
    """
    Display summary statistics across all comparison results.

    Args:
        results: List of comparison results
    """
    console.print("\n" + "=" * 100)
    console.print("[bold green]SUMMARY STATISTICS[/bold green]")
    console.print("=" * 100 + "\n")

    # Calculate averages
    avg_rag_time = sum(r['comparison_metrics']['rag_time'] for r in results) / len(results)
    avg_kg_time = sum(r['comparison_metrics']['kg_time'] for r in results) / len(results)
    avg_rag_sources = sum(r['comparison_metrics']['rag_sources'] for r in results) / len(results)
    avg_kg_facts = sum(r['comparison_metrics']['kg_facts'] for r in results) / len(results)
    avg_kg_entities = sum(r['comparison_metrics']['kg_entities'] for r in results) / len(results)
    avg_kg_relationships = sum(r['comparison_metrics']['kg_relationships'] for r in results) / len(results)

    # Create summary table
    table = Table(title="Average Metrics Across All Questions", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Traditional RAG", style="blue")
    table.add_column("Knowledge Graph RAG", style="magenta")

    table.add_row("Avg Query Time", f"{avg_rag_time:.2f}s", f"{avg_kg_time:.2f}s")
    table.add_row("Avg Retrieved Items", f"{avg_rag_sources:.1f} chunks", f"{avg_kg_facts:.1f} facts")
    table.add_row("Avg Entities", "N/A", f"{avg_kg_entities:.1f}")
    table.add_row("Avg Relationships", "N/A", f"{avg_kg_relationships:.1f}")

    console.print(table)

    # Winner determination
    console.print("\n[bold yellow]Overall Assessment:[/bold yellow]")
    console.print(f"  • Knowledge Graph provides [bold]{avg_kg_entities:.1f}[/bold] entity references on average")
    console.print(f"  • Knowledge Graph finds [bold]{avg_kg_relationships:.1f}[/bold] relationships on average")
    console.print(f"  • Knowledge Graph retrieves [bold]{(avg_kg_facts/avg_rag_sources - 1) * 100:.1f}%[/bold] more contextual information")

    if avg_kg_time < avg_rag_time:
        console.print(f"  • Knowledge Graph is [bold green]{(avg_rag_time/avg_kg_time):.2f}x faster[/bold green] on average")
    else:
        console.print(f"  • Traditional RAG is [bold]{(avg_kg_time/avg_rag_time):.2f}x faster[/bold] on average")

    console.print("\n[bold green]✓ Knowledge Graph provides richer, more structured context for answering questions[/bold green]")
