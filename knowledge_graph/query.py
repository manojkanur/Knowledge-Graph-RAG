"""Query interface for Knowledge Graph RAG."""

from typing import Dict, Any
from .kg_pipeline import KnowledgeGraphRAG


async def query_kg(
    kg_system: KnowledgeGraphRAG,
    question: str,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Query the Knowledge Graph RAG system and return formatted results.

    Args:
        kg_system: Initialized KnowledgeGraphRAG instance
        question: User's question
        verbose: Whether to print detailed information

    Returns:
        Dictionary with answer and metrics
    """
    result = await kg_system.query(question)

    if verbose:
        print("\n" + "=" * 80)
        print("KNOWLEDGE GRAPH RAG RESULT")
        print("=" * 80)
        print(f"\nQuestion: {question}")
        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nMetrics:")
        print(f"  - Total Query Time: {result['metrics']['query_time']:.2f}s")
        print(f"  - Retrieval Time: {result['metrics']['retrieval_time']:.2f}s")
        print(f"  - Generation Time: {result['metrics']['generation_time']:.2f}s")
        print(f"  - Facts Retrieved: {result['metrics']['num_facts']}")
        print(f"  - Entities Found: {result['metrics']['num_entities']}")
        print(f"  - Relationships: {result['metrics']['num_relationships']}")
        print(f"  - Answer Tokens: {result['metrics']['answer_tokens']}")

        if result['entities']:
            print(f"\nEntities Involved:")
            for entity in result['entities'][:10]:  # Show first 10
                print(f"  - {entity}")

        if result['facts']:
            print(f"\nKey Facts Retrieved:")
            for i, fact in enumerate(result['facts'][:5], 1):  # Show first 5
                print(f"\n  Fact {i}:")
                print(f"  {fact[:300]}..." if len(fact) > 300 else f"  {fact}")

    return result
