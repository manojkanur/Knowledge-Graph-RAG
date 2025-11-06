# Quick Start Guide

Get the demo running in 5 minutes!

## Prerequisites

- Python 3.9+
- Docker Desktop installed and running
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Step 1: Set Up Neo4j (1 minute)

```bash
# Start Neo4j with Docker
docker-compose up -d

# Verify it's running
docker ps
```

You should see `neo4j-kg-demo` running on ports 7474 and 7687.

**Optional**: Open http://localhost:7474 in your browser to access Neo4j Browser
- Username: `neo4j`
- Password: `knowledge_graph_demo_2024`

## Step 2: Set Up Python Environment (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure OpenAI API Key (30 seconds)

Edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

The Neo4j settings are already configured to match the Docker setup!

## Step 4: Run the Demo (30 seconds)

```bash
python demo.py
```

## First Time Setup

When you run the demo for the first time:

1. It will load the sample API documentation
2. Build the vector index (Traditional RAG) - ~5 seconds
3. Build the knowledge graph - ~2-3 minutes (one-time only!)
4. Show the interactive menu

## Recommended First Demo Flow

From the menu, try this sequence:

1. **Option 1**: Run single question comparison
   - Choose question **1** or **3** (most impressive)
   - Compare both answers

2. **Option 3**: Visualize knowledge graph
   - Open the generated `knowledge_graph.html` in your browser
   - Zoom and explore the graph

3. **Option 4**: Interactive mode
   - Ask your own questions
   - See real-time comparisons

## Troubleshooting

### Neo4j won't start

```bash
# Check if port 7687 is already in use
docker ps -a

# Stop any existing Neo4j containers
docker stop neo4j-kg-demo
docker rm neo4j-kg-demo

# Try again
docker-compose up -d
```

### Python packages won't install

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing again
pip install -r requirements.txt
```

### "Invalid API key" error

1. Make sure you edited `.env` (not `.env.example`)
2. Copy your full API key including `sk-`
3. No quotes needed around the key

### Demo is slow

First run is slow because it builds the knowledge graph. Subsequent runs use the cached graph and are much faster!

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Try all 7 demo questions
- Customize with your own data
- Present to your audience!

## Stopping the Demo

```bash
# Stop Python demo: Ctrl+C

# Stop Neo4j (optional)
docker-compose down

# Stop Neo4j and delete data (clean slate)
docker-compose down -v
```

---

**You're ready to demo!** 🚀
