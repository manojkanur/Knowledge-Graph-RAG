# Knowledge Graph vs Traditional RAG Demo

A comprehensive demonstration comparing Traditional RAG (Retrieval-Augmented Generation) with Knowledge Graph-based RAG using LangChain, Graphiti, and Neo4j.

## Overview

This project showcases the advantages of Knowledge Graph-based RAG systems over Traditional vector similarity RAG by:

- **Query Response Quality**: Side-by-side comparison of answers
- **Relationship Discovery**: Demonstrating how KGs capture entity relationships that RAG misses
- **Visual Exploration**: Interactive graph visualization
- **Performance Metrics**: Detailed comparison of retrieval time, accuracy, and context richness

## Architecture

### Traditional RAG
- **Vector Store**: FAISS for fast similarity search
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: GPT-4 Turbo
- **Approach**: Chunks documents → Embeds → Retrieves top-k similar chunks → Generates answer

### Knowledge Graph RAG
- **Graph Database**: Neo4j for storing entities and relationships
- **Framework**: Graphiti for automatic entity/relationship extraction
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: GPT-4 Turbo
- **Approach**: Extracts entities & relationships → Builds knowledge graph → Traverses graph for relevant facts → Generates answer

## Key Advantages of Knowledge Graphs

1. **Structured Context**: Understands relationships between entities (e.g., "AuthenticationService depends on UserManager")
2. **Multi-hop Reasoning**: Can traverse relationships to find connected information
3. **Entity-Centric**: Maintains entity identities across the entire corpus
4. **Relationship Awareness**: Explicitly captures "depends on", "interacts with", "uses" relationships
5. **Better for Complex Queries**: Excels at questions about system architecture and dependencies

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for Neo4j)
- OpenAI API key
- 8GB RAM recommended

## Installation

### 1. Clone or Download the Project

```bash
cd KnowledgeGraph_LC
```

### 2. Set Up Python Environment

Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Neo4j with Docker

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.18.0
    container_name: neo4j-kg-demo
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=neo4j/your_password_here
      - NEO4J_PLUGINS=["apoc"]
      - NEO4J_dbms_security_procedures_unrestricted=apoc.*
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs

volumes:
  neo4j_data:
  neo4j_logs:
```

Start Neo4j:

```bash
docker-compose up -d
```

Verify Neo4j is running:
- Open http://localhost:7474 in your browser
- Login with username: `neo4j`, password: `your_password_here`

### 5. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here

# Optional: Model Configuration
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## Running the Demo

### Start the Interactive Demo

```bash
python demo.py
```

### Demo Menu Options

1. **Run Single Question Comparison**
   - Compare both systems on one question
   - Choose from predefined questions or ask your own
   - See detailed results and metrics

2. **Run Full Comparison Suite**
   - Test 7 predefined questions
   - Generate comprehensive metrics
   - Create visualization plots

3. **Visualize Knowledge Graph**
   - Generate interactive HTML visualization
   - Explore entities and relationships
   - Color-coded by node type

4. **Interactive Mode**
   - Ask unlimited questions
   - Real-time comparison
   - Great for live demos

5. **View Graph Statistics**
   - See node and relationship counts
   - Understand graph complexity

## Understanding the Results

### Query Comparison Output

```
TRADITIONAL RAG RESULT
Question: How does the AuthenticationService relate to the UserManager?
Answer: The AuthenticationService depends on UserManager for user verification...
Metrics:
  - Query Time: 1.23s
  - Source Chunks: 4
  - Answer Tokens: 87

KNOWLEDGE GRAPH RAG RESULT
Question: How does the AuthenticationService relate to the UserManager?
Answer: The AuthenticationService has a direct dependency on UserManager. It uses
UserManager to verify user permissions and interact with user data...
Metrics:
  - Total Query Time: 1.45s
  - Facts Retrieved: 8
  - Entities Found: 5
  - Relationships: 12
  - Answer Tokens: 124
```

### Key Metrics

- **Query Time**: Total time to retrieve and generate answer
- **Source Chunks (RAG)**: Number of text chunks retrieved
- **Facts (KG)**: Number of knowledge graph facts retrieved
- **Entities (KG)**: Number of entities involved in the answer
- **Relationships (KG)**: Number of relationships traversed

### What to Look For

1. **Richer Context**: KG typically finds more related facts
2. **Entity Awareness**: KG explicitly identifies entities
3. **Relationship Discovery**: KG reveals connections RAG misses
4. **Better for "How" Questions**: KG excels at explaining relationships

## Sample Questions That Highlight KG Advantages

1. **"How does the AuthenticationService relate to the UserManager?"**
   - Shows direct dependency relationships

2. **"What services depend on the PermissionManager?"**
   - Demonstrates reverse relationship lookup

3. **"Explain the file upload workflow and all the services involved."**
   - Multi-hop traversal through service chain

4. **"How are share links related to notifications?"**
   - Indirect relationships through intermediate services

5. **"What is the relationship between QuotaManager and StorageManager?"**
   - Service interaction patterns

## Visualizations

### Knowledge Graph Visualization

After running option 3, open `knowledge_graph.html` in your browser to see:
- **Red nodes**: Entities (services, components)
- **Green nodes**: Episodes (document chunks)
- **Orange nodes**: Facts
- **Edges**: Relationships between nodes

### Comparison Metrics Plot

After running the full suite, `comparison_metrics.png` shows:
- Query time comparison
- Retrieved items comparison
- Entities and relationships graph
- Average metrics summary

## Project Structure

```
KnowledgeGraph_LC/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment template
├── .env                               # Your configuration (create this)
├── docker-compose.yml                 # Neo4j setup (create this)
├── demo.py                            # Main demo script
├── sample_data/
│   └── api_documentation.txt          # Sample technical documentation
├── traditional_rag/
│   ├── __init__.py
│   ├── rag_pipeline.py                # RAG implementation
│   └── query.py                       # RAG query interface
├── knowledge_graph/
│   ├── __init__.py
│   ├── kg_pipeline.py                 # KG RAG implementation
│   └── query.py                       # KG query interface
└── comparison/
    ├── __init__.py
    ├── compare.py                     # Comparison tools
    └── visualize.py                   # Visualization tools
