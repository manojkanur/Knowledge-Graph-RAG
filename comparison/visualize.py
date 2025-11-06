"""Visualization tools for Knowledge Graph and comparison metrics."""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any
from pyvis.network import Network
from neo4j import GraphDatabase


def visualize_graph(
    neo4j_uri: str,
    neo4j_user: str,
    neo4j_password: str,
    output_file: str = "knowledge_graph.html",
    max_nodes: int = 100
) -> None:
    """
    Visualize the knowledge graph using pyvis.

    Args:
        neo4j_uri: Neo4j URI
        neo4j_user: Neo4j username
        neo4j_password: Neo4j password
        output_file: Output HTML file path
        max_nodes: Maximum number of nodes to visualize
    """
    print(f"Generating knowledge graph visualization...")

    # Connect to Neo4j
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    # Create network
    net = Network(
        height="750px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=True
    )

    net.barnes_hut(
        gravity=-80000,
        central_gravity=0.3,
        spring_length=250,
        spring_strength=0.001,
        damping=0.09,
        overlap=0
    )

    # Query graph data
    with driver.session() as session:
        # Get nodes
        node_query = f"""
        MATCH (n)
        RETURN id(n) as id, labels(n) as labels, properties(n) as properties
        LIMIT {max_nodes}
        """
        nodes = session.run(node_query)

        node_ids = set()
        for record in nodes:
            node_id = str(record["id"])
            labels = record["labels"]
            props = record["properties"]

            # Determine node properties
            label = labels[0] if labels else "Node"
            title = f"{label}\n" + "\n".join([f"{k}: {v}" for k, v in props.items()][:5])

            # Color by type
            color = "#97c2fc"  # Default blue
            if "Entity" in labels:
                color = "#fb7e81"  # Red for entities
            elif "Episode" in labels:
                color = "#7be141"  # Green for episodes
            elif "Fact" in labels:
                color = "#ffa500"  # Orange for facts

            # Get display name
            name = props.get("name", props.get("title", f"Node {node_id}"))
            if len(name) > 30:
                name = name[:27] + "..."

            net.add_node(
                node_id,
                label=name,
                title=title,
                color=color,
                size=20
            )
            node_ids.add(node_id)

        # Get relationships
        if node_ids:
            rel_query = f"""
            MATCH (a)-[r]->(b)
            WHERE id(a) IN {list(range(max_nodes))} AND id(b) IN {list(range(max_nodes))}
            RETURN id(a) as source, id(b) as target, type(r) as type, properties(r) as properties
            LIMIT {max_nodes * 2}
            """
            relationships = session.run(rel_query)

            for record in relationships:
                source = str(record["source"])
                target = str(record["target"])
                rel_type = record["type"]

                if source in node_ids and target in node_ids:
                    net.add_edge(
                        source,
                        target,
                        title=rel_type,
                        label=rel_type[:20],
                        arrows="to"
                    )

    driver.close()

    # Save visualization
    net.show(output_file)
    print(f"Knowledge graph visualization saved to: {output_file}")


