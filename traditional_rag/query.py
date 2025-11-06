"""Query interface for Traditional RAG."""

from typing import Dict, Any
from .rag_pipeline import TraditionalRAG


def query_rag(rag_system: TraditionalRAG, question: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Query the Traditional RAG system and return formatted results.

    Args:
        rag_system: Initialized TraditionalRAG instance
        question: User's question
        verbose: Whether to print detailed information

    Returns:
        Dictionary with answer and metrics
    """
    result = rag_system.query(question)

    if verbose:
        print("\n" + "=" * 80)
        print("TRADITIONAL RAG RESULT")
        print("=" * 80)
        print(f"\nQuestion: {question}")
        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nMetrics:")
        print(f"  - Query Time: {result['metrics']['query_time']:.2f}s")
        print(f"  - Source Chunks: {result['metrics']['num_source_chunks']}")
        print(f"  - Answer Tokens: {result['metrics']['answer_tokens']}")
        print("\nSource Chunks:")
        for i, doc in enumerate(result['source_documents'], 1):
            print(f"\n  Chunk {i} (ID: {doc.metadata.get('chunk_id', 'N/A')}):")
            print(f"  {doc.page_content[:200]}...")

    return result