```

## Troubleshooting

### Neo4j Connection Issues

**Error**: `Failed to establish connection to Neo4j`

**Solution**:
1. Verify Neo4j is running: `docker ps`
2. Check port 7687 is accessible
3. Verify credentials in `.env` match `docker-compose.yml`

### OpenAI API Errors

**Error**: `Invalid API key` or `Rate limit exceeded`

**Solution**:
1. Verify API key is correct in `.env`
2. Check your OpenAI account has available credits
3. Reduce request rate if hitting limits

### Memory Issues

**Error**: Process killed or out of memory

**Solution**:
1. Reduce `chunk_size` in `rag_pipeline.py` (line 28)
2. Process fewer documents at once
3. Increase Docker memory allocation

### Import Errors

**Error**: `ModuleNotFoundError`

**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

### Graphiti Build Issues

**Error**: Building knowledge graph takes too long

**Solution**:
1. This is normal - KG building is more intensive than vector indexing
2. Reduce document size for faster testing
3. Graph is cached - subsequent runs use existing graph

## Presenting the Demo

### Recommended Flow for Mixed Audience

1. **Start with Overview** (2 min)
   - Explain what RAG is
   - Introduce Knowledge Graphs concept

2. **Run Single Comparison** (5 min)
   - Choose Question 1 or 3
   - Show both results side-by-side
   - Highlight KG advantages

3. **Show Visualization** (3 min)
   - Open knowledge_graph.html
   - Zoom into interesting entity clusters
   - Show relationship paths

4. **Run Interactive Demo** (5-10 min)
   - Take questions from audience
   - Compare answers live
   - Discuss differences

5. **Show Metrics** (3 min)
   - Display comparison_metrics.png
   - Discuss trade-offs
   - Explain when to use each approach

### Key Talking Points

- **Traditional RAG**: Fast, simple, good for straightforward Q&A
- **Knowledge Graph**: Better for complex queries, relationship-heavy domains
- **Trade-offs**: KG requires more setup but provides richer context
- **Use Cases**: KG excels in technical documentation, enterprise knowledge bases

## Customizing for Your Domain

### Using Your Own Data

1. Replace `sample_data/api_documentation.txt` with your content
2. Adjust `chunk_size` in `traditional_rag/rag_pipeline.py` if needed
3. Rebuild the graph: Answer "yes" when prompted in demo.py

### Adding Custom Questions

Edit `DEMO_QUESTIONS` list in `demo.py`:

```python
DEMO_QUESTIONS = [
    "Your custom question 1?",
    "Your custom question 2?",
    # ...
]
```

### Tuning Parameters

**Traditional RAG** (`traditional_rag/rag_pipeline.py`):
- `chunk_size`: Size of text chunks (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200)
- `k`: Number of chunks to retrieve (default: 4)

**Knowledge Graph** (`knowledge_graph/kg_pipeline.py`):
- `max_facts`: Maximum facts to retrieve (default: 10)

## Performance Benchmarks

Tested on: Windows 11, Intel i7, 16GB RAM

**Traditional RAG**:
- Index build: ~5-10 seconds
- Query time: ~1-2 seconds
- Memory: ~500MB

**Knowledge Graph**:
- Graph build: ~2-5 minutes (one-time)
- Query time: ~1-3 seconds
- Memory: ~1GB
- Neo4j: ~500MB

## Citation and References

This demo uses:
- [LangChain](https://github.com/langchain-ai/langchain) - RAG framework
- [Graphiti](https://github.com/getzep/graphiti) - Knowledge graph framework
- [Neo4j](https://neo4j.com/) - Graph database
- [OpenAI](https://openai.com/) - LLM and embeddings

## License

This demo is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check Troubleshooting section above
2. Review Neo4j logs: `docker logs neo4j-kg-demo`
3. Verify all dependencies are installed correctly

## Next Steps

After running this demo:
1. Try with your own domain data
2. Experiment with different questions
3. Explore the Neo4j Browser (http://localhost:7474)
4. Adjust parameters to optimize for your use case
5. Consider hybrid approaches combining both methods

---

**Happy Demoing!** Show the world the power of Knowledge Graphs!
