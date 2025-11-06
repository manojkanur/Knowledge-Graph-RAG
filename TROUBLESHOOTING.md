# Troubleshooting Guide

Common issues and their solutions.

## Neo4j Issues

### Cannot Connect to Neo4j

**Error Message:**
```
Failed to establish connection to bolt://localhost:7687
```

**Solutions:**

1. **Check if Neo4j is running:**
   ```bash
   docker ps
   ```
   Should show `neo4j-kg-demo` container

2. **If not running, start it:**
   ```bash
   docker-compose up -d
   ```

3. **Check Neo4j logs:**
   ```bash
   docker logs neo4j-kg-demo
   ```

4. **Verify port 7687 is not in use:**
   ```bash
   # Windows
   netstat -ano | findstr :7687

   # macOS/Linux
   lsof -i :7687
   ```

5. **Reset Neo4j completely:**
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

### Neo4j Authentication Failed

**Error Message:**
```
The client is unauthorized due to authentication failure
```

**Solution:**

Check `.env` file has correct credentials:
```
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=knowledge_graph_demo_2024
```

Must match `docker-compose.yml`:
```yaml
NEO4J_AUTH=neo4j/knowledge_graph_demo_2024
```

### Neo4j Browser Won't Load

**Problem:** http://localhost:7474 doesn't open

**Solutions:**

1. Wait 30 seconds after starting (Neo4j takes time to initialize)

2. Check container status:
   ```bash
   docker ps
   docker logs neo4j-kg-demo
   ```

3. Try restarting:
   ```bash
   docker-compose restart
   ```

### Graph Building Takes Forever

**Problem:** Knowledge graph build is extremely slow

**Possible Causes:**

1. **First time is normal** - Building graph with GPT-4 takes 2-5 minutes
2. **Network issues** - Slow OpenAI API responses
3. **Rate limiting** - Too many API calls

**Solutions:**

1. **Be patient** - First build is slow, subsequent queries are fast

2. **Check OpenAI API status:**
   ```bash
   curl https://status.openai.com/api/v2/status.json
   ```

3. **Reduce document size for testing:**
   Edit `sample_data/api_documentation.txt` to be shorter

4. **Check if graph already exists:**
   ```python
   # In demo.py, select option 5
   # If nodes > 0, graph is already built
   ```

## Python Issues

### ModuleNotFoundError

**Error Message:**
```
ModuleNotFoundError: No module named 'langchain'
```

**Solution:**

1. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   pip list | grep langchain
   pip list | grep graphiti
   ```

### Import Error: Graphiti

**Error Message:**
```
ImportError: cannot import name 'Graphiti' from 'graphiti_core'
```

**Solution:**

1. **Upgrade graphiti:**
   ```bash
   pip install --upgrade graphiti-core
   ```

2. **Check version:**
   ```bash
   pip show graphiti-core
   ```
   Should be >= 0.3.0

3. **Reinstall if needed:**
   ```bash
   pip uninstall graphiti-core
   pip install graphiti-core==0.3.0
   ```

### OpenSSL or SSL Errors

**Error Message:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**

**Windows:**
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

**macOS:**
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

## OpenAI API Issues

### Invalid API Key

**Error Message:**
```
openai.AuthenticationError: Invalid API key
```

**Solutions:**

1. **Check .env file exists** (not just .env.example):
   ```bash
   # Should show .env
   ls -la .env
   ```

2. **Verify API key format:**
   ```
   OPENAI_API_KEY=sk-...your-key...
   ```
   - Must start with `sk-`
   - No quotes needed
   - No spaces

3. **Test API key:**
   ```python
   import openai
   import os
   from dotenv import load_dotenv

   load_dotenv()
   client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
   print(client.models.list())
   ```

4. **Generate new key:**
   - Go to https://platform.openai.com/api-keys
   - Create new secret key
   - Update .env file

### Rate Limit Exceeded

**Error Message:**
```
openai.RateLimitError: Rate limit exceeded
```

**Solutions:**

1. **Wait and retry** - Rate limits reset after time

2. **Check your usage:**
   - Visit https://platform.openai.com/usage
   - Verify you have remaining quota

3. **Reduce concurrent requests:**
   - Process fewer documents at once
   - Add delays between API calls

4. **Upgrade OpenAI plan** if needed

### Model Not Found

**Error Message:**
```
openai.NotFoundError: The model 'gpt-4-turbo-preview' does not exist
```

**Solution:**

1. **Check model access** - Verify your account has GPT-4 access

2. **Use GPT-3.5 instead** - Edit .env:
   ```
   OPENAI_MODEL=gpt-3.5-turbo
   ```

3. **Check model availability:**
   ```python
   import openai
   client = openai.OpenAI()
   models = client.models.list()
   for model in models:
       if 'gpt' in model.id:
           print(model.id)
   ```

## Memory Issues

### Out of Memory

**Error Message:**
```
MemoryError: Unable to allocate memory
```

**Solutions:**

1. **Reduce chunk size** in `traditional_rag/rag_pipeline.py`:
   ```python
   chunk_size=500  # Instead of 1000
   ```

2. **Process fewer documents:**
   - Shorten sample_data/api_documentation.txt
   - Split into multiple runs

3. **Increase Docker memory:**
   - Docker Desktop → Settings → Resources
   - Increase memory limit to 4GB or more

4. **Close other applications**

### Python Process Killed

**Problem:** Python suddenly exits

**Solutions:**

1. **Check system memory:**
   ```bash
   # Windows
   wmic OS get FreePhysicalMemory

   # macOS/Linux
   free -h
   ```

2. **Monitor memory usage:**
   ```bash
   # While demo runs
   docker stats neo4j-kg-demo
   ```

3. **Reduce batch size** - Process documents in smaller batches

## Demo Runtime Issues

### No Output or Frozen

**Problem:** Demo seems stuck

**Solutions:**

1. **Check if waiting for API response:**
   - OpenAI API can take 10-30 seconds per request
   - Look for activity indicators

2. **Check network connectivity:**
   ```bash
   ping api.openai.com
   ```

3. **Restart the demo:**
   - Press Ctrl+C
   - Run `python demo.py` again

### Slow Queries

**Problem:** Queries take 30+ seconds

**Possible Causes:**

1. **First query on KG** - Initializes connections
2. **Cold start** - Neo4j needs to warm up
3. **Complex query** - Multi-hop traversal

**Solutions:**

1. **Run a simple query first** to warm up

2. **Reduce max_facts** in `knowledge_graph/kg_pipeline.py`:
   ```python
   max_facts=5  # Instead of 10
   ```

3. **Check Neo4j performance:**
   - Open http://localhost:7474
   - Run: `:sysinfo`

### Visualization Won't Generate

**Problem:** knowledge_graph.html not created

**Solutions:**

1. **Check file permissions:**
   ```bash
   # Should be writable
   ls -la
   ```

2. **Run with explicit path:**
   ```python
   visualize_graph(..., output_file="./knowledge_graph.html")
   ```

3. **Check Neo4j has data:**
   ```bash
   # From demo menu, option 5
   # Should show nodes > 0
   ```

4. **Check pyvis is installed:**
   ```bash
   pip show pyvis
   ```

## Docker Issues

### Docker Not Running

**Error Message:**
```
Cannot connect to the Docker daemon
```

**Solution:**

1. **Start Docker Desktop:**
   - Windows: Start Docker Desktop from Start Menu
   - macOS: Start Docker from Applications
   - Linux: `sudo systemctl start docker`

2. **Verify Docker is running:**
   ```bash
   docker info
   ```

### Port Already in Use

**Error Message:**
```
Bind for 0.0.0.0:7687 failed: port is already allocated
```

**Solutions:**

1. **Find what's using the port:**
   ```bash
   # Windows
   netstat -ano | findstr :7687

   # macOS/Linux
   lsof -i :7687
   ```

2. **Stop conflicting container:**
   ```bash
   docker ps -a
   docker stop <container_id>
   ```

3. **Change port in docker-compose.yml:**
   ```yaml
   ports:
     - "7688:7687"  # Use different port
   ```

   Then update .env:
   ```
   NEO4J_URI=bolt://localhost:7688
   ```

### Docker Volume Issues

**Problem:** Neo4j data not persisting

**Solution:**

1. **Check volumes exist:**
   ```bash
   docker volume ls
   ```

2. **Remove and recreate:**
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

## Platform-Specific Issues

### Windows Specific

**Long Path Issues:**
```
FileNotFoundError: [Errno 2] No such file or directory
```

**Solution:** Enable long paths
```bash
# Run as Administrator
reg add HKLM\SYSTEM\CurrentControlSet\Control\FileSystem /v LongPathsEnabled /t REG_DWORD /d 1 /f
```

**Windows Defender Blocks Scripts:**

**Solution:** Add exception
- Windows Security → Virus & threat protection
- Add exclusion for project folder

### macOS Specific

**Command Not Found:**
```
-bash: python: command not found
```

**Solution:** Use `python3` instead
```bash
python3 -m venv venv
python3 demo.py
```

**Permission Denied:**

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

### Linux Specific

**Docker Permission Denied:**
```
Got permission denied while trying to connect to Docker daemon
```

**Solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Still Having Issues?

### Diagnostic Script

Create `diagnose.py`:
```python
import sys
import os

print("Python Version:", sys.version)
print("Python Path:", sys.executable)
print("\nEnvironment Variables:")
print("OPENAI_API_KEY:", "SET" if os.getenv("OPENAI_API_KEY") else "NOT SET")
print("NEO4J_URI:", os.getenv("NEO4J_URI"))

print("\nInstalled Packages:")
try:
    import langchain
    print("✓ langchain:", langchain.__version__)
except:
    print("✗ langchain: NOT INSTALLED")

try:
    import graphiti_core
    print("✓ graphiti_core")
except:
    print("✗ graphiti_core: NOT INSTALLED")

try:
    import neo4j
    print("✓ neo4j:", neo4j.__version__)
except:
    print("✗ neo4j: NOT INSTALLED")

print("\nDocker Status:")
import subprocess
try:
    result = subprocess.run(['docker', 'ps'], capture_output=True)
    print(result.stdout.decode())
except:
    print("✗ Docker not accessible")
```

Run it:
```bash
python diagnose.py
```

### Clean Slate Reset

If all else fails, start fresh:

```bash
# Stop everything
docker-compose down -v

# Remove virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Start over
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
docker-compose up -d
```

### Getting Help

1. **Check Neo4j logs:**
   ```bash
   docker logs neo4j-kg-demo --tail 100
   ```

2. **Enable debug mode** in demo.py:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Test components individually:**
   ```python
   # Test Neo4j
   from neo4j import GraphDatabase
   driver = GraphDatabase.driver("bolt://localhost:7687",
                                  auth=("neo4j", "knowledge_graph_demo_2024"))
   driver.verify_connectivity()

   # Test OpenAI
   import openai
   client = openai.OpenAI(api_key="your-key")
   client.models.list()
   ```

---

Most issues are configuration-related. Double-check your .env file and ensure Neo4j is running!
