# MCP Quadrant - Document & Location Search

A Model Context Protocol (MCP) server providing coordinate conversion tools and document search with Qdrant vector database, featuring quadrant-based spatial search and filtering.

## 🚀 Features

- **Document Storage**: Store and retrieve document chunks with optional geolocation
- **Quadrant-Based Search**: Search within specific geographic quadrants (NE, NW, SE, SW)
- **Location-Based Search**: Find documents near specific coordinates
- **Hybrid Search**: Combine semantic search with geospatial filtering
- **Fast Vector Search**: Powered by Qdrant's efficient vector similarity search

## 🚀 Quick Start with UV

### 1. Install UV (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Setup the Project

```bash
# Navigate to your project directory
cd MCP_ADDRESS

# Create a virtual environment and install dependencies
uv venv
uv pip install -e .
```

### 3. Run the MCP Server

```bash
# Activate the virtual environment (optional, uv can run without activation)
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Run
uv run python main.py

# OR run directly without activating venv
uv run main.py
```

The server will start on `http://0.0.0.0:8000`

# To run the MCP inspector

> npx @modelcontextprotocol/inspector http://0.0.0.0:8000/sse

## 🔧 Configure Claude Desktop

Add this to your Claude Desktop config file:

**Location:**

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**

```json
{
  "mcpServers": {
    "quadrant": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/MCP_ADDRESS",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

**Replace `/absolute/path/to/MCP_QUADRANT`** with your actual project path.

## 📦 Available Tools

### Coordinate Conversion
1. **tlc_to_address_tool** - Convert TLC codes to addresses
2. **address_to_tlc_tool** - Convert addresses to TLC codes
3. **address_to_plasma_tool** - Convert addresses to Plasma format
4. **plasma_to_address_tool** - Convert Plasma coordinates to addresses

### Document Search & Storage
5. **store_document_chunks** - Store document chunks with optional geolocation
6. **search_documents_by_quadrant** - Search within a specific geographic quadrant
7. **search_documents_near_location** - Search near specific coordinates
8. **search_documents_by_filename** - Search documents by filename

## 🛠️ Development Commands

```bash
# Install dependencies
uv pip install -e .

# Install with geocoding support
uv pip install -e ".[geocoding]"

# Update dependencies
uv pip install --upgrade mcp fastmcp uvicorn starlette qdrant-client sentence-transformers

# Run the server
uv run python main.py

# Run tests (after adding tests)
uv run pytest

# Format code (if you add ruff/black)
uv run ruff format .
```

## � Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

## �📝 Example Usage

### Store Documents
```python
# Store document chunks with location
store_document_chunks(
    chunks=["Document about New York", "Another document"],
    filename="nyc_docs.txt",
    coordinates=(40.7128, -74.0060)  # NYC coordinates
)
```

### Search by Quadrant
```python
# Search in Northeast quadrant
results = search_documents_by_quadrant(
    query="restaurants",
    quadrant="NE",  # NE, NW, SE, SW
    top_k=5
)
```

### Search Near Location
```python
# Search within 5km of a location
results = search_documents_near_location(
    query="hotels",
    latitude=40.7128,
    longitude=-74.0060,
    radius_km=5.0
)
```

### Search by Filename
```python
# Search documents by filename
results = search_documents_by_filename(
    filename="example.txt",
    quadrant="NE",  # Optional
    top_k=10
)
```

## 📝 Project Structure

```
mcp_address/
├── services/
│   ├── __init__.py
│   ├── qdrant_client.py    # Qdrant client and search functions
│   └── quadrant_utils.py   # Quadrant-based utilities
├── tools/
│   ├── __init__.py
│   ├── address_plasma.py   # Address → Plasma conversion
│   ├── address_TLC.py      # Address → TLC conversion
│   ├── plasma_address.py   # Plasma → Address conversion
│   └── TLC_address.py      # TLC → Address conversion
├── server.py              # SSE server setup
├── main.py                # Main MCP server
├── requirements.txt       # Pip requirements
├── pyproject.toml         # UV/Python project config
└── README.md              # This file
```

## 🔄 Next Steps

1. Set up your Qdrant database and update `.env` with credentials
2. Test the document storage and search functionality
3. Implement custom document processing pipelines if needed
4. Monitor and optimize search performance
5. Restart Claude Desktop to load the updated MCP server

## 📚 Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Guide](https://github.com/jlowin/fastmcp)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Sentence Transformers](https://www.sbert.net/)

## 🐛 Troubleshooting

**Server won't start:**

- Check that all dependencies are installed: `uv pip list`
- Verify Python version: `uv run python --version` (should be 3.10+)
- Check for syntax errors in your modules
- Ensure Qdrant server is accessible and credentials are correct

**Qdrant Connection Issues:**

- Verify QDRANT_URL and QDRANT_API_KEY in .env
- Check network connectivity to Qdrant server
- Ensure Qdrant server is running and accessible

**Search Performance:**

- For large datasets, consider adding indexes
- Adjust `top_k` parameter to limit results
- Use filters to narrow down search scope

**Claude Desktop Integration:**

- Restart Claude Desktop after making changes
- Verify the path in `claude_desktop_config.json` is absolute
- Check Claude Desktop logs for errors

**Import errors:**

- Make sure you're in the project directory
- Run `uv pip install -e .` to install in editable mode
- Check that all required dependencies are installed