def plot_comparison_metrics(
    results: List[Dict[str, Any]],
    output_file: str = "comparison_metrics.png"
) -> None:
    """
    Plot comparison metrics between Traditional RAG and Knowledge Graph RAG.

    Args:
        results: List of comparison results from compare_systems
        output_file: Output image file path
    """
    if not results:
        print("No results to plot")
        return

    print(f"Generating comparison metrics plot...")

    # Extract data
    questions = [f"Q{i+1}" for i in range(len(results))]
    rag_times = [r['comparison_metrics']['rag_time'] for r in results]
    kg_times = [r['comparison_metrics']['kg_time'] for r in results]
    rag_sources = [r['comparison_metrics']['rag_sources'] for r in results]
    kg_facts = [r['comparison_metrics']['kg_facts'] for r in results]
    kg_entities = [r['comparison_metrics']['kg_entities'] for r in results]
    kg_relationships = [r['comparison_metrics']['kg_relationships'] for r in results]

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Traditional RAG vs Knowledge Graph RAG Comparison', fontsize=16, fontweight='bold')

    # 1. Query Time Comparison
    ax1 = axes[0, 0]
    x = np.arange(len(questions))
    width = 0.35
    ax1.bar(x - width/2, rag_times, width, label='Traditional RAG', color='#3498db', alpha=0.8)
    ax1.bar(x + width/2, kg_times, width, label='Knowledge Graph RAG', color='#e74c3c', alpha=0.8)
    ax1.set_xlabel('Questions')
    ax1.set_ylabel('Query Time (seconds)')
    ax1.set_title('Query Time Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(questions)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    # 2. Retrieved Items Comparison
    ax2 = axes[0, 1]
    ax2.bar(x - width/2, rag_sources, width, label='RAG Chunks', color='#3498db', alpha=0.8)
    ax2.bar(x + width/2, kg_facts, width, label='KG Facts', color='#e74c3c', alpha=0.8)
    ax2.set_xlabel('Questions')
    ax2.set_ylabel('Number of Items')
    ax2.set_title('Retrieved Items Comparison')
    ax2.set_xticks(x)
    ax2.set_xticklabels(questions)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)

    # 3. Knowledge Graph Entities and Relationships
    ax3 = axes[1, 0]
    ax3.bar(x - width/2, kg_entities, width, label='Entities', color='#2ecc71', alpha=0.8)
    ax3.bar(x + width/2, kg_relationships, width, label='Relationships', color='#f39c12', alpha=0.8)
    ax3.set_xlabel('Questions')
    ax3.set_ylabel('Count')
    ax3.set_title('Knowledge Graph: Entities & Relationships')
    ax3.set_xticks(x)
    ax3.set_xticklabels(questions)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)

    # 4. Average Metrics Summary
    ax4 = axes[1, 1]
    avg_metrics = {
        'Query Time\n(RAG)': np.mean(rag_times),
        'Query Time\n(KG)': np.mean(kg_times),
        'Items\n(RAG)': np.mean(rag_sources),
        'Items\n(KG)': np.mean(kg_facts),
        'Entities\n(KG)': np.mean(kg_entities),
        'Relations\n(KG)': np.mean(kg_relationships)
    }

    colors = ['#3498db', '#e74c3c', '#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    bars = ax4.bar(avg_metrics.keys(), avg_metrics.values(), color=colors, alpha=0.8)
    ax4.set_ylabel('Average Value')
    ax4.set_title('Average Metrics Summary')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Comparison metrics plot saved to: {output_file}")

    # Also display the plot
    plt.show()


def create_entity_relationship_diagram(
    neo4j_uri: str,
    neo4j_user: str,
    neo4j_password: str,
    entity_name: str,
    output_file: str = "entity_relationships.html"
) -> None:
    """
    Create a focused visualization of a specific entity and its relationships.

    Args:
        neo4j_uri: Neo4j URI
        neo4j_user: Neo4j username
        neo4j_password: Neo4j password
        entity_name: Name of the entity to visualize
        output_file: Output HTML file path
    """
    print(f"Creating entity relationship diagram for: {entity_name}")

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    net = Network(
        height="600px",
        width="100%",
        bgcolor="#ffffff",
        font_color="black",
        directed=True
    )

    with driver.session() as session:
        # Get entity and connected nodes
        query = """
        MATCH (e:Entity {name: $entity_name})-[r]-(connected)
        RETURN e, r, connected
        LIMIT 50
        """
        results = session.run(query, entity_name=entity_name)

        nodes_added = set()

        for record in results:
            entity = record["e"]
            relationship = record["r"]
            connected = record["connected"]

            # Add entity node
            entity_id = str(id(entity))
            if entity_id not in nodes_added:
                net.add_node(entity_id, label=entity["name"], color="#e74c3c", size=30)
                nodes_added.add(entity_id)

            # Add connected node
            connected_id = str(id(connected))
            if connected_id not in nodes_added:
                label = connected.get("name", connected.get("title", "Node"))
                net.add_node(connected_id, label=label[:30], color="#3498db", size=20)
                nodes_added.add(connected_id)

            # Add relationship
            rel_type = type(relationship).__name__
            net.add_edge(entity_id, connected_id, label=rel_type, arrows="to")

    driver.close()

    net.show(output_file)
    print(f"Entity relationship diagram saved to: {output_file}")
